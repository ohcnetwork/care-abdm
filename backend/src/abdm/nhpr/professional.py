"""
M4 for a Care user (ADR-015): link an existing HPR ID by logging in, create an HPID (journey 1),
register the professional profile (journey 2), and hold the person's HPR token for the HFR writes.

registries/nhpr/hpr: the token "proves who the professional is, not that your client may call", so
every call still carries the integration bearer. Login by password and by Aadhaar OTP have a
published verify step; mobile OTP has a send call only (docs/findings.md N5).
"""

import logging

from django.utils import timezone

from abdm import errors
from abdm.models import AbdmHpidTransaction, AbdmHprLogin, AbdmHprProfile, AbdmOutboundRequest
from abdm.nhpr import client, rules

logger = logging.getLogger(__name__)

MAX_OTP_ATTEMPTS = 3


class HprError(Exception):
    def __init__(self, code: str, message: str, request_id: str = "", details: list[str] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.request_id = request_id
        # The registry's own words, 1 line each, carried beside the plug sentence (abdm-m3 design.md).
        self.details = list(details or [])

    @property
    def detail(self) -> str:
        return " ".join(self.details)

    def as_dict(self) -> dict:
        return {
            "errors": self.message,
            "detail": self.detail,
            "details": self.details,
            "code": self.code,
            "requestId": self.request_id,
        }


REFUSED = "The registry refused the request."


def _raise_from(exc: client.NhprError) -> HprError:
    """A refused registry call: the registry's own words when it sent any (see facility._raise_from)."""
    failure = errors.classify(
        code=exc.code, http_status=exc.row.http_status if exc.row else None, message=str(exc), request_id=exc.request_id
    )
    lines = client.refusal_lines(exc.row)
    message = f"{REFUSED} {' '.join(lines)}" if lines else f"{failure.what} {failure.next_step}".strip()
    return HprError(failure.code or "NHPR_ERROR", message, exc.request_id, lines)


# Observed 2026-09-21: `searchByHprId` and `existsByHprId` answer HTTP 422 `HIS-3008 "Invalid HPID."`
# for an id nobody holds, where the page says 404 (docs/findings.md N20).
NOT_FOUND_CODES = ("HIS-3008",)


def _is_not_found(exc: client.NhprError) -> bool:
    if exc.row is None:
        return False
    if exc.row.http_status == 404:
        return True
    text = str(exc)
    return exc.row.http_status == 422 and any(code in text for code in NOT_FOUND_CODES)


def profile_for(user, *, heal: bool = False) -> AbdmHprProfile | None:
    """The user's HPR profile. With `heal`, a profile that holds an id and no name (the account call
    was refused at login, N25) fills itself from the public record once, 1 registry call."""
    profile = AbdmHprProfile.objects.filter(user=user).first()
    if heal and profile is not None and not profile.name and (profile.hpr_id or profile.hpr_id_number):
        _fill_from_public_record(profile)
        if profile.name:
            profile.save(
                update_fields=[
                    "hpr_id",
                    "hpr_id_number",
                    "name",
                    "category_code",
                    "sub_category_code",
                    "role",
                    "modified_date",
                ]
            )
    return profile


def _store_token(profile: AbdmHprProfile, token_data: dict, method: str) -> None:
    profile.token = token_data["token"]
    profile.token_expires_at = token_data["expires_at"]
    profile.refresh_token = token_data["refresh_token"]
    profile.refresh_expires_at = token_data["refresh_expires_at"]
    profile.token_method = method
    profile.token_issued_at = timezone.now()


# `hpid/get/categories?role=2` names 100 "Facility Manager" (observed 2026-09-21); the other categories
# (1 Doctor, 2 Nurse, ...) are healthcare professionals (registries/nhpr/hpr §Who can enrol).
FACILITY_MANAGER_CATEGORY = "100"


def _fill_from_public_record(profile: AbdmHprProfile) -> None:
    """`searchByHprId`: the public record (name, both id forms, category) when the account call is
    refused. Observed 2026-09-21: `GET /v1/account/information` answers HIS-500 on every try, and the
    public record is what the login dialog already showed (findings N25)."""
    hpr_id = profile.hpr_id or rules.hpr_id_number_digits(profile.hpr_id_number)
    if not hpr_id:
        return
    try:
        row = client.ok(client.search_hpr_id(hpr_id))
    except client.NhprError as exc:
        logger.warning("abdm: public HPR record refused after login: %s", exc)
        return
    record = rules.parse_hpr_search(row.response_json)
    profile.hpr_id = (profile.hpr_id or record["hpr_id"])[:128]
    profile.hpr_id_number = (profile.hpr_id_number or rules.format_hpr_id_number(record["hpr_id_number"]))[:32]
    profile.name = (record["name"] or profile.name)[:256]
    profile.category_code = (record["category_id"] or profile.category_code)[:16]
    profile.sub_category_code = (record["sub_category_id"] or profile.sub_category_code)[:16]
    if profile.role is None and profile.category_code:
        profile.role = 2 if profile.category_code == FACILITY_MANAGER_CATEGORY else 1


def _fill_from_account(profile: AbdmHprProfile) -> None:
    """`GET /v1/account/information` with the person's token: the HPR ID in both forms, the name,
    the category codes. A refusal leaves the login valid: the claims of the token still name the id,
    and the public record fills the rest."""
    try:
        row = client.ok(client.account_information(profile.token))
    except client.NhprError as exc:
        logger.warning("abdm: account information refused after login: %s", exc)
        claims = rules.jwt_claims(profile.token)
        profile.hpr_id = profile.hpr_id or str(claims.get("hprId") or claims.get("preferred_username") or "")[:128]
        profile.hpr_id_number = (
            profile.hpr_id_number or rules.format_hpr_id_number(str(claims.get("hprIdNumber") or ""))[:32]
        )
        _fill_from_public_record(profile)
        return
    account = rules.parse_account_information(row.response_json)
    profile.account = account
    profile.hpr_id = str(account.get("hprId") or profile.hpr_id)[:128]
    profile.hpr_id_number = rules.format_hpr_id_number(str(account.get("hprIdNumber") or profile.hpr_id_number))[:32]
    profile.name = str(
        account.get("name")
        or " ".join(p for p in (account.get("firstName"), account.get("middleName"), account.get("lastName")) if p)
        or profile.name
    )[:256]
    profile.category_code = str(account.get("hpCategoryCode") or profile.category_code)[:16]
    profile.sub_category_code = str(account.get("hpSubCategoryCode") or profile.sub_category_code)[:16]
    try:
        profile.role = int(account["role"]) if account.get("role") not in (None, "") else profile.role
    except (TypeError, ValueError):
        pass


def _same_identity(profile: AbdmHprProfile, hpr_id: str) -> bool:
    """Does the id the person typed name the profile already linked? A form the profile does not
    hold yet (number vs address) cannot disagree, so it passes."""
    if rules.hpr_id_kind(hpr_id) == "number":
        return not profile.hpr_id_number or rules.hpr_id_number_digits(hpr_id) == rules.hpr_id_number_digits(
            profile.hpr_id_number
        )
    return not profile.hpr_id or rules.normalise_hpr_address(hpr_id).lower() == profile.hpr_id.lower()


def _finish_login(user, hpr_id: str, row: AbdmOutboundRequest, method: str) -> AbdmHprProfile:
    token_data = rules.parse_token_response(row.response_json)
    if not token_data["token"]:
        raise HprError("NO_TOKEN", "The registry answered without a token.", row.request_id)
    profile, _ = AbdmHprProfile.objects.get_or_create(user=user)
    if (profile.hpr_id or profile.hpr_id_number) and not _same_identity(profile, hpr_id):
        # A second HPR ID on the same Care account: the docs give a person 1 HPID for a career.
        raise HprError(
            "OTHER_HPR_ID",
            f"This Care account is linked to {profile.hpr_id or profile.hpr_id_number}. Unlink it first.",
        )
    _store_token(profile, token_data, method)
    if rules.hpr_id_kind(hpr_id) == "number":
        profile.hpr_id_number = profile.hpr_id_number or rules.format_hpr_id_number(hpr_id)
    else:
        profile.hpr_id = profile.hpr_id or rules.normalise_hpr_address(hpr_id)
    profile.source = profile.source or profile.Source.LOGIN
    _fill_from_account(profile)
    profile.verified_at = timezone.now()
    profile.save()
    return profile


# --- login (registries/nhpr/hpr §Getting an HPR token later) --------------------------------------


def login_password(user, hpr_id: str, password: str) -> AbdmHprProfile:
    if not rules.hpr_id_kind(hpr_id):
        raise HprError("FIX_REQUEST", "Enter the HPR ID as name@hpr.abdm or as the 14-digit number.")
    if not password:
        raise HprError("FIX_REQUEST", "Enter the password.")
    try:
        row = client.ok(client.login_password(hpr_id, password))
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    return _finish_login(user, hpr_id, row, "password")


def login_init(user, hpr_id: str, method: str) -> AbdmHprLogin:
    if not rules.hpr_id_kind(hpr_id):
        raise HprError("FIX_REQUEST", "Enter the HPR ID as name@hpr.abdm or as the 14-digit number.")
    if method != "aadhaar_otp":
        raise HprError(
            "FIX_REQUEST",
            "Log in with the password or with an Aadhaar OTP. The registry publishes no mobile OTP verify call.",
        )
    try:
        row = client.ok(client.login_init(hpr_id, "AADHAAR_OTP"))
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    data = rules.parse_login_init(row.response_json)
    if not data["txn_id"]:
        raise HprError("NO_TXN", "The registry answered without a transaction id.", row.request_id)
    return AbdmHprLogin.objects.create(
        user=user,
        hpr_id=rules.normalise_hpr_address(hpr_id),
        auth_method="AADHAAR_OTP",
        txn_id=data["txn_id"],
        mobile_masked=data["mobile_masked"],
    )


def login_verify(user, login: AbdmHprLogin, otp: str) -> AbdmHprProfile:
    if login.status != login.Status.OTP_SENT:
        raise HprError("FIX_REQUEST", "This login is finished. Start again.")
    if login.attempts >= MAX_OTP_ATTEMPTS:
        login.status = login.Status.FAILED
        login.save(update_fields=["status", "modified_date"])
        raise HprError("FIX_REQUEST", "Too many attempts. Start again.")
    login.attempts += 1
    try:
        row = client.ok(client.login_confirm_aadhaar_otp(login.txn_id, otp))
    except client.NhprError as exc:
        error = _raise_from(exc)
        login.error_code = error.code[:64]
        login.error_message = error.message[:512]
        login.save()
        raise error from exc
    profile = _finish_login(user, login.hpr_id, row, "aadhaar_otp")
    login.status = login.Status.VERIFIED
    login.save()
    return profile


def logout(user) -> None:
    profile = profile_for(user)
    if profile is None:
        return
    if profile.token:
        client.logout(profile.token)  # best effort; the row records the answer
    profile.token = ""
    profile.token_expires_at = None
    profile.refresh_token = ""
    profile.refresh_expires_at = None
    profile.save()


def unlink(user) -> None:
    logout(user)
    AbdmHprProfile.objects.filter(user=user).delete()
    AbdmHprLogin.objects.filter(user=user).delete()
    AbdmHpidTransaction.objects.filter(user=user).exclude(status=AbdmHpidTransaction.Status.CREATED).delete()


def verify_hpr_id(hpr_id: str) -> dict:
    """`searchByHprId`: the public record behind an id, for the desk to confirm before a login."""
    if not rules.hpr_id_kind(hpr_id):
        raise HprError("FIX_REQUEST", "Enter the HPR ID as name@hpr.abdm or as the 14-digit number.")
    try:
        row = client.ok(client.search_hpr_id(rules.normalise_hpr_address(hpr_id)))
    except client.NhprError as exc:
        if _is_not_found(exc):
            raise HprError("NOT_FOUND", "The HPR holds no professional with this ID.") from exc
        raise _raise_from(exc) from exc
    return rules.parse_hpr_search(row.response_json)


# --- journey 1: create an HPID -------------------------------------------------------------------


def current_transaction(user) -> AbdmHpidTransaction | None:
    return (
        AbdmHpidTransaction.objects.filter(user=user)
        .exclude(status__in=[AbdmHpidTransaction.Status.CREATED, AbdmHpidTransaction.Status.FAILED])
        .order_by("-created_date")
        .first()
    )


def _advance(txn: AbdmHpidTransaction, row: AbdmOutboundRequest) -> None:
    """Carry the transaction id forward when a step's answer rotates it (findings N30).

    Every HPID step is keyed by `txnId`, and the sandbox hands back a **new** uuid instead of the
    one sent. Keeping the old one makes the next step fail with `HIS-1026 "Transaction is not found
    for UUID"`. The field is only overwritten when the answer actually names one; the caller saves.
    Recorded as findings N32.
    """
    txn_id = rules.next_txn_id(row.response_json)
    if txn_id and txn_id != txn.txn_id:
        logger.info("abdm: HPID transaction rotated %s -> %s (%s)", txn.txn_id, txn_id, row.operation_id)
        txn.txn_id = txn_id[:128]


def _txn_fail(txn: AbdmHpidTransaction, exc: client.NhprError) -> HprError:
    error = _raise_from(exc)
    txn.error_code = error.code[:64]
    txn.error_message = error.message[:512]
    txn.last_request = exc.row
    txn.save()
    return error


def hpid_start(user) -> AbdmHpidTransaction:
    """`aadhaar/generateLink`: the person completes the Aadhaar OTP on the NHPR page the URL opens."""
    if profile_for(user) and profile_for(user).hpr_id:
        raise HprError("OTHER_HPR_ID", "This Care account already has an HPR ID.")
    try:
        row = client.ok(client.aadhaar_generate_link())
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    data = rules.parse_aadhaar_link(row.response_json)
    if not data["txn_id"]:
        raise HprError("NO_TXN", "The registry answered without a transaction id.", row.request_id)
    AbdmHpidTransaction.objects.filter(user=user, status=AbdmHpidTransaction.Status.LINK_CREATED).update(
        status=AbdmHpidTransaction.Status.FAILED, error_code="SUPERSEDED"
    )
    return AbdmHpidTransaction.objects.create(
        user=user,
        txn_id=data["txn_id"][:128],
        aadhaar_url=data["url"][:1024],
        link_expires_at=timezone.now() + timezone.timedelta(seconds=rules.AADHAAR_LINK_VALIDITY_SECONDS),
        mobile_masked=data["mobile_masked"][:32],
        last_request=row,
    )


def hpid_poll(user, txn: AbdmHpidTransaction) -> AbdmHpidTransaction:
    """`isAuthenticated`; when true, `verifyOTP` (the demographics) and `checkHpIdAccountExist`."""
    if txn.status != txn.Status.LINK_CREATED:
        return txn
    try:
        row = client.ok(client.aadhaar_is_authenticated(txn.txn_id))
        if not rules.parse_boolean(row.response_json):
            txn.last_request = row
            txn.save(update_fields=["last_request", "modified_date"])
            return txn
        _advance(txn, row)
        details_row = client.ok(client.aadhaar_verify_otp(txn.txn_id))
        parsed = rules.parse_aadhaar_details(details_row.response_json)
        txn.details = parsed["details"]
        txn.photo = parsed["photo"]
        txn.mobile_masked = str(parsed["details"].get("mobileNumber") or txn.mobile_masked)[:32]
        _advance(txn, details_row)
        exists_row = client.ok(client.check_account_exists(txn.txn_id))
    except client.NhprError as exc:
        raise _txn_fail(txn, exc) from exc
    existing = rules.parse_account_exists(exists_row.response_json)
    _advance(txn, exists_row)
    txn.last_request = exists_row
    if existing["exists"]:
        # The person already holds an HPID: link it, do not create a second (skill: "let the answer pick the path").
        token = existing.pop("token", "")
        txn.existing = existing
        txn.hpr_id = existing["hpr_id"][:128]
        txn.hpr_id_number = rules.format_hpr_id_number(existing["hpr_id_number"])[:32]
        txn.status = txn.Status.ACCOUNT_EXISTS
        txn.photo = ""
        txn.save()
        profile, _ = AbdmHprProfile.objects.get_or_create(user=user)
        profile.hpr_id = txn.hpr_id or profile.hpr_id
        profile.hpr_id_number = txn.hpr_id_number or profile.hpr_id_number
        profile.name = (existing["name"] or profile.name)[:256]
        profile.category_code = (existing["category_id"] or profile.category_code)[:16]
        profile.sub_category_code = (existing["sub_category_id"] or profile.sub_category_code)[:16]
        profile.source = profile.Source.LOGIN
        if token:
            _store_token(
                profile,
                {"token": token, "expires_at": None, "refresh_token": "", "refresh_expires_at": None},
                "aadhaar_link",
            )
            _fill_from_account(profile)
        profile.verified_at = timezone.now()
        profile.save()
        return txn
    txn.status = txn.Status.AADHAAR_VERIFIED
    txn.save()
    return txn


def hpid_mobile(txn: AbdmHpidTransaction, mobile: str) -> AbdmHpidTransaction:
    """Mobile match first; an OTP only when it is false (registries/nhpr/hpr: "Call
    demographicAuthViaMobile first, and generate the mobile OTP only when it returns false")."""
    digits = "".join(ch for ch in (mobile or "") if ch.isdigit())[-10:]
    if len(digits) != 10:
        raise HprError("FIX_REQUEST", "Enter the 10-digit mobile number.")
    if txn.status != txn.Status.AADHAAR_VERIFIED:
        raise HprError("FIX_REQUEST", "Complete the Aadhaar step first.")
    try:
        row = client.ok(client.mobile_auth(txn.txn_id, digits))
        matched = rules.parse_mobile_auth(row.response_json)
        txn.mobile_masked = f"******{digits[-4:]}"
        _advance(txn, row)
        if matched["verified"]:
            txn.mobile_verified = True
            txn.status = txn.Status.MOBILE_VERIFIED
            txn.last_request = row
            txn.save()
            return txn
        otp_row = client.ok(client.mobile_otp_generate(txn.txn_id, digits))
    except client.NhprError as exc:
        raise _txn_fail(txn, exc) from exc
    _advance(txn, otp_row)
    txn.otp_sent_at = timezone.now()
    txn.last_request = otp_row
    txn.save()
    return txn


def hpid_mobile_verify(txn: AbdmHpidTransaction, otp: str) -> AbdmHpidTransaction:
    if txn.status != txn.Status.AADHAAR_VERIFIED or not txn.otp_sent_at:
        raise HprError("FIX_REQUEST", "Ask for the mobile OTP first.")
    if not (otp or "").isdigit():
        raise HprError("FIX_REQUEST", "Enter the OTP digits.")
    try:
        row = client.ok(client.mobile_otp_verify(txn.txn_id, otp))
    except client.NhprError as exc:
        raise _txn_fail(txn, exc) from exc
    _advance(txn, row)
    txn.mobile_verified = True
    txn.status = txn.Status.MOBILE_VERIFIED
    txn.last_request = row
    txn.save()
    return txn


def hpid_suggestions(txn: AbdmHpidTransaction) -> list[str]:
    if txn.status != txn.Status.MOBILE_VERIFIED:
        raise HprError("FIX_REQUEST", "Verify the mobile number first.")
    try:
        row = client.ok(client.hpid_suggestions(txn.txn_id))
    except client.NhprError as exc:
        raise _txn_fail(txn, exc) from exc
    _advance(txn, row)
    txn.suggestions = rules.parse_suggestions(row.response_json)[:20]
    txn.last_request = row
    txn.save()
    return txn.suggestions


def hpid_create(user, txn: AbdmHpidTransaction, params: dict) -> AbdmHprProfile:
    """`createHprIdWithPreVerified`; the names come from the Aadhaar details unless the desk edited them."""
    if txn.status != txn.Status.MOBILE_VERIFIED:
        raise HprError("FIX_REQUEST", "Verify the mobile number first.")
    first, middle, last = rules.split_name(str(txn.details.get("name") or ""))
    try:
        body = rules.create_hpid_body(
            txn_id=txn.txn_id,
            username=str(params.get("username") or ""),
            email=str(params.get("email") or txn.details.get("email") or ""),
            encrypted_password=client.encrypt(str(params.get("password") or "")) if params.get("password") else "",
            first_name=str(params.get("first_name") or first),
            middle_name=str(params.get("middle_name") or middle),
            last_name=str(params.get("last_name") or last),
            profile_photo_b64=str(params.get("profile_photo") or txn.photo or ""),
            category_code=int(params.get("category_code") or 0),
            sub_category_code=int(params.get("sub_category_code") or 0),
            state_code=str(params.get("state_code") or ""),
            district_code=str(params.get("district_code") or ""),
            role=int(params.get("role") or 1),
        )
    except (ValueError, TypeError) as exc:
        raise HprError("FIX_REQUEST", str(exc)) from exc
    if not body["password"]:
        raise HprError("FIX_REQUEST", "Choose a password.")
    if not body["email"]:
        raise HprError("FIX_REQUEST", "Enter an email address.")
    if not body["stateCode"] or not body["districtCode"]:
        raise HprError("FIX_REQUEST", "Pick the state and the district.")
    try:
        row = client.ok(client.create_hpid(body))
    except client.NhprError as exc:
        raise _txn_fail(txn, exc) from exc
    created = rules.parse_created_hpid(row.response_json)
    profile, _ = AbdmHprProfile.objects.get_or_create(user=user)
    profile.hpr_id = (created["hpr_id"] or f"{body['hprId']}{rules.HPR_DOMAIN}")[:128]
    profile.hpr_id_number = rules.format_hpr_id_number(created["hpr_id_number"])[:32]
    profile.name = (
        created["name"] or " ".join(p for p in (body["firstName"], body["middleName"], body["lastName"]) if p)
    )[:256]
    profile.category_code = str(body["hpCategoryCode"])
    profile.sub_category_code = str(body["hpSubCategoryCode"])
    profile.role = body["role"]
    profile.source = profile.Source.CREATED
    if created["token"]:
        _store_token(
            profile,
            {"token": created["token"], "expires_at": None, "refresh_token": "", "refresh_expires_at": None},
            "created",
        )
        _fill_from_account(profile)
    profile.verified_at = timezone.now()
    profile.save()
    txn.status = txn.Status.CREATED
    txn.hpr_id = profile.hpr_id
    txn.hpr_id_number = profile.hpr_id_number
    txn.photo = ""
    txn.last_request = row
    txn.save()
    return profile


def hpid_cancel(txn: AbdmHpidTransaction) -> None:
    txn.status = txn.Status.FAILED
    txn.error_code = "CANCELLED"
    txn.photo = ""
    txn.save()


# --- journey 2: register the professional --------------------------------------------------------


def _token(user) -> tuple[AbdmHprProfile, str]:
    profile = profile_for(user)
    if profile is None or not (profile.hpr_id or profile.hpr_id_number):
        raise HprError("NO_HPR_ID", "Link or create an HPR ID first.")
    if not profile.token_valid:
        raise HprError("NO_HPR_SESSION", "Log in with your HPR ID again. The registry token has expired.")
    return profile, profile.token


def register(user, practitioner: dict, update: bool = False) -> AbdmHprProfile:
    profile, token = _token(user)
    try:
        body = rules.register_professional_body(token, practitioner)
    except ValueError as exc:
        raise HprError("FIX_REQUEST", str(exc)) from exc
    try:
        row = client.ok(client.update_professional(body) if update else client.register_professional(body))
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    result = row.response_json if isinstance(row.response_json, dict) else {"result": row.response_json}
    profile.professional = {**(profile.professional or {}), "lastRegistration": _trim(result)}
    profile.registered_at = profile.registered_at or timezone.now()
    profile.save()
    return profile


def _trim(value, depth=0):
    """Drop base64 blobs from a stored answer."""
    if isinstance(value, dict):
        return {k: _trim(v, depth + 1) for k, v in value.items() if not (isinstance(v, str) and len(v) > 2000)}
    if isinstance(value, list):
        return [_trim(v, depth + 1) for v in value[:50]]
    return value


def documents(user) -> dict:
    profile, token = _token(user)
    # Observed 2026-09-21: `fetch-documents-list` with the address answered HTTP 422 HIS-3008
    # "Invalid HPID". The page sends `hprid: <HPR_ID>`; the 14 digits are tried first (findings N26).
    hpr_id = rules.hpr_id_number_digits(profile.hpr_id_number) or profile.hpr_id
    try:
        row = client.ok(client.fetch_documents_list(hpr_id, token))
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    data = row.response_json if isinstance(row.response_json, dict) else {}
    return _document_slots(data.get("documentList") if isinstance(data.get("documentList"), dict) else data)


def _document_slots(document_list: dict) -> dict:
    """`{documentList{profileDetails{...}, registrationDetails[...], qualificationDetails[...]}}` →
    the slot ids the upload call needs, without the bytes."""
    slots = []

    def walk(node, group):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, dict) and "id" in value:
                    slots.append(
                        {
                            "group": group,
                            "type": key,
                            "id": value.get("id"),
                            "hasData": bool(value.get("data")),
                            "system": value.get("systemOfMedicide") or value.get("systemOfMedicine") or "",
                        }
                    )
                else:
                    walk(value, key)
        elif isinstance(node, list):
            for item in node:
                walk(item, group)

    walk(document_list or {}, "")
    return {"slots": slots}


