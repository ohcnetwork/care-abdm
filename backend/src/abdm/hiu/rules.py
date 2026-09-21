"""
Pure rules for M3 (HIU). No Django imports, so backend/tests can import this module.

Sources (docs mirror of 2026-09-19, catalogue 2026.09.16):
  /docs/hiecm/v3/milestones/m3                     the 3 journeys and "What you build, in order"
  /docs/hiecm/v3/concepts/consent                  purpose codes, HI types, the 5 consent states
  /docs/hiecm/v3/concepts/data-flow                the key exchange and the 20-minute window
  /docs/hiecm/v3/api/m3/endpoints/m3-consent-management-data-flow-hiu/01..12
                                                   every body shape quoted in the builders and parsers below
  /docs/hiecm/v3/api/m2/endpoints/m2-consent-management-data-flow-hip/05-m2-post-health-information-transfer
                                                   the body the HIP pushes to our data push URL
"""

import re
from datetime import UTC, datetime, timedelta

from abdm import errors
from abdm.hip.rules import DATA_PUSH_WINDOW, parse_iso, within  # noqa: F401 - re-exported for the service

# concepts/consent "Purpose of use codes": 6 codes, and the display text the patient reads.
PURPOSES: dict[str, str] = {
    "CAREMGT": "Care Management",
    "BTG": "Break the Glass",
    "PUBHLTH": "Public Health",
    "HPAYMT": "Healthcare Payment",
    "DSRCH": "Disease Specific Healthcare Research",
    "PATRQT": "Self Requested",
}
DEFAULT_PURPOSE = "CAREMGT"

# The 8 `hiTypes` values of the consent init schema (MCP get_operation, `consent.hiTypes.items.enum`).
HI_TYPES: tuple[str, ...] = (
    "OPConsultation",
    "Prescription",
    "DiagnosticReport",
    "DischargeSummary",
    "ImmunizationRecord",
    "HealthDocumentRecord",
    "WellnessRecord",
    "Invoice",
)
# Rithvik, 2026-09-19: the desk asks for the 7 clinical types; Invoice stays off unless ticked.
DEFAULT_HI_TYPES: tuple[str, ...] = HI_TYPES[:-1]

# Rithvik, 2026-09-19: records of the last 12 months; the consent runs 30 days from the request.
DEFAULT_RANGE = timedelta(days=365)
DEFAULT_VALIDITY = timedelta(days=30)
# `permission.accessMode` and `permission.frequency` as the endpoint example sends them. The docs
# define neither the modes nor the frequency (docs/findings.md L2).
ACCESS_MODE = "VIEW"
FREQUENCY = {"unit": "HOUR", "value": 1, "repeats": 0}
# `purpose.refUri`: the example sends `www.abc.com`; the field must match ^[a-zA-Z0-9_\-@,. ":/]{0,255}$.
PURPOSE_REF_URI = "https://terminology.hl7.org/ValueSet/v3-PurposeOfUse"

# The consent request states (concepts/consent "The states a consent moves through") plus the 2
# the plug adds for a request that never reached the HIE-CM.
REQUEST_STATES = ("REQUESTED", "GRANTED", "DENIED", "EXPIRED", "REVOKED")
ARTEFACT_STATES = ("GRANTED", "DENIED", "EXPIRED", "REVOKED")

# Our data push URL, relative to the bridge URL. The docs let the HIU name any https URL
# (m3 request page: `dataPushUrl`); keeping it under the bridge lets the signed catch-all receive it.
DATA_PUSH_PATH = "/v3/hiu/health-information/transfer"

# NRCES document profiles -> ABDM HI type, read off `Composition.meta.profile` of a received bundle.
PROFILE_HI_TYPES: dict[str, str] = {
    "OPConsultRecord": "OPConsultation",
    "PrescriptionRecord": "Prescription",
    "DiagnosticReportRecord": "DiagnosticReport",
    "DischargeSummaryRecord": "DischargeSummary",
    "ImmunizationRecord": "ImmunizationRecord",
    "HealthDocumentRecord": "HealthDocumentRecord",
    "WellnessRecord": "WellnessRecord",
    "InvoiceRecord": "Invoice",
}

