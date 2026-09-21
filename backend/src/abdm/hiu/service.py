"""
M3 (HIU) journeys: raise a consent request, follow it through the patient's decision, fetch the
artefacts, request the data, decrypt the push, store the records (ADR-014).

Docs: /docs/hiecm/v3/milestones/m3 (3 journeys), the 12 pages under
/docs/hiecm/v3/api/m3/endpoints/m3-consent-management-data-flow-hiu/, /concepts/consent and
/concepts/data-flow. Every body is built and parsed in `hiu/rules.py`; this module owns the rows.

Correlation. A callback that answers a call we made carries our REQUEST-ID in `response.requestId`,
and `callbacks/receiver.py` links it to the `AbdmOutboundRequest` row. The gateway-initiated
notify names our `consentRequestId`; the HIP push names the `transactionId` the gateway issued on
`on-request`. No header is trusted for routing.

Everything that talks to ABDM runs inside a Celery task or a desk request; nothing here blocks on
a callback.
"""

import base64
import json
import logging
from urllib.parse import quote

from care.emr.models.patient import Patient
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from django.utils import timezone

from abdm import errors
from abdm.facility.service import get_config, hip_id_for
from abdm.gateway import outbound
from abdm.gateway.session import utc_timestamp
from abdm.hip import crypto
from abdm.hip.contexts import patient_abha
from abdm.hiu import rules
from abdm.models import (
    AbdmCallback,
    AbdmConsentArtefact,
    AbdmConsentRequest,
    AbdmFetchedRecord,
    AbdmFetchRequest,
    AbdmOutboundRequest,
)
from abdm.settings import plugin_settings

logger = logging.getLogger(__name__)

INIT_URL = "/api/hiecm/consent/v3/request/init"
STATUS_URL = "/api/hiecm/consent/v3/request/status"
NOTIFY_ACK_URL = "/api/hiecm/consent/v3/request/hiu/on-notify"
FETCH_URL = "/api/hiecm/consent/v3/fetch"
HI_REQUEST_URL = "/api/hiecm/data-flow/v3/health-information/request"
HI_NOTIFY_URL = "/api/hiecm/data-flow/v3/health-information/notify"
HI_STATUS_URL = "/api/hiecm/data-flow/v3/health-information/request/status/{transaction_id}"
PROVIDERS_URL = "/api/hiecm/gateway/v3/providers"

Succeeded = AbdmOutboundRequest.Status.SUCCEEDED


class HiuError(Exception):
    """A refusal the plug decides for itself. `code` is a plug code in `errors.PLUG_CODES`."""

    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code
        self.message = message


def hiu_name(facility) -> str:
    config = get_config(facility)
    return rules.safe_text(config.get("hip_name") or config.get("facility_name") or facility.name, "HIU")


def data_push_url() -> str:
    base = str(plugin_settings.CALLBACK_BASE_URL or "").rstrip("/")
    return f"{base}/api/abdm{rules.DATA_PUSH_PATH}" if base else ""


def _requester(user) -> tuple[str, dict]:
    """The HPR ID when the user linked one (ADR-015), else the council registration or the username."""
    from abdm.nhpr.professional import requester_identifier as hpr_identifier

    name = rules.safe_text(getattr(user, "full_name", "") or getattr(user, "username", ""), "Care user")
    identifier = hpr_identifier(user) if getattr(user, "pk", None) else None
    if identifier is None:
        identifier = rules.requester_identifier(
            registration=getattr(user, "doctor_medical_council_registration", "") or "",
            username=getattr(user, "username", "") or "",
            system=str(plugin_settings.CALLBACK_BASE_URL or "care"),
        )
    return name, identifier


def _record_failure(row, request: AbdmOutboundRequest | None, fallback_code: str = "") -> None:
    """Store the classified failure of a refused call on the row (ADR-012)."""
    if request is None:
        failure = errors.classify(code=fallback_code)
    else:
        failure = outbound.failure(request)
    row.error_code = (failure.code or fallback_code or "")[:64]
    row.error_message = failure.summary()[:512]


# --- journey 1: raise the request --------------------------------------------------------------