def upload(user, docs: list[dict]) -> dict:
    profile, token = _token(user)
    try:
        body = rules.upload_documents_body(token, docs)
    except ValueError as exc:
        raise HprError("FIX_REQUEST", str(exc)) from exc
    try:
        row = client.ok(client.upload_documents(body))
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    return row.response_json if isinstance(row.response_json, dict) else {"result": row.response_json}


def professional_info(user) -> dict:
    profile, token = _token(user)
    body = rules.professional_info_body(hpr_id=profile.hpr_id or profile.hpr_id_number, name=profile.name)
    try:
        row = client.ok(client.fetch_professional_info(body, token))
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    data = row.response_json if isinstance(row.response_json, dict) else {"result": row.response_json}
    profile.professional = {**(profile.professional or {}), "info": _trim(data)}
    profile.save(update_fields=["professional", "modified_date"])
    return profile.professional["info"]


# --- what the page reads; what M3 reads ----------------------------------------------------------


def requester_identifier(user) -> dict | None:
    """M3 `consent.requester.identifier` when the user holds an HPR ID (ADR-015): the 14 digits."""
    profile = profile_for(user)
    if profile is None or not (profile.hpr_id_number or profile.hpr_id):
        return None
    value = rules.hpr_id_number_digits(profile.hpr_id_number) or profile.hpr_id
    return {"value": value, "type": "HPR_ID", "system": "https://hpr.abdm.gov.in"}