_ABHA_ADDRESS_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.\-!]+[a-zA-Z0-9]@(abdm|sbx)$")


def to_abdm_iso(value: datetime) -> str:
    """`2021-09-28T12:30:08.573Z`: UTC, ISO 8601, 3 fractional digits, `Z`. Every date field of the
    M3 pages is validated against `\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$`."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    value = value.astimezone(UTC)
    return value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond // 1000:03d}Z"


def abha_address_ok(value: str) -> bool:
    return bool(_ABHA_ADDRESS_RE.match(value or ""))


def safe_text(value: str, fallback: str = "") -> str:
    """Clip a free-text value to what the `^[a-zA-Z0-9_\\-@,. ":/]{0,255}$` fields accept."""
    cleaned = re.sub(r'[^a-zA-Z0-9_\-@,. ":/]', " ", str(value or "")).strip()
    cleaned = re.sub(r"\s{2,}", " ", cleaned)[:255]
    return cleaned or fallback


def default_request(now: datetime) -> dict:
    return {
        "purpose_code": DEFAULT_PURPOSE,
        "hi_types": list(DEFAULT_HI_TYPES),
        "date_from": now - DEFAULT_RANGE,
        "date_to": now,
        "data_erase_at": now + DEFAULT_VALIDITY,
        "hip_id": "",
        "hip_name": "",
    }


def validate_request(params: dict, now: datetime) -> dict:
    """Normalise what the desk sent. Raises ValueError with the sentence the desk reads."""
    defaults = default_request(now)
    purpose = str(params.get("purpose_code") or defaults["purpose_code"]).upper()
    if purpose not in PURPOSES:
        raise ValueError(f"Purpose must be 1 of {', '.join(PURPOSES)}.")
    hi_types = [str(h) for h in (params.get("hi_types") or defaults["hi_types"])]
    unknown = [h for h in hi_types if h not in HI_TYPES]
    if unknown:
        raise ValueError(f"Unknown record type: {', '.join(unknown)}.")
    if not hi_types:
        raise ValueError("Select at least 1 record type.")
    date_from = parse_iso(params.get("date_from")) if params.get("date_from") else defaults["date_from"]
    date_to = parse_iso(params.get("date_to")) if params.get("date_to") else defaults["date_to"]
    erase_at = parse_iso(params.get("data_erase_at")) if params.get("data_erase_at") else defaults["data_erase_at"]
    if date_from is None or date_to is None or erase_at is None:
        raise ValueError("Dates must be ISO 8601.")
    # Observed on the sandbox 2026-09-19 (findings L9): a `dateRange.to` in the future is refused with
    # ABDM-9999 "Invalid from/to date and Date must be a present/before date". The desk picks a day, and
    # the end of today is in the future, so the range ends now at the latest.
    date_to = min(date_to, now)
    if date_from > date_to:
        raise ValueError("The start of the date range is after its end.")
    if erase_at <= now:
        raise ValueError("The consent validity must end in the future.")
    hip_id = safe_text(params.get("hip_id") or "")
    hip_name = safe_text(params.get("hip_name") or "")
    if hip_id and not hip_name:
        raise ValueError("A provider needs both an id and a name.")
    return {
        "purpose_code": purpose,
        "hi_types": list(dict.fromkeys(hi_types)),
        "date_from": date_from,
        "date_to": date_to,
        "data_erase_at": erase_at,
        "hip_id": hip_id,
        "hip_name": hip_name,
    }


# --- request body builders (field names quoted from the M3 flow pages) ---------------------------


def consent_request_body(
    *,
    abha_address: str,
    hiu_id: str,
    hiu_name: str,
    requester_name: str,
    requester_identifier: dict,
    purpose_code: str,
    hi_types: list[str],
    date_from: datetime,
    date_to: datetime,
    data_erase_at: datetime,
    hip_id: str = "",
    hip_name: str = "",
) -> dict:
    """`01-m3-post-consent-v3-request-init`. `hip` is nullable in the schema, so it is sent only
    when the desk picked a provider. `careContexts` is optional and is never sent: the HIU does not
    know the other facility's references."""
    consent: dict = {
        "purpose": {"text": PURPOSES[purpose_code], "code": purpose_code, "refUri": PURPOSE_REF_URI},
        "patient": {"id": abha_address},
        "hiu": {"id": hiu_id, "name": hiu_name, "type": "HIU"},
        "requester": {"name": requester_name, "identifier": dict(requester_identifier)},
        "hiTypes": list(hi_types),
        "permission": {
            "accessMode": ACCESS_MODE,
            "dateRange": {"from": to_abdm_iso(date_from), "to": to_abdm_iso(date_to)},
            "dataEraseAt": to_abdm_iso(data_erase_at),
            "frequency": dict(FREQUENCY),
        },
    }
    if hip_id:
        consent["hip"] = {"id": hip_id, "name": hip_name, "type": "HIP"}
    return {"consent": consent}


