"""
Pure rules for M4, the NHPR (HPR + HFR). No Django imports, so backend/tests can import this module.

Sources (docs mirror of 2026-09-19, catalogue 2026.09.16):
  /docs/hiecm/v3/milestones/m4                    the 4 journeys and their order
  /docs/hiecm/v3/registries/nhpr, nhpr/hpr, nhpr/hfr
                                                  hosts, tokens, formats, the role codes
  /docs/hiecm/v3/api/m4/endpoints/<flow>/<nn>-*   every body quoted in the builders and parsers below
Every NHPR call takes the integration bearer token. The HFR create and submit calls also take a
person's HPR token in `x-hprid-auth` (registries/nhpr/hfr §The link to the HPR token).
"""

import re
from datetime import UTC, datetime

# --- formats (registries/nhpr/hpr, nhpr/hfr) --------------------------------------------------

HPR_ID_NUMBER_RE = re.compile(r"^\d{2}-\d{4}-\d{4}-\d{4}$|^\d{14}$")
HPR_ID_ADDRESS_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{2,}@hpr\.abdm$")
HPR_DOMAIN = "@hpr.abdm"
HPR_ID_TYPE = "hpr_id"
FACILITY_ID_RE = re.compile(r"^IN[A-Za-z0-9]{10}$")
# HFR §Bridge linkage: 15 characters or fewer, no special characters, unique per bridge in a facility.
HIP_NAME_RE = re.compile(r"^[A-Za-z0-9 ]{1,15}$")
# `hpid/suggestion` gives usernames; createHprIdWithPreVerified takes `hprId` (the alias) and `domainName`.
USERNAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{2,63}$")

# registries/nhpr/hpr §Who can enrol: the role code of createHprIdWithPreVerified.
ROLES = {1: "Healthcare Professional", 2: "Facility Manager", 3: "Healthcare Professional and Facility Manager"}
# m4-authentication/04: `authMethod` values named by searchByHprId `authMethods`.
AUTH_METHODS = ("PASSWORD", "AADHAAR_OTP", "MOBILE_OTP")
# The 2 login routes with a published verify step. MOBILE_OTP has a send call and no verify call
# (docs/findings.md N5).
LOGIN_METHODS = ("password", "aadhaar_otp")
# aadhaar/generateLink body, quoted from m4-registration-api-s-collection-via-aadhaar/01.
AADHAAR_LINK_SCOPES = ["nhpr-register"]
AADHAAR_LINK_SOURCE = "NHPR"
# The Aadhaar link URL is valid 5 minutes (milestones/m4 journey 1).
AADHAAR_LINK_VALIDITY_SECONDS = 5 * 60
# `MutipleHRPAddUpdateServices` HRP.type values (m4-multiple-hrp-api/01; milestones/m4 journey 4).
LINK_TYPES = ("HIP", "HIU")
# HFR onboarding steps, in the fixed order of registries/nhpr/hfr §The onboarding journey.
ONBOARDING_STEPS = ("dedup", "basic", "additional", "detailed", "submit")
# The facility statuses the pages show (`facilityStatus`, onboarding `status`).
FACILITY_STATUSES = ("Draft", "Submitted", "Verified", "Created", "Saved", "success")

# `facility/search` limits: HIS-4047 "Please enter valid resultsPerPage, Min value is 10, Max value
# is 15" (observed 2026-09-21, findings N29). The page documents no limit.
RESULTS_PER_PAGE_MIN = 10
RESULTS_PER_PAGE_MAX = 15

# The registry facts observed on the sandbox on 2026-09-21 (docs/findings.md N16-N19). A name search
# needs `stateLGDCode` and `ownershipCode` (HIS-1070 "Required OwnershipCode Field is empty").
# `get-master-types` names 17 master types; the wizard's pickers use these.
MASTER_TYPES = (
    "MEDICINE",
    "OWNER",
    "CENTRAL-GOVERNMENT",
    "PROFIT-TYPE",
    "NON-PROFIT-TYPE",
    "TYPE-SERVICE",
    "SALUTATION",
    "FACILITY-REGION",
    "SPECIALITY-TYPE",
    "ADDRESS-PROOF",
    "FAC-STATUS",
    "IT-EQUIPMENT",
    "GENERAL-INFO-OPTIONS",
    "IMAGING",
    "DIAGNOSTIC",
    "DAYS-OF-OPERATION",
    "SOURCE",
)
# `get-owner-subtype` refuses every `ownerSubtypeCode` but these 3 ("It should be one of C, P, or
# NP"; "Only 'P' or 'NP' are accepted for Ownership Code 'P' or 'PP'"). No master lists them; the
# basic-information example sends `G` / `C` / `MOHF`.
OWNER_SUBTYPES = {"G": ("C",), "P": ("P", "NP"), "PP": ("P", "NP")}


def owner_subtypes_for(ownership_code: str) -> list[dict]:
    names = {"C": "Central Government", "P": "For profit", "NP": "Not for profit"}
    return [{"code": code, "name": names[code]} for code in OWNER_SUBTYPES.get((ownership_code or "").strip(), ())]


def hpr_id_number_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def format_hpr_id_number(value: str) -> str:
    """`71266557771234` -> `71-2665-5777-1234`, the form the registry prints."""
    digits = hpr_id_number_digits(value)
    if len(digits) != 14:
        return value or ""
    return f"{digits[:2]}-{digits[2:6]}-{digits[6:10]}-{digits[10:]}"


