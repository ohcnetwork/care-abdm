"""
Thin wrappers over every NHPR call the plug makes (M4, ADR-015). 1 function per operation; the body
comes from `nhpr/rules.py`; every call is recorded by `gateway.outbound.send()` and never raises.

Host: `ABDM_HSP_URL` + `/v4/int` (registries/nhpr §Base URLs; the HRP linkage call has used it since
2026-09-14). Bearer: the gateway session token, which `send()` adds. A person's HPR token goes in
`x-hprid-auth` where a page names it (HFR basic information and submit) and as the bearer of the
profile calls, which are "by JWT" (m4-profile/09).
"""

import logging
import re

from django.core.cache import cache

from abdm.gateway import outbound
from abdm.models import AbdmOutboundRequest
from abdm.nhpr import crypto, rules
from abdm.settings import plugin_settings

logger = logging.getLogger(__name__)

CERT_CACHE_KEY = "abdm:nhpr:public_key_pem"
CERT_CACHE_TTL = 6 * 60 * 60
MASTERS_CACHE_TTL = 24 * 60 * 60


class NhprError(Exception):
    def __init__(self, row: AbdmOutboundRequest | None, message: str = ""):
        self.row = row
        self.request_id = row.request_id if row else ""
        self.code = (row.error_code if row else "") or "NHPR_ERROR"
        super().__init__(message or (outbound.failure_detail(row) if row else "NHPR call failed"))


def base_url() -> str:
    return f"{plugin_settings.HSP_URL.rstrip('/')}/v4/int"


def call(
    operation_id: str,
    path: str,
    body: dict | None = None,
    *,
    method: str = "POST",
    hpr_token: str = "",
    hpr_bearer: bool = False,
    facility=None,
    patient=None,
) -> AbdmOutboundRequest:
    """Send 1 NHPR call. `hpr_token` fills `x-hprid-auth`; `hpr_bearer` makes it the bearer too."""
    headers: dict[str, str] = {}
    if hpr_token:
        headers["x-hprid-auth"] = hpr_token
        if hpr_bearer:
            headers["Authorization"] = f"Bearer {hpr_token}"
    # The NHPR is not the consent manager: it takes no X-CM-ID (the M4 pages list none).
    row = outbound.send(
        operation_id,
        f"{base_url()}{path}",
        body,
        method=method,
        facility=facility,
        patient=patient,
        extra_headers=headers or None,
        role="none",
    )
    return row


def ok(row: AbdmOutboundRequest) -> AbdmOutboundRequest:
    if row.status != AbdmOutboundRequest.Status.SUCCEEDED:
        raise NhprError(row)
    return row


# The registry's envelope code repeats the HTTP status (`HIS-422`, `HIS-400`, `HIS-500`); the cause is
# in `details[]` (`HIS-1070 Required OwnershipCode Field is empty.`). Observed 2026-09-21.
_ENVELOPE_CODE_RE = re.compile(r"^HIS-[45]\d\d\b")


def refusal_words(row: AbdmOutboundRequest | None) -> str:
    """The registry's own words for a refused row: the specific `details[]` lines when there are
    any, else the envelope message, else the HTTP status. Shown to the administrator as they came
    (abdm-m3 design.md: never replace the message ABDM sent with words of your own)."""
    if row is None:
        return ""
    lines = outbound.error_lines(row.response_json)
    specific = [line for line in lines if not _ENVELOPE_CODE_RE.match(line)]
    words = " ".join(dict.fromkeys(specific or lines)).strip()
    if words:
        return words
    return f"HTTP {row.http_status}" if row.http_status else ""


def json_of(row: AbdmOutboundRequest):
    return row.response_json


# --- certificate and encryption ------------------------------------------------------------------


def public_key():
    """The NHPR RSA key (`GET /api/v1/auth/cert`), cached 6 h. Raises NhprError or CertificateError."""
    pem = cache.get(CERT_CACHE_KEY)
    if pem is None:
        row = ok(call("m4-auth-cert", "/api/v1/auth/cert", None, method="GET"))
        payload = row.response_json
        text = payload.get("text") if isinstance(payload, dict) and "text" in payload else payload
        key = crypto.load_public_key(text)
        from cryptography.hazmat.primitives import serialization

        pem = key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()
        cache.set(CERT_CACHE_KEY, pem, timeout=CERT_CACHE_TTL)
        return key
    return crypto.load_public_key(pem)


