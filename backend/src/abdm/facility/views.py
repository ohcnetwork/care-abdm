from care.facility.models import Facility
from care.security.authorization import AuthorizationController
from django.shortcuts import get_object_or_404
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.facility import service
from abdm.gateway.bridge import HrpRegistrationError
from abdm.settings import plugin_settings


class FacilityAbdmConfigBody(BaseModel):
    facility_id: str = ""
    facility_name: str = ""
    hip_name: str = ""
    counters: list[str] = []


def _facility(facility_id):
    return get_object_or_404(Facility, external_id=facility_id)


def _can_update(request, facility):
    # Care checks this permission in care/emr/api/viewsets/facility.py.
    if not AuthorizationController.call("can_update_facility_obj", request.user, facility):
        raise PermissionDenied("You do not have permission to update this facility.")


def _with_share_settings(config: dict) -> dict:
    """Read-only deployment values the setup page needs. Not stored in the extension."""
    return {**config, "share_qr_url_template": plugin_settings.SHARE_QR_URL_TEMPLATE}


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
        # The setup page is where an administrator looks when linking misbehaves, so it is the
        # right moment to re-read the HIP ID from the gateway (1 live call; never raises).
        service.sync_hip_id(facility)
        return Response(_with_share_settings(service.get_config(facility)))

    def put(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        data = _parse(FacilityAbdmConfigBody, request.data)
        try:
            return Response(_with_share_settings(service.save_config(facility, data.model_dump())))
        except ValueError as exc:
            raise ValidationError({"errors": str(exc)}) from exc


class FacilityHrpServices(APIView):
    """POST registers this facility as an HIP service on the instance bridge."""

    permission_classes = [IsAuthenticated]

    def post(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        try:
            return Response(service.register_hrp_service(facility))
        except HrpRegistrationError as exc:
            raise ValidationError({"errors": str(exc)}) from exc