def requester_identifier(*, registration: str, username: str, system: str) -> dict:
    """`consent.requester.identifier {value, type, system}` (all required). The docs example is
    `REG1` / `MH1001` / `https://www.sample.com` and defines no type list (findings L3). The
    medical council registration is sent when the user has one; the Care username otherwise."""
    value = safe_text(registration) or safe_text(username, "unknown")
    kind = "MEDICAL_COUNCIL_REGISTRATION" if safe_text(registration) else "CARE_USERNAME"
    return {"value": value, "type": kind, "system": safe_text(system, "care")}


def consent_status_body(consent_request_id: str) -> dict:
    """`03-m3-post-consent-v3-request-status`."""
    return {"consentRequestId": consent_request_id}


def consent_notify_ack_body(artefact_ids: list[str], request_id: str, ok: bool = True) -> dict:
    """`06-m3-post-consent-v3-request-hiu-on-notify`. `acknowledgement` is an array here (the HIP
    ack is 1 object); `response.requestId` is the REQUEST-ID of the notify callback."""
    return {
        "acknowledgement": [{"status": "OK" if ok else "ERROR", "consentId": cid} for cid in artefact_ids],
        "response": {"requestId": request_id},
    }


def consent_fetch_body(artefact_id: str) -> dict:
    """`07-m3-post-consent-v3-fetch`."""
    return {"consentId": artefact_id}


def key_material_block(public_key_b64: str, nonce_b64: str, expiry: datetime) -> dict:
    """`hiRequest.keyMaterial` as the M3 request page sends it: `curve25519` in lower case and
    `parameters: "Ephemeral public key"`. The HIP push uses `Curve25519` and a different
    `parameters` text; our own HIP compares both case-insensitively (hip/crypto.py)."""
    return {
        "cryptoAlg": "ECDH",
        "curve": "curve25519",
        "dhPublicKey": {
            "expiry": to_abdm_iso(expiry),
            "parameters": "Ephemeral public key",
            "keyValue": public_key_b64,
        },
        "nonce": nonce_b64,
    }


def hi_request_body(
    *, artefact_id: str, date_from: datetime, date_to: datetime, data_push_url: str, key_material: dict
) -> dict:
    """`09-m3-post-data-flow-v3-health-information-request`."""
    return {
        "hiRequest": {
            "consent": {"id": artefact_id},
            "dateRange": {"from": to_abdm_iso(date_from), "to": to_abdm_iso(date_to)},
            "dataPushUrl": data_push_url,
            "keyMaterial": dict(key_material),
        }
    }


