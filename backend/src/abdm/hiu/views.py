"""
Care-facing M3 endpoints for the MFE (ADR-014). The records another facility shares are clinical
data, so every route is gated on `can_view_clinical_data` for the patient
(care/security/authorization/patient.py:94-101). No key material ever leaves the server.
"""

from care.emr.models.patient import Patient
from care.facility.models import Facility
from care.security.authorization import AuthorizationController
from django.shortcuts import get_object_or_404
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm import errors
from abdm.hiu import service
from abdm.models import AbdmConsentRequest, AbdmFetchedRecord


def _patient(request, patient_id) -> Patient:
    patient = get_object_or_404(Patient, external_id=patient_id)
    if not AuthorizationController.call("can_view_clinical_data", request.user, patient):
        raise PermissionDenied
    return patient


def _facility(facility_id) -> Facility:
    if not facility_id:
        raise ValidationError({"errors": "facility is required."})
    return get_object_or_404(Facility, external_id=facility_id)


def _plug_error(exc: service.HiuError) -> ValidationError:
    failure = errors.classify(code=exc.code, message=exc.message)
    return ValidationError({"errors": f"{failure.what} {failure.next_step}".strip(), "code": exc.code})


class ConsentRequestBody(BaseModel):
    facility_id: str
    purpose_code: str = ""
    hi_types: list[str] = []
    date_from: str = ""
    date_to: str = ""
    data_erase_at: str = ""
    hip_id: str = ""
    hip_name: str = ""


class PatientConsentRequests(APIView):
    """GET the consent requests of this patient at `?facility=`; POST a new one (journey 1)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = _patient(request, patient_id)
        facility = _facility(request.query_params.get("facility"))
        return Response(service.hiu_state(patient, facility))

    def post(self, request, patient_id):
        patient = _patient(request, patient_id)
        try:
            body = ConsentRequestBody.model_validate(request.data or {})
        except PydanticValidationError as exc:
            raise ValidationError({"errors": "; ".join(e["msg"] for e in exc.errors())}) from exc
        facility = _facility(body.facility_id)
        try:
            row = service.create_consent_request(patient, facility, request.user, body.model_dump())
        except service.HiuError as exc:
            raise _plug_error(exc) from exc
        except ValueError as exc:
            raise ValidationError({"errors": str(exc)}) from exc
        state = service.hiu_state(patient, facility)
        state["created"] = str(row.external_id)
        return Response(state, status=202 if row.status != row.Status.FAILED else 502)


class ConsentRequestAction(APIView):
    """POST .../consent-requests/<id>/refresh (poll the request and any open transfer) or
    .../fetch (a new health-information request under every live artefact)."""

    permission_classes = [IsAuthenticated]

    def post(self, request, patient_id, request_id, action):
        patient = _patient(request, patient_id)
        row = get_object_or_404(
            AbdmConsentRequest.objects.select_related("facility", "patient"), external_id=request_id, patient=patient
        )
        if action == "refresh":
            service.refresh(row)
        elif action == "fetch":
            try:
                service.fetch_again(row)
            except service.HiuError as exc:
                raise _plug_error(exc) from exc
        else:
            raise ValidationError({"errors": "Unknown action."})
        return Response(service.hiu_state(patient, row.facility))


class FetchedRecordDetail(APIView):
    """GET 1 decrypted bundle. 410 once the content was erased (the row stays as the audit trail)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id, record_id):
        patient = _patient(request, patient_id)
        record = get_object_or_404(AbdmFetchedRecord, external_id=record_id, patient=patient)
        data = service.record_detail(record)
        return Response(data, status=200 if record.available else 410)


class ProviderSearch(APIView):
    """GET providers?name=: the gateway's provider directory, for the optional HIP picker."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = str(request.query_params.get("name") or "").strip()
        if len(name) < 3:
            raise ValidationError({"errors": "Type at least 3 characters."})
        try:
            return Response({"results": service.search_providers(name)})
        except service.HiuError as exc:
            return Response({"errors": exc.message or "ABDM refused the search.", "code": exc.code}, status=502)