def invalidate_public_key() -> None:
    cache.delete(CERT_CACHE_KEY)


def encrypt(value: str) -> str:
    return crypto.encrypt(value, public_key())


# --- tier A: search and linkage ------------------------------------------------------------------


def search_facilities(**kwargs) -> AbdmOutboundRequest:
    return call("m4-facility-search", "/FacilityManagement/v1.5/facility/search", rules.facility_search_body(**kwargs))


def hrp_linkage(body: dict, facility=None) -> AbdmOutboundRequest:
    return call("gateway-register-bridge-services", "/v1/bridges/MutipleHRPAddUpdateServices", body, facility=facility)


def facility_otp_send(facility_id: str, facility=None) -> AbdmOutboundRequest:
    return call(
        "m4-facility-otp-send",
        "/v1.5/facility/sendOtpToContact",
        rules.facility_otp_send_body(facility_id),
        facility=facility,
    )


def facility_otp_validate(body: dict, facility=None) -> AbdmOutboundRequest:
    return call("m4-facility-otp-validate", "/v1.5/facility/validateOtp", body, facility=facility)


# --- HPR login and profile -----------------------------------------------------------------------


def login_password(hpr_id: str, password: str) -> AbdmOutboundRequest:
    return call("m4-auth-password", "/api/v1/auth/authPassword", rules.login_password_body(hpr_id, password))


def login_init(hpr_id: str, auth_method: str) -> AbdmOutboundRequest:
    return call("m4-auth-init", "/api/v1/auth/init", rules.login_init_body(hpr_id, auth_method))


def login_confirm_aadhaar_otp(txn_id: str, otp: str) -> AbdmOutboundRequest:
    return call(
        "m4-auth-confirm-aadhaar-otp", "/api/v1/auth/confirmWithAadhaarOtp", rules.login_confirm_body(txn_id, otp)
    )


def search_hpr_id(hpr_id: str) -> AbdmOutboundRequest:
    return call("m4-search-by-hpr-id", f"/v1/search/searchByHprId/{hpr_id}", None, method="GET")


def exists_hpr_id(hpr_id: str) -> AbdmOutboundRequest:
    return call("m4-exists-by-hpr-id", f"/v1/search/existsByHprId/{hpr_id}", None, method="GET")


def account_information(hpr_token: str) -> AbdmOutboundRequest:
    return call(
        "m4-account-information",
        "/v1/account/information?masked=true",
        None,
        method="GET",
        hpr_token=hpr_token,
        hpr_bearer=True,
    )


def logout(hpr_token: str) -> AbdmOutboundRequest:
    return call("m4-auth-logout", "/v4/auth/logout", None, method="GET", hpr_token=hpr_token, hpr_bearer=True)


# --- journey 1: HPID creation --------------------------------------------------------------------


def aadhaar_generate_link() -> AbdmOutboundRequest:
    return call("m4-aadhaar-generate-link", "/aadhaar/generateLink", rules.aadhaar_link_body())


def aadhaar_is_authenticated(txn_id: str) -> AbdmOutboundRequest:
    return call("m4-aadhaar-is-authenticated", "/aadhaar/isAuthenticated", rules.txn_body(txn_id))


def aadhaar_verify_otp(txn_id: str) -> AbdmOutboundRequest:
    return call("m4-registration-verify-otp", "/v2/registration/aadhaar/verifyOTP", rules.txn_body(txn_id))


def check_account_exists(txn_id: str) -> AbdmOutboundRequest:
    return call(
        "m4-registration-account-exists",
        "/v1/registration/aadhaar/checkHpIdAccountExist",
        rules.account_exists_body(txn_id),
    )


def mobile_auth(txn_id: str, mobile: str) -> AbdmOutboundRequest:
    return call(
        "m4-registration-mobile-auth",
        "/v2/registration/aadhaar/demographicAuthViaMobile",
        rules.mobile_auth_body(txn_id, encrypt(mobile)),
    )


def mobile_otp_generate(txn_id: str, mobile: str) -> AbdmOutboundRequest:
    return call(
        "m4-registration-mobile-otp",
        "/v1/registration/aadhaar/generateMobileOTP",
        rules.mobile_otp_body(txn_id, mobile),
    )