def create_consent_request(patient: Patient, facility, user, params: dict) -> AbdmConsentRequest:
    """Send `consent/v3/request/init` and store the row. A refusal is stored, never raised."""
    now = timezone.now()
    hiu_id = hip_id_for(facility)
    if not hiu_id:
        raise HiuError("NO_FACILITY", "ABDM does not recognise this facility.")
    address, _ = patient_abha(patient)
    if not address:
        raise HiuError("NO_ABHA", "This patient has no ABHA address.")
    if not data_push_url():
        raise HiuError("NO_CALLBACK_URL", "The ABDM callback URL is not set.")
    clean = rules.validate_request(params, now)  # ValueError reaches the view as a 400
    requester_name, identifier = _requester(user)
    body = rules.consent_request_body(
        abha_address=address,
        hiu_id=hiu_id,
        hiu_name=hiu_name(facility),
        requester_name=requester_name,
        requester_identifier=identifier,
        purpose_code=clean["purpose_code"],
        hi_types=clean["hi_types"],
        date_from=clean["date_from"],
        date_to=clean["date_to"],
        data_erase_at=clean["data_erase_at"],
        hip_id=clean["hip_id"],
        hip_name=clean["hip_name"],
    )
    row = AbdmConsentRequest.objects.create(
        patient=patient,
        facility=facility,
        requested_by=user if getattr(user, "pk", None) else None,
        abha_address=address,
        purpose_code=clean["purpose_code"],
        hi_types=clean["hi_types"],
        date_from=clean["date_from"],
        date_to=clean["date_to"],
        data_erase_at=clean["data_erase_at"],
        hip_id=clean["hip_id"],
        hip_name=clean["hip_name"][:256],
    )
    request = outbound.send("m3-consent-request-init", INIT_URL, body, facility=facility, patient=patient, role="hiu")
    row.init_request = request
    if request.status != Succeeded:
        row.status = row.Status.FAILED
        _record_failure(row, request)
    row.save()
    return row


def handle_on_init(callback: AbdmCallback) -> dict:
    """`/v3/hiu/consent/request/on-init`: the HIE-CM id of the request, or an error."""
    data = rules.parse_on_init(callback.parsed_json or {})
    row = (
        AbdmConsentRequest.objects.filter(init_request=callback.outbound_request).first()
        if callback.outbound_request_id
        else None
    )
    if row is None:
        raise ValueError(f"on-init answers no consent request we sent (requestId {data['request_id']!r})")
    if data["consent_request_id"]:
        row.consent_request_id = data["consent_request_id"][:128]
        row.error_code = ""
        row.error_message = ""
    elif data["error_code"]:
        row.status = row.Status.FAILED
        failure = errors.classify(
            code=data["error_code"], message=data["error_message"], request_id=callback.response_request_id
        )
        row.error_code = failure.code[:64]
        row.error_message = failure.summary()[:512]
    row.save()
    return {"consent_request": str(row.external_id), "consent_request_id": row.consent_request_id, "status": row.status}


def refresh_status(row: AbdmConsentRequest) -> AbdmConsentRequest:
    """`consent/v3/request/status`: the answer lands on `on-status`. Journey 1: "You may poll"."""
    if not row.consent_request_id:
        return row
    request = outbound.send(
        "m3-consent-request-status",
        STATUS_URL,
        rules.consent_status_body(row.consent_request_id),
        facility=row.facility,
        patient=row.patient,
        role="hiu",
    )
    row.status_request = request
    row.status_checked_at = timezone.now()
    row.save(update_fields=["status_request", "status_checked_at", "modified_date"])
    return row


def _apply_decision(row: AbdmConsentRequest, status: str, reason: str = "") -> None:
    if status not in rules.REQUEST_STATES or status == row.status:
        return
    row.status = status
    if status != "REQUESTED":
        row.decided_at = timezone.now()
    if reason:
        row.reason = reason[:512]


def handle_on_status(callback: AbdmCallback) -> dict:
    """`/v3/hiu/consent/request/on-status`: REQUESTED, DENIED, EXPIRED or REVOKED."""
    data = rules.parse_on_status(callback.parsed_json or {})
    row = None
    if callback.outbound_request_id:
        row = AbdmConsentRequest.objects.filter(status_request=callback.outbound_request).first()
    if row is None and data["consent_request_id"]:
        row = AbdmConsentRequest.objects.filter(consent_request_id=data["consent_request_id"]).first()
    if row is None:
        raise ValueError(f"on-status names no consent request we know ({data['consent_request_id']!r})")
    if data["error_code"]:
        failure = errors.classify(code=data["error_code"], message=data["error_message"])
        row.error_code = failure.code[:64]
        row.error_message = failure.summary()[:512]
    else:
        _apply_decision(row, data["status"])
        if data["status"] in ("REVOKED", "EXPIRED"):
            for artefact in row.artefacts.all():
                _settle_artefact(artefact, data["status"])
    row.save()
    return {"consent_request": str(row.external_id), "status": row.status}


