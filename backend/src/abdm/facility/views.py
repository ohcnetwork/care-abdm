from care.emr.models.organization import Organization
from care.facility.models import Facility
from care.security.authorization import AuthorizationController
from django.shortcuts import get_object_or_404
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.facility import create, service
from abdm.gateway.bridge import HrpRegistrationError
from abdm.nhpr import facility as hfr
from abdm.nhpr.views import refused, search_from_query
from abdm.settings import plugin_settings


class FacilityAbdmConfigBody(BaseModel):
    """The 2 typed fields. The HFR id and name come only from a registry link (ADR-016)."""

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
        config = service.get_config(facility)
        if config["facility_id"] and not config["hfr"]:
            # A facility linked before ADR-016 holds the id and the name but no registry record.
            # 1 lookup fills it; a refusal leaves the card with the id and the name.
            try:
                config = hfr.link_registry_facility(facility, config["facility_id"], None)["config"]
            except hfr.HfrError:
                pass
        return Response(_with_share_settings(config))

    def put(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        data = _parse(FacilityAbdmConfigBody, request.data)
        try:
            return Response(_with_share_settings(service.save_config(facility, data.model_dump(exclude_unset=True))))
        except ValueError as exc:
            raise ValidationError({"errors": str(exc)}) from exc


class FacilityHrpServices(APIView):
    """POST registers this facility as an HIP service on the instance bridge."""

    permission_classes = [IsAuthenticated]

    def post(self, request, facility_id):
        facility = _facility(facility_id)
        _can_update(request, facility)
        if not service.is_linked(facility):
            raise ValidationError({"errors": "Link the facility to its Health Facility Registry record first."})
        try:
            return Response(service.register_hrp_service(facility))
        except HrpRegistrationError as exc:
            # Returned, not raised: a raise here rolls back the outbound row and `last_error` (findings J9).
            return Response({"errors": str(exc), "code": "HRP_REFUSED"}, status=502)


# --- "Add a facility" (ADR-016): gated on Care's `can_create_facility`; the organization is optional ---


def _organization(organization_id) -> Organization | None:
    if not organization_id:
        return None
    return get_object_or_404(Organization, external_id=organization_id, org_type="govt")


class FacilityFormOptions(APIView):
    """GET: Care's facility type and feature lists, for the plug's own facility form."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(create.form_options())


class HfrSearchForCreate(APIView):
    """GET ?facility_id=IN... | ?name=&state=&ownership=&district=&page=: the registry, before a Care
    facility exists."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        create.require_can_create(request.user)
        q = request.query_params
        try:
            if q.get("facility_id"):
                record = hfr.lookup(str(q.get("facility_id")))
                return Response({"facilities": [record] if record else [], "message": "", "total": 1, "pages": 1})
            return Response(search_from_query(q))
        except hfr.HfrError as exc:
            return refused(exc)


class HfrPrefill(APIView):
    """GET ?facility_id=IN...: the record, the Care fields it fills, the matching government organizations."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        create.require_can_create(request.user)
        try:
            return Response(create.prefill(str(request.query_params.get("facility_id") or "")))
        except hfr.HfrError as exc:
            return refused(exc)


class CreateFacilityBody(BaseModel):
    care: dict
    registry_id: str = ""
    hip_name: str = ""
    organization: str = ""  # optional context: the default `geo_organization` when the form sent none


class CreateFacility(APIView):
    """POST {care, registry_id?, hip_name?, organization?}: create the Care facility through Care's own
    path and link the registry record."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        create.require_can_create(request.user)
        body = _parse(CreateFacilityBody, request.data)
        care_data = dict(body.care)
        organization = _organization(body.organization.strip())
        if organization is not None:
            care_data.setdefault("geo_organization", str(organization.external_id))
        try:
            return Response(
                create.create_facility(
                    request, care_data, registry_id=body.registry_id.strip(), hip_name=body.hip_name.strip()
                ),
                status=201,
            )
        except hfr.HfrError as exc:
            return refused(exc)