def hpr_id_kind(value: str) -> str:
    """`number` for the 14 digits, `address` for `name@hpr.abdm`, `username` for a bare alias, else ``."""
    text = (value or "").strip()
    if HPR_ID_NUMBER_RE.match(text):
        return "number"
    if HPR_ID_ADDRESS_RE.match(text):
        return "address"
    if USERNAME_RE.match(text):
        return "username"
    return ""


def normalise_hpr_address(value: str) -> str:
    """A bare username becomes `username@hpr.abdm`; an address is kept; a number is kept."""
    text = (value or "").strip()
    kind = hpr_id_kind(text)
    if kind == "username":
        return f"{text}{HPR_DOMAIN}"
    return text


def facility_id_ok(value: str) -> bool:
    return bool(FACILITY_ID_RE.match((value or "").strip()))


def hip_name_ok(value: str) -> bool:
    return bool(HIP_NAME_RE.match(value or ""))


def default_hip_name(facility_name: str) -> str:
    """The first 15 letters, digits and spaces of the name (HFR §Bridge linkage rules)."""
    cleaned = re.sub(r"[^A-Za-z0-9 ]", "", facility_name or "")
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()[:15].strip()
    return cleaned


# --- Care facility prefill from a registry record (ADR-016) ------------------------------------

# Care facility type names (care/facility/models/facility.py FACILITY_TYPES) by registry hints.
# The registry publishes no type-to-type table (findings N13); the person confirms the pick.
_GOVERNMENT_TYPE_HINTS = (
    ("medical college", "Govt Medical College Hospitals"),
    ("district hospital", "District Hospitals"),
    ("taluk", "Taluk Hospitals"),
    ("community health", "Community Health Centres"),
    ("family health", "Family Health Centres"),
    ("primary health", "Primary Health Centres"),
    ("women", "Women and Child Health Centres"),
    ("child", "Women and Child Health Centres"),
)


def is_government(record: dict) -> bool:
    text = f"{record.get('ownershipCode') or ''} {record.get('ownership') or ''}".lower()
    return text.strip().startswith("g") or "government" in text or "public" in text


def suggest_care_facility_type(record: dict) -> str:
    """A Care facility type name for a registry record: labs and telemedicine by the type text,
    government sub-types by the name, hospitals by ownership, else "Other"."""
    kind = str(record.get("facilityType") or "").lower()
    name = str(record.get("facilityName") or "").lower()
    government = is_government(record)
    if "lab" in kind or "diagnos" in kind:
        return "Govt Labs" if government else "Private Labs"
    if "tele" in kind:
        return "TeleMedicine"
    if government:
        for hint, care_type in _GOVERNMENT_TYPE_HINTS:
            if hint in kind or hint in name:
                return care_type
        return "Other"
    if any(word in kind for word in ("hospital", "nursing", "clinic", "dispensary", "centre", "center")):
        return "Private Hospital"
    return "Other"


_COORDINATE_LIMIT = {"latitude": 90.0, "longitude": 180.0}


def coordinate(value, kind: str, *, strict: bool = False) -> str:
    """A coordinate the HFR accepts: 1 to 6 decimal places, inside the range of its kind
    (`HIS-4019` latitude, `HIS-4020` longitude).

    Care holds a coordinate with 16 decimal places (`Facility.latitude`), and the registry search
    answers with 15, so every value that crosses into an HFR body must be shortened first.
    An empty value gives an empty string. With `strict`, a value the registry would refuse raises
    a `ValueError` that names the field, so the plug refuses before the call (ADR-012).
    """
    limit = _COORDINATE_LIMIT[kind]
    raw = str(value if value is not None else "").strip()
    if not raw:
        return ""
    try:
        number = float(raw)
    except ValueError:
        if strict:
            raise ValueError(f"{kind} must be a number.") from None
        return ""
    if not -limit <= number <= limit:
        if strict:
            raise ValueError(f"{kind} must be between -{limit:.6f} and +{limit:.6f}.")
        return ""
    text = f"{number:.6f}".rstrip("0")
    return f"{text}0" if text.endswith(".") else text


def care_prefill(record: dict) -> dict:
    """The Care facility form fields a registry record can fill. Everything else stays typed."""

    def _float(value, kind: str):
        text = coordinate(value, kind)
        return float(text) if text else None

    pincode = str(record.get("pincode") or "").strip()
    return {
        "name": str(record.get("facilityName") or "").strip(),
        "address": str(record.get("address") or "").strip(),
        "pincode": int(pincode) if re.fullmatch(r"[1-9][0-9]{5}", pincode) else None,
        # 6 decimal places, so the value Care stores can go back to the registry unchanged.
        "latitude": _float(record.get("latitude"), "latitude"),
        "longitude": _float(record.get("longitude"), "longitude"),
        "facility_type": suggest_care_facility_type(record),
        "state_name": str(record.get("stateName") or "").strip(),
        "district_name": str(record.get("districtName") or "").strip(),
    }


def now_iso(now: datetime | None = None) -> str:
    return (now or datetime.now(UTC)).strftime(
        "%Y-%m-%dT%H:%M:%S."
    ) + f"{(now or datetime.now(UTC)).microsecond // 1000:03d}Z"


# --- journey 4 and tier A: linkage, lookup, search ---------------------------------------------


