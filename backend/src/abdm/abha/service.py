"""
Flow orchestration: calls the ABHA client and records AbhaTransaction state.
Views stay thin; this is the only place that decides what is persisted.
"""

import logging
from datetime import timedelta

from django.utils import timezone

from abdm.abha import client
from abdm.abha.client import AbhaServiceError, LoginHint, OtpSystem
from abdm.care_seams import AbhaAddressIdentifier, AbhaNumberIdentifier
from abdm.models import AbhaTransaction

logger = logging.getLogger(__name__)

# Fields of the ABDM profile/account body that we never persist or return: photo blobs are
# large and are PII we have no use for; tokens must never reach the browser.
_STRIP_KEYS = {"profilePhoto", "photo", "tokens", "token", "_t_token"}

LOGIN_KIND_BY_HINT: dict[LoginHint, str] = {
    "mobile": AbhaTransaction.Kind.LOGIN_MOBILE,
    "abha-number": AbhaTransaction.Kind.LOGIN_ABHA_NUMBER,
    "abha-address": AbhaTransaction.Kind.LOGIN_ABHA_ADDRESS,
    "aadhaar": AbhaTransaction.Kind.LOGIN_AADHAAR,
}


def _upsert(txn_id: str, kind: str, user, **fields) -> AbhaTransaction:
    txn, _ = AbhaTransaction.objects.get_or_create(txn_id=txn_id, defaults={"kind": kind, "created_by": user})
    for k, v in fields.items():
        setattr(txn, k, v)
    txn.save()
    return txn


def _capture_token(txn: AbhaTransaction, tokens: dict | None) -> None:
    """Persist an X-token (+ refresh token) response: {token, expiresIn, refreshToken, refreshExpiresIn}."""
    if not tokens or not tokens.get("token"):
        return
    now = timezone.now()
    txn.x_token = tokens["token"]
    expires_in = tokens.get("expiresIn")
    txn.x_token_expires_at = now + timedelta(seconds=int(expires_in)) if expires_in else None
    # A refresh response may omit refreshToken (docs don't say); keep the previous one in that case.
    if tokens.get("refreshToken"):
        txn.refresh_token = tokens["refreshToken"]
        refresh_in = tokens.get("refreshExpiresIn")
        txn.refresh_token_expires_at = now + timedelta(seconds=int(refresh_in)) if refresh_in else None
    txn.save(
        update_fields=[
            "x_token",
            "x_token_expires_at",
            "refresh_token",
            "refresh_token_expires_at",
            "modified_date",
        ]
    )


def _clean(d: dict) -> dict:
    return {k: v for k, v in d.items() if k not in _STRIP_KEYS}


# --- X-token lifecycle -------------------------------------------------------


class NoUserSession(Exception):
    """No usable X-token and no way to refresh one: the person must authenticate (OTP) again."""


def ensure_x_token(txn: AbhaTransaction) -> str:
    """Return a live X-token for this transaction, refreshing via the R-token when it has expired.

    Real-world shape of the problem: X-token lives ~30 min (observed expiresIn from
    select-account), the refresh token far longer. A nurse pulling up a patient's ABHA card
    the day after registration should not be sent back for an OTP; this is what makes the card
    work on any later visit while the refresh token still lives.
    """
    if txn.x_token_valid:
        return txn.x_token
    if not txn.refresh_token_valid:
        raise NoUserSession()
    try:
        res = client.refresh_x_token(txn.refresh_token)
    except AbhaServiceError as exc:
        if exc.status_code in (400, 401, 403):
            # Refresh token revoked/expired server-side: drop it so status flips to "needs OTP".
            txn.refresh_token = ""
            txn.refresh_token_expires_at = None
            txn.save(update_fields=["refresh_token", "refresh_token_expires_at", "modified_date"])
            raise NoUserSession() from exc
        raise
    logger.info("abdm: refreshed X-token for txn %s; response keys=%s", txn.txn_id, sorted(res.keys()))
    _capture_token(txn, res)
    if not txn.x_token_valid:
        raise NoUserSession()
    return txn.x_token


