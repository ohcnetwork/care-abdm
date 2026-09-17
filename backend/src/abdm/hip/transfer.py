"""
Health-information request and data transfer (M2 journey 4).

/docs/hiecm/v3/concepts/data-flow, stage 2: before the HIP retrieves anything it checks
  1. the consent is valid and active (GRANTED, not past dataEraseAt),
  2. the requested date range sits inside the consent range (a wider window is refused),
  3. the encryption parameters are correct (ECDH, Curve25519, 32-byte key and nonce).
Then it packages FHIR bundles, encrypts them (hip/crypto.py), pushes them to `dataPushUrl`
(body shape: m3-on-health-information-transfer) and calls m2-hip-data-flow-notify.
Timeout: 20 minutes from the request. Everything here runs inside a Celery task.
"""

import json
import logging

from care.emr.models.encounter import Encounter
from django.utils import timezone

from abdm.facility.service import facility_for_hip_id, hip_id_for
from abdm.fhir import BundleError, available_hi_types, build_bundle
from abdm.gateway import outbound
from abdm.gateway.session import utc_timestamp
from abdm.hip import crypto, rules
from abdm.models import AbdmCallback, AbdmCareContext, AbdmConsent, AbdmDataRequest

logger = logging.getLogger(__name__)

ON_REQUEST_URL = "/api/hiecm/data-flow/v3/health-information/hip/on-request"
NOTIFY_URL = "/api/hiecm/data-flow/v3/health-information/notify"


class TransferError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _facility(callback: AbdmCallback, consent: AbdmConsent | None):
    if consent is not None and consent.facility_id:
        return consent.facility
    return facility_for_hip_id(callback.hip_id_header)


def _validate(row: AbdmDataRequest, consent: AbdmConsent | None) -> None:
    now = timezone.now()
    if consent is None:
        raise TransferError("ABDM-1062", f"Consent {row.consent_artefact_id} is not known to this HIP")
    if consent.status != AbdmConsent.Status.GRANTED:
        raise TransferError("ABDM-1062", f"Consent {consent.consent_id} is {consent.status}, not GRANTED")
    if consent.data_erase_at and consent.data_erase_at < now:
        raise TransferError("ABDM-1061", f"Consent {consent.consent_id} expired at {consent.data_erase_at.isoformat()}")
    if not rules.within(row.date_from, row.date_to, consent.date_from, consent.date_to):
        raise TransferError("ABDM-1063", "The requested date range is outside the consent date range")
    if not row.data_push_url.startswith("https://"):
        raise TransferError("ABDM-1010", "dataPushUrl must be an https URL")
    try:
        crypto.check_key_material(row.key_material)
    except crypto.KeyMaterialError as exc:
        raise TransferError("ABDM-1010", f"keyMaterial rejected: {exc}") from exc


def handle_health_information_request(callback: AbdmCallback) -> dict:
    """Store the request, validate it, acknowledge it, then transfer. Returns the row summary."""
    data = rules.parse_hi_request(callback.parsed_json or {})
    if not data["transaction_id"]:
        raise ValueError("Health information request has no transactionId")
    consent = AbdmConsent.objects.filter(consent_id=data["consent_id"]).first() if data["consent_id"] else None
    received_at = callback.received_at or timezone.now()
    row, created = AbdmDataRequest.objects.get_or_create(
        transaction_id=data["transaction_id"],
        defaults={
            "consent": consent,
            "consent_artefact_id": data["consent_id"],
            "facility": _facility(callback, consent),
            "data_push_url": data["data_push_url"][:1024],
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "key_material": data["key_material"],
            "received_at": received_at,
            "deadline_at": received_at + rules.DATA_PUSH_WINDOW,
            "callback": callback,
        },
    )
    if not created:
        # build-it-well: callbacks repeat. The first row keeps its outcome.
        return {"transaction_id": row.transaction_id, "status": row.status, "duplicate": True}
    try:
        _validate(row, consent)
    except TransferError as exc:
        row.status = row.Status.FAILED
        row.error_code = exc.code
        row.error_message = exc.message[:512]
        row.ack_request = outbound.send(
            "m2-hip-health-information-on-request",
            ON_REQUEST_URL,
            rules.hi_request_ack_body(row.transaction_id, callback.request_id_header, ok=False),
            facility=row.facility,
        )
        row.save()
        return {"transaction_id": row.transaction_id, "status": row.status, "error": exc.code}
    row.ack_request = outbound.send(
        "m2-hip-health-information-on-request",
        ON_REQUEST_URL,
        rules.hi_request_ack_body(row.transaction_id, callback.request_id_header),
        facility=row.facility,
    )
    row.status = row.Status.ACKNOWLEDGED
    row.save()
    transfer(row)
    return {"transaction_id": row.transaction_id, "status": row.status, "entries": len(row.entries)}