def hrp_linkage_body(facility_id: str, facility_name: str, bridge_id: str, hip_name: str, types=LINK_TYPES) -> dict:
    """`m4-multiple-hrp-api/01`: 1 HRP entry per link type. The sandbox returned both `HIP` and
    `HIU` for a `HIP` registration (findings B18); sending both names the M3 role explicitly."""
    if not facility_id_ok(facility_id):
        raise ValueError("HFR facility ID must start with IN and have 12 characters.")
    if not hip_name_ok(hip_name):
        raise ValueError("HIP name must be 15 characters or fewer with no special characters.")
    unknown = [t for t in types if t not in LINK_TYPES]
    if unknown or not types:
        raise ValueError("Link types must be HIP, HIU or both.")
    return {
        "facilityId": facility_id,
        "facilityName": facility_name,
        "HRP": [{"bridgeId": bridge_id, "hipName": hip_name, "type": kind, "active": True} for kind in types],
    }


def facility_search_body(
    *,
    facility_id: str = "",
    name: str = "",
    state_lgd: str = "",
    district_lgd: str = "",
    sub_district_lgd: str = "",
    pincode: str = "",
    ownership: str = "",
    page: int = 1,
    per_page: int = 10,
) -> dict:
    """`m4-search/02`: by facility ID, or by name with the filters. Every key is sent, empty when
    unused, as the page example does. Observed 2026-09-21: a name search is refused (HTTP 422,
    HIS-1070) unless `stateLGDCode` and `ownershipCode` are both set; `facility/search()` refuses
    such a search locally before any call. `resultsPerPage` must be 10 to 15 (HIS-4047 "Please enter
    valid resultsPerPage, Min value is 10, Max value is 15", observed 2026-09-21, findings N29); the
    page states no limit. The builder clamps the value, so no caller can send a refused one."""
    return {
        "ownershipCode": ownership or "",
        "subDistrictLGDCode": sub_district_lgd or "",
        "pincode": pincode or "",
        "facilityName": name or "",
        "facilityId": facility_id or "",
        "page": max(1, int(page or 1)),
        "resultsPerPage": min(max(RESULTS_PER_PAGE_MIN, int(per_page or RESULTS_PER_PAGE_MIN)), RESULTS_PER_PAGE_MAX),
        "stateLGDCode": state_lgd or "",
        "districtLGDCode": district_lgd or "",
    }


def parse_facility_search(payload) -> dict:
    """`{facilities[], message, totalFacilities, numberOfPages}` (m4-search/02 200 shape). The
    sandbox row (2026-09-21) also carries `systemOfMedicineCode`, `subDistrictLGDCode`,
    `villageCityTownName`, `villageCityTownLGDCode`, `workingInPsu`, `facPsuName`, `govtCategory`
    and `govtMinistries`; the codes are kept for the HFR wizard prefill."""
    data = payload if isinstance(payload, dict) else {}
    out = []
    for item in data.get("facilities") or []:
        if not isinstance(item, dict):
            continue
        out.append(
            {
                "facilityId": str(item.get("facilityId") or ""),
                "facilityName": str(item.get("facilityName") or ""),
                "facilityStatus": str(item.get("facilityStatus") or ""),
                "facilityType": str(item.get("facilityType") or ""),
                "facilityTypeCode": str(item.get("facilityTypeCode") or ""),
                "ownership": str(item.get("ownership") or ""),
                "ownershipCode": str(item.get("ownershipCode") or ""),
                "systemOfMedicine": str(item.get("systemOfMedicine") or ""),
                "systemOfMedicineCode": str(item.get("systemOfMedicineCode") or ""),
                "address": str(item.get("address") or ""),
                "pincode": str(item.get("pincode") or ""),
                "stateName": str(item.get("stateName") or ""),
                "stateLGDCode": str(item.get("stateLGDCode") or ""),
                "districtName": str(item.get("districtName") or ""),
                "districtLGDCode": str(item.get("districtLGDCode") or ""),
                "subDistrictName": str(item.get("subDistrictName") or ""),
                "subDistrictLGDCode": str(item.get("subDistrictLGDCode") or ""),
                "villageCityTownName": str(item.get("villageCityTownName") or ""),
                "villageCityTownLGDCode": str(item.get("villageCityTownLGDCode") or ""),
                "latitude": str(item.get("latitude") or ""),
                "longitude": str(item.get("longitude") or ""),
            }
        )

    def _int(v):
        try:
            return int(v)
        except (TypeError, ValueError):
            return 0

    return {
        "facilities": out,
        "message": str(data.get("message") or ""),
        "total": _int(data.get("totalFacilities")),
        "pages": _int(data.get("numberOfPages")),
    }


def facility_otp_send_body(facility_id: str) -> dict:
    """`m4-hfr-hrp-linkage-apis/01`."""
    return {"facilityId": facility_id}


def facility_otp_validate_body(facility_id: str, transaction_id: str, otp: str, source: str, source_id: str) -> dict:
    """`m4-hfr-hrp-linkage-apis/02`. `source` and `sourceId` name a programme (the example: AB-PMJAY)."""
    return {
        "facilityId": facility_id,
        "sourceId": source_id,
        "otp": otp,
        "source": source,
        "transactionId": transaction_id,
    }


# --- HPR login (registries/nhpr/hpr §Getting an HPR token later) ---------------------------------