def txn_summary(txn: AbdmHpidTransaction | None) -> dict | None:
    if txn is None:
        return None
    failure = None
    if txn.error_code and txn.error_code not in ("CANCELLED", "SUPERSEDED"):
        failure = errors.classify(
            code=txn.error_code,
            message=txn.error_message,
            request_id=txn.last_request.request_id if txn.last_request_id else "",
        ).as_dict()
        failure["detail"] = txn.error_message
    return {
        "id": str(txn.external_id),
        "status": txn.status,
        "aadhaarUrl": txn.aadhaar_url,
        "linkExpiresAt": txn.link_expires_at,
        "details": {k: v for k, v in (txn.details or {}).items() if k not in ("txnId",)},
        "mobileMasked": txn.mobile_masked,
        "mobileVerified": txn.mobile_verified,
        "otpSentAt": txn.otp_sent_at,
        "suggestions": txn.suggestions,
        "existing": txn.existing,
        "hprId": txn.hpr_id,
        "hprIdNumber": txn.hpr_id_number,
        "failure": failure,
    }


def hpr_state(user) -> dict:
    profile = profile_for(user, heal=True)
    login = (
        AbdmHprLogin.objects.filter(user=user, status=AbdmHprLogin.Status.OTP_SENT).order_by("-created_date").first()
    )
    return {
        "profile": {
            "hprId": profile.hpr_id,
            "hprIdNumber": profile.hpr_id_number,
            "name": profile.name,
            "categoryCode": profile.category_code,
            "subCategoryCode": profile.sub_category_code,
            "role": profile.role,
            "source": profile.source,
            "account": profile.account,
            "registeredAt": profile.registered_at,
            "verifiedAt": profile.verified_at,
            "professional": profile.professional,
        }
        if profile and (profile.hpr_id or profile.hpr_id_number)
        else None,
        "session": {
            "active": bool(profile and profile.token_valid),
            "expiresAt": profile.token_expires_at if profile else None,
            "method": profile.token_method if profile else "",
        },
        "pendingLogin": {
            "id": str(login.external_id),
            "hprId": login.hpr_id,
            "mobileMasked": login.mobile_masked,
            "attempts": login.attempts,
        }
        if login
        else None,
        "transaction": txn_summary(current_transaction(user)),
        "loginMethods": list(rules.LOGIN_METHODS),
        "roles": [{"code": code, "name": name} for code, name in rules.ROLES.items()],
        "careUser": {
            "username": getattr(user, "username", ""),
            "name": getattr(user, "full_name", "") or "",
            "councilRegistration": getattr(user, "doctor_medical_council_registration", "") or "",
        },
    }
