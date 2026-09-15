"""
Pure rules for Scan and Share. No Django imports, so backend/tests can import this module.

Source: /docs/hiecm/v3/api/m1/endpoints/m1-on-share-acknowledgement and the PHR page
"Scan and share at a facility" (docs/abdm-docs-mirror/llms-full.txt).
"""

import re

# Counter rules: up to 20 alphanumeric characters, no special characters. A counter must not
# be the HFR facility ID, the HPID, the HIP ID, or the HIP name.
COUNTER_RE = re.compile(r"^[A-Za-z0-9]{1,20}$")

# The PHR page gives `profile.expiry` in seconds and says the token is valid for 30 minutes.
TOKEN_EXPIRY_SECONDS = "1800"


def validate_counters(counters: list[str], config: dict) -> list[str]:
    """Check the counter codes against the docs rules. Returns the cleaned list."""
    cleaned: list[str] = []
    forbidden = {
        str(config.get(key) or "").strip().lower() for key in ("facility_id", "hip_id", "hip_name") if config.get(key)
    }
    for raw in counters:
        code = str(raw or "").strip()
        if not code:
            continue
        if not COUNTER_RE.match(code):
            raise ValueError(f"Counter '{code}' must be 1 to 20 letters or digits with no spaces or symbols.")
        if code.lower() in forbidden:
            raise ValueError(f"Counter '{code}' must not be the facility ID, the HIP ID, or the HIP name.")
        if code.lower() in {c.lower() for c in cleaned}:
            raise ValueError(f"Counter '{code}' is listed more than once.")
        cleaned.append(code)
    return cleaned


def token_number(context: str, sequence: int) -> str:
    """Format `<context>-<nnn>`. The docs give only an example (`TKN-0042`); the format is ours."""
    return f"{context}-{sequence:03d}"


def prefill_profile(patient: dict, shared_at: str) -> dict:
    """Map the shared `profile.patient` block onto the account-profile keys the registration
    prefill reads (frontend/src/components/abdm/patient-registration-form.tsx::apply).
    kycPhoto is left out."""
    address = patient.get("address") or {}
    if not isinstance(address, dict):
        address = {}
    return {
        "ABHANumber": patient.get("abhaNumber") or "",
        "abhaAddress": patient.get("abhaAddress") or "",
        "name": patient.get("name") or "",
        "gender": patient.get("gender") or "",
        "dob": patient.get("dob") or "",
        "mobile": patient.get("mobile") or "",
        "address": address.get("line") or "",
        "districtName": address.get("district") or "",
        "stateName": address.get("state") or "",
        "pinCode": address.get("pinCode") or "",
        "sharedAt": shared_at,
    }


def ack_body(
    *,
    abha_address: str,
    context: str,
    token: str,
    request_id: str,
    error: tuple[str, str] | None = None,
) -> dict:
    """Body of m1-on-share-acknowledgement. `error` is (code, message) for FAILURE."""
    ack: dict = {"abhaAddress": abha_address}
    if error is None:
        ack["status"] = "SUCCESS"
        ack["profile"] = {"context": context, "tokenNumber": token, "expiry": TOKEN_EXPIRY_SECONDS}
    else:
        ack["status"] = "FAILURE"
        ack["error"] = {"code": error[0], "message": error[1]}
    body: dict = {"acknowledgement": ack}
    # The PHR page of the docs adds `response.requestId` (the REQUEST-ID of the share).
    # The M1 page does not. Send it when known.
    if request_id:
        body["response"] = {"requestId": request_id}
    return body
