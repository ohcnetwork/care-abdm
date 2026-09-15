"""
ABHA service client for M1 Journey 1 (ABHA creation by Aadhaar OTP) and the
mobile-verify sub-step. Every method maps 1:1 to one documented endpoint; the
docstring cites the page. Response bodies marked UNDOCUMENTED are returned raw
and logged so the real shape can be recorded in docs/findings.md after the
first live run.

Docs (mirrored in docs/abdm-docs-mirror/pages/m1/):
  m1-enrolment-request-otp      POST /v3/enrollment/request/otp
  m1-enrolment-by-aadhaar       POST /v3/enrollment/enrol/byAadhaar       (200 body UNDOCUMENTED)
  m1-enrolment-verify-abdm-otp  POST /v3/enrollment/auth/byAbdm
  m1-enrolment-address-suggestions GET /v3/enrollment/enrol/suggestion    (header TRANSACTION_ID)
  m1-enrolment-claim-abha-address  POST /v3/enrollment/enrol/abha-address
  m1-profile-get-account        GET  /v3/profile/account                  (needs X-token)
"""

import logging
from typing import Literal

import requests

from abdm.abha.crypto import encrypt
from abdm.gateway.session import gateway_headers, get_access_token
from abdm.settings import plugin_settings

logger = logging.getLogger(__name__)

CONSENT = {"code": "abha-enrollment", "version": "1.4"}  # from the byAadhaar example


class AbhaServiceError(Exception):
    def __init__(self, status_code: int, body, request_id: str):
        self.status_code = status_code
        self.body = body
        self.request_id = request_id
        super().__init__(f"ABHA service HTTP {status_code} (REQUEST-ID {request_id}): {body}")

    def abdm_code(self) -> str | None:
        # 422 shape: {"error": {"code": "ABDM-1204", "message": ...}}; 400 shape: {"<field>": "<msg>"}
        if isinstance(self.body, dict):
            err = self.body.get("error")
            if isinstance(err, dict):
                return err.get("code")
        return None

    def message(self) -> str:
        if isinstance(self.body, dict):
            err = self.body.get("error")
            if isinstance(err, dict) and err.get("message"):
                return err["message"]
            fields = {k: v for k, v in self.body.items() if k != "timestamp"}
            if fields:
                return "; ".join(f"{k}: {v}" for k, v in fields.items())
        return str(self.body)


def _headers(extra: dict | None = None, x_token: str | None = None) -> dict:
    headers = gateway_headers(get_access_token())
    headers.pop("X-CM-ID", None)  # gateway-only header; ABHA service calls work without it
    if x_token:
        headers["X-token"] = f"Bearer {x_token}"  # docs: value carries a `Bearer ` prefix
    if extra:
        headers.update(extra)
    return headers


def _call(method: str, path: str, *, json=None, headers: dict | None = None, raw: bool = False):
    headers = headers or _headers()
    url = f"{plugin_settings.ABHA_URL}{path}"
    response = requests.request(
        method, url, headers=headers, json=json, timeout=plugin_settings.REQUEST_TIMEOUT_SECONDS
    )
    request_id = headers["REQUEST-ID"]
    if raw and 200 <= response.status_code < 300:
        body = None
    else:
        try:
            body = response.json() if response.text else {}
        except ValueError:
            body = response.text
    logger.info("abha %s %s -> %s (REQUEST-ID %s)", method, path, response.status_code, request_id)
    if not 200 <= response.status_code < 300:
        raise AbhaServiceError(response.status_code, body, request_id)
    if raw:
        return response
    if not isinstance(body, dict):
        # A 2xx with a non-JSON body is a contract surprise worth surfacing, not silently wrapping.
        raise AbhaServiceError(response.status_code, body, request_id)
    return body


# --- Journey 1 -------------------------------------------------------------


def request_aadhaar_otp(aadhaar_number: str) -> dict:
    """-> {txnId, message}"""
    return _call(
        "POST",
        "/v3/enrollment/request/otp",
        json={
            "scope": ["abha-enrol"],
            "loginHint": "aadhaar",
            "loginId": encrypt(aadhaar_number),
            "otpSystem": "aadhaar",
        },
    )


