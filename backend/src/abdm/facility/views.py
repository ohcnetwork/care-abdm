from care.facility.models import Facility
from care.security.authorization import AuthorizationController
from django.shortcuts import get_object_or_404
from pydantic import BaseModel, Field
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.facility import service
from abdm.gateway.bridge import BridgeError
from abdm.gateway.hrp import HrpRegistrationError


class FacilityAbdmConfigBody(BaseModel):
    hip_id: str = ""
    bridge_id: str = ""
    service_id: str = ""
    facility_id: str = ""
    facility_name: str = ""
    hip_name: str = ""
    x_hip_id_source: str = Field(default="hip_id")
    bridge_url: str = ""


class BridgeUrlBody(BaseModel):
    url: str | None = None


def _facility(facility_id):
    return get_object_or_404(Facility, external_id=facility_id)


def _can_update(request, facility):
    # Care checks this permission in care/emr/api/viewsets/facility.py.
    if not AuthorizationController.call("can_update_facility_obj", request.user, facility):
        raise PermissionDenied("You do not have permission to update this facility.")


def _parse(model, data):
    try:
        return model.model_validate(data)
    except PydanticValidationError as exc:
        raise ValidationError({"errors": "; ".join(e["msg"] for e in exc.errors())}) from exc


class FacilityAbdmConfig(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        return Response(service.get_config(facility))

    def put(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        data = _parse(FacilityAbdmConfigBody, request.data)
        try:
            return Response(service.save_config(facility, data.model_dump()))
        except ValueError as exc:
            raise ValidationError({"errors": str(exc)}) from exc


class FacilityBridgeUrl(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        data = _parse(BridgeUrlBody, request.data or {})
        try:
            return Response(service.register_bridge_url(facility, data.url))
        except BridgeError as exc:
            raise ValidationError({"errors": str(exc)}) from exc


class FacilityHrpServices(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        try:
            return Response(service.read_bridge_services(facility))
        except HrpRegistrationError as exc:
            raise ValidationError({"errors": str(exc)}) from exc

    def post(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        try:
            return Response(service.register_hrp_service(facility))
        except HrpRegistrationError as exc:
            raise ValidationError({"errors": str(exc)}) from exc