# --- journey 2: the patient decides ------------------------------------------------------------


def _settle_artefact(artefact: AbdmConsentArtefact, status: str) -> None:
    """REVOKED or EXPIRED: stop fetching and erase what we hold (milestones/m3 step 6)."""
    if status in AbdmConsentArtefact.Status.values and status != artefact.status:
        artefact.status = status
        artefact.status_changed_at = timezone.now()
        artefact.save(update_fields=["status", "status_changed_at", "modified_date"])
    if status in ("REVOKED", "EXPIRED", "DENIED"):
        erase_records(artefact)


def handle_consent_notify(callback: AbdmCallback) -> dict:
    """`/v3/hiu/consent/request/notify`: GRANTED (with artefact ids), DENIED, EXPIRED or REVOKED.
    Acknowledge with `consent/v3/request/hiu/on-notify`, then fetch every new artefact."""
    data = rules.parse_consent_notify(callback.parsed_json or {})
    status = data["status"]
    row = (
        AbdmConsentRequest.objects.filter(consent_request_id=data["consent_request_id"])
        .select_related("patient", "facility")
        .first()
        if data["consent_request_id"]
        else None
    )
    artefacts: list[AbdmConsentArtefact] = []
    if status == "REVOKED":
        # The page: "consentArtefacts is an array of revoked consent artefact ids".
        artefacts = list(
            AbdmConsentArtefact.objects.filter(artefact_id__in=data["artefact_ids"]).select_related(
                "consent_request__patient", "consent_request__facility"
            )
        )
        if row is None and artefacts:
            row = artefacts[0].consent_request
        for artefact in artefacts:
            _settle_artefact(artefact, "REVOKED")
        if row is not None:
            live = row.artefacts.exclude(status=AbdmConsentArtefact.Status.REVOKED).exists()
            if not live:
                _apply_decision(row, "REVOKED", data["reason"])
    elif row is None:
        raise ValueError(f"notify names no consent request we raised ({data['consent_request_id']!r})")
    elif status == "GRANTED":
        for artefact_id in data["artefact_ids"]:
            artefact, _ = AbdmConsentArtefact.objects.get_or_create(
                artefact_id=artefact_id[:128],
                defaults={
                    "consent_request": row,
                    "status": AbdmConsentArtefact.Status.GRANTED,
                    "hip_id": row.hip_id,
                    "hip_name": row.hip_name,
                    "hi_types": row.hi_types,
                    "date_from": row.date_from,
                    "date_to": row.date_to,
                    "data_erase_at": row.data_erase_at,
                },
            )
            artefacts.append(artefact)
        _apply_decision(row, "GRANTED", data["reason"])
    elif status in ("DENIED", "EXPIRED"):
        _apply_decision(row, status, data["reason"])
        for artefact in row.artefacts.all():
            _settle_artefact(artefact, status)
    else:
        logger.warning("abdm: consent notify %s carried status %r", data["consent_request_id"], status)
    if row is not None:
        row.save()
    # The ack names the artefact ids when there are any; a denial or an expiry has none, so the
    # request id goes in that field, as the page example does (docs/findings.md L4).
    ack_ids = [a.artefact_id for a in artefacts] or ([data["consent_request_id"]] if data["consent_request_id"] else [])
    ack = outbound.send(
        "m3-consent-notify-ack",
        NOTIFY_ACK_URL,
        rules.consent_notify_ack_body(ack_ids, callback.request_id_header, ok=status in rules.REQUEST_STATES),
        facility=row.facility if row else None,
        patient=row.patient if row else None,
        role="hiu",
    )
    fetched = 0
    if status == "GRANTED":
        for artefact in artefacts:
            if artefact.fetch_request_id is None:
                fetch_artefact(artefact)
                fetched += 1
    return {
        "consent_request": str(row.external_id) if row else None,
        "status": status,
        "artefacts": len(artefacts),
        "fetch_calls": fetched,
        "ack": ack.status,
    }


# --- journey 3: fetch the artefact, then the records --------------------------------------------


