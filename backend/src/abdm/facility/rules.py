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
    """The stored setup. The registered name is the registry's own value (ADR-016), so only the
    id and the HIP name are checked here; `validate_facility_name` stays for typed names."""
    validate_facility_id(str(config.get("facility_id") or ""))
    validate_hip_name(str(config.get("hip_name") or ""))


ALREADY_ASSOCIATED_RE = re.compile(
    r"Hfr-Id\s*=\s*(?P<hfr>[A-Za-z0-9_]+).*?Service-Id\s*=\s*(?P<service>[A-Za-z0-9_]+)",
    re.IGNORECASE | re.DOTALL,
)


def already_associated_service(lines: list[str], facility_id: str) -> str:
    """The service id inside an "already associated" refusal, when it names our facility.

    Observed 2026-09-22 on `gateway-register-bridge-services`: HTTP 200 with the error envelope
        code 2500, "Bridge-Id=SBXID_035123 is already associated with Hfr-Id=IN3210000772 for
        Service-Id=IN3210000772, Service-Name=SECONDARY FACIL"
    HRP registration is once per (bridge, facility): a repeat is refused, not re-applied. That
    refusal is not a failure — it states the facility is already a service on this bridge and
    names the service id. Returns the service id only when `Hfr-Id` is this facility (the bare
    id, or the registry's `<facilityId>_<n>` form), so a refusal about another facility still
    fails loudly. Returns an empty string otherwise.
    """
    facility_id = str(facility_id or "").strip().upper()
    if not facility_id:
        return ""
    for line in lines or []:
        text = str(line or "")
        if "already associated" not in text.lower():
            continue
        match = ALREADY_ASSOCIATED_RE.search(text)
        if not match:
            continue
        hfr = match.group("hfr").upper()
        if hfr == facility_id or hfr.rsplit("_", 1)[0] == facility_id:
            return match.group("service")
    return ""


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
