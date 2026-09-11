"""
Care-facing API for ABHA (M1). The browser never calls ABDM; it calls these and the
plug does encryption + gateway auth server-side.

Auth: Care's default DRF stack (JWT + IsAuthenticated + CareAuthentication).
Gates (care/security/authorization/patient.py):
  - enrol/login flows (no patient yet)  → can_create_patient     (:87)
  - patient link / status / card        → can_write_patient_obj  (:58) / can_view_patient_obj (:49)

Errors from ABDM are relayed as HTTP 502 with {"abdm_code", "message", "request_id"}
so the UI can show the ABDM message and support has the REQUEST-ID.
"""

import re
from typing import Literal

from care.emr.models.patient import Patient
from care.security.authorization import AuthorizationController
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.abha import client, service
from abdm.abha.checksums import is_valid_aadhaar
from abdm.abha.client import AbhaServiceError
from abdm.care_seams import EXTENSION_NAME, AbhaAddressIdentifier, AbhaNumberIdentifier
from abdm.models import AbhaTransaction
from abdm.signals import LinkError, link_patient_to_transaction

# --- request bodies --------------------------------------------------------


class AadhaarOtpRequest(BaseModel):
    aadhaar_number: str = Field(min_length=12, max_length=12)

    @field_validator("aadhaar_number")
    @classmethod
    def _verhoeff(cls, v):
        if not is_valid_aadhaar(v):
            raise ValueError("Invalid Aadhaar number (checksum)")
        return v


class TxnRequest(BaseModel):
    txn_id: str


class EnrolByAadhaarRequest(TxnRequest):
    otp: str = Field(min_length=6, max_length=6)
    mobile: str = Field(min_length=10, max_length=10)


class MobileRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=10)


class MobileOtpRequest(TxnRequest, MobileRequest):
    pass


class OtpRequest(TxnRequest):
    otp: str = Field(min_length=6, max_length=6)


class ClaimAddressRequest(TxnRequest):
    abha_address: str = Field(min_length=4)


class SelectAccountRequest(TxnRequest):
    abha_number: str = Field(min_length=14, max_length=17)


class LoginOtpRequest(BaseModel):
    """One body for every "log in to an existing ABHA" entry point.

    hint       what the person identifies with (m1-login-request-otp loginHint / phr variant)
    login_id   the raw value: 10-digit mobile, 14-digit ABHA number (dashes optional),
               ABHA address (name@abdm / name@sbx), or 12-digit Aadhaar
    otp_system where the OTP is delivered: `abdm` = mobile registered with ABHA,
               `aadhaar` = mobile registered with Aadhaar (UIDAI). `mobile` only allows `abdm`.
    """

    hint: Literal["mobile", "abha-number", "abha-address", "aadhaar"]
    login_id: str = Field(min_length=3, max_length=128)
    otp_system: Literal["abdm", "aadhaar"] = "abdm"

    @model_validator(mode="after")
    def _shape(self):
        v = self.login_id.strip()
        if self.hint == "mobile":
            v = re.sub(r"\D", "", v)
            if not re.fullmatch(r"[6-9]\d{9}", v):
                raise ValueError("Enter a 10-digit Indian mobile number")
            if self.otp_system != "abdm":
                raise ValueError("Mobile login only supports the abdm OTP system")
        elif self.hint == "abha-number":
            v = re.sub(r"\D", "", v)
            if not re.fullmatch(r"\d{14}", v):
                raise ValueError("ABHA number must be 14 digits")
        elif self.hint == "aadhaar":
            v = re.sub(r"\D", "", v)
            if not is_valid_aadhaar(v):
                raise ValueError("Invalid Aadhaar number (checksum)")
        else:  # abha-address
            v = v.lower()
            if not re.fullmatch(r"[a-z0-9._]{3,}(@[a-z]+)?", v):
                raise ValueError("Enter an ABHA address like name@abdm")
        self.login_id = v
        return self


# --- base ------------------------------------------------------------------


def relay(e: AbhaServiceError) -> Response:
    return Response(
        {
            "abdm_code": e.abdm_code(),
            "message": e.message(),
            "request_id": e.request_id,
            "upstream_status": e.status_code,
        },
        status=502,
    )


class AbdmView(APIView):
    body_model: type[BaseModel] | None = None

    def authorize(self, request, **kwargs):
        if not AuthorizationController.call("can_create_patient", request.user):
            raise PermissionDenied

    def body(self, request):
        if self.body_model is None:
            return None
        try:
            return self.body_model.model_validate(request.data)
        except PydanticValidationError as e:
            # Surface only the human message(s); the UI shows `errors` verbatim to the front desk.
            msgs = [err["msg"].removeprefix("Value error, ") for err in e.errors()]
            raise ValidationError({"errors": "; ".join(msgs)}) from e

    def post(self, request, **kwargs):
        self.authorize(request, **kwargs)
        data = self.body(request)
        try:
            return Response(self.handle(request, data, **kwargs))
        except AbhaServiceError as e:
            return relay(e)
        except ValueError as e:
            raise ValidationError({"errors": str(e)}) from e

    def handle(self, request, data, **kwargs):  # pragma: no cover - abstract
        raise NotImplementedError


# --- Journey 1: enrol by Aadhaar OTP ---------------------------------------


