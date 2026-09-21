"""
Facility-level ABDM state lives in `Facility.extensions["abdm"]` (care_seams.AbdmFacilityExtension).

Fields the user enters: `hip_name`, `counters`.
Fields a registry link writes (ADR-016): `facility_id` (HFR), `facility_name`, `hfr` (the registry
record at link time). Nobody types an HFR id: the setup page and the "Add a facility" wizard find the
record in the registry and link it. `hfr_onboarding` holds the resumable HFR registration (journey 3).
Fields the server writes: `hip_id`, `hrp_registered_at`, `last_error`.

HIP ID. The docs say it equals the HFR facility ID, and the docs team confirmed that on
2026-09-14. The sandbox disagrees (findings E1): the HSP Registry issued the service id
`IN1410000232_1` for facility `IN1410000232`, the link token's own claims carry
`hipId: IN1410000232_1`, and a call sent with the bare HFR id is accepted (202) but its callback
is never delivered. The plug therefore reads the HIP ID off the gateway's own service list
(`gateway-list-bridge-services`) and stores it here. Until the registry has issued one the HIP ID is
empty, the facility is not "configured" for M2, and no linking call goes out: a call sent with the
bare HFR id is accepted (202) but never answered, which is worse than a clear refusal.
`hip_id_for()` is the only place the rest of the plug reads it from.
"""

from django.utils import timezone

from abdm.facility.rules import find_hip_service, validate_facility_setup
from abdm.share.rules import validate_counters

EXTENSION_NAME = "abdm"
EDITABLE_FIELDS = ("hip_name", "counters")
# The registry fields the snapshot keeps (nhpr.rules.parse_facility_search names them).
REGISTRY_FIELDS = (
    "facilityId",
    "facilityName",
    "facilityStatus",
    "facilityType",
    "facilityTypeCode",
    "ownership",
    "ownershipCode",
    "systemOfMedicine",
    "address",
    "pincode",
    "stateName",
    "stateLGDCode",
    "districtName",
    "districtLGDCode",
    "subDistrictName",
    "latitude",
    "longitude",
)


def get_config(facility) -> dict:
    config = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    config.setdefault("counters", [])
    config["facility_id"] = str(config.get("facility_id") or "")
    config["hip_id"] = str(config.get("hip_id") or "")
    config["hfr"] = dict(config.get("hfr") or {})
    config.pop("hfr_onboarding", None)  # read through get_onboarding(); too large for every reader
    return config


def is_linked(facility) -> bool:
    """True when a registry record is linked: the facility has an HFR facility id."""
    return bool(get_config(facility)["facility_id"])


def hip_id_for(facility) -> str:
    """The value every outbound call sends as `X-HIP-ID` and every body names as `hip.id`."""
    if facility is None:
        return ""
    return get_config(facility)["hip_id"]


def facility_for_hip_id(hip_id: str):
    """The Care facility behind an inbound `X-HIP-ID` or `metaData.hipId`: the stored HIP ID,
    the HFR facility ID, or the HFR id with the registry's `_<n>` suffix stripped."""
    from care.facility.models import Facility
    from django.db.models import Q

    value = str(hip_id or "").strip()
    if not value:
        return None
    candidates = {value, value.rsplit("_", 1)[0]}
    return Facility.objects.filter(
        Q(extensions__abdm__hip_id=value) | Q(extensions__abdm__facility_id__in=list(candidates))
    ).first()


def is_configured(facility) -> bool:
    """True when the facility can act as an HIP: the gateway holds a HIP service for it."""
    return bool(hip_id_for(facility))


def get_counters(facility) -> list[str]:
    return [str(c) for c in (get_config(facility).get("counters") or []) if c]


def _write_config(facility, config: dict) -> None:
    extensions = dict(facility.extensions or {})
    extensions[EXTENSION_NAME] = dict(config)
    facility.extensions = extensions
    facility.save(update_fields=["extensions"])


