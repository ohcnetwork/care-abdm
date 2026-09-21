"""
M4 for a Care facility (ADR-015): find a registry facility and link it, and onboard a new facility
to the HFR (journey 3) with the manager's HPR token.

registries/nhpr/hfr: the 5 onboarding calls run in a fixed order; a facility not submitted stays in
Draft and "goes nowhere"; the `IN` facility id is known after submission. Basic information and submit
take the person's HPR token in `x-hprid-auth`.

State (ADR-016): the link and the onboarding live in `Facility.extensions["abdm"]` (`hfr`,
`hfr_onboarding`), not in a table. Every registry call is already logged in AbdmOutboundRequest.
"""

import logging

from django.utils import timezone

from abdm import errors
from abdm.facility import service as facility_service
from abdm.models import AbdmHprProfile, AbdmOutboundRequest
from abdm.nhpr import client, rules

logger = logging.getLogger(__name__)


class HfrError(Exception):
    def __init__(self, code: str, message: str, request_id: str = "", details: list[str] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.request_id = request_id
        # The registry's own words, 1 line per `details[]` entry ("Required OwnershipCode Field is
        # empty."). The person on the setup page is an administrator, so the API carries them beside
        # the plug sentence (abdm-m3 design.md: never replace the message ABDM sent with your own).
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


def _raise_from(exc: client.NhprError, code: str = "") -> HfrError:
    """A refused registry call. The message carries the registry's own words when it sent any;
    the classified sentence covers a transport failure or an empty answer."""
    failure = errors.classify(
        code=exc.code, http_status=exc.row.http_status if exc.row else None, message=str(exc), request_id=exc.request_id
    )
    lines = client.refusal_lines(exc.row)
    message = f"{REFUSED} {' '.join(lines)}" if lines else f"{failure.what} {failure.next_step}".strip()
    return HfrError(code or failure.code, message, exc.request_id, lines)


# --- tier A: lookup, search, link ---------------------------------------------------------------


def lookup(facility_id: str) -> dict | None:
    """The registry record behind 1 `IN` facility id, or None."""
    value = (facility_id or "").strip().upper()
    if not rules.facility_id_ok(value):
        raise HfrError("FIX_REQUEST", "HFR facility ID must start with IN and have 12 characters.")
    try:
        row = client.ok(client.search_facilities(facility_id=value, per_page=5))
    except client.NhprError as exc:
        if exc.row is not None and exc.row.http_status == 404:
            return None
        raise _raise_from(exc) from exc
    result = rules.parse_facility_search(row.response_json)
    for item in result["facilities"]:
        if item["facilityId"].upper() == value:
            return item
    return result["facilities"][0] if len(result["facilities"]) == 1 else None


def search(*, name: str, state_lgd: str = "", district_lgd: str = "", ownership: str = "", page: int = 1) -> dict:
    """A name search. The registry refuses one without a state and an ownership (HTTP 422, HIS-1070,
    observed 2026-09-21), so the plug refuses it first and names the missing value."""
    if len((name or "").strip()) < 3:
        raise HfrError("FIX_REQUEST", "Type at least 3 characters of the facility name.")
    if not (state_lgd or "").strip():
        raise HfrError("FIX_REQUEST", "Choose the state. The registry needs it for a name search.")
    if not (ownership or "").strip():
        raise HfrError("FIX_REQUEST", "Choose the ownership. The registry needs it for a name search.")
    try:
        row = client.ok(
            client.search_facilities(
                name=name.strip(),
                state_lgd=state_lgd.strip(),
                district_lgd=(district_lgd or "").strip(),
                ownership=ownership.strip(),
                page=page,
                per_page=10,
            )
        )
    except client.NhprError as exc:
        if exc.row is not None and exc.row.http_status == 404:
            return {"facilities": [], "message": "", "total": 0, "pages": 0}
        raise _raise_from(exc) from exc
    return rules.parse_facility_search(row.response_json)


def link_record(facility, record: dict, user=None) -> dict:
    """Store a registry record on the Care facility (id, registered name, the record itself), so the
    HRP linkage sends the exact HFR name (the 2026-09-14 name-mismatch refusal)."""
    try:
        facility_service.set_registry_link(facility, record, user)
    except ValueError as exc:
        raise HfrError("FIX_REQUEST", str(exc)) from exc
    facility_service.sync_hip_id(facility)
    return {"config": facility_service.get_config(facility), "registry": record}


def link_registry_facility(facility, facility_id: str, user=None) -> dict:
    """Look 1 `IN` id up in the registry and link the record it names."""
    record = lookup(facility_id)
    if record is None:
        raise HfrError("NOT_FOUND", "The HFR holds no facility with this ID.")
    return link_record(facility, record, user)


def send_facility_otp(facility, facility_id: str) -> dict:
    try:
        row = client.ok(client.facility_otp_send(facility_id, facility=facility))
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    data = row.response_json if isinstance(row.response_json, dict) else {}
    return {
        "transactionId": str(data.get("transactionId") or ""),
        "message": str(data.get("message") or ""),
        "status": str(data.get("status") or ""),
    }


def validate_facility_otp(
    facility, *, facility_id: str, transaction_id: str, otp: str, source: str, source_id: str
) -> dict:
    body = rules.facility_otp_validate_body(facility_id, transaction_id, otp, source, source_id)
    try:
        row = client.ok(client.facility_otp_validate(body, facility=facility))
    except client.NhprError as exc:
        raise _raise_from(exc) from exc
    data = row.response_json if isinstance(row.response_json, dict) else {}
    return {"message": str(data.get("message") or ""), "status": str(data.get("status") or "")}


# --- journey 3: onboarding ---------------------------------------------------------------------


def hpr_token_for(user) -> tuple[AbdmHprProfile, str]:
    profile = AbdmHprProfile.objects.filter(user=user).first()
    if profile is None or not profile.token_valid:
        raise HfrError(
            "NO_HPR_SESSION", "Log in with your HPR ID first. The registry needs a facility manager's token."
        )
    return profile, profile.token


OPEN_STATUSES = ("draft", "basic_saved", "additional_saved", "detailed_saved")
NEXT_STEP = {
    "draft": "basic",
    "basic_saved": "additional",
    "additional_saved": "detailed",
    "detailed_saved": "submit",
    "submitted": "submit",
}


def current_onboarding(facility) -> dict | None:
    state = facility_service.get_onboarding(facility)
    return state or None


def start_onboarding(facility, user) -> dict:
    """The unfinished onboarding, or a fresh draft. A submitted one is replaced: the facility is
    linked by then, and the registry keeps the record."""
    current = current_onboarding(facility)
    if current and current.get("status") in OPEN_STATUSES:
        return current
    state = {
        "status": "draft",
        "tracking_id": "",
        "facility_id": "",
        "dedup_results": [],
        "basic": {},
        "additional": {},
        "detailed": {},
        "submit": {},
        "last_message": "",
        "submitted_at": None,
        "started_at": timezone.now().isoformat(),
        "started_by": str(getattr(user, "username", "") or ""),
        "hpr_id": "",
        "error_code": "",
        "error_message": "",
        "last_request_id": "",
    }
    return facility_service.save_onboarding(facility, state)


def _record(state: dict, row: AbdmOutboundRequest | None, result: dict | None = None) -> None:
    state["last_request_id"] = row.request_id if row is not None else ""
    if result:
        state["last_message"] = (result.get("message") or "")[:512]
        if result.get("error"):
            state["error_code"] = "HFR_ERROR"
            state["error_message"] = result["error"][:512]


def _fail(facility, state: dict, exc: client.NhprError) -> HfrError:
    error = _raise_from(exc)
    state["error_code"] = error.code[:64]
    state["error_message"] = error.message[:1024]
    state["error_details"] = [line[:512] for line in error.details[:10]]
    state["last_request_id"] = exc.row.request_id if exc.row is not None else exc.request_id
    facility_service.save_onboarding(facility, state)
    return error


def run_step(facility, state: dict, step: str, payload: dict, user) -> dict:
    """1 onboarding call. `payload` is the documented body of the step, minus `trackingId`.
    The state is saved after every call, so a closed tab loses nothing."""
    if step not in rules.ONBOARDING_STEPS:
        raise HfrError("FIX_REQUEST", f"Step must be 1 of {', '.join(rules.ONBOARDING_STEPS)}.")
    payload = payload if isinstance(payload, dict) else {}
    state["error_code"] = ""
    state["error_message"] = ""
    state["error_details"] = []
    try:
        if step == "dedup":
            body = rules.dedup_body(
                name=str(payload.get("name") or facility.name),
                address=str(payload.get("address") or facility.address or ""),
                district_lgd=str(payload.get("district") or ""),
                sub_district_lgd=str(payload.get("subDistrict") or ""),
                village_lgd=str(payload.get("village") or ""),
                facility_id=str(payload.get("facilityId") or ""),
            )
            row = client.ok(client.dedup_search(body, facility=facility))
            results = row.response_json if isinstance(row.response_json, list) else []
            state["dedup_results"] = [r for r in results if isinstance(r, dict)][:20]
            _record(state, row)
            return facility_service.save_onboarding(facility, state)
        profile, token = hpr_token_for(user)
        state["hpr_id"] = profile.hpr_id
        if step == "basic":
            info = (
                payload.get("facilityInformation") if isinstance(payload.get("facilityInformation"), dict) else payload
            )
            body = rules.basic_information_body(info, state.get("tracking_id") or "")
            row = client.ok(client.basic_information(body, token, facility=facility))
            result = rules.parse_onboarding_result(row.response_json)
            if not result["tracking_id"] and not state.get("tracking_id"):
                raise HfrError(
                    "NO_TRACKING_ID", "The registry saved nothing: no tracking id came back.", row.request_id
                )
            state["tracking_id"] = (result["tracking_id"] or state.get("tracking_id") or "")[:64]
            state["basic"] = rules.strip_photos(info)
            state["status"] = "basic_saved"
            _record(state, row, result)
            return facility_service.save_onboarding(facility, state)
        if step == "additional":
            body = rules.additional_information_body(payload, state["tracking_id"])
            row = client.ok(client.additional_information(body, token, facility=facility))
            state["additional"] = {k: v for k, v in body.items() if k != "trackingId"}
            state["status"] = "additional_saved"
            _record(state, row, rules.parse_onboarding_result(row.response_json))
            return facility_service.save_onboarding(facility, state)
        if step == "detailed":
            body = rules.detailed_information_body(payload, state["tracking_id"])
            row = client.ok(client.detailed_information(body, token, facility=facility))
            state["detailed"] = {k: v for k, v in body.items() if k != "trackingId"}
            state["status"] = "detailed_saved"
            _record(state, row, rules.parse_onboarding_result(row.response_json))
            return facility_service.save_onboarding(facility, state)
        body = rules.submit_body(payload, state["tracking_id"])
        row = client.ok(client.submit_facility(body, token, facility=facility))
        result = rules.parse_onboarding_result(row.response_json)
        state["submit"] = {k: v for k, v in body.items() if k != "trackingId"}
        state["status"] = "submitted"
        state["submitted_at"] = timezone.now().isoformat()
        state["facility_id"] = (result["facility_id"] or _find_submitted_facility_id(state))[:32]
        _record(state, row, result)
        facility_service.save_onboarding(facility, state)
        if state["facility_id"]:
            try:
                link_registry_facility(facility, state["facility_id"], user)
            except HfrError as exc:
                logger.warning("abdm: submitted facility %s not linkable yet: %s", state["facility_id"], exc)
        return facility_service.get_onboarding(facility)
    except ValueError as exc:
        raise HfrError("FIX_REQUEST", str(exc)) from exc
    except client.NhprError as exc:
        raise _fail(facility, state, exc) from exc


def _find_submitted_facility_id(state: dict) -> str:
    """The submit answer may carry no `IN` id (the pages show none). Search the HFR by the name,
    state and ownership we sent; take the 1 match whose status is not Draft."""
    basic = state.get("basic") if isinstance(state.get("basic"), dict) else {}
    name = str(basic.get("facilityName") or "")
    address = basic.get("facilityAddressDetails") if isinstance(basic.get("facilityAddressDetails"), dict) else {}
    region = str(address.get("stateLGDCode") or "")
    ownership = str(basic.get("ownershipCode") or "")
    if not name:
        return ""
    try:
        found = search(name=name, state_lgd=region, ownership=ownership)
    except HfrError:
        return ""
    matches = [
        f for f in found["facilities"] if f["facilityName"].strip().lower() == name.strip().lower() and f["facilityId"]
    ]
    return matches[0]["facilityId"] if len(matches) == 1 else ""


def onboarding_summary(state: dict | None) -> dict | None:
    if not state:
        return None
    failure = None
    if state.get("error_code"):
        failure = errors.classify(
            code=str(state.get("error_code") or ""),
            message=str(state.get("error_message") or ""),
            request_id=str(state.get("last_request_id") or ""),
        ).as_dict()
        failure["detail"] = str(state.get("error_message") or "")
        # The registry's lines, for the wizard's failure notice (1 bullet each).
        failure["details"] = [str(line) for line in (state.get("error_details") or []) if line]
    status = str(state.get("status") or "draft")
    return {
        "status": status,
        "nextStep": NEXT_STEP.get(status, "basic"),
        "trackingId": str(state.get("tracking_id") or ""),
        "facilityId": str(state.get("facility_id") or ""),
        "dedupResults": state.get("dedup_results") or [],
        "basic": state.get("basic") or {},
        "additional": state.get("additional") or {},
        "detailed": state.get("detailed") or {},
        "submit": state.get("submit") or {},
        "lastMessage": str(state.get("last_message") or ""),
        "submittedAt": state.get("submitted_at"),
        "createdAt": state.get("started_at"),
        "startedBy": str(state.get("started_by") or ""),
        "hprId": str(state.get("hpr_id") or ""),
        "failure": failure,
    }


def hfr_state(facility, user) -> dict:
    """What the setup page's HFR card and the wizard read."""
    from abdm.nhpr.professional import profile_for

    profile = profile_for(user, heal=True)
    return {
        "config": facility_service.get_config(facility),
        "onboarding": onboarding_summary(current_onboarding(facility)),
        "hprSession": {
            "hprId": (profile.hpr_id or profile.hpr_id_number) if profile else "",
            "name": profile.name if profile else "",
            "active": bool(profile and profile.token_valid),
            "expiresAt": profile.token_expires_at if profile else None,
            "role": profile.role if profile else None,
        },
        "prefill": {
            "facilityName": facility.name,
            "address": facility.address or "",
            "pincode": str(facility.pincode or ""),
            "phone": facility.phone_number or "",
            # 1 to 6 decimal places, because Care holds 16 (HIS-4019, HIS-4020).
            "latitude": rules.coordinate(facility.latitude, "latitude"),
            "longitude": rules.coordinate(facility.longitude, "longitude"),
        },
    }