# --- Journey 1 -------------------------------------------------------------


def enrol_request_otp(aadhaar: str, user) -> dict:
    """The view has already required `consent=true`; record it against the transaction (CRT_ABHA_102)."""
    res = client.request_aadhaar_otp(aadhaar)
    _upsert(
        res["txnId"],
        AbhaTransaction.Kind.ENROL_AADHAAR,
        user,
        consent_recorded_at=timezone.now(),
        consent_code=client.CONSENT["code"],
        consent_version=client.CONSENT["version"],
    )
    return res


def enrol_verify(txn_id: str, otp: str, mobile: str, user) -> dict:
    res = client.enrol_by_aadhaar(txn_id, otp, mobile)
    profile = res.get("ABHAProfile") or {}
    txn = _upsert(
        res.get("txnId") or txn_id,
        AbhaTransaction.Kind.ENROL_AADHAAR,
        user,
        abha_number=profile.get("ABHANumber", "") or "",
        abha_address=(profile.get("phrAddress") or [""])[0]
        if isinstance(profile.get("phrAddress"), list)
        else profile.get("phrAddress", "") or "",
        profile=_clean(profile),
        is_new=res.get("isNew"),
    )
    _capture_token(txn, res.get("tokens"))
    # Never return the user token to the browser.
    return {k: v for k, v in res.items() if k != "tokens"}


def enrol_claim_address(txn_id: str, abha_address: str) -> dict:
    res = client.claim_abha_address(txn_id, abha_address)
    AbhaTransaction.objects.filter(txn_id=txn_id).update(
        abha_address=res.get("preferredAbhaAddress") or abha_address,
        abha_number=res.get("healthIdNumber")
        or AbhaTransaction.objects.filter(txn_id=txn_id).values_list("abha_number", flat=True).first()
        or "",
    )
    return res


# --- Login to an existing ABHA (mobile / ABHA number / ABHA address / Aadhaar) ---


def _login_params(txn: AbhaTransaction) -> tuple[LoginHint, OtpSystem]:
    hint = txn.profile.get("_hint", "mobile")
    otp_system = txn.profile.get("_otp_system", "abdm")
    return hint, otp_system


def login_request_otp(hint: LoginHint, login_id: str, otp_system: OtpSystem, user) -> dict:
    res = client.login_request_otp(hint, login_id, otp_system)
    txn = _upsert(res["txnId"], LOGIN_KIND_BY_HINT[hint], user)
    # The verify call must repeat the same scope; remember what this txn was started with.
    txn.profile = {**txn.profile, "_hint": hint, "_otp_system": otp_system}
    txn.save(update_fields=["profile", "modified_date"])
    return res


def _finalize_login(txn: AbhaTransaction, tokens: dict, seed: dict | None = None) -> dict:
    """We hold an X-token: persist it, fetch the full account profile (name, DOB, gender,
    address, pincode, kycVerified — what registration prefill needs), mark txn complete."""
    _capture_token(txn, tokens)
    profile = dict(seed or {})
    try:
        profile = {**profile, **_clean(client.get_profile(txn.x_token))}
    except AbhaServiceError as exc:
        # Login succeeded; a failed profile read must not fail the flow. The wizard shows
        # what we have (ABHA number/address) and registration prefill is just thinner.
        logger.warning("abdm: GET /v3/profile/account failed after login (txn %s): %s", txn.txn_id, exc)
    txn.abha_number = profile.get("ABHANumber") or txn.abha_number or ""
    txn.abha_address = profile.get("preferredAbhaAddress") or txn.abha_address or ""
    txn.profile = {k: v for k, v in profile.items() if not k.startswith("_")}
    txn.is_new = False
    txn.save(update_fields=["abha_number", "abha_address", "profile", "is_new", "modified_date"])
    return {
        "txnId": txn.txn_id,
        "authResult": "success",
        "completed": True,
        "ABHANumber": txn.abha_number,
        "preferredAbhaAddress": txn.abha_address,
        "name": profile.get("name"),
        "profile": txn.profile,
        "existingPatient": existing_patient_for(txn),
    }


