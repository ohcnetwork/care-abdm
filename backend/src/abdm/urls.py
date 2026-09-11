from django.http import JsonResponse
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from abdm.abha import views as abha
from abdm.callbacks import views as callbacks
from abdm.facility import views as facility_views
from abdm.gateway.session import GatewaySessionError, get_access_token


def healthy(request):
    return JsonResponse({"status": "ok", "plug": "abdm"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def gateway_status(request):
    """Dev/ops probe: can this deployment obtain a gateway session? Token is never returned."""
    try:
        token = get_access_token()
    except GatewaySessionError as e:
        return JsonResponse({"ok": False, "status_code": e.status_code, "request_id": e.request_id}, status=502)
    return JsonResponse({"ok": True, "token_prefix": token[:8]})


def callback_route(route):
    return path(route, callbacks.GenericCallbackView.as_view(), {"path": route})


urlpatterns = [
    path("health", healthy),
    path("gateway/status", gateway_status),
    # M2 step 1 — ADR-007 facility and bridge proof.
    path("facilities/<uuid:facility_id>/abdm", facility_views.FacilityAbdmConfig.as_view()),
    path("facilities/<uuid:facility_id>/abdm/bridge-url", facility_views.FacilityBridgeUrl.as_view()),
    path("facilities/<uuid:facility_id>/abdm/hrp-services", facility_views.FacilityHrpServices.as_view()),
    # M2 step 2 — callback log and probe.
    path("callbacks", callbacks.CallbackList.as_view()),
    path("callbacks/<uuid:callback_id>", callbacks.CallbackDetail.as_view()),
    callback_route("v3/hip/token/on-generate-token"),
    callback_route("v3/link/on_carecontext"),
    callback_route("v3/links/context/on-notify"),
    callback_route("v3/patients/sms/on-notify"),
    callback_route("api/v3/hip/patient/care-context/discover"),
    callback_route("v0.5/care-contexts/discover"),
    callback_route("api/v3/hip/link/care-context/init"),
    callback_route("v0.5/links/link/init"),
    callback_route("api/v3/hip/link/care-context/confirm"),
    callback_route("v0.5/links/link/confirm"),
    callback_route("v0.5/consents/hip/notify"),
    callback_route("api/v3/hip/health-information/request"),
    callback_route("v0.5/health-information/hip/request"),
    # M1 Journey 1 — ABHA creation by Aadhaar OTP
    path("abha/enrol/aadhaar/request-otp", abha.RequestAadhaarOtp.as_view()),
    path("abha/enrol/aadhaar/verify", abha.EnrolByAadhaar.as_view()),
    path("abha/enrol/mobile/request-otp", abha.RequestMobileOtp.as_view()),
    path("abha/enrol/mobile/verify", abha.VerifyMobileOtp.as_view()),
    path("abha/enrol/address/suggestions", abha.AddressSuggestions.as_view()),
    path("abha/enrol/address/claim", abha.ClaimAbhaAddress.as_view()),
    # M1 — login to an existing ABHA. One entry point; body.hint ∈ mobile|abha-number|abha-address|aadhaar.
    path("abha/login/request-otp", abha.LoginRequestOtp.as_view()),
    path("abha/login/verify", abha.LoginVerifyOtp.as_view()),
    path("abha/login/select-account", abha.LoginSelectAccount.as_view()),
    # Completed transaction read-back (registration prefill after find-by-ABHA)
    path("abha/transactions/<str:txn_id>", abha.TransactionDetail.as_view()),
    # Patient-scoped (patient external_id)
    path("patients/<uuid:patient_id>/abha", abha.PatientAbhaStatus.as_view()),
    path("patients/<uuid:patient_id>/abha/link", abha.PatientAbhaLink.as_view()),
    path("patients/<uuid:patient_id>/abha/card", abha.PatientAbhaCard.as_view()),
]