def enrol_by_aadhaar(txn_id: str, otp: str, mobile: str) -> dict:
    """UNDOCUMENTED 200 body. Docs hint: `tokens.token` (user token), profile details.
    Permanent side effect: never retry blindly."""
    return _call(
        "POST",
        "/v3/enrollment/enrol/byAadhaar",
        json={
            "authData": {
                "authMethods": ["otp"],
                "otp": {"txnId": txn_id, "otpValue": encrypt(otp), "mobile": mobile},
            },
            "consent": CONSENT,
        },
        headers=_headers({"BENEFIT_NAME": "healthid api"}),
    )


def request_mobile_otp(txn_id: str, mobile: str) -> dict:
    """Journey 2 (communication mobile): scope gains mobile-verify, otpSystem abdm."""
    return _call(
        "POST",
        "/v3/enrollment/request/otp",
        json={
            "scope": ["abha-enrol", "mobile-verify"],
            "loginHint": "mobile",
            "loginId": encrypt(mobile),
            "otpSystem": "abdm",
            "txnId": txn_id,
        },
    )


def verify_mobile_otp(txn_id: str, otp: str) -> dict:
    """-> {txnId, authResult, message, accounts}"""
    return _call(
        "POST",
        "/v3/enrollment/auth/byAbdm",
        json={
            "scope": ["abha-enrol", "mobile-verify"],
            "authData": {"authMethods": ["otp"], "otp": {"txnId": txn_id, "otpValue": encrypt(otp)}},
        },
    )


def address_suggestions(txn_id: str) -> dict:
    """-> {txnId, abhaAddressList}"""
    return _call("GET", "/v3/enrollment/enrol/suggestion", headers=_headers({"TRANSACTION_ID": txn_id}))


def claim_abha_address(txn_id: str, abha_address: str) -> dict:
    """-> {healthIdNumber}  (the ABHA number comes back as healthIdNumber)"""
    return _call(
        "POST",
        "/v3/enrollment/enrol/abha-address",
        json={"txnId": txn_id, "abhaAddress": abha_address, "preferred": 1},
    )


# --- Journey 5 (+ number/address/Aadhaar variants): login to an existing ABHA


# Login "hints" (what the person identifies themselves with) × OTP systems.
# Contract: MCP get_operation m1_login_request_otp (examples login_abha_via_mobile_number,
# login_via_abha_number_mobile_otp, login_abha_via_aadhaar_number; description lists
# loginHint ∈ {mobile, aadhaar, abha-number}) and m1_phr_request_otp (loginHint abha-address,
# scope abha-address-login + mobile-verify|aadhaar-verify, different path).
LoginHint = Literal["mobile", "abha-number", "abha-address", "aadhaar"]
OtpSystem = Literal["abdm", "aadhaar"]

_LOGIN_PATHS = {
    # (request-otp, verify)
    "profile": ("/v3/profile/login/request/otp", "/v3/profile/login/verify"),
    "phr": ("/v3/phr/web/login/abha/request/otp", "/v3/phr/web/login/abha/verify"),
}


def _login_scope(hint: LoginHint, otp_system: OtpSystem) -> tuple[list[str], str]:
    """-> (scope, path family). `mobile` hint only supports the abdm OTP system."""
    verify = "aadhaar-verify" if otp_system == "aadhaar" else "mobile-verify"
    if hint == "abha-address":
        return ["abha-address-login", verify], "phr"
    return ["abha-login", verify], "profile"


def _wire_login_id(hint: LoginHint, login_id: str) -> str:
    """Put `login_id` in the plaintext shape the service accepts, before encryption.

    Observed on sandbox 2026-09-11 (docs/findings.md) with a synthetic Luhn-valid number:
    14 bare digits -> 400 {"loginId": "LoginId is invalid"}; the same digits as
    NN-NNNN-NNNN-NNNN -> 404 ABDM-1114 "User not found" (format accepted, account looked up).
    The docs give no example for loginHint `abha-number`, so the dashes are a sandbox finding.
    Callers pass 14 digits (abdm/abha/views.py LoginOtpRequest strips the separators)."""
    if hint != "abha-number":
        return login_id
    d = login_id.replace("-", "")
    return f"{d[0:2]}-{d[2:6]}-{d[6:10]}-{d[10:14]}" if len(d) == 14 else login_id