def existing_patient_for(txn: AbhaTransaction) -> dict | None:
    """Is this ABHA already on a CARE patient? Drives the desk's "open vs register" choice.
    Lookup by ABHA number first (stable), then address (may be re-pointed by the user)."""
    patient = None
    if txn.abha_number:
        patient = AbhaNumberIdentifier.find_patient(txn.abha_number)
    if patient is None and txn.abha_address:
        patient = AbhaAddressIdentifier.find_patient(txn.abha_address)
    if patient is None:
        return None
    return {
        "id": str(patient.external_id),
        "name": patient.name,
        "phone_number": patient.phone_number,
        "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        "year_of_birth": patient.year_of_birth,
        "gender": patient.gender,
    }


def login_verify(txn_id: str, otp: str, user) -> dict:
    """Two possible outcomes, decided from the body not the hint:
    - accounts + T-token (mobile login): caller must pick an account -> `completed: False`
    - X-token directly (number/address/aadhaar): done -> `completed: True` with the profile."""
    txn = AbhaTransaction.objects.get(txn_id=txn_id)
    hint, otp_system = _login_params(txn)
    res = client.login_verify_otp(hint, otp_system, txn_id, otp)
    if res.get("txnId") and res["txnId"] != txn.txn_id:
        # ABDM may hand back a new txnId; keep both resolvable.
        txn = _upsert(res["txnId"], txn.kind, user, profile=txn.profile)
    accounts = [_clean(a) for a in res.get("accounts") or []]
    # An X-token comes with expiresIn/refreshToken; a T-token comes with an accounts list only.
    is_x_token = bool(res.get("token")) and (res.get("refreshToken") or res.get("expiresIn")) and len(accounts) <= 1
    if is_x_token:
        return _finalize_login(txn, res, seed=accounts[0] if accounts else None)
    txn.profile = {**txn.profile, "_t_token": res.get("token", ""), "accounts": accounts}
    txn.save(update_fields=["profile", "modified_date"])
    return {
        "txnId": txn.txn_id,
        "authResult": res.get("authResult"),
        "message": res.get("message"),
        "completed": False,
        "accounts": accounts,
    }


def login_select(txn_id: str, abha_number: str) -> dict:
    txn = AbhaTransaction.objects.get(txn_id=txn_id)
    t_token = txn.profile.get("_t_token", "")
    account = next((a for a in txn.profile.get("accounts", []) if a.get("ABHANumber") == abha_number), None)
    if account is None:
        raise ValueError("ABHA number is not among the accounts returned for this login")
    res = client.login_select_account(txn_id, t_token, abha_number)
    txn.abha_number = abha_number
    txn.abha_address = account.get("preferredAbhaAddress", "") or ""
    txn.save(update_fields=["abha_number", "abha_address", "modified_date"])
    return _finalize_login(txn, res, seed=account)


# --- Read side ---------------------------------------------------------------


def transaction_summary(txn: AbhaTransaction) -> dict:
    """What the browser may know about a completed transaction (no tokens)."""
    return {
        "txnId": txn.txn_id,
        "kind": txn.kind,
        "ABHANumber": txn.abha_number,
        "preferredAbhaAddress": txn.abha_address,
        "isNew": txn.is_new,
        "profile": {k: v for k, v in txn.profile.items() if not k.startswith("_") and k != "accounts"},
        "patient": str(txn.patient.external_id) if txn.patient_id else None,
        "linkedAt": txn.linked_at,
        "consentRecordedAt": txn.consent_recorded_at,
        "sessionAvailable": txn.session_available,
        "existingPatient": existing_patient_for(txn),
    }