def fetch_artefact(artefact: AbdmConsentArtefact) -> AbdmConsentArtefact:
    """`consent/v3/fetch`: the detail lands on `on-fetch`."""
    row = artefact.consent_request
    request = outbound.send(
        "m3-consent-fetch",
        FETCH_URL,
        rules.consent_fetch_body(artefact.artefact_id),
        facility=row.facility,
        patient=row.patient,
        role="hiu",
    )
    artefact.fetch_request = request
    if request.status != Succeeded:
        _record_failure(artefact, request)
    artefact.save()
    return artefact


def handle_on_fetch(callback: AbdmCallback) -> dict:
    """`/v3/hiu/consent/on-fetch`: the artefact detail. A live GRANTED artefact starts the
    health-information request at once (Rithvik, 2026-09-19: automatic)."""
    data = rules.parse_on_fetch(callback.parsed_json or {})
    artefact = None
    if callback.outbound_request_id:
        artefact = (
            AbdmConsentArtefact.objects.filter(fetch_request=callback.outbound_request)
            .select_related("consent_request__patient", "consent_request__facility")
            .first()
        )
    if artefact is None and data["artefact_id"]:
        artefact = (
            AbdmConsentArtefact.objects.filter(artefact_id=data["artefact_id"])
            .select_related("consent_request__patient", "consent_request__facility")
            .first()
        )
    if artefact is None:
        raise ValueError(f"on-fetch names no artefact we asked for ({data['artefact_id']!r})")
    if data["error_code"]:
        failure = errors.classify(code=data["error_code"], message=data["error_message"])
        artefact.error_code = failure.code[:64]
        artefact.error_message = failure.summary()[:512]
        artefact.save()
        return {"artefact": artefact.artefact_id, "error": artefact.error_code}
    artefact.hip_id = (data["hip_id"] or artefact.hip_id)[:128]
    artefact.hip_name = (data["hip_name"] or artefact.hip_name)[:256]
    artefact.hi_types = data["hi_types"] or artefact.hi_types
    artefact.care_context_references = data["care_context_references"]
    artefact.date_from = data["date_from"] or artefact.date_from
    artefact.date_to = data["date_to"] or artefact.date_to
    artefact.data_erase_at = data["data_erase_at"] or artefact.data_erase_at
    artefact.detail = data["detail"]
    artefact.signature = data["signature"]
    artefact.fetched_at = timezone.now()
    artefact.error_code = ""
    artefact.error_message = ""
    if data["status"] in AbdmConsentArtefact.Status.values:
        artefact.status = data["status"]
    artefact.save()
    if data["status"] in ("REVOKED", "EXPIRED", "DENIED"):
        erase_records(artefact)
        return {"artefact": artefact.artefact_id, "status": artefact.status}
    fetch = None
    if rules.artefact_is_live(artefact.status, artefact.data_erase_at, timezone.now()):
        if not artefact.fetches.filter(status__in=AbdmFetchRequest.IN_FLIGHT).exists():
            fetch = request_health_information(artefact)
    return {
        "artefact": artefact.artefact_id,
        "status": artefact.status,
        "fetch": str(fetch.external_id) if fetch else None,
    }


def request_health_information(artefact: AbdmConsentArtefact, date_from=None, date_to=None) -> AbdmFetchRequest:
    """`data-flow/v3/health-information/request` with a fresh X25519 key pair and our nonce. The
    private key stays on the row until the push is decrypted or the 20-minute window passes."""
    now = timezone.now()
    row = artefact.consent_request
    if not rules.artefact_is_live(artefact.status, artefact.data_erase_at, now):
        raise HiuError("CONSENT_NOT_LIVE", "The patient permission has ended.")
    push_url = data_push_url()
    if not push_url:
        raise HiuError("NO_CALLBACK_URL", "The ABDM callback URL is not set.")
    keys = crypto.new_session_keys()
    private_raw = keys.private_key.private_bytes(
        serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption()
    )
    date_from = date_from or artefact.date_from or row.date_from
    date_to = date_to or artefact.date_to or row.date_to
    deadline = now + rules.DATA_PUSH_WINDOW
    fetch = AbdmFetchRequest.objects.create(
        artefact=artefact,
        date_from=date_from,
        date_to=date_to,
        data_push_url=push_url,
        private_key=base64.b64encode(private_raw).decode("ascii"),
        nonce=keys.nonce_b64,
        requested_at=now,
        deadline_at=deadline,
    )
    body = rules.hi_request_body(
        artefact_id=artefact.artefact_id,
        date_from=date_from,
        date_to=date_to,
        data_push_url=push_url,
        key_material=rules.key_material_block(keys.public_key_b64, keys.nonce_b64, deadline),
    )
    request = outbound.send(
        "m3-health-information-request", HI_REQUEST_URL, body, facility=row.facility, patient=row.patient, role="hiu"
    )
    fetch.hi_request = request
    if request.status != Succeeded:
        fetch.status = fetch.Status.FAILED
        fetch.private_key = ""
        _record_failure(fetch, request)
    fetch.save()
    return fetch