def hiu_notify_body(
    *, artefact_id: str, transaction_id: str, done_at: str, hiu_id: str, hip_id: str, entries: list[dict]
) -> dict:
    """`11-m3-post-data-flow-v3-health-information-notify`, HIU side: `sessionStatus` RECEIVED or
    FAILED, `hiStatus` OK or ERRORED per care context."""
    ok = bool(entries) and any(e.get("hiStatus") == "OK" for e in entries)
    return {
        "notification": {
            "consentId": artefact_id,
            "transactionId": transaction_id,
            "doneAt": done_at,
            "notifier": {"type": "HIU", "id": hiu_id},
            "statusNotification": {
                "sessionStatus": "RECEIVED" if ok else "FAILED",
                "hipId": hip_id,
                "statusResponses": [
                    {
                        "careContextReference": e.get("careContextReference", ""),
                        "hiStatus": e.get("hiStatus", "ERRORED"),
                        "description": safe_text(e.get("description", ""), "Data received"),
                    }
                    for e in entries
                ],
            },
        }
    }


# --- callback parsers (field names quoted from the M3 flow pages) --------------------------------


def _dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def parse_error(parsed: dict) -> tuple[str, str]:
    """`error {code, message}`; the pages send `error: null` on success. Codes may carry a trailing
    `: ` (the pages say so), so the code goes through `errors.normalize_code`."""
    error = _dict(parsed.get("error"))
    return errors.normalize_code(error.get("code")), str(error.get("message") or "")


def parse_on_init(parsed: dict) -> dict:
    """`02-m3-post-v3-hiu-consent-request-on-init`: `consentRequest.id` or `error`."""
    code, message = parse_error(parsed)
    return {
        "consent_request_id": str(_dict(parsed.get("consentRequest")).get("id") or ""),
        "request_id": str(_dict(parsed.get("response")).get("requestId") or ""),
        "error_code": code,
        "error_message": message,
    }


def parse_on_status(parsed: dict) -> dict:
    """`04-m3-post-v3-hiu-consent-request-on-status`: `consentRequest {id, status}`."""
    code, message = parse_error(parsed)
    request = _dict(parsed.get("consentRequest"))
    return {
        "consent_request_id": str(request.get("id") or ""),
        "status": str(request.get("status") or "").upper(),
        "request_id": str(_dict(parsed.get("response")).get("requestId") or ""),
        "error_code": code,
        "error_message": message,
    }


def parse_consent_notify(parsed: dict) -> dict:
    """`05-m3-post-v3-hiu-consent-request-notify`: `notification {consentRequestId, status, reason,
    consentArtefacts[{id}]}`. For REVOKED the page says the artefact list names the revoked ids."""
    notification = _dict(parsed.get("notification")) or parsed
    artefacts = notification.get("consentArtefacts")
    ids = (
        [str(a.get("id")) for a in artefacts if isinstance(a, dict) and a.get("id")]
        if isinstance(artefacts, list)
        else []
    )
    return {
        "consent_request_id": str(notification.get("consentRequestId") or ""),
        "status": str(notification.get("status") or "").upper(),
        "reason": str(notification.get("reason") or ""),
        "artefact_ids": ids,
    }


def parse_on_fetch(parsed: dict) -> dict:
    """`08-m3-post-v3-hiu-consent-on-fetch`: `consent {status, consentDetail {...}, signature}`.
    `permission.dateRange` sits inside `consentDetail.permission`; `dataEraseAt` and `frequency`
    sit beside `permission` on this page, not inside it as on the init page, so both places are read."""
    consent = _dict(parsed.get("consent"))
    detail = _dict(consent.get("consentDetail"))
    permission = _dict(detail.get("permission"))
    date_range = _dict(permission.get("dateRange"))
    hip = _dict(detail.get("hip"))
    hiu = _dict(detail.get("hiu"))
    code, message = parse_error(parsed)
    return {
        "status": str(consent.get("status") or "").upper(),
        "artefact_id": str(detail.get("consentId") or ""),
        "abha_address": str(_dict(detail.get("patient")).get("id") or ""),
        "hip_id": str(hip.get("id") or ""),
        "hip_name": str(hip.get("name") or ""),
        "hiu_id": str(hiu.get("id") or ""),
        "hi_types": [str(h) for h in detail.get("hiTypes") or [] if h],
        "care_context_references": [
            str(c.get("careContextReference") or "")
            for c in detail.get("careContexts") or []
            if isinstance(c, dict) and c.get("careContextReference")
        ],
        "date_from": parse_iso(date_range.get("from")),
        "date_to": parse_iso(date_range.get("to")),
        "data_erase_at": parse_iso(detail.get("dataEraseAt") or permission.get("dataEraseAt")),
        "signature": str(consent.get("signature") or ""),
        "detail": detail,
        "request_id": str(_dict(parsed.get("response")).get("requestId") or ""),
        "error_code": code,
        "error_message": message,
    }


