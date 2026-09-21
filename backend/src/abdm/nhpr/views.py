"""
Care-facing M4 endpoints (ADR-015).

Facility side: gated on `can_update_facility_obj`, like the setup page. User side: the caller acts on
their own Care account (`users/me/...`); the HPR token never leaves the server. Masters: any
authenticated user, cached 24 h.
"""

from care.facility.models import Facility
from care.security.authorization import AuthorizationController
from django.shortcuts import get_object_or_404
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.models import AbdmHprLogin
from abdm.nhpr import client
from abdm.nhpr import facility as hfr
from abdm.nhpr import professional as hpr


def _facility(request, facility_id) -> Facility:
    facility = get_object_or_404(Facility, external_id=facility_id)
    if not AuthorizationController.call("can_update_facility_obj", request.user, facility):
        raise PermissionDenied("You do not have permission to update this facility.")
    return facility


def _parse(model, data):
    try:
        return model.model_validate(data or {})
    except PydanticValidationError as exc:
        raise ValidationError({"errors": "; ".join(e["msg"] for e in exc.errors())}) from exc


# Codes the plug decides before or without a registry call. Everything else is a registry refusal.
LOCAL_CODES = {"FIX_REQUEST", "NO_HPR_SESSION", "NO_HPR_ID", "OTHER_HPR_ID", "ALREADY_LINKED"}


def refused(exc) -> Response:
    """The failure answer, returned and never raised. DRF's exception handler calls `set_rollback()`
    under Care's `ATOMIC_REQUESTS`, so a raised error after a registry call drops the
    `AbdmOutboundRequest` row of that call (observed 2026-09-21: the log held the REQUEST-ID of an
    HTTP 422, the table held no row; findings J9). The body is `{errors, detail, code, requestId}`."""
    if exc.code == "NOT_FOUND":
        return Response(exc.as_dict(), status=404)
    return Response(exc.as_dict(), status=400 if exc.code in LOCAL_CODES else 502)


# --- facility side ---------------------------------------------------------------------------------


class HfrLookup(APIView):
    """GET ?facility_id=IN...: the registry record, or 404."""

    permission_classes = [IsAuthenticated]

    def get(self, request, facility_id):
        _facility(request, facility_id)
        try:
            record = hfr.lookup(str(request.query_params.get("facility_id") or ""))
        except hfr.HfrError as exc:
            return refused(exc)
        if record is None:
            return Response({"errors": "The HFR holds no facility with this ID."}, status=404)
        return Response(record)


def search_from_query(q) -> dict:
    """`?name=&state=&ownership=&district=&page=`: fuzzy on the name, exact on the codes. The state
    and the ownership are required by the registry (facility.search refuses without them)."""
    try:
        page = int(q.get("page") or 1)
    except ValueError:
        page = 1
    return hfr.search(
        name=str(q.get("name") or ""),
        state_lgd=str(q.get("state") or ""),
        district_lgd=str(q.get("district") or ""),
        ownership=str(q.get("ownership") or ""),
        page=page,
    )


class HfrSearch(APIView):
    """GET ?name=&state=&ownership=&district=&page=: the registry search for this facility's card."""

    permission_classes = [IsAuthenticated]

    def get(self, request, facility_id):
        _facility(request, facility_id)
        try:
            return Response(search_from_query(request.query_params))
        except hfr.HfrError as exc:
            return refused(exc)


class LinkBody(BaseModel):
    facility_id: str


class HfrLink(APIView):
    """POST {facility_id}: store the registry id and name on this Care facility."""

    permission_classes = [IsAuthenticated]

    def post(self, request, facility_id):
        facility = _facility(request, facility_id)
        body = _parse(LinkBody, request.data)
        try:
            return Response(hfr.link_registry_facility(facility, body.facility_id, request.user))
        except hfr.HfrError as exc:
            return refused(exc)


class OnboardingBody(BaseModel):
    step: str
    payload: dict = {}


class HfrOnboarding(APIView):
    """GET the wizard state; POST {step, payload} runs 1 onboarding call."""

    permission_classes = [IsAuthenticated]

    def get(self, request, facility_id):
        facility = _facility(request, facility_id)
        return Response(hfr.hfr_state(facility, request.user))

    def post(self, request, facility_id):
        facility = _facility(request, facility_id)
        body = _parse(OnboardingBody, request.data)
        onboarding = hfr.start_onboarding(facility, request.user)
        try:
            hfr.run_step(facility, onboarding, body.step, body.payload, request.user)
        except hfr.HfrError as exc:
            state = hfr.hfr_state(facility, request.user)
            state.update(exc.as_dict())
            return Response(state, status=400 if exc.code in LOCAL_CODES else 502)
        return Response(hfr.hfr_state(facility, request.user))


class OtpBody(BaseModel):
    action: str
    facility_id: str
    transaction_id: str = ""
    otp: str = ""
    source: str = ""
    source_id: str = ""


class HfrOtp(APIView):
    """POST {action: send|validate, ...}: the OTP to the contact registered against a facility."""

    permission_classes = [IsAuthenticated]

    def post(self, request, facility_id):
        facility = _facility(request, facility_id)
        body = _parse(OtpBody, request.data)
        try:
            if body.action == "send":
                return Response(hfr.send_facility_otp(facility, body.facility_id))
            if body.action == "validate":
                return Response(
                    hfr.validate_facility_otp(
                        facility,
                        facility_id=body.facility_id,
                        transaction_id=body.transaction_id,
                        otp=body.otp,
                        source=body.source,
                        source_id=body.source_id,
                    )
                )
        except hfr.HfrError as exc:
            return refused(exc)
        raise ValidationError({"errors": "action must be send or validate."})