def handle_hi_on_request(callback: AbdmCallback) -> dict:
    """`/v3/hiu/health-information/on-request`: the transaction id the push will carry."""
    data = rules.parse_hi_on_request(callback.parsed_json or {})
    fetch = (
        AbdmFetchRequest.objects.filter(hi_request=callback.outbound_request).first()
        if callback.outbound_request_id
        else None
    )
    if fetch is None:
        raise ValueError(f"on-request answers no health-information request we sent ({data['request_id']!r})")
    if data["error_code"]:
        fetch.status = fetch.Status.FAILED
        fetch.private_key = ""
        failure = errors.classify(
            code=data["error_code"], message=data["error_message"], request_id=callback.response_request_id
        )
        fetch.error_code = failure.code[:64]
        fetch.error_message = failure.summary()[:512]
    else:
        fetch.transaction_id = data["transaction_id"][:128]
        fetch.status = fetch.Status.ACKNOWLEDGED
        fetch.acknowledged_at = timezone.now()
    fetch.save()
    return {"fetch": str(fetch.external_id), "transaction_id": fetch.transaction_id, "status": fetch.status}


def _load_private(fetch: AbdmFetchRequest) -> tuple[X25519PrivateKey, bytes]:
    private = X25519PrivateKey.from_private_bytes(base64.b64decode(fetch.private_key))
    return private, base64.b64decode(fetch.nonce)


def handle_transfer(callback: AbdmCallback) -> dict:
    """The HIP push at our data push URL: decrypt every entry with the key of the transaction,
    check the MD5, store the bundle, and after the last page notify RECEIVED or FAILED."""
    data = rules.parse_transfer(callback.parsed_json or {})
    fetch = (
        AbdmFetchRequest.objects.filter(transaction_id=data["transaction_id"])
        .select_related("artefact__consent_request__patient", "artefact__consent_request__facility")
        .first()
        if data["transaction_id"]
        else None
    )
    if fetch is None:
        raise ValueError(f"push names no transaction we requested ({data['transaction_id']!r})")
    _scrub_callback(callback, data)
    if not fetch.private_key:
        return {"fetch": str(fetch.external_id), "skipped": "key already used or expired", "status": fetch.status}
    artefact = fetch.artefact
    row = artefact.consent_request
    now = timezone.now()
    results: list[dict] = []
    try:
        peer_public, peer_nonce = crypto.check_key_material(data["key_material"])
        private, own_nonce = _load_private(fetch)
    except (crypto.KeyMaterialError, ValueError) as exc:
        results = [
            {"careContextReference": e["careContextReference"], "hiStatus": "ERRORED", "description": str(exc)[:200]}
            for e in data["entries"]
        ] or [{"careContextReference": "", "hiStatus": "ERRORED", "description": str(exc)[:200]}]
        fetch.error_code = "DECRYPT_FAILED"
    else:
        for entry in data["entries"]:
            results.append(_store_entry(fetch, artefact, row, entry, private, own_nonce, peer_public, peer_nonce, now))
    fetch.entries = list(fetch.entries or []) + results
    fetch.pages_expected = max(1, data["page_count"])
    fetch.pages_received = (fetch.pages_received or 0) + 1
    complete = fetch.pages_received >= fetch.pages_expected
    if complete:
        ok = [e for e in fetch.entries if e.get("hiStatus") == "OK"]
        if ok and len(ok) == len(fetch.entries):
            fetch.status = fetch.Status.RECEIVED
        elif ok:
            fetch.status = fetch.Status.PARTIAL
        else:
            fetch.status = fetch.Status.FAILED
            fetch.error_code = fetch.error_code or "DECRYPT_FAILED"
            fetch.error_message = (fetch.entries[0].get("description") if fetch.entries else "No entry")[:512]
        fetch.received_at = now
        fetch.private_key = ""
        fetch.notify_request = outbound.send(
            "m3-health-information-notify",
            HI_NOTIFY_URL,
            rules.hiu_notify_body(
                artefact_id=artefact.artefact_id,
                transaction_id=fetch.transaction_id,
                done_at=utc_timestamp(),
                hiu_id=hip_id_for(row.facility),
                hip_id=artefact.hip_id,
                entries=fetch.entries,
            ),
            facility=row.facility,
            patient=row.patient,
            role="hiu",
        )
    fetch.save()
    return {
        "fetch": str(fetch.external_id),
        "status": fetch.status,
        "page": f"{fetch.pages_received}/{fetch.pages_expected}",
        "entries": len(results),
        "stored": sum(1 for e in results if e.get("hiStatus") == "OK"),
    }