def parse_hi_on_request(parsed: dict) -> dict:
    """`10-m3-post-v3-hiu-health-information-on-request`: `hiRequest {transactionId, sessionStatus}`
    or `error`."""
    code, message = parse_error(parsed)
    request = _dict(parsed.get("hiRequest"))
    return {
        "transaction_id": str(request.get("transactionId") or ""),
        "session_status": str(request.get("sessionStatus") or "").upper(),
        "request_id": str(_dict(parsed.get("response")).get("requestId") or ""),
        "error_code": code,
        "error_message": message,
    }


def parse_transfer(parsed: dict) -> dict:
    """The HIP push (`m2-consent-management-data-flow-hip/05-m2-post-health-information-transfer`):
    `pageNumber, pageCount, transactionId, entries[{content, media, checksum, careContextReference}],
    keyMaterial`. `entries[].link` is allowed by the prose ("content or link"); a link entry is
    recorded as ERRORED because the docs give it no shape."""
    entries = []
    for entry in parsed.get("entries") or []:
        if not isinstance(entry, dict):
            continue
        entries.append(
            {
                "content": str(entry.get("content") or ""),
                "link": str(entry.get("link") or ""),
                "media": str(entry.get("media") or ""),
                "checksum": str(entry.get("checksum") or ""),
                "careContextReference": str(entry.get("careContextReference") or ""),
            }
        )

    def _int(value, default):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    return {
        "transaction_id": str(parsed.get("transactionId") or ""),
        "page_number": _int(parsed.get("pageNumber"), 1),
        "page_count": _int(parsed.get("pageCount"), 1),
        "entries": entries,
        "key_material": _dict(parsed.get("keyMaterial")),
    }


# --- received bundles -------------------------------------------------------------------------


def bundle_summary(bundle: dict) -> dict:
    """What the desk lists for 1 received bundle: the HI type (from the Composition profile), the
    Composition title and date. Nothing here is trusted beyond display."""
    entries = bundle.get("entry") if isinstance(bundle, dict) else None
    composition: dict = {}
    for entry in entries or []:
        resource = _dict(_dict(entry).get("resource"))
        if resource.get("resourceType") == "Composition":
            composition = resource
            break
    profiles = [str(p) for p in (_dict(composition.get("meta")).get("profile") or []) if p]
    hi_type = ""
    for profile in profiles:
        name = profile.rstrip("/").rsplit("/", 1)[-1]
        if name in PROFILE_HI_TYPES:
            hi_type = PROFILE_HI_TYPES[name]
            break
    return {
        "hi_type": hi_type,
        "title": str(composition.get("title") or "")[:256],
        "authored_at": parse_iso(composition.get("date")),
        "resource_count": len(entries) if isinstance(entries, list) else 0,
    }


def request_is_open(status: str) -> bool:
    """The desk may still hear back: the patient has not decided."""
    return status == "REQUESTED"


def artefact_is_live(status: str, data_erase_at: datetime | None, now: datetime) -> bool:
    """A GRANTED artefact whose validity has not run out. Past it the plug stops fetching and
    erases what it holds (milestones/m3 step 6; Rithvik 2026-09-19)."""
    return status == "GRANTED" and (data_erase_at is None or data_erase_at > now)