def _encounters_in_range(consent: AbdmConsent, row: AbdmDataRequest) -> list[AbdmCareContext]:
    contexts = AbdmCareContext.objects.filter(
        facility=row.facility, status=AbdmCareContext.Status.LINKED
    ).select_related("encounter")
    if consent.care_context_references:
        contexts = contexts.filter(reference_number__in=consent.care_context_references)
    elif consent.patient_id:
        contexts = contexts.filter(patient=consent.patient)
    else:
        return []
    picked = []
    for context in contexts:
        encounter: Encounter = context.encounter
        start = rules.parse_iso((encounter.period or {}).get("start")) if isinstance(encounter.period, dict) else None
        start = start or encounter.created_date
        if rules.within(start, start, row.date_from, row.date_to):
            picked.append(context)
    return picked


def build_entries(row: AbdmDataRequest, consent: AbdmConsent, keys: crypto.SessionKeys) -> list[dict]:
    """1 encrypted entry per (care context, HI type) named by the consent and held by the encounter."""
    peer_public, peer_nonce = crypto.check_key_material(row.key_material)
    wanted = set(consent.hi_types or [])
    entries: list[dict] = []
    for context in _encounters_in_range(consent, row):
        types = [t for t in available_hi_types(context.encounter) if not wanted or t in wanted]
        if not types:
            entries.append(
                {
                    "careContextReference": context.reference_number,
                    "hiType": "",
                    "hiStatus": "ERRORED",
                    "description": "No record of the consented HI types exists for this care context",
                }
            )
            continue
        for hi_type in types:
            try:
                bundle = build_bundle(context.encounter, hi_type)
            except BundleError as exc:
                entries.append(
                    {
                        "careContextReference": context.reference_number,
                        "hiType": hi_type,
                        "hiStatus": "ERRORED",
                        "description": str(exc)[:256],
                    }
                )
                continue
            plaintext = json.dumps(bundle, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            entries.append(
                {
                    "careContextReference": context.reference_number,
                    "hiType": hi_type,
                    "hiStatus": "OK",
                    "description": f"{hi_type} bundle {bundle.get('id', '')}",
                    "checksum": crypto.md5_checksum(plaintext),
                    "content": crypto.encrypt(plaintext, keys, peer_public, peer_nonce),
                }
            )
    return entries


def transfer(row: AbdmDataRequest) -> AbdmDataRequest:
    consent = row.consent or AbdmConsent.objects.filter(consent_id=row.consent_artefact_id).first()
    hip_id = hip_id_for(row.facility)
    keys = crypto.new_session_keys()
    try:
        entries = build_entries(row, consent, keys) if consent else []
        if not entries:
            raise TransferError(
                "NO_RECORDS", "No linked care context of this consent has records in the requested range"
            )
        if timezone.now() > row.deadline_at:
            raise TransferError("DEADLINE", "The 20 minute data push window has passed")
        pushed = [e for e in entries if e.get("hiStatus") == "OK"]
        if pushed:
            body = {
                "pageNumber": 1,
                "pageCount": 1,
                "transactionId": row.transaction_id,
                "entries": [
                    {
                        "content": e["content"],
                        "media": "application/fhir+json",
                        "checksum": e["checksum"],
                        "careContextReference": e["careContextReference"],
                    }
                    for e in pushed
                ],
                "keyMaterial": crypto.key_material_block(keys, row.deadline_at.strftime("%Y-%m-%dT%H:%M:%S.000Z")),
            }
            row.push_request = outbound.send("m2-data-push", row.data_push_url, body, facility=row.facility)
            if row.push_request.status != row.push_request.Status.SUCCEEDED:
                for e in pushed:
                    e["hiStatus"] = "ERRORED"
                    e["description"] = f"Data push failed: {outbound.failure_detail(row.push_request)}"[:256]
            else:
                row.pushed_at = timezone.now()
        # Ciphertext stays out of the table: it is large and useless after the push.
        row.entries = [{k: v for k, v in e.items() if k != "content"} for e in entries]
        row.status = row.Status.TRANSFERRED if row.pushed_at else row.Status.FAILED
        if not row.pushed_at:
            row.error_code = row.error_code or "PUSH_FAILED"
            row.error_message = (entries[0].get("description") or "Data push failed")[:512]
    except TransferError as exc:
        row.entries = []
        row.status = row.Status.FAILED
        row.error_code = exc.code[:64]
        row.error_message = exc.message[:512]
    row.notify_request = outbound.send(
        "m2-hip-data-flow-notify",
        NOTIFY_URL,
        rules.data_flow_notify_body(row.consent_artefact_id, row.transaction_id, utc_timestamp(), hip_id, row.entries),
        facility=row.facility,
    )
    row.save()
    return row


def data_request_summary(row: AbdmDataRequest) -> dict:
    return {
        "id": str(row.external_id),
        "transactionId": row.transaction_id,
        "consentId": row.consent_artefact_id,
        "status": row.status,
        "receivedAt": row.received_at,
        "deadlineAt": row.deadline_at,
        "pushedAt": row.pushed_at,
        "entries": row.entries,
        "errorCode": row.error_code,
        "errorMessage": row.error_message,
    }
