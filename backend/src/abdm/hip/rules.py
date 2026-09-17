"""
Pure rules for M2. No Django imports, so backend/tests can import this module.

Sources:
  /docs/hiecm/v3/concepts/linking        care context = reference number + display, no clinical detail;
                                         1 per OPD visit or IPD admission; link token valid 6 months
  /docs/hiecm/v3/api/m2/endpoints/*      body shapes quoted in the builders below
  /docs/hiecm/v3/concepts/data-flow      20 minutes from the request to the data push
  /docs/hiecm/v3/getting-started/build-it-well  callbacks repeat: deduplicate
"""

import base64
import hashlib
import hmac
import json
import re
import secrets
from datetime import UTC, datetime, timedelta

from abdm import errors

LINK_TOKEN_VALIDITY = timedelta(days=180)  # docs: "six months" (confirmed: the JWT `exp` is iat + 182.5 days)
DATA_PUSH_WINDOW = timedelta(minutes=20)  # docs: "20 minutes from the start of the request"
OTP_VALIDITY = timedelta(minutes=10)  # plug choice: the docs do not give a value
OTP_MAX_ATTEMPTS = 3  # plug choice
OTP_LENGTH = 6  # docs: `confirmation.token` is "The 6-digit OTP the patient entered"

# Rithvik, ADR-008 decision 2: FHIR `amb` -> OPD, `imp` -> IPD; class display text otherwise.
ENCOUNTER_CLASS_DISPLAY = {
    "amb": "OPD",
    "imp": "IPD",
    "emer": "Emergency",
    "obsenc": "Observation",
    "vr": "Virtual",
    "hh": "Home care",
}

GENDER_CODES = {"male": "M", "female": "F", "transgender": "O", "non_binary": "O", "other": "O"}


def care_context_display(encounter_class: str | None, when: datetime | None) -> str:
    """'OPD records for 10 Sep 2026'. The docs forbid clinical detail in the display name."""
    kind = ENCOUNTER_CLASS_DISPLAY.get(encounter_class or "", (encounter_class or "Visit").title())
    day = when.strftime("%d %b %Y") if when else "an unknown date"
    return f"{kind} records for {day}"


def gender_code(gender: str | None) -> str:
    """ABDM wants M, F or O (m2-generate-link-token). Care stores male/female/transgender/non_binary."""
    return GENDER_CODES.get((gender or "").lower(), "O")


def abha_number_digits(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")


def jwt_claims(token: str) -> dict:
    """The claim set of a JWT, read without verification (empty when the value is not a JWT).
    Observed link-token claims (2026-09-17): hipId, abhaNumber, transactionId, abhaAddress, sub, iat, exp."""
    parts = (token or "").split(".")
    if len(parts) != 3:
        return {}
    try:
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload))
    except (ValueError, TypeError, json.JSONDecodeError):
        return {}
    return claims if isinstance(claims, dict) else {}


def _jwt_time(token: str, claim: str) -> datetime | None:
    value = jwt_claims(token).get(claim)
    try:
        return datetime.fromtimestamp(int(value), tz=UTC) if value else None
    except (ValueError, TypeError, OverflowError):
        return None


def jwt_expiry(token: str) -> datetime | None:
    return _jwt_time(token, "exp")


def link_token_expiry(token: str, now: datetime) -> datetime:
    return jwt_expiry(token) or (now + LINK_TOKEN_VALIDITY)


def normalize_error_code(value) -> str:
    """`"ABDM-1027: "` -> `"ABDM-1027"`. The docs warn that codes arrive with trailing punctuation
    and whitespace; observed 2026-09-17 on an on-generate-token error callback. Compare codes only
    through this function."""
    return errors.normalize_code(value)


def mask_mobile(mobile: str | None) -> str:
    digits = re.sub(r"\D", "", mobile or "")
    return f"******{digits[-4:]}" if len(digits) >= 4 else "******"


def new_otp() -> str:
    return "".join(secrets.choice("0123456789") for _ in range(OTP_LENGTH))


