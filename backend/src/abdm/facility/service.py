"""
Facility-level ABDM state lives in `Facility.extensions["abdm"]` (care_seams.AbdmFacilityExtension).

Fields the user enters: `facility_id` (HFR), `facility_name`, `hip_name`, `counters`.
Fields the server writes: `hrp_registered_at`, `last_error`.
HIP ID is not stored: the docs team confirmed on 2026-09-14 that it equals the HFR
facility ID, so `hip_id_for()` derives it.
"""

from django.utils import timezone

from abdm.facility.rules import validate_facility_setup
from abdm.share.rules import validate_counters

EXTENSION_NAME = "abdm"
EDITABLE_FIELDS = ("facility_id", "facility_name", "hip_name", "counters")


def get_config(facility) -> dict:
    config = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    config.setdefault("counters", [])
    config["hip_id"] = str(config.get("facility_id") or "")
    return config


def hip_id_for(facility) -> str:
    if facility is None:
        return ""
    return get_config(facility)["hip_id"]


def facility_for_hip_id(hip_id: str):
    """The Care facility behind an inbound `X-HIP-ID` or `metaData.hipId`.

    The docs team says HIP ID = HFR facility ID (`IN1410000232`). The gateway's own service id
    for that facility is `IN1410000232_1` (observed 2026-09-15, findings B18). Both forms match."""
    from care.facility.models import Facility

    value = str(hip_id or "").strip()
    if not value:
        return None
    candidates = {value, value.rsplit("_", 1)[0]}
    return Facility.objects.filter(extensions__abdm__facility_id__in=list(candidates)).first()


def is_configured(facility) -> bool:
    """True when the facility can act as an HIP: it has an HFR facility ID."""
    return bool(hip_id_for(facility))


def get_counters(facility) -> list[str]:
    return [str(c) for c in (get_config(facility).get("counters") or []) if c]


def _write_config(facility, config: dict) -> None:
    stored = {k: v for k, v in config.items() if k != "hip_id"}
    extensions = dict(facility.extensions or {})
    extensions[EXTENSION_NAME] = stored
    facility.extensions = extensions
    facility.save(update_fields=["extensions"])


def save_config(facility, data: dict) -> dict:
    config = get_config(facility)
    for field in EDITABLE_FIELDS:
        if field in data:
            config[field] = data[field]
    config["hip_id"] = str(config.get("facility_id") or "")
    validate_facility_setup(config)
    config["counters"] = validate_counters(list(config.get("counters") or []), config)
    _write_config(facility, config)
    return get_config(facility)


def _save_operational_fields(facility, **fields) -> dict:
    config = get_config(facility)
    config.update(fields)
    _write_config(facility, config)
    return get_config(facility)


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
    config = _save_operational_fields(facility, hrp_registered_at=timezone.now().isoformat(), last_error="")
    return {"config": config, "gateway": result}