def login_request_otp(hint: LoginHint, login_id: str, otp_system: OtpSystem = "abdm") -> dict:
    """m1-login-request-otp / m1-phr-request-otp -> {txnId, message}.
    `login_id` is the raw mobile / ABHA number / ABHA address / Aadhaar; encrypted here.
    NOTE phr example shows otpSystem "abdm, aadhaar" (a template placeholder); we send one value."""
    scope, family = _login_scope(hint, otp_system)
    return _call(
        "POST",
        _LOGIN_PATHS[family][0],
        json={
            "scope": scope,
            "loginHint": hint,
            "loginId": encrypt(_wire_login_id(hint, login_id)),
            "otpSystem": otp_system,
        },
        headers=_headers({"BENEFIT_NAME": "healthid api"}),
    )


def login_verify_otp(hint: LoginHint, otp_system: OtpSystem, txn_id: str, otp: str) -> dict:
    """m1-login-verify / m1-phr-verify.
    mobile hint  -> {txnId, authResult, token (T-token), accounts:[{ABHANumber, preferredAbhaAddress, name}]}
    other hints  -> {txnId, authResult, token (X-token), expiresIn, refreshToken, refreshExpiresIn, accounts?}
    Which of the two the body is must be decided from the fields, not the hint (see service)."""
    scope, family = _login_scope(hint, otp_system)
    return _call(
        "POST",
        _LOGIN_PATHS[family][1],
        json={
            "scope": scope,
            "authData": {"authMethods": ["otp"], "otp": {"txnId": txn_id, "otpValue": encrypt(otp)}},
        },
        headers=_headers({"BENEFIT_NAME": "healthid api"}),
    )


def login_select_account(txn_id: str, t_token: str, abha_number: str) -> dict:
    """m1-login-select-account -> {token (X-token), expiresIn, refreshToken, refreshExpiresIn}.
    Docs: T-token carries a `Bearer ` prefix in every recorded request."""
    return _call(
        "POST",
        "/v3/profile/login/verify/user",
        json={"ABHANumber": abha_number, "txnId": txn_id},
        headers=_headers({"T-token": f"Bearer {t_token}"}),
    )


# --- Journey 7: profile and card (need X-token) -----------------------------


def get_abha_card(x_token: str):
    """m1-profile-get-abha-card. 200 body UNDOCUMENTED (content-type observed at runtime)."""
    return _call("GET", "/v3/profile/account/abha-card", headers=_headers(x_token=x_token), raw=True)


def get_profile(x_token: str) -> dict:
    """-> profile (ABHANumber, preferredAbhaAddress, name, gender, dob parts, ...)"""
    return _call("GET", "/v3/profile/account", headers=_headers(x_token=x_token))


def refresh_x_token(refresh_token: str) -> dict:
    """m1-token-refresh: GET /v3/profile/account/request/token, header R-token.
    -> {token, expiresIn, refreshToken, refreshExpiresIn}  (fields hypothesised from the
    select-account response; the page documents no 200 body — log the real one).
    The page (re-read 2026-09-15) sends `R-token` bare. It is not yet confirmed against the
    sandbox, so a 401 on the bare form retries with the `Bearer ` prefix that X-token and
    T-token carry, and logs which form worked (docs/findings.md C8)."""
    try:
        return _call("GET", "/v3/profile/account/request/token", headers=_headers({"R-token": refresh_token}))
    except AbhaServiceError as exc:
        if exc.status_code != 401:
            raise
        logger.info("abdm: bare R-token rejected (%s); retrying with the Bearer prefix", exc.abdm_code())
        body = _call(
            "GET", "/v3/profile/account/request/token", headers=_headers({"R-token": f"Bearer {refresh_token}"})
        )
        logger.warning("abdm: R-token accepted only WITH the Bearer prefix — update docs/findings.md C8")
        return body