def login_password_body(hpr_id: str, password: str) -> dict:
    """`m4-authentication/01`: `{idType, domainName, hprId, password}`. The example sends `idType`
    and `domainName` empty; the create call names them `hpr_id` and `@hpr.abdm`, so the plug sends
    those for an address and leaves them empty for the 14-digit number."""
    kind = hpr_id_kind(hpr_id)
    address = normalise_hpr_address(hpr_id)
    return {
        "idType": HPR_ID_TYPE if kind in ("address", "username") else "",
        "domainName": HPR_DOMAIN if kind in ("address", "username") else "",
        "hprId": address,
        "password": password,
    }


def login_init_body(hpr_id: str, auth_method: str) -> dict:
    """`m4-authentication/04`: `{idType, domainName, authMethod, hprId}`."""
    if auth_method not in AUTH_METHODS:
        raise ValueError("authMethod must be PASSWORD, AADHAAR_OTP or MOBILE_OTP.")
    body = login_password_body(hpr_id, "")
    body.pop("password")
    body["authMethod"] = auth_method
    return body


def login_confirm_body(txn_id: str, otp: str) -> dict:
    """`m4-authentication/03`: `{otp, txnId}`. The OTP travels as the page shows it, plain."""
    return {"otp": str(otp), "txnId": txn_id}


def parse_token_response(payload) -> dict:
    """`{token, expiresIn, refreshToken, refreshExpiresIn}` (m4-authentication/01 200 shape).
    `expiresIn` in the example is an epoch second (1733639805), not a duration; both are read."""
    data = payload if isinstance(payload, dict) else {}
    token = str(data.get("token") or data.get("accessToken") or "")
    return {
        "token": token,
        "expires_at": _expiry(data.get("expiresIn")),
        "refresh_token": str(data.get("refreshToken") or ""),
        "refresh_expires_at": _expiry(data.get("refreshExpiresIn")),
    }


def _expiry(value) -> datetime | None:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    if number <= 0:
        return None
    now = datetime.now(UTC)
    # An epoch second is far larger than any duration the registry would send.
    if number > 10_000_000:
        return datetime.fromtimestamp(number, tz=UTC)
    return datetime.fromtimestamp(now.timestamp() + number, tz=UTC)


def jwt_claims(token: str) -> dict:
    import base64
    import json

    parts = (token or "").split(".")
    if len(parts) != 3:
        return {}
    try:
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload))
    except (ValueError, TypeError):
        return {}
    return claims if isinstance(claims, dict) else {}


def parse_login_init(payload) -> dict:
    """`{transactionId, mobileNumber}` (m4-authentication/04) or `{txnId, mobileNumber}`."""
    data = payload if isinstance(payload, dict) else {}
    return {
        "txn_id": str(data.get("transactionId") or data.get("txnId") or ""),
        "mobile_masked": str(data.get("mobileNumber") or ""),
    }


def parse_hpr_search(payload) -> dict:
    """`m4-searched/02`: `{hprIdNumber, name, authMethods[], hprId, categoryId, subCategoryId}`."""
    data = payload if isinstance(payload, dict) else {}
    methods = data.get("authMethods")
    return {
        "hpr_id_number": str(data.get("hprIdNumber") or ""),
        "hpr_id": str(data.get("hprId") or ""),
        "name": str(data.get("name") or ""),
        "auth_methods": [str(m) for m in methods if m] if isinstance(methods, list) else [],
        "category_id": str(data.get("categoryId") or ""),
        "sub_category_id": str(data.get("subCategoryId") or ""),
    }


def parse_account_information(payload) -> dict:
    """`m4-profile/09`: the profile behind an HPR token. Photos are dropped (kycPhoto, profilePhoto)."""
    data = payload if isinstance(payload, dict) else {}
    keep = (
        "hprIdNumber",
        "hprId",
        "mobile",
        "firstName",
        "middleName",
        "lastName",
        "name",
        "yearOfBirth",
        "monthOfBirth",
        "dayOfBirth",
        "gender",
        "email",
        "stateCode",
        "districtCode",
        "subDistrictCode",
        "pincode",
        "address",
        "stateName",
        "districtName",
        "hpCategoryCode",
        "hpSubCategoryCode",
        "categoryName",
        "subCategoryName",
        "role",
        "kycVerified",
        "hprRegistrationStatus",
    )
    return {k: data[k] for k in keep if k in data and data[k] not in (None, "")}


# --- journey 1: HPID creation (m4-registration-api-s-collection-via-aadhaar/01..09) --------------


def aadhaar_link_body() -> dict:
    return {"scopes": list(AADHAAR_LINK_SCOPES), "source": AADHAAR_LINK_SOURCE}


def parse_aadhaar_link(payload) -> dict:
    """The page shows `{txnId, mobileNumber}`; the milestone says the call returns "txnId and a
    temporary URL, valid 5 minutes". Every URL-shaped key is read (docs/findings.md N2)."""
    data = payload if isinstance(payload, dict) else {}
    url = ""
    for key in ("url", "link", "aadhaarLink", "redirectUrl", "authUrl"):
        if isinstance(data.get(key), str) and data[key].startswith("http"):
            url = data[key]
            break
    return {
        "txn_id": str(data.get("txnId") or data.get("transactionId") or ""),
        "url": url,
        "mobile_masked": str(data.get("mobileNumber") or ""),
    }


def txn_body(txn_id: str) -> dict:
    return {"txnId": txn_id}


