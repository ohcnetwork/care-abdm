"""
Care-facing M2 endpoints for the MFE. Gates come from care/security/authorization/encounter.py
and patient.py. No ABDM token or link token ever leaves the server.
"""

from care.emr.models.encounter import Encounter
from care.emr.models.patient import Patient
from care.facility.models import Facility
from care.security.authorization import AuthorizationController
from django.db.models import Q
from django.shortcuts import get_object_or_404
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.facility.service import hip_id_for
from abdm.hip import contexts
from abdm.hip.consent import consent_summary
from abdm.hip.transfer import data_request_summary
from abdm.models import AbdmCallback, AbdmCareContext, AbdmConsent, AbdmDataRequest, AbdmLinkToken, AbdmOutboundRequest


def _encounter(request, encounter_id, perm):
    encounter = get_object_or_404(Encounter, external_id=encounter_id)
    if not AuthorizationController.call(perm, request.user, encounter):
        raise PermissionDenied
    return encounter


def _patient(request, patient_id, perm):
    patient = get_object_or_404(Patient, external_id=patient_id)
    if not AuthorizationController.call(perm, request.user, patient):
        raise PermissionDenied
    return patient


def _request_summary(row: AbdmOutboundRequest) -> dict:
    return {
        "requestId": row.request_id,
        "operationId": row.operation_id,
        "status": row.status,
        "httpStatus": row.http_status,
        "errorCode": row.error_code,
        "sentAt": row.sent_at,
        "callbacks": [
            {
                "path": c.path,
                "signatureStatus": c.signature_status,
                "processedStatus": c.processed_status,
                "receivedAt": c.received_at,
            }
            for c in AbdmCallback.objects.filter(outbound_request=row).order_by("received_at")
        ],
    }


def care_context_state(encounter: Encounter) -> dict:
    context = AbdmCareContext.objects.filter(encounter=encounter).first()
    address, number = contexts.patient_abha(encounter.patient)
    token = AbdmLinkToken.objects.filter(patient=encounter.patient, facility=encounter.facility).first()
    # Token and SMS requests are per patient and facility, not per encounter; the desk still needs to see them.
    activity = AbdmOutboundRequest.objects.filter(
        Q(encounter=encounter)
        | Q(
            patient=encounter.patient,
            facility=encounter.facility,
            operation_id__in=["m2-generate-link-token", "m2-sms-deep-link-notify"],
        )
    ).order_by("-sent_at")[:10]
    return {
        "facilityConfigured": bool(hip_id_for(encounter.facility)),
        "patientAbhaAddress": address,
        "patientAbhaNumber": number,
        "linkToken": {"status": token.status, "expiresAt": token.expires_at, "errorCode": token.error_code}
        if token
        else None,
        "careContext": {
            "referenceNumber": context.reference_number,
            "display": context.display,
            "hiTypes": context.hi_types,
            "status": context.status,
            "linkedVia": context.linked_via,
            "linkedAt": context.linked_at,
            "notifiedAt": context.notified_at,
            "errorCode": context.error_code,
            "errorMessage": context.error_message,
        }
        if context
        else None,
        "activity": [_request_summary(row) for row in activity],
    }


class EncounterCareContext(APIView):
    """GET the link state of this Encounter as a care context."""

    permission_classes = [IsAuthenticated]

    def get(self, request, encounter_id):
        return Response(care_context_state(_encounter(request, encounter_id, "can_view_encounter_obj")))


class EncounterCareContextLink(APIView):
    """POST: link this Encounter now (or notify about new records). Runs the sync inline so the
    desk sees the gateway acknowledgement; callbacks finish the state later."""

    permission_classes = [IsAuthenticated]

    def post(self, request, encounter_id):
        encounter = _encounter(request, encounter_id, "can_update_encounter_obj")
        if not hip_id_for(encounter.facility):
            raise ValidationError({"errors": "This facility has no HFR facility ID. Complete the ABDM setup first."})
        contexts.sync_encounter(encounter)
        return Response(care_context_state(encounter))


class SmsLinkBody(BaseModel):
    facility_id: str


class PatientSmsLink(APIView):
    """POST: ask ABDM to send the patient an SMS deep link to the ABHA app (journey 2)."""

    permission_classes = [IsAuthenticated]

    def post(self, request, patient_id):
        patient = _patient(request, patient_id, "can_write_patient_obj")
        try:
            body = SmsLinkBody.model_validate(request.data)
        except PydanticValidationError as exc:
            raise ValidationError({"errors": "; ".join(e["msg"] for e in exc.errors())}) from exc
        facility = get_object_or_404(Facility, external_id=body.facility_id)
        try:
            row = contexts.send_sms_deep_link(patient, facility)
        except contexts.LinkingError as exc:
            raise ValidationError({"errors": str(exc)}) from exc
        return Response(_request_summary(row), status=202 if row.status == row.Status.SUCCEEDED else 502)


class PatientConsents(APIView):
    """GET the consent artefacts the gateway notified for this patient, newest first."""

    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = _patient(request, patient_id, "can_view_patient_obj")
        rows = AbdmConsent.objects.filter(patient=patient).order_by("-notified_at")[:50]
        requests = AbdmDataRequest.objects.filter(consent__patient=patient).order_by("-received_at")[:50]
        return Response(
            {
                "consents": [consent_summary(c) for c in rows],
                "dataRequests": [data_request_summary(r) for r in requests],
            }
        )
