from django.utils import timezone

from abdm.gateway import bridge, hrp

EXTENSION_NAME = "abdm"
EDITABLE_FIELDS = (
    "hip_id",
    "bridge_id",
    "service_id",
    "facility_id",
    "facility_name",
    "hip_name",
    "x_hip_id_source",
    "bridge_url",
)
X_HIP_ID_SOURCES = {"hip_id", "bridge_id", "service_id"}


def get_config(facility) -> dict:
    config = dict((facility.extensions or {}).get(EXTENSION_NAME) or {})
    config.setdefault("x_hip_id_source", "hip_id")
    return config


def save_config(facility, data: dict) -> dict:
    config = get_config(facility)
    for field in EDITABLE_FIELDS:
        if field in data:
            config[field] = data[field]
    if config.get("x_hip_id_source") not in X_HIP_ID_SOURCES:
        raise ValueError("Select a valid X-HIP-ID source.")
    extensions = dict(facility.extensions or {})
    extensions[EXTENSION_NAME] = config
    facility.extensions = extensions
    facility.save(update_fields=["extensions"])
    return config


def _save_operational_fields(facility, **fields) -> dict:
    config = get_config(facility)
    config.update(fields)
    extensions = dict(facility.extensions or {})
    extensions[EXTENSION_NAME] = config
    facility.extensions = extensions
    facility.save(update_fields=["extensions"])
    return config


def register_bridge_url(facility, url: str | None = None) -> dict:
    try:
        result = bridge.update_bridge_url(url or get_config(facility).get("bridge_url") or None, facility=facility)
    except Exception as exc:
        _save_operational_fields(facility, last_error=str(exc))
        raise
    config = _save_operational_fields(
        facility,
        bridge_url=result["url"],
        bridge_url_registered_at=timezone.now().isoformat(),
        last_error="",
    )
    return {"config": config, "gateway": result}


def register_hrp_service(facility) -> dict:
    try:
        result = hrp.register_bridge_services(facility)
    except Exception as exc:
        _save_operational_fields(facility, last_error=str(exc))
        raise
    config = _save_operational_fields(facility, hrp_registered_at=timezone.now().isoformat(), last_error="")
    return {"config": config, "gateway": result}


def read_bridge_services(facility) -> dict:
    config = get_config(facility)
    if config.get("service_id"):
        return hrp.get_bridge_service(config["service_id"], facility=facility)
    return hrp.list_bridge_services(facility=facility)