def parse_boolean(payload) -> bool:
    """`isAuthenticated` answers a bare boolean; a `{verified}` or `{status}` object is tolerated."""
    if isinstance(payload, bool):
        return payload
    if isinstance(payload, str):
        return payload.strip().lower() == "true"
    if isinstance(payload, dict):
        for key in ("verified", "authenticated", "isAuthenticated", "status"):
            if isinstance(payload.get(key), bool):
                return payload[key]
            if isinstance(payload.get(key), str) and payload[key].lower() in ("true", "false"):
                return payload[key].lower() == "true"
    return False


def parse_aadhaar_details(payload) -> dict:
    """`verifyOTP` (03): the Aadhaar demographics. The photo is kept only until the HPID is created
    (it is the `profilePhoto` of the create call); everything else is display."""
    data = payload if isinstance(payload, dict) else {}
    keep = (
        "txnId",
        "mobileNumber",
        "gender",
        "name",
        "email",
        "pincode",
        "birthdate",
        "careOf",
        "house",
        "street",
        "landmark",
        "locality",
        "villageTownCity",
        "subDist",
        "district",
        "state",
        "postOffice",
        "address",
    )
    return {
        "details": {k: data[k] for k in keep if data.get(k) not in (None, "")},
        "photo": str(data.get("photo") or ""),
    }


def split_name(full_name: str) -> tuple[str, str, str]:
    parts = [p for p in (full_name or "").split() if p]
    if not parts:
        return "", "", ""
    if len(parts) == 1:
        return parts[0], "", ""
    if len(parts) == 2:
        return parts[0], "", parts[1]
    return parts[0], " ".join(parts[1:-1]), parts[-1]


def account_exists_body(txn_id: str) -> dict:
    """(05): `{txnId, preverifiedCheck}`."""
    return {"txnId": txn_id, "preverifiedCheck": True}


def parse_account_exists(payload) -> dict:
    """(05) 200 shape: an existing account with `token`, `hprIdNumber`, `hprId`, `new: false`."""
    data = payload if isinstance(payload, dict) else {}
    hpr_id_number = str(data.get("hprIdNumber") or "")
    return {
        "exists": bool(hpr_id_number) and data.get("new") is not True,
        "hpr_id_number": hpr_id_number,
        "hpr_id": str(data.get("hprId") or ""),
        "token": str(data.get("token") or ""),
        "name": str(data.get("name") or ""),
        "category_id": str(data.get("categoryId") or ""),
        "sub_category_id": str(data.get("subCategoryId") or ""),
        "state_code": str(data.get("stateCode") or ""),
        "district_code": str(data.get("districtCode") or ""),
    }


def mobile_auth_body(txn_id: str, encrypted_mobile: str) -> dict:
    """(04): the mobile number RSA/ECB/PKCS1 encrypted with the NHPR certificate."""
    return {"txnId": txn_id, "mobileNumber": encrypted_mobile}


def parse_mobile_auth(payload) -> dict:
    data = payload if isinstance(payload, dict) else {}
    return {"verified": parse_boolean(data), "reason": str(data.get("reason") or data.get("errorCode") or "")}


def mobile_otp_body(txn_id: str, mobile: str) -> dict:
    """(07): `{mobile, txnId}`, the mobile plain as the page shows it."""
    return {"mobile": mobile, "txnId": txn_id}


def mobile_otp_verify_body(txn_id: str, otp_value: str) -> dict:
    """(08): `{otp, txnId}`. The page types `otp` as `<BASE64 ENCODED STRING>`; registries/nhpr/hpr
    names the OTP among the RSA/ECB/PKCS1 encrypted fields, so the caller passes the encrypted
    (base64) value."""
    return {"otp": otp_value, "txnId": txn_id}


def parse_suggestions(payload) -> list[str]:
    if isinstance(payload, list):
        return [str(s) for s in payload if s]
    if isinstance(payload, dict):
        for key in ("suggestions", "hprIdSuggestions", "data"):
            if isinstance(payload.get(key), list):
                return [str(s) for s in payload[key] if s]
    return []


def create_hpid_body(
    *,
    txn_id: str,
    username: str,
    email: str,
    encrypted_password: str,
    first_name: str,
    middle_name: str,
    last_name: str,
    profile_photo_b64: str,
    category_code: int,
    sub_category_code: int,
    state_code: str,
    district_code: str,
    role: int,
) -> dict:
    """(09) `createHprIdWithPreVerified`. `password` and `email` are among the RSA-encrypted fields
    (registries/nhpr/hpr); the caller passes the password encrypted and the email is sent plain
    because the example shows a readable address (docs/findings.md N3). `clientId: V4` and
    `sourceType: AADHAAR` follow the example; `council: false`."""
    if not USERNAME_RE.match(username or ""):
        raise ValueError("Choose a username of 3 to 64 letters, digits, dots, underscores or dashes.")
    if role not in ROLES:
        raise ValueError("Role must be 1, 2 or 3.")
    return {
        "idType": HPR_ID_TYPE,
        "domainName": HPR_DOMAIN,
        "email": email,
        "firstName": first_name,
        "middleName": middle_name,
        "lastName": last_name,
        "password": encrypted_password,
        "profilePhoto": profile_photo_b64,
        "txnId": txn_id,
        "hprId": username,
        "sourceType": "AADHAAR",
        "hpCategoryCode": int(category_code),
        "hpSubCategoryCode": int(sub_category_code),
        "clientId": "V4",
        "stateCode": str(state_code),
        "districtCode": str(district_code),
        "council": False,
        "role": int(role),
    }