def mobile_otp_verify(txn_id: str, otp: str) -> AbdmOutboundRequest:
    return call(
        "m4-registration-mobile-otp-verify",
        "/v1/registration/aadhaar/verifyMobileOTP",
        rules.mobile_otp_verify_body(txn_id, encrypt(otp)),
    )


def hpid_suggestions(txn_id: str) -> AbdmOutboundRequest:
    return call("m4-registration-hpid-suggestion", "/v1/registration/aadhaar/hpid/suggestion", rules.txn_body(txn_id))


def create_hpid(body: dict) -> AbdmOutboundRequest:
    return call("m4-registration-create-hpid", "/v2/registration/aadhaar/createHprIdWithPreVerified", body)


# --- journey 2: register the professional --------------------------------------------------------


def register_professional(body: dict) -> AbdmOutboundRequest:
    return call("m4-register-professional", "/apis/v1/doctors/register-professional-new", body)


def update_professional(body: dict) -> AbdmOutboundRequest:
    return call("m4-update-professional", "/apis/v1/doctors/update-professional-new", body)


def fetch_documents_list(hpr_id: str, hpr_token: str) -> AbdmOutboundRequest:
    return call(
        "m4-fetch-documents-list",
        "/apis/v1/doctors/fetch-documents-list",
        rules.documents_list_body(hpr_id),
        hpr_token=hpr_token,
    )


def upload_documents(body: dict) -> AbdmOutboundRequest:
    return call("m4-upload-documents", "/apis/v1/uploads/upload-document", body)


def fetch_professional_info(body: dict, hpr_token: str = "") -> AbdmOutboundRequest:
    return call("m4-fetch-professional-info", "/apis/v1/doctors/fetch-professional-info", body, hpr_token=hpr_token)


# --- journey 3: HFR onboarding -------------------------------------------------------------------


def dedup_search(body: dict, facility=None) -> AbdmOutboundRequest:
    return call("m4-hfr-dedup-search", "/search/address/filter/deduplicate", body, facility=facility)


def basic_information(body: dict, hpr_token: str, facility=None) -> AbdmOutboundRequest:
    return call(
        "m4-hfr-basic-information", "/v1.5/facility/basic-information", body, hpr_token=hpr_token, facility=facility
    )


def additional_information(body: dict, hpr_token: str, facility=None) -> AbdmOutboundRequest:
    return call(
        "m4-hfr-additional-information",
        "/v1.5/facility/additional-information",
        body,
        hpr_token=hpr_token,
        facility=facility,
    )


def detailed_information(body: dict, hpr_token: str, facility=None) -> AbdmOutboundRequest:
    return call(
        "m4-hfr-detailed-information",
        "/v1.5/facility/detailed-information",
        body,
        hpr_token=hpr_token,
        facility=facility,
    )


def submit_facility(body: dict, hpr_token: str, facility=None) -> AbdmOutboundRequest:
    return call(
        "m4-hfr-submit-facility", "/v1.5/facility/submit-facility", body, hpr_token=hpr_token, facility=facility
    )


# --- masters -------------------------------------------------------------------------------------

