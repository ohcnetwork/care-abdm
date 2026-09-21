"""
"Add a facility" (ADR-016): creates a Care facility, in-process through Care's own create path, and
links a registry record to it in the same request. Entered from the ABDM admin dashboard or from an
organization's facilities page (the host `AddFacilitySheet` override); the organization is optional
context, not a scope.

Care facts (care/emr/api/viewsets/facility.py, care/emr/resources/facility/spec.py):
- `FacilityViewSet.handle_create` validates `FacilityCreateSpec`, checks `can_create_facility`,
  saves the row (which creates the root FacilityOrganization and makes the creator its admin).
- `geo_organization` must be a government organization; the host form only accepts a leaf.
- Government organizations carry no LGD codes, so a registry record's state and district are matched
  by name (findings N14); the person picks the local body and the ward.
"""

import json

from care.emr.api.viewsets.facility import FacilityViewSet
from care.emr.models.organization import Organization
from care.emr.resources.organization.spec import OrganizationReadSpec
from care.facility.models import Facility
from care.facility.models.facility import FACILITY_TYPES, FacilityFeature
from care.security.authorization import AuthorizationController
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import PermissionDenied, ValidationError

from abdm.facility import service as facility_service
from abdm.nhpr import facility as hfr
from abdm.nhpr import rules


def form_options() -> dict:
    """Care's own choice lists, so the plug form never drifts from the host."""
    return {
        "facilityTypes": [{"id": code, "name": name} for code, name in FACILITY_TYPES],
        "features": [{"id": int(choice.value), "name": str(choice.label)} for choice in FacilityFeature],
    }


def require_can_create(user) -> None:
    if not AuthorizationController.call("can_create_facility", user):
        raise PermissionDenied("You do not have permission to create facilities.")


def _org_json(org) -> dict | None:
    return OrganizationReadSpec.serialize(org).to_json() if org is not None else None


def geo_suggestions(state_name: str, district_name: str) -> dict:
    """The Care government organizations whose names equal the registry's state and district."""
    state = district = None
    if (state_name or "").strip():
        state = Organization.objects.filter(
            org_type="govt", parent__isnull=True, name__iexact=state_name.strip()
        ).first()
    if state is not None and (district_name or "").strip():
        district = Organization.objects.filter(
            org_type="govt", parent=state, name__iexact=district_name.strip()
        ).first()
    return {"state": _org_json(state), "district": _org_json(district)}


def prefill(facility_id: str) -> dict:
    """1 registry record, the Care fields it fills and the government organizations it points at."""
    record = hfr.lookup(facility_id)
    if record is None:
        raise hfr.HfrError("NOT_FOUND", "The HFR holds no facility with this ID.")
    fields = rules.care_prefill(record)
    existing = Facility.objects.filter(extensions__abdm__facility_id=record["facilityId"]).first()
    return {
        "registry": record,
        "care": fields,
        "geo": geo_suggestions(fields["state_name"], fields["district_name"]),
        "hipName": rules.default_hip_name(record["facilityName"]),
        "alreadyLinked": ({"id": str(existing.external_id), "name": existing.name} if existing is not None else None),
    }


def _viewset(request) -> FacilityViewSet:
    viewset = FacilityViewSet()
    viewset.request = request
    viewset.format_kwarg = None
    viewset.action = "create"
    viewset.kwargs = {}
    return viewset


def create_facility(request, care_data: dict, *, registry_id: str = "", hip_name: str = "") -> dict:
    """Create the Care facility the way `POST /api/v1/facility/` does, then link the registry record
    named by `registry_id` (looked up live, never trusted from the browser)."""
    care_data = dict(care_data)
    care_data.pop("extensions", None)  # the link is the only writer of extensions["abdm"]
    record = None
    if registry_id:
        record = hfr.lookup(registry_id)
        if record is None:
            raise hfr.HfrError("NOT_FOUND", "The HFR holds no facility with this ID.")
        taken = Facility.objects.filter(extensions__abdm__facility_id=record["facilityId"]).first()
        if taken is not None:
            raise hfr.HfrError(
                "ALREADY_LINKED", f"Registry facility {record['facilityId']} is already linked to {taken.name}."
            )
    try:
        created = _viewset(request).handle_create(care_data)
    except PydanticValidationError as exc:
        # The same shape core returns (care/emr/api/viewsets/base.py emr_exception_handler).
        raise ValidationError({"errors": json.loads(exc.json())}) from exc
    facility = Facility.objects.get(external_id=created["id"])
    registry = None
    if record is not None:
        registry = hfr.link_record(facility, record, request.user)["registry"]
    if hip_name:
        try:
            facility_service.save_config(facility, {"hip_name": hip_name})
        except ValueError as exc:
            raise ValidationError({"errors": str(exc)}) from exc
    return {"facility": created, "abdm": facility_service.get_config(facility), "registry": registry}


def last_failure_for(facility) -> dict | None:
    """The most recent refused ABDM call at this facility (ADR-012 D7). Ops reads the code and
    ABDM's own words here, so nobody has to open the database to see an ABDM-1092 or a 303001."""
    from abdm.gateway import outbound
    from abdm.models import AbdmOutboundRequest

    row = (
        AbdmOutboundRequest.objects.filter(facility=facility, status=AbdmOutboundRequest.Status.FAILED)
        .order_by("-sent_at")
        .first()
    )
    if row is None:
        return None
    failure = outbound.failure(row)
    return {
        "operation_id": row.operation_id,
        "request_id": row.request_id,
        "sent_at": row.sent_at,
        "http_status": row.http_status,
        **failure.as_dict(),
    }


def list_facilities(request, organization=None) -> list[dict]:
    """The facilities the caller can see (Care's own visibility rules; a superuser sees all), with
    their ABDM state: the registry link, the services, the HFR onboarding and the last problem."""
    queryset = _viewset(request).get_queryset()
    if organization is not None:
        queryset = queryset.filter(geo_organization_cache__overlap=[organization.id])
    rows = []
    for facility in queryset.order_by("name"):
        config = facility_service.get_config(facility)
        onboarding = facility_service.get_onboarding(facility)
        rows.append(
            {
                "id": str(facility.external_id),
                "name": facility.name,
                "facility_type": dict(FACILITY_TYPES).get(facility.facility_type, ""),
                "facility_id": config["facility_id"],
                "facility_name": str(config.get("facility_name") or ""),
                "registry_status": str(config["hfr"].get("facilityStatus") or ""),
                "hip_id": config["hip_id"],
                "hip_name": str(config.get("hip_name") or ""),
                "counters": config.get("counters", []),
                "hrp_registered_at": config.get("hrp_registered_at"),
                "onboarding_status": str(onboarding.get("status") or ""),
                "last_error": str(config.get("last_error") or ""),
                "last_failure": last_failure_for(facility),
            }
        )
    return rows