def parse_created_hpid(payload) -> dict:
    """(09) publishes no 200 body ("read what comes back"). The keys the sibling pages use are read."""
    data = payload if isinstance(payload, dict) else {}
    return {
        "hpr_id_number": str(data.get("hprIdNumber") or data.get("hprId_number") or ""),
        "hpr_id": str(data.get("hprId") or ""),
        "token": str(data.get("token") or data.get("hprToken") or ""),
        "name": str(data.get("name") or ""),
    }


# --- journey 2: register the professional (m4-enrollment) --------------------------------------

PRACTITIONER_BLOCKS = (
    "healthProfessionalType",
    "profilePhoto",
    "officialMobileCode",
    "officialMobile",
    "officialMobileStatus",
    "officialEmail",
    "officialEmailStatus",
    "visibleProfilePicture",
    "profileVisibleToPublic",
    "personalInformation",
    "addressAsPerKYC",
    "communicationAddress",
    "contactInformation",
    "registrationAcademic",
    "currentWorkDetails",
)


def register_professional_body(hpr_token: str, practitioner: dict) -> dict:
    """`m4-enrollment/01`: `{hprToken, practitioner{...}}`. The practitioner block is the form as the
    desk filled it; only the documented top-level keys pass, so a stray key never reaches the
    registry. The registry rejects display values: every code must come from a master call."""
    if not isinstance(practitioner, dict) or not practitioner:
        raise ValueError("The professional profile is empty.")
    body = {k: practitioner[k] for k in PRACTITIONER_BLOCKS if k in practitioner}
    unknown = sorted(set(practitioner) - set(PRACTITIONER_BLOCKS))
    if unknown:
        raise ValueError(f"Unknown profile block: {', '.join(unknown)}.")
    personal = body.get("personalInformation")
    if not isinstance(personal, dict) or not str(personal.get("firstName") or "").strip():
        raise ValueError("personalInformation.firstName is required.")
    academic = body.get("registrationAcademic")
    if not isinstance(academic, dict) or not academic.get("registrationData"):
        raise ValueError("registrationAcademic.registrationData needs at least 1 registration.")
    return {"hprToken": hpr_token, "practitioner": body}


def documents_list_body(hpr_id: str) -> dict:
    """`m4-enrollment/03`: `{hprid}`."""
    return {"hprid": hpr_id}


DOCUMENT_TYPES = ("profilePhoto", "degreeCertificate", "registrationCertificate", "proofOfWorkCertificate")
FILE_TYPES = ("pdf", "png", "jpeg", "jpg")
# registries/nhpr/hpr §What your system has to hold: 1 MB photo, 5 MB anything else.
MAX_PHOTO_BYTES = 1 * 1024 * 1024
MAX_DOCUMENT_BYTES = 5 * 1024 * 1024