def otp_hash(otp: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{otp}".encode()).hexdigest()


def otp_matches(otp: str, salt: str, stored_hash: str) -> bool:
    return hmac.compare_digest(otp_hash(str(otp), salt), stored_hash or "")


def within(
    from_dt: datetime | None, to_dt: datetime | None, outer_from: datetime | None, outer_to: datetime | None
) -> bool:
    """Is [from_dt, to_dt] inside [outer_from, outer_to]? Open bounds pass. The docs say a wider
    window is refused, not trimmed."""
    if outer_from and from_dt and from_dt < outer_from:
        return False
    if outer_to and to_dt and to_dt > outer_to:
        return False
    return True


def parse_iso(value) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def identifiers_of(patient: dict, kind: str) -> list[dict]:
    values = patient.get(kind) if isinstance(patient, dict) else None
    return [v for v in values if isinstance(v, dict)] if isinstance(values, list) else []


def abha_candidates(patient: dict) -> tuple[str, str]:
    """(abha_address, abha_number_digits) named by an inbound discovery request.

    `patient.id` is the identifier to search by (m2-on-discovery-request). The shape of
    `verifiedIdentifiers[]` is not published; a `{type, value}` pair is the only shape that
    fits an object list, so both `type` and `value` are read case-insensitively. Only
    verified identifiers count (ADR-008 decision 3: no demographic match)."""
    address = ""
    number = ""
    pid = str(patient.get("id") or "") if isinstance(patient, dict) else ""
    if "@" in pid:
        address = pid.lower()
    elif len(abha_number_digits(pid)) == 14:
        number = abha_number_digits(pid)
    for ident in identifiers_of(patient, "verifiedIdentifiers"):
        kind = str(ident.get("type") or "").upper()
        value = str(ident.get("value") or "")
        if "ADDRESS" in kind or ("@" in value and not address):
            address = address or value.lower()
        elif ("ABHA" in kind or "HEALTH" in kind or "NUMBER" in kind) and len(abha_number_digits(value)) == 14:
            number = number or abha_number_digits(value)
    return address, number


# --- request body builders (field names quoted from the endpoint pages) -------------------


def patient_block(reference_number: str, display: str, care_contexts: list[dict], hi_types: list[str]) -> dict:
    return {
        "referenceNumber": reference_number,
        "display": display,
        "careContexts": [{"referenceNumber": c["referenceNumber"], "display": c["display"]} for c in care_contexts],
        "hiType": list(hi_types),
        "count": len(care_contexts),
    }


def generate_token_body(abha_address: str, abha_number: str, name: str, gender: str, year_of_birth: int) -> dict:
    body = {"abhaAddress": abha_address, "name": name, "gender": gender_code(gender), "yearOfBirth": int(year_of_birth)}
    digits = abha_number_digits(abha_number)
    if digits:
        body["abhaNumber"] = int(digits)  # the page types abhaNumber as integer
    return body


def link_body(abha_address: str, abha_number: str, patient: dict) -> dict:
    body = {"abhaAddress": abha_address, "patient": [patient]}
    digits = abha_number_digits(abha_number)
    if digits:
        body["abhaNumber"] = digits  # this page types abhaNumber as string
    return body


def notify_body(
    abha_address: str, care_context_reference: str, hi_types: list[str], date: str, hip_id: str, hip_name: str
) -> dict:
    return {
        "notification": {
            "patient": {"id": abha_address},
            "careContext": {"patientReference": abha_address, "careContextReference": care_context_reference},
            "hiTypes": list(hi_types),
            "date": date,
            "hip": {"id": hip_id, "name": hip_name, "type": "HIP"},
        }
    }


def sms_body(request_id: str, timestamp: str, phone: str, hip_id: str, hip_name: str) -> dict:
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) == 10:
        digits = f"91{digits}"  # docs example: "917812345678", country code first
    return {
        "requestId": request_id,
        "timestamp": timestamp,
        "notification": {"phoneNo": digits, "hip": {"name": hip_name, "id": hip_id}},
    }


def on_discover_body(transaction_id: str, patients: list[dict], request_id: str) -> dict:
    return {"transactionId": transaction_id, "patient": patients, "response": {"requestId": request_id}}


def on_init_body(transaction_id: str, link_reference: str, hint: str, expiry: str, request_id: str) -> dict:
    return {
        "transactionId": transaction_id,
        "link": {
            "referenceNumber": link_reference,
            "authenticationType": "DIRECT",
            "meta": {"communicationMedium": "MOBILE", "communicationHint": hint, "communicationExpiry": expiry},
        },
        "response": {"requestId": request_id},
    }


def on_confirm_body(patients: list[dict], request_id: str, error: tuple[str, str] | None = None) -> dict:
    body: dict = {"patient": patients, "response": {"requestId": request_id}}
    if error:
        # The on-confirm page lists no error field. Every other callback answer carries
        # `error {code, message}`, so the same block is sent here (docs/findings.md).
        body["error"] = {"code": error[0], "message": error[1]}
    return body