def save_config(facility, data: dict) -> dict:
    """The 2 fields a person edits on the setup page. The registry fields come from `set_registry_link`."""
    stored = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    for field in EDITABLE_FIELDS:
        if field in data:
            stored[field] = data[field]
    validate_facility_setup(stored)
    stored["counters"] = validate_counters(list(stored.get("counters") or []), stored)
    _write_config(facility, stored)
    return get_config(facility)


def registry_snapshot(record: dict, user=None) -> dict:
    """The part of a registry record the extension keeps, plus who linked it and when."""
    snapshot = {k: str(record.get(k) or "") for k in REGISTRY_FIELDS}
    snapshot["linked_at"] = timezone.now().isoformat()
    snapshot["linked_by"] = str(getattr(user, "username", "") or "")
    return snapshot


def set_registry_link(facility, record: dict, user=None) -> dict:
    """Link 1 registry record to the Care facility: the HFR id, the registered name (the HRP linkage
    must send it exactly) and the record itself. A default HIP name is derived when none is set.
    A different HFR id means a different service: the HIP ID is forgotten until the registry
    names it again (`sync_hip_id`)."""
    from abdm.nhpr.rules import default_hip_name

    stored = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    facility_id = str(record.get("facilityId") or "").strip().upper()
    if not facility_id:
        raise ValueError("The registry record has no facility id.")
    if facility_id != str(stored.get("facility_id") or ""):
        stored.pop("hip_id", None)
        stored.pop("hrp_registered_at", None)
    stored["facility_id"] = facility_id
    stored["facility_name"] = str(record.get("facilityName") or "")
    stored["hfr"] = registry_snapshot(record, user)
    if not stored.get("hip_name"):
        stored["hip_name"] = default_hip_name(stored["facility_name"])
    stored["last_error"] = ""
    validate_facility_setup(stored)
    stored["counters"] = validate_counters(list(stored.get("counters") or []), stored)
    _write_config(facility, stored)
    return get_config(facility)


def get_onboarding(facility) -> dict:
    """The resumable HFR onboarding state, or an empty dict when none was started."""
    stored = (facility.extensions or {}).get(EXTENSION_NAME) or {}
    state = stored.get("hfr_onboarding")
    return dict(state) if isinstance(state, dict) else {}


def save_onboarding(facility, state: dict) -> dict:
    stored = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    stored["hfr_onboarding"] = dict(state)
    _write_config(facility, stored)
    return get_onboarding(facility)


def _save_operational_fields(facility, **fields) -> dict:
    stored = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    stored.update(fields)
    _write_config(facility, stored)
    return get_config(facility)


def sync_hip_id(facility, services: list | None = None) -> str:
    """Store the service id the gateway holds for this facility's HFR id. Reads the bridge live
    when `services` is not given. Returns the HIP ID in use afterwards (never raises)."""
    from abdm.gateway import bridge

    config = get_config(facility)
    if not config["facility_id"]:
        return ""
    if services is None:
        try:
            services = bridge.bridge_services()["services"]
        except bridge.BridgeError:
            return config["hip_id"]
    found = find_hip_service(config["facility_id"], services)
    if found and found != str(config.get("hip_id") or ""):
        config = _save_operational_fields(facility, hip_id=found)
    return config["hip_id"]


def _with_name_mismatch_hint(error: str) -> str:
    if "provided facility name is not matched with registered name" not in error.lower():
        return error
    hint = "The facility name must match the Health Facility Registry record exactly."
    return error if hint in error else f"{error} {hint}"


def register_hrp_service(facility) -> dict:
    from abdm.gateway import bridge

    try:
        result = bridge.register_hrp_service(facility, get_config(facility))
    except Exception as exc:
        _save_operational_fields(facility, last_error=_with_name_mismatch_hint(str(exc)))
        raise
    _save_operational_fields(facility, hrp_registered_at=timezone.now().isoformat(), last_error="")
    sync_hip_id(facility)
    return {"config": get_config(facility), "gateway": result}