def _errored(reference: str, description: str) -> dict:
    return {"careContextReference": reference, "hiStatus": "ERRORED", "description": description[:200]}


def _store_entry(fetch, artefact, row, entry, private, own_nonce, peer_public, peer_nonce, now) -> dict:
    reference = entry["careContextReference"]
    if not entry["content"]:
        return _errored(reference, "Link entries are not supported; content expected")
    try:
        plaintext = crypto.decrypt(entry["content"], private, own_nonce, peer_public, peer_nonce)
    except Exception as exc:  # noqa: BLE001 - any failure here is "could not decrypt"
        return _errored(reference, f"Decryption failed: {exc}")
    checksum_ok = bool(entry["checksum"]) and crypto.md5_checksum(plaintext) == entry["checksum"].strip().lower()
    try:
        bundle = json.loads(plaintext.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return _errored(reference, f"Content is not JSON: {exc}")
    if not isinstance(bundle, dict):
        return _errored(reference, "Content is not a FHIR bundle")
    summary = rules.bundle_summary(bundle)
    AbdmFetchedRecord.objects.create(
        fetch=fetch,
        artefact=artefact,
        patient=row.patient,
        facility=row.facility,
        care_context_reference=reference[:256],
        hi_type=summary["hi_type"],
        title=summary["title"],
        authored_at=summary["authored_at"],
        hip_id=artefact.hip_id,
        hip_name=artefact.hip_name,
        checksum_ok=checksum_ok,
        resource_count=summary["resource_count"],
        bundle=bundle,
        received_at=now,
        erase_at=artefact.data_erase_at,
    )
    # AES-GCM already authenticates the content, so a checksum mismatch is recorded, not refused
    # (the docs do not say which serialisation the MD5 covers; docs/findings.md L5).
    description = "Data received successfully" if checksum_ok else "Data received; MD5 checksum did not match"
    return {"careContextReference": reference, "hiStatus": "OK", "description": description}


def _scrub_callback(callback: AbdmCallback, data: dict) -> None:
    """Ciphertext is never kept (models.py invariant): the stored callback loses `entries[].content`."""
    parsed = dict(callback.parsed_json or {})
    parsed["entries"] = [{k: v for k, v in e.items() if k != "content"} for e in data["entries"]]
    callback.parsed_json = parsed
    callback.raw_body = "[entries[].content removed after decryption]"
    callback.save(update_fields=["parsed_json", "raw_body", "modified_date"])


def check_transfer_status(fetch: AbdmFetchRequest) -> AbdmOutboundRequest | None:
    """`GET health-information/request/status/{transaction-id}`: `{transactionId, status}`."""
    if not fetch.transaction_id:
        return None
    row = fetch.artefact.consent_request
    return outbound.send(
        "m3-health-information-request-status",
        HI_STATUS_URL.format(transaction_id=fetch.transaction_id),
        None,
        method="GET",
        facility=row.facility,
        patient=row.patient,
        role="hiu",
    )


def refresh(row: AbdmConsentRequest) -> AbdmConsentRequest:
    """The desk's "Check": poll the request while it is open; ask the gateway about a transfer
    that has not landed."""
    if rules.request_is_open(row.status):
        refresh_status(row)
    for artefact in row.artefacts.all():
        for fetch in artefact.fetches.filter(status=AbdmFetchRequest.Status.ACKNOWLEDGED):
            check_transfer_status(fetch)
    return row


def fetch_again(row: AbdmConsentRequest) -> list[AbdmFetchRequest]:
    """The desk's "Fetch again": a new health-information request under every live artefact that
    has no request in flight."""
    now = timezone.now()
    out = []
    for artefact in row.artefacts.all():
        if not rules.artefact_is_live(artefact.status, artefact.data_erase_at, now):
            continue
        if artefact.fetches.filter(status__in=AbdmFetchRequest.IN_FLIGHT, deadline_at__gt=now).exists():
            continue
        out.append(request_health_information(artefact))
    if not out:
        raise HiuError("CONSENT_NOT_LIVE", "No live permission to fetch under.")
    return out


# --- retention and housekeeping ------------------------------------------------------------------


def erase_records(artefact: AbdmConsentArtefact, now=None) -> int:
    now = now or timezone.now()
    count = 0
    for record in artefact.records.filter(erased_at__isnull=True):
        record.bundle = {}
        record.erased_at = now
        record.save(update_fields=["bundle", "erased_at", "modified_date"])
        count += 1
    return count


def erase_due_records(now=None) -> int:
    """Erase every bundle past its `erase_at` (the consent `dataEraseAt`)."""
    now = now or timezone.now()
    count = 0
    for record in AbdmFetchedRecord.objects.filter(erased_at__isnull=True, erase_at__lte=now):
        record.bundle = {}
        record.erased_at = now
        record.save(update_fields=["bundle", "erased_at", "modified_date"])
        count += 1
    return count


def expire_stale_fetches(now=None) -> int:
    """A request with no push inside the 20-minute window: drop the key, tell the gateway FAILED
    ("FAILED when data was not sent", the notify page), and let the desk fetch again."""
    now = now or timezone.now()
    count = 0
    stale = AbdmFetchRequest.objects.filter(
        status__in=[AbdmFetchRequest.Status.REQUESTED, AbdmFetchRequest.Status.ACKNOWLEDGED], deadline_at__lt=now
    ).select_related("artefact__consent_request__facility", "artefact__consent_request__patient")
    for fetch in stale:
        fetch.status = fetch.Status.FAILED
        fetch.private_key = ""
        fetch.error_code = "NO_DATA"
        fetch.error_message = errors.classify(code="NO_DATA").summary()[:512]
        row = fetch.artefact.consent_request
        if fetch.transaction_id:
            fetch.notify_request = outbound.send(
                "m3-health-information-notify",
                HI_NOTIFY_URL,
                rules.hiu_notify_body(
                    artefact_id=fetch.artefact.artefact_id,
                    transaction_id=fetch.transaction_id,
                    done_at=utc_timestamp(),
                    hiu_id=hip_id_for(row.facility),
                    hip_id=fetch.artefact.hip_id,
                    entries=[],
                ),
                facility=row.facility,
                patient=row.patient,
                role="hiu",
            )
        fetch.save()
        count += 1
    return count


def housekeeping() -> dict:
    now = timezone.now()
    return {"expired_fetches": expire_stale_fetches(now), "erased_records": erase_due_records(now)}


# --- provider directory ----------------------------------------------------------------------------


def search_providers(name: str) -> list[dict]:
    """`GET gateway/v3/providers?name=`: `[{identifier{name,id}, facilityType[], isHIP, ...}]`.
    204 means no match. Returns `[{id, name, isHip}]` for the desk picker."""
    query = rules.safe_text(name)
    if not query:
        return []
    request = outbound.send(
        "gateway-get-providers", f"{PROVIDERS_URL}?name={quote(query)}", None, method="GET", facility=None
    )
    if request.status != Succeeded:
        raise HiuError(request.error_code or "HTTP_ERROR", outbound.failure_detail(request))
    payload = request.response_json if isinstance(request.response_json, list) else []
    out = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        identifier = item.get("identifier") if isinstance(item.get("identifier"), dict) else {}
        pid = str(identifier.get("id") or "")
        if pid:
            out.append({"id": pid, "name": str(identifier.get("name") or pid), "isHip": bool(item.get("isHIP"))})
    return out


# --- what the desk reads ------------------------------------------------------------------------


def _failure_of(row, request: AbdmOutboundRequest | None) -> dict | None:
    if not row.error_code:
        return None
    failure = errors.classify(
        code=row.error_code,
        message=row.error_message,
        request_id=request.request_id if request else "",
    )
    block = failure.as_dict()
    block["detail"] = row.error_message
    return block


def record_summary(record: AbdmFetchedRecord) -> dict:
    return {
        "id": str(record.external_id),
        "careContextReference": record.care_context_reference,
        "hiType": record.hi_type,
        "title": record.title,
        "authoredAt": record.authored_at,
        "hipId": record.hip_id,
        "hipName": record.hip_name,
        "checksumOk": record.checksum_ok,
        "resourceCount": record.resource_count,
        "receivedAt": record.received_at,
        "eraseAt": record.erase_at,
        "erasedAt": record.erased_at,
        "available": record.available,
    }


def fetch_summary(fetch: AbdmFetchRequest) -> dict:
    return {
        "id": str(fetch.external_id),
        "transactionId": fetch.transaction_id,
        "status": fetch.status,
        "requestedAt": fetch.requested_at,
        "deadlineAt": fetch.deadline_at,
        "acknowledgedAt": fetch.acknowledged_at,
        "receivedAt": fetch.received_at,
        "pages": f"{fetch.pages_received}/{fetch.pages_expected}",
        "entries": fetch.entries,
        "requestId": fetch.hi_request.request_id if fetch.hi_request_id else "",
        "failure": _failure_of(fetch, fetch.hi_request),
    }


def artefact_summary(artefact: AbdmConsentArtefact, now) -> dict:
    return {
        "id": str(artefact.external_id),
        "artefactId": artefact.artefact_id,
        "status": artefact.status,
        "live": rules.artefact_is_live(artefact.status, artefact.data_erase_at, now),
        "hipId": artefact.hip_id,
        "hipName": artefact.hip_name,
        "hiTypes": artefact.hi_types,
        "careContextReferences": artefact.care_context_references,
        "dateFrom": artefact.date_from,
        "dateTo": artefact.date_to,
        "dataEraseAt": artefact.data_erase_at,
        "fetchedAt": artefact.fetched_at,
        "failure": _failure_of(artefact, artefact.fetch_request),
        "fetches": [fetch_summary(f) for f in artefact.fetches.order_by("-requested_at")],
        "records": [record_summary(r) for r in artefact.records.order_by("-received_at")],
    }


def consent_request_summary(row: AbdmConsentRequest, now=None) -> dict:
    now = now or timezone.now()
    requested_by = row.requested_by
    return {
        "id": str(row.external_id),
        "consentRequestId": row.consent_request_id,
        "status": row.status,
        "open": rules.request_is_open(row.status),
        "purposeCode": row.purpose_code,
        "purposeText": rules.PURPOSES.get(row.purpose_code, row.purpose_code),
        "hiTypes": row.hi_types,
        "dateFrom": row.date_from,
        "dateTo": row.date_to,
        "dataEraseAt": row.data_erase_at,
        "hipId": row.hip_id,
        "hipName": row.hip_name,
        "requestedBy": (getattr(requested_by, "full_name", "") or getattr(requested_by, "username", ""))
        if requested_by
        else "",
        "requestedAt": row.created_date,
        "statusCheckedAt": row.status_checked_at,
        "decidedAt": row.decided_at,
        "reason": row.reason,
        "requestId": row.init_request.request_id if row.init_request_id else "",
        "failure": _failure_of(row, row.init_request),
        "artefacts": [artefact_summary(a, now) for a in row.artefacts.order_by("created_date")],
    }


def hiu_state(patient: Patient, facility) -> dict:
    """What the ABDM tab's 3rd card reads: the requests of this patient at this facility, newest first."""
    now = timezone.now()
    address, _ = patient_abha(patient)
    defaults = rules.default_request(now)
    rows = (
        AbdmConsentRequest.objects.filter(patient=patient, facility=facility)
        .select_related("requested_by", "init_request")
        .prefetch_related("artefacts__fetches", "artefacts__records")
        .order_by("-created_date")[:50]
    )
    return {
        "facilityConfigured": bool(hip_id_for(facility)),
        "callbackUrlSet": bool(data_push_url()),
        "patientAbhaAddress": address,
        "purposes": [{"code": code, "text": text} for code, text in rules.PURPOSES.items()],
        "hiTypes": list(rules.HI_TYPES),
        "defaults": {
            "purposeCode": defaults["purpose_code"],
            "hiTypes": defaults["hi_types"],
            "dateFrom": defaults["date_from"],
            "dateTo": defaults["date_to"],
            "dataEraseAt": defaults["data_erase_at"],
        },
        "requests": [consent_request_summary(r, now) for r in rows],
    }


def record_detail(record: AbdmFetchedRecord) -> dict:
    data = record_summary(record)
    data["bundle"] = record.bundle if record.available else None
    return data