# --- user side -------------------------------------------------------------------------------------


class HprState(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(hpr.hpr_state(request.user))


class HprLoginBody(BaseModel):
    method: str = "password"
    hpr_id: str
    password: str = ""


class HprLogin(APIView):
    """POST {method, hpr_id, password?}: password logs in at once; aadhaar_otp sends the OTP."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        body = _parse(HprLoginBody, request.data)
        try:
            if body.method == "password":
                hpr.login_password(request.user, body.hpr_id, body.password)
            else:
                hpr.login_init(request.user, body.hpr_id, body.method)
        except hpr.HprError as exc:
            return refused(exc)
        return Response(hpr.hpr_state(request.user))


class HprVerifyBody(BaseModel):
    login_id: str
    otp: str


class HprLoginVerify(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        body = _parse(HprVerifyBody, request.data)
        login = get_object_or_404(AbdmHprLogin, external_id=body.login_id, user=request.user)
        try:
            hpr.login_verify(request.user, login, body.otp)
        except hpr.HprError as exc:
            return refused(exc)
        return Response(hpr.hpr_state(request.user))


class HprVerifyId(APIView):
    """GET ?hpr_id=: the public record behind an HPR ID (`searchByHprId`)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(hpr.verify_hpr_id(str(request.query_params.get("hpr_id") or "")))
        except hpr.HprError as exc:
            return refused(exc)


class HprSessionAction(APIView):
    """POST logout | unlink."""

    permission_classes = [IsAuthenticated]

    def post(self, request, action):
        if action == "logout":
            hpr.logout(request.user)
        elif action == "unlink":
            hpr.unlink(request.user)
        else:
            raise ValidationError({"errors": "action must be logout or unlink."})
        return Response(hpr.hpr_state(request.user))


class HpidBody(BaseModel):
    mobile: str = ""
    otp: str = ""
    username: str = ""
    email: str = ""
    password: str = ""
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    profile_photo: str = ""
    category_code: int | str = ""
    sub_category_code: int | str = ""
    state_code: str = ""
    district_code: str = ""
    role: int = 1


class HpidCreate(APIView):
    """POST create/<action>: start | poll | mobile | mobile-verify | suggestions | finish | cancel."""

    permission_classes = [IsAuthenticated]

    def post(self, request, action):
        body = _parse(HpidBody, request.data)
        txn = hpr.current_transaction(request.user)
        try:
            if action == "start":
                hpr.hpid_start(request.user)
            else:
                if txn is None:
                    raise hpr.HprError("FIX_REQUEST", "No HPID creation in progress. Start one.")
                if action == "poll":
                    hpr.hpid_poll(request.user, txn)
                elif action == "mobile":
                    hpr.hpid_mobile(txn, body.mobile)
                elif action == "mobile-verify":
                    hpr.hpid_mobile_verify(txn, body.otp)
                elif action == "suggestions":
                    hpr.hpid_suggestions(txn)
                elif action == "finish":
                    hpr.hpid_create(request.user, txn, body.model_dump())
                elif action == "cancel":
                    hpr.hpid_cancel(txn)
                else:
                    raise ValidationError({"errors": "Unknown action."})
        except hpr.HprError as exc:
            state = hpr.hpr_state(request.user)
            state.update(exc.as_dict())
            return Response(state, status=400 if exc.code in LOCAL_CODES else 502)
        return Response(hpr.hpr_state(request.user))


class RegisterBody(BaseModel):
    practitioner: dict


class HprRegister(APIView):
    """POST register (new) or register/update with the full practitioner block."""

    permission_classes = [IsAuthenticated]

    def post(self, request, action=""):
        body = _parse(RegisterBody, request.data)
        try:
            hpr.register(request.user, body.practitioner, update=(action == "update"))
        except hpr.HprError as exc:
            return refused(exc)
        return Response(hpr.hpr_state(request.user))


class DocumentsBody(BaseModel):
    documents: list[dict]


class HprDocuments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(hpr.documents(request.user))
        except hpr.HprError as exc:
            return refused(exc)

    def post(self, request):
        body = _parse(DocumentsBody, request.data)
        try:
            return Response(hpr.upload(request.user, body.documents))
        except hpr.HprError as exc:
            return refused(exc)


class HprProfessionalInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(hpr.professional_info(request.user))
        except hpr.HprError as exc:
            return refused(exc)


# --- masters ---------------------------------------------------------------------------------------


class Masters(APIView):
    """GET nhpr/masters/<kind>?...: 1 code list from the NHPR, normalised to [{code, name, children?}]."""

    permission_classes = [IsAuthenticated]

    def get(self, request, kind):
        try:
            rows = client.masters(kind, dict(request.query_params.items()))
        except ValueError as exc:
            raise ValidationError({"errors": str(exc)}) from exc
        except client.NhprError as exc:
            return Response({"errors": str(exc), "code": exc.code, "requestId": exc.request_id}, status=502)
        return Response({"results": rows})