def base64_size(data_b64: str) -> int:
    text = (data_b64 or "").strip()
    padding = text.count("=", max(0, len(text) - 2))
    return max(0, (len(text) * 3) // 4 - padding)


def upload_documents_body(hpr_token: str, documents: list[dict]) -> dict:
    """`m4-enrollment/04`: `{hpr_token, document[{document_id, document_type, fileType, data}]}`."""
    out = []
    for doc in documents or []:
        if not isinstance(doc, dict):
            continue
        kind = str(doc.get("document_type") or "")
        file_type = str(doc.get("fileType") or "").lower()
        data = str(doc.get("data") or "")
        if kind not in DOCUMENT_TYPES:
            raise ValueError(f"document_type must be 1 of {', '.join(DOCUMENT_TYPES)}.")
        if file_type not in FILE_TYPES:
            raise ValueError("fileType must be pdf, png, jpeg or jpg.")
        limit = MAX_PHOTO_BYTES if kind == "profilePhoto" else MAX_DOCUMENT_BYTES
        if base64_size(data) > limit:
            raise ValueError(f"{kind} is larger than {limit // (1024 * 1024)} MB.")
        try:
            document_id = int(doc.get("document_id"))
        except (TypeError, ValueError) as exc:
            raise ValueError("document_id must be an integer from the documents list.") from exc
        out.append({"document_id": document_id, "document_type": kind, "fileType": file_type, "data": data})
    if not out:
        raise ValueError("Attach at least 1 document.")
    return {"hpr_token": hpr_token, "document": out}


def professional_info_body(hpr_id: str = "", name: str = "", registration_number: str = "", council: str = "") -> dict:
    """`m4-enrollment/05`: `{practitioner{id, name, contactNumber, state, registrationNumber, stateCouncilName}}`."""
    return {
        "practitioner": {
            "id": hpr_id,
            "name": name,
            "contactNumber": "",
            "state": "",
            "registrationNumber": registration_number,
            "stateCouncilName": council,
        }
    }


# --- journey 3: HFR onboarding (m4-onboarding-apis/01..05) ---------------------------------------

BASIC_KEYS = (
    "facilityName",
    "facilityAddressDetails",
    "facilityContactInformation",
    "ownershipCode",
    "ownershipSubTypeCode",
    "ownershipSubTypeCode2",
    "typeOfServiceCode",
    "systemOfMedicineCode",
    "facilityTypeCode",
    "specialityTypeCode",
    "facilityUploads",
    "facilityAddressProof",
    "facilitySubType",
    "workingInPsu",
    "facPsuName",
    "facilityOperationalStatus",
    "timingsOfFacility",
    "abdmCompliantSoftware",
)
ADDITIONAL_KEYS = ("linkedProgramIds", "generalInformation")
DETAILED_KEYS = (
    "specialities",
    "medicalInfrastructure",
    "pharmacyDetails",
    "bloodBankDetails",
    "imagingServices",
    "diagnosticServices",
)
SUBMIT_KEYS = ("sourceOfInformation", "sourceUniqueID", "facilitySuperUser")


def _only(payload: dict, keys: tuple[str, ...], label: str) -> dict:
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be an object.")
    unknown = sorted(set(payload) - set(keys))
    if unknown:
        raise ValueError(f"Unknown {label} field: {', '.join(unknown)}.")
    return {k: payload[k] for k in keys if k in payload}


def dedup_body(
    *, name: str, address: str, district_lgd: str, sub_district_lgd: str, village_lgd: str = "", facility_id: str = ""
) -> dict:
    """`m4-onboarding-apis/01`. `facilityId` here is the 6-digit facility unique id, not the `IN` id
    (registries/nhpr/hfr §The facility ID)."""
    return {
        "name": name,
        "address": address,
        "district": district_lgd,
        "subDistrict": sub_district_lgd,
        "village": village_lgd or "",
        "geolocation": "",
        "facilityId": facility_id or "",
    }


def basic_information_body(facility_information: dict, tracking_id: str = "") -> dict:
    """`m4-onboarding-apis/02`: `{trackingId, facilityInformation{...}}`. An empty `trackingId`
    creates the record; the returned `trackingId` is carried by every later step."""
    info = _only(facility_information, BASIC_KEYS, "facilityInformation")
    if not str(info.get("facilityName") or "").strip():
        raise ValueError("facilityName is required.")
    address = info.get("facilityAddressDetails")
    if not isinstance(address, dict) or not str(address.get("stateLGDCode") or ""):
        raise ValueError("facilityAddressDetails.stateLGDCode is required.")
    # HIS-4019 and HIS-4020: 1 to 6 decimal places. A value prefilled from Care carries 16.
    address = dict(address)
    for kind in ("latitude", "longitude"):
        address[kind] = coordinate(address.get(kind), kind, strict=True)
    info["facilityAddressDetails"] = address
    uploads = info.get("facilityUploads") if isinstance(info.get("facilityUploads"), dict) else {}
    for key in ("facilityBoardPhoto", "facilityBuildingPhoto"):
        photo = uploads.get(key) if isinstance(uploads.get(key), dict) else {}
        if base64_size(str(photo.get("value") or "")) > MAX_DOCUMENT_BYTES:
            raise ValueError(f"{key} is larger than 5 MB.")
    return {"trackingId": tracking_id or "", "facilityInformation": info}


def additional_information_body(payload: dict, tracking_id: str) -> dict:
    """`m4-onboarding-apis/03`."""
    if not tracking_id:
        raise ValueError("Save the basic information first: no tracking id.")
    body = _only(payload, ADDITIONAL_KEYS, "additional information")
    body["trackingId"] = tracking_id
    return body


# `medicalInfrastructure` (m4-onboarding-apis/04). The registry sums the first 6 against
# `totalNumberOfBeds` and refuses a difference (HIS-1070, observed 2026-09-21, findings N27); the ICU
# beds, the ventilators and the dental chairs are outside the sum.
BED_SUM_FIELDS = (
    "countIPDBedsWithoutOxygen",
    "countIPDBedsWithOxygen",
    "countHDUBedsWithVentilators",
    "countHDUBedsWithoutVentilators",
    "countDayCareBedsWithoutOxygen",
    "countDayCareBedsWithOxygen",
)
INFRASTRUCTURE_FIELDS = BED_SUM_FIELDS + (
    "countICUBedsWithVentilators",
    "countICUBedsWithoutVentilators",
    "totalNumberOfVentilators",
    "countDentalChairs",
)


def _count(value, field: str) -> int:
    """A bed or equipment count: a whole number, 0 or more; an empty value is 0."""
    if value in (None, ""):
        return 0
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field} must be a whole number.") from None
    if number < 0:
        raise ValueError(f"{field} cannot be negative.")
    return number


def medical_infrastructure(payload) -> dict:
    """Every count as an integer, 0 when absent, and `totalNumberOfBeds` **derived** as the sum of the
    6 counts the registry sums, so its equality rule can never be broken by a typed total. A typed
    `totalNumberOfBeds` is ignored."""
    data = payload if isinstance(payload, dict) else {}
    unknown = sorted(set(data) - set(INFRASTRUCTURE_FIELDS) - {"totalNumberOfBeds"})
    if unknown:
        raise ValueError(f"Unknown medicalInfrastructure field: {', '.join(unknown)}.")
    counts = {field: _count(data.get(field), field) for field in INFRASTRUCTURE_FIELDS}
    counts["totalNumberOfBeds"] = sum(counts[field] for field in BED_SUM_FIELDS)
    return counts


