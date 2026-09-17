"""
Facility-level ABDM state lives in `Facility.extensions["abdm"]` (care_seams.AbdmFacilityExtension).

Fields the user enters: `facility_id` (HFR), `facility_name`, `hip_name`, `counters`.
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
EDITABLE_FIELDS = ("facility_id", "facility_name", "hip_name", "counters")


def get_config(facility) -> dict:
    config = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    config.setdefault("counters", [])
    config["facility_id"] = str(config.get("facility_id") or "")
    config["hip_id"] = str(config.get("hip_id") or "")
    return config


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
    stored = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    for field in EDITABLE_FIELDS:
        if field in data:
            stored[field] = data[field]
    if stored.get("facility_id") != get_config(facility)["facility_id"]:
        # A new HFR id means a new service: forget the HIP ID until the registry names it again.
        stored.pop("hip_id", None)
        stored.pop("hrp_registered_at", None)
    validate_facility_setup(stored)
    stored["counters"] = validate_counters(list(stored.get("counters") or []), stored)
    _write_config(facility, stored)
    return get_config(facility)


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