# kind -> (method, path, body builder or None, query builder or None). Every answer is normalised to
# [{code, name, children?}] by rules.parse_code_values and cached 24 h.
MASTERS: dict[str, tuple] = {
    # HFR (m4-utilities)
    "lgd-states": ("GET", "/v1.5/facility/lgd/states", None, None),
    "lgd-districts": ("GET", "/v1.5/facility/lgd/districts", None, lambda p: {"stateCode": p.get("state", "")}),
    "lgd-subdistricts": (
        "GET",
        "/v1.5/facility/lgd/subdistricts",
        None,
        lambda p: {"districtCode": p.get("district", "")},
    ),
    "facility-master-types": ("GET", "/v1.5/facility/get-master-types", None, None),
    "facility-master": ("GET", "/v1.5/facility/get-master-data", None, lambda p: {"type": p.get("type", "")}),
    "facility-types": (
        "POST",
        "/v1.5/facility/fetch-facility-type",
        lambda p: {"ownershipCode": p.get("ownership", ""), "systemOfMedicineCode": p.get("som", "")},
        None,
    ),
    "facility-subtypes": (
        "POST",
        "/v1.5/facility/fetch-facility-Sub-type",
        lambda p: {"facilityTypeCode": p.get("type", "")},
        None,
    ),
    "owner-subtypes": (
        "POST",
        "/v1.5/facility/get-owner-subtype",
        lambda p: {"ownershipCode": p.get("ownership", ""), "ownerSubtypeCode": p.get("subtype", "")},
        None,
    ),
    "specialities": (
        "POST",
        "/v1.5/facility/get-specialities",
        lambda p: {"systemOfMedicineCode": p.get("som", "")},
        None,
    ),
    "psu": ("GET", "/getPsuDetailsByMinistry", None, None),
    # HPR (m4-utility, m4-util). `hpid/get/categories` and `subCategories` take `role` (1 professional,
    # 2 facility manager, 3 both): without it the sandbox answers HIS-3028 "Role is not valid".
    "hpr-categories": ("GET", "/hpid/get/categories", None, lambda p: {"role": p.get("role", "1")}),
    "hpr-subcategories": (
        "GET",
        "/hpid/get/subCategories",
        None,
        lambda p: {"categoryCode": p.get("category", ""), "role": p.get("role", "1")},
    ),
    "hpr-states": ("GET", "/apis/v1/masters/states", None, None),
    "hpr-districts": ("GET", "/apis/v1/masters/district/{state}", None, None),
    "hpr-subdistricts": ("GET", "/apis/v1/masters/sub-districts/{district}", None, None),
    "countries": ("GET", "/apis/v1/masters/countries", None, None),
    "languages": ("GET", "/apis/v1/masters/languages", None, None),
    "system-of-medicines": ("GET", "/apis/v1/masters/system-of-medicines", None, None),
    "medical-councils": ("GET", "/apis/v1/masters/medical-councils", None, None),
    # m4-utility/14 names the query `medicineName`, the system of medicine as written ("Modern Medicine").
    "medical-councils-by-system": (
        "GET",
        "/apis/v1/masters/medical-councils/name",
        None,
        lambda p: {"medicineName": p.get("system", "")},
    ),
    "nurse-councils": ("GET", "/apis/v1/masters/nurse-councils", None, None),
    "courses": (
        "POST",
        "/apis/v1/masters/courses",
        lambda p: rules.courses_body(p.get("system", ""), p.get("hpr_type", "doctor"), p.get("count", 0)),
        None,
    ),
    "colleges": ("GET", "/apis/v1/masters/colleges/{state}/{medicine}", None, None),
    "colleges-by-state": ("GET", "/apis/v1/masters/colleges/{state}", None, None),
    "universities": ("GET", "/apis/v1/masters/universites/{college}", None, None),
    "all-universities": ("GET", "/apis/v1/masters/universites", None, None),
    "affiliated-boards": ("GET", "/apis/v1/masters/affiliated-board", None, None),
    "affiliated-boards-by-state": ("GET", "/apis/v1/masters/affiliated-board/states/{state}", None, None),
}


def masters(kind: str, params: dict | None = None) -> list[dict]:
    """1 master list, normalised to `[{code, name, children?}]`, cached 24 h per kind and params.
    `owner-subtype-codes` is answered locally: the registry publishes no master for the 3 codes it
    accepts (rules.OWNER_SUBTYPES)."""
    params = {k: str(v) for k, v in (params or {}).items() if v not in (None, "")}
    if kind == "owner-subtype-codes":
        return rules.owner_subtypes_for(params.get("ownership", ""))
    if kind not in MASTERS:
        raise ValueError(f"Unknown master: {kind}")
    method, path, body_of, query_of = MASTERS[kind]
    try:
        path = path.format(**params)
    except KeyError as exc:
        raise ValueError(f"Master {kind} needs the parameter {exc.args[0]}.") from exc
    if query_of:
        from urllib.parse import urlencode

        query = urlencode({k: v for k, v in query_of(params).items() if v})
        path = f"{path}?{query}" if query else path
    key = f"abdm:nhpr:master:{kind}:{path}:{sorted(params.items())}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    row = ok(call(f"m4-master-{kind}", path, body_of(params) if body_of else None, method=method))
    rows = rules.parse_code_values(row.response_json)
    cache.set(key, rows, timeout=MASTERS_CACHE_TTL)
    return rows