class RequestAadhaarOtp(AbdmView):
    body_model = AadhaarOtpRequest

    def handle(self, request, data, **kwargs):
        return service.enrol_request_otp(data.aadhaar_number, request.user)


class EnrolByAadhaar(AbdmView):
    body_model = EnrolByAadhaarRequest

    def handle(self, request, data, **kwargs):
        return service.enrol_verify(data.txn_id, data.otp, data.mobile, request.user)


class RequestMobileOtp(AbdmView):
    body_model = MobileOtpRequest

    def handle(self, request, data, **kwargs):
        return client.request_mobile_otp(data.txn_id, data.mobile)


class VerifyMobileOtp(AbdmView):
    body_model = OtpRequest

    def handle(self, request, data, **kwargs):
        return client.verify_mobile_otp(data.txn_id, data.otp)


class AddressSuggestions(AbdmView):
    body_model = TxnRequest

    def handle(self, request, data, **kwargs):
        return client.address_suggestions(data.txn_id)


class ClaimAbhaAddress(AbdmView):
    body_model = ClaimAddressRequest

    def handle(self, request, data, **kwargs):
        return service.enrol_claim_address(data.txn_id, data.abha_address)


# --- Login to an existing ABHA (mobile / ABHA number / ABHA address / Aadhaar) ---


class LoginRequestOtp(AbdmView):
    body_model = LoginOtpRequest

    def handle(self, request, data, **kwargs):
        return service.login_request_otp(data.hint, data.login_id, data.otp_system, request.user)


class LoginVerifyOtp(AbdmView):
    body_model = OtpRequest

    def handle(self, request, data, **kwargs):
        return service.login_verify(data.txn_id, data.otp, request.user)


class LoginSelectAccount(AbdmView):
    body_model = SelectAccountRequest

    def handle(self, request, data, **kwargs):
        return service.login_select(data.txn_id, data.abha_number)


class TransactionDetail(APIView):
    """Read a completed transaction (for registration prefill after find-by-ABHA).
    Same gate as starting a flow: anyone who may create patients. Tokens never leave."""

    def get(self, request, txn_id):
        if not AuthorizationController.call("can_create_patient", request.user):
            raise PermissionDenied
        txn = get_object_or_404(AbhaTransaction, txn_id=txn_id)
        return Response(service.transaction_summary(txn))


# --- Patient-scoped --------------------------------------------------------


def _patient(request, patient_id, perm):
    patient = get_object_or_404(Patient, external_id=patient_id)
    if not AuthorizationController.call(perm, request.user, patient):
        raise PermissionDenied
    return patient


def _status_payload(patient: Patient) -> dict:
    ext = (patient.extensions or {}).get(EXTENSION_NAME) or {}
    number = AbhaNumberIdentifier.get(patient)
    txn = AbhaTransaction.objects.filter(patient=patient).order_by("-linked_at").first() if number else None
    return {
        "linked": bool(number),
        "abha_number": number,
        "abha_address": AbhaAddressIdentifier.get(patient),
        "abha_linked_at": ext.get("abha_linked_at"),
        "abha_source": ext.get("abha_source"),
        "kyc_verified": ext.get("kyc_verified"),
        "profile": {
            k: txn.profile.get(k)
            for k in ("name", "firstName", "lastName", "gender", "dob", "mobile", "status", "abhaStatus")
        }
        if txn
        else None,
        "card_available": bool(txn and txn.session_available),
    }


class PatientAbhaStatus(APIView):
    def get(self, request, patient_id):
        return Response(_status_payload(_patient(request, patient_id, "can_view_patient_obj")))


class PatientAbhaLink(AbdmView):
    """Attach a completed transaction (enrol or login) to an existing patient."""

    body_model = TxnRequest

    def authorize(self, request, patient_id, **kwargs):
        self.patient = _patient(request, patient_id, "can_write_patient_obj")

    def handle(self, request, data, **kwargs):
        txn = get_object_or_404(AbhaTransaction, txn_id=data.txn_id)
        try:
            link_patient_to_transaction(self.patient, txn)
        except LinkError as e:
            raise ValidationError({"errors": str(e)}) from e
        self.patient.refresh_from_db()
        return _status_payload(self.patient)


class _PatientAbhaBinary(APIView):
    fetch = None

    def get(self, request, patient_id):
        patient = _patient(request, patient_id, "can_view_patient_obj")
        # Newest transaction that ever held a session; ensure_x_token refreshes it if it has lapsed.
        txn = AbhaTransaction.objects.filter(patient=patient).exclude(x_token="").order_by("-linked_at").first()
        if not txn:
            return Response({"errors": "No ABHA session for this patient; verify via OTP first."}, status=409)
        try:
            x_token = service.ensure_x_token(txn)
        except service.NoUserSession:
            return Response(
                {"errors": "The ABHA session for this patient has expired; re-verify via OTP to refresh."},
                status=409,
            )
        except AbhaServiceError as e:
            return relay(e)
        try:
            upstream = type(self).fetch(x_token)
        except AbhaServiceError as e:
            return relay(e)
        # UNDOCUMENTED content type: pass through whatever ABDM sends.
        return HttpResponse(
            upstream.content, content_type=upstream.headers.get("Content-Type", "application/octet-stream")
        )


class PatientAbhaCard(_PatientAbhaBinary):
    fetch = staticmethod(client.get_abha_card)