def specialities(payload) -> list[dict]:
    """The speciality rows of the detailed step, with every code **unprefixed**.

    2 code spaces, as with the facility type (findings N21): `get-specialities`
    (m4-utilities/07) answers the code prefixed with the system of medicine — `"D-S44"`,
    `"UN-S68"` — while the detailed-information body takes the bare code, `"S44"`, `"S68"`
    (m4-onboarding-apis/04 example). Sending the master code as answered is refused with
    `HIS-1070 "Invalid SpecialityCode provided for SystemOfMedicineCode -UN"` (observed
    2026-09-21, findings N30). The prefix is stripped here, so no caller can send a refused
    code and a bare code passes through unchanged.
    """
    rows = payload if isinstance(payload, list) else []
    out = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Each speciality row must be an object.")
        unknown = sorted(set(row) - {"systemOfMedicineCode", "isSpecializationAvalaible", "specialities"})
        if unknown:
            raise ValueError(f"Unknown speciality field: {', '.join(unknown)}.")
        som = str(row.get("systemOfMedicineCode") or "").strip()
        codes = row.get("specialities")
        codes = codes if isinstance(codes, list) else []
        prefix = f"{som}-"
        out.append(
            {
                "systemOfMedicineCode": som,
                "isSpecializationAvalaible": str(row.get("isSpecializationAvalaible") or "N").strip(),
                "specialities": [
                    code[len(prefix) :] if som and code.startswith(prefix) else code
                    for code in (str(c).strip() for c in codes)
                    if code
                ],
            }
        )
    return out


def detailed_information_body(payload: dict, tracking_id: str) -> dict:
    """`m4-onboarding-apis/04`. The bed total is derived (`medical_infrastructure`) and the
    speciality codes are unprefixed (`specialities`)."""
    if not tracking_id:
        raise ValueError("Save the basic information first: no tracking id.")
    body = _only(payload, DETAILED_KEYS, "detailed information")
    if "specialities" in body:
        body["specialities"] = specialities(body["specialities"])
    if "medicalInfrastructure" in body:
        body["medicalInfrastructure"] = medical_infrastructure(body["medicalInfrastructure"])
    body["trackingId"] = tracking_id
    return body


def submit_body(payload: dict, tracking_id: str) -> dict:
    """`m4-onboarding-apis/05`."""
    if not tracking_id:
        raise ValueError("Save the basic information first: no tracking id.")
    body = _only(payload or {}, SUBMIT_KEYS, "submit")
    body["trackingId"] = tracking_id
    return body


def parse_onboarding_result(payload) -> dict:
    """`{trackingId, status, message, errorStatus}` (the 4 onboarding 200 shapes)."""
    data = payload if isinstance(payload, dict) else {}
    error = data.get("errorStatus")
    return {
        "tracking_id": str(data.get("trackingId") or ""),
        "status": str(data.get("status") or ""),
        "message": str(data.get("message") or ""),
        "error": str(error) if error not in (None, "", {}) else "",
        "facility_id": str(data.get("facilityId") or ""),
    }


def strip_photos(facility_information: dict) -> dict:
    """The stored copy of the basic step keeps the photo names and drops the bytes."""
    info = dict(facility_information or {})
    uploads = info.get("facilityUploads")
    if isinstance(uploads, dict):
        info["facilityUploads"] = {
            key: {"name": str((value or {}).get("name") or ""), "value": "" if (value or {}).get("value") else ""}
            for key, value in uploads.items()
            if isinstance(value, dict)
        }
    if isinstance(info.get("facilityAddressProof"), list):
        info["facilityAddressProof"] = [
            {k: ("" if k in ("value", "data") else v) for k, v in item.items()}
            for item in info["facilityAddressProof"]
            if isinstance(item, dict)
        ]
    return info


# --- masters (m4-utilities, m4-utility, m4-util) ---------------------------------------------------


# The name field of each master shape observed on the sandbox (2026-09-21): the facility masters
# answer `{type, data[{code, value}]}`, the LGD calls `[{code, name, districts?}]`, the HPR masters
# `[{id, name}]`, `[{id, districtName, isoCode}]`, `[{id, subDistrictName}]`, `[{id, enShortName,
# nationality}]` (countries) and `[{id, medicalSystem, code, hprType}]` (systems of medicine).
_MASTER_NAME_KEYS = ("value", "name", "desc", "districtName", "subDistrictName", "enShortName", "medicalSystem")


def _first_present(item: dict, keys: tuple[str, ...]):
    for key in keys:
        if item.get(key) not in (None, ""):
            return item[key]
    return None


def parse_code_values(payload) -> list[dict]:
    """Every master shape becomes `[{code, name, children?}]` for the desk pickers. The register
    bodies take the master `id` (`registeredWithCouncil: "47"`, `college: "1022"`, m4-enrollment/01),
    so `id` wins over a slug `code` when both exist (systems of medicine carry both). Values are
    stripped: the sandbox pads the OWNER master (`"G         "`) and the languages (`" English "`)."""
    rows = payload
    if isinstance(payload, dict):
        rows = payload.get("data") if isinstance(payload.get("data"), list) else payload.get("masterTypes")
    out = []
    for item in rows or []:
        if not isinstance(item, dict):
            continue
        code = _first_present(item, ("id", "code", "type")) if "id" in item else _first_present(item, ("code", "type"))
        name = _first_present(item, _MASTER_NAME_KEYS)
        if code is None or name is None:
            continue
        row = {"code": str(code).strip(), "name": str(name).strip()}
        if isinstance(item.get("subCategories"), list):
            row["children"] = parse_code_values(item["subCategories"])
        if isinstance(item.get("districts"), list):
            row["children"] = parse_code_values(item["districts"])
        out.append(row)
    return out


def courses_body(system_of_medicine: str, hpr_type: str, qualification_count: int = 0) -> dict:
    """`m4-utility/08`: the example sends `{systemOfMedicine, hprType, qualificationCount}`."""
    return {
        "systemOfMedicine": system_of_medicine,
        "hprType": hpr_type,
        "qualificationCount": int(qualification_count or 0),
    }
