"""
Route table for the `abdm` plug. Care mounts it at /api/abdm/ (care/config/urls.py:111-112).
Mirrors: frontend/src/lib/careApi.ts and bruno/. Change all 3 together.
"""

from django.http import JsonResponse
from django.urls import path, re_path

from abdm.abha import views as abha
from abdm.callbacks import views as callbacks
from abdm.facility import views as facility_views
from abdm.gateway import views as gateway_views
from abdm.hip import views as hip_views
from abdm.share import views as share_views


def healthy(request):
    return JsonResponse({"status": "ok", "plug": "abdm"})


urlpatterns = [
    # --- probes and instance setup (the bridge is 1 per clientId; ADR-010) ---
    path("health", healthy),
    path("gateway/status", gateway_views.GatewayStatus.as_view()),
    path("bridge", gateway_views.BridgeState.as_view()),
    path("bridge/register-url", gateway_views.BridgeRegisterUrl.as_view()),
    path("admin/overview", gateway_views.AdminOverview.as_view()),
    # --- facility setup (ADR-007): HFR facility ID, names, counters; HRP service registration ---
    path("facilities/<uuid:facility_id>/abdm", facility_views.FacilityAbdmConfig.as_view()),
    path("facilities/<uuid:facility_id>/abdm/hrp-services", facility_views.FacilityHrpServices.as_view()),
    # --- M1 Scan and Share: front desk inbox (the gateway callback lands on the catch-all below) ---
    path("facilities/<uuid:facility_id>/abdm/profile-shares", share_views.ProfileShareList.as_view()),
    path("facilities/<uuid:facility_id>/abdm/profile-shares/<uuid:share_id>", share_views.ProfileShareDetail.as_view()),
    path(
        "facilities/<uuid:facility_id>/abdm/profile-shares/<uuid:share_id>/dismiss",
        share_views.ProfileShareDismiss.as_view(),
    ),
    # --- callback log (superuser) ---
    path("callbacks", callbacks.CallbackList.as_view()),
    path("callbacks/<uuid:callback_id>", callbacks.CallbackDetail.as_view()),
    # --- M2 desk endpoints ---
    path("encounters/<uuid:encounter_id>/care-context", hip_views.EncounterCareContext.as_view()),
    path("encounters/<uuid:encounter_id>/care-context/link", hip_views.EncounterCareContextLink.as_view()),
    path(
        "encounters/<uuid:encounter_id>/share-items/<uuid:item_id>/<str:action>",
        hip_views.ShareItemExclude.as_view(),
    ),
    path("patients/<uuid:patient_id>/abha/sms-link", hip_views.PatientSmsLink.as_view()),
    path("patients/<uuid:patient_id>/abha/consents", hip_views.PatientConsents.as_view()),
    # --- M1 Journey 1: ABHA creation by Aadhaar OTP ---
    path("abha/enrol/aadhaar/request-otp", abha.RequestAadhaarOtp.as_view()),
    path("abha/enrol/aadhaar/verify", abha.EnrolByAadhaar.as_view()),
    path("abha/enrol/mobile/request-otp", abha.RequestMobileOtp.as_view()),
    path("abha/enrol/mobile/verify", abha.VerifyMobileOtp.as_view()),
    path("abha/enrol/address/suggestions", abha.AddressSuggestions.as_view()),
    path("abha/enrol/address/claim", abha.ClaimAbhaAddress.as_view()),
    # --- M1: login to an existing ABHA. body.hint in mobile|abha-number|abha-address|aadhaar ---
    path("abha/login/request-otp", abha.LoginRequestOtp.as_view()),
    path("abha/login/verify", abha.LoginVerifyOtp.as_view()),
    path("abha/login/select-account", abha.LoginSelectAccount.as_view()),
    # --- completed transaction read-back (registration prefill) ---
    path("abha/transactions/<str:txn_id>", abha.TransactionDetail.as_view()),
    # --- patient-scoped M1 ---
    path("patients/<uuid:patient_id>/abha", abha.PatientAbhaStatus.as_view()),
    path("patients/<uuid:patient_id>/abha/link", abha.PatientAbhaLink.as_view()),
    path("patients/<uuid:patient_id>/abha/card", abha.PatientAbhaCard.as_view()),
    # Every gateway callback, last on purpose. The bridge URL is `<base>/api/abdm`, so the gateway
    # posts to `/api/abdm/<callback path>`; callbacks/paths.py maps the path to its operation and
    # a path the docs never named is still stored (operation id empty, `unhandled`) instead of
    # vanishing as a Care 404. Observed 2026-09-17: the real paths carry an `/api` prefix the docs
    # omit (`/api/abdm/api/v3/hip/token/on-generate-token`).
    re_path(r"^(?P<path>.+)$", callbacks.GenericCallbackView.as_view()),
]
