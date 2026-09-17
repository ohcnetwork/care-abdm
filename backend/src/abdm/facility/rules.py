"""Pure validation rules for the ABDM facility setup form."""

import re

FACILITY_ID_RE = re.compile(r"^IN[A-Za-z0-9]{10}$")
FACILITY_NAME_RE = re.compile(r"^[A-Za-z0-9 \-_.(),/]+$")
HIP_NAME_RE = re.compile(r"^[A-Za-z0-9 ]{1,15}$")


def validate_facility_id(value: str) -> None:
    if value and not FACILITY_ID_RE.fullmatch(value):
        raise ValueError("HFR facility ID must start with IN and have 12 characters.")


def validate_facility_name(value: str) -> None:
    if value and not FACILITY_NAME_RE.fullmatch(value):
        raise ValueError("Facility name can use only letters, digits, space, and -_.(),/.")


def validate_hip_name(value: str) -> None:
    if value and not HIP_NAME_RE.fullmatch(value):
        raise ValueError("HIP name must be 15 characters or fewer with no special characters.")


def validate_facility_setup(config: dict) -> None:
    validate_facility_id(str(config.get("facility_id") or ""))
    validate_facility_name(str(config.get("facility_name") or ""))
    validate_hip_name(str(config.get("hip_name") or ""))


def find_hip_service(facility_id: str, services: list) -> str:
    """The id of the HIP service the gateway holds for an HFR facility id, or an empty string.

    Observed 2026-09-15 (`gateway-list-bridge-services`): the registry names the service
    `<facilityId>_<n>` (`IN1410000232_1`) and tags it `types: ["HIP", "HIU"]`. The docs page
    shows `serviceId` with `isHip`; both shapes are read. An exact match wins over a suffixed one;
    an inactive service is ignored."""
    facility_id = str(facility_id or "")
    if not facility_id:
        return ""
    best = ""
    for service in services or []:
        if not isinstance(service, dict):
            continue
        service_id = str(service.get("id") or service.get("serviceId") or "")
        types = [str(t).upper() for t in (service.get("types") or [])]
        is_hip = "HIP" in types or bool(service.get("isHip")) or not (types or "isHip" in service)
        if not is_hip or service.get("active") is False:
            continue
        if service_id == facility_id:
            return service_id
        if service_id.startswith(f"{facility_id}_") and not best:
            best = service_id
    return best