def consent_ack_body(consent_id: str, request_id: str, ok: bool = True) -> dict:
    return {
        "acknowledgement": {"status": "OK" if ok else "ERROR", "consentId": consent_id},
        "response": {"requestId": request_id},
    }


def hi_request_ack_body(transaction_id: str, request_id: str, ok: bool = True) -> dict:
    return {
        "hiRequest": {"transactionId": transaction_id, "sessionStatus": "ACKNOWLEDGED" if ok else "ERRORED"},
        "response": {"requestId": request_id},
    }


def data_flow_notify_body(consent_id: str, transaction_id: str, done_at: str, hip_id: str, entries: list[dict]) -> dict:
    ok = bool(entries) and all(e.get("hiStatus") == "OK" for e in entries)
    return {
        "notification": {
            "consentId": consent_id,
            "transactionId": transaction_id,
            "doneAt": done_at,
            "notifier": {"type": "HIP", "id": hip_id},
            "statusNotification": {
                "sessionStatus": "TRANSFERRED" if ok else "FAILED",
                "hipId": hip_id,
                "statusResponses": [
                    {
                        "careContextReference": e["careContextReference"],
                        "hiStatus": e.get("hiStatus", "ERRORED"),
                        "description": e.get("description", ""),
                    }
                    for e in entries
                ],
            },
        }
    }


def parse_hi_request(parsed: dict) -> dict:
    """Read the inbound health-information request. The HIP page publishes no body, so the
    shape is taken from the HIU request page and the P2 on-share page: `hiRequest{consent{id},
    dateRange{from,to}, dataPushUrl, keyMaterial}` with `transactionId` at the top level or
    inside `hiRequest`."""
    hi = parsed.get("hiRequest") if isinstance(parsed.get("hiRequest"), dict) else {}
    consent = hi.get("consent") if isinstance(hi.get("consent"), dict) else {}
    date_range = hi.get("dateRange") if isinstance(hi.get("dateRange"), dict) else {}
    return {
        "transaction_id": str(parsed.get("transactionId") or hi.get("transactionId") or ""),
        "consent_id": str(consent.get("id") or hi.get("consentId") or parsed.get("consentId") or ""),
        "date_from": parse_iso(date_range.get("from")),
        "date_to": parse_iso(date_range.get("to")),
        "data_push_url": str(hi.get("dataPushUrl") or ""),
        "key_material": hi.get("keyMaterial") if isinstance(hi.get("keyMaterial"), dict) else {},
    }


def parse_consent_notification(parsed: dict) -> dict:
    """Read the consent notification (m3-on-consent-request-notify-hip body)."""
    detail = parsed.get("consentDetail") if isinstance(parsed.get("consentDetail"), dict) else {}
    notification = parsed.get("notification") if isinstance(parsed.get("notification"), dict) else {}
    if not detail and notification:
        # Tolerate a `notification{status, consentId, consentDetail}` wrapper, the shape M3 pages
        # use for HIU notifications, until the sandbox shows the HIP shape.
        parsed = notification
        detail = parsed.get("consentDetail") if isinstance(parsed.get("consentDetail"), dict) else {}
    permission = detail.get("permission") if isinstance(detail.get("permission"), dict) else {}
    date_range = permission.get("dateRange") if isinstance(permission.get("dateRange"), dict) else {}
    patient = detail.get("patient") if isinstance(detail.get("patient"), dict) else {}
    hip = detail.get("hip") if isinstance(detail.get("hip"), dict) else {}
    hiu = detail.get("hiu") if isinstance(detail.get("hiu"), dict) else {}
    purpose = detail.get("purpose") if isinstance(detail.get("purpose"), dict) else {}
    return {
        "status": str(parsed.get("status") or "").upper(),
        "consent_id": str(parsed.get("consentId") or detail.get("consentId") or ""),
        "abha_address": str(patient.get("id") or ""),
        "hip_id": str(hip.get("id") or ""),
        "hiu_id": str(hiu.get("id") or ""),
        "hiu_name": str(hiu.get("name") or ""),
        "purpose_code": str(purpose.get("code") or ""),
        "hi_types": [str(h) for h in detail.get("hiTypes") or [] if h],
        "care_context_references": [
            str(c.get("careContextReference") or "")
            for c in detail.get("careContexts") or []
            if isinstance(c, dict) and c.get("careContextReference")
        ],
        "date_from": parse_iso(date_range.get("from")),
        "date_to": parse_iso(date_range.get("to")),
        "data_erase_at": parse_iso(permission.get("dataEraseAt")),
        "signature": str(parsed.get("signature") or ""),
        "detail": detail,
    }
