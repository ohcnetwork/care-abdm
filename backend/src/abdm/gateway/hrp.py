"""
HRP (Health Repository Provider) service registration in the HSP Registry.

Contract source (read 2026-09-09):
  https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md

The page conflicts with itself on the host. The prose says
`https://apihspsbx.abdm.gov.in`. The curl example says the gateway host.
Observed against the sandbox 2026-09-14:
  gateway host -> HTTP 503, body "Please make a valid request."
  prose host   -> HTTP 200, body [{"error": {...}}] for a bad facility name
So the registration goes to HSP_URL, and the read endpoints stay on the
gateway host, where both hosts answer HTTP 200.
"""

from abdm.gateway.outbound import failure_detail, send
from abdm.settings import plugin_settings

REGISTER_BRIDGE_SERVICES_PATH = "/v4/int/v1/bridges/MutipleHRPAddUpdateServices"
LIST_BRIDGE_SERVICES_PATH = "/api/hiecm/gateway/v3/bridge-services"
GET_BRIDGE_SERVICE_PATH = "/api/hiecm/gateway/v3/bridge-service/serviceId/{service_id}"


REQUIRED_REGISTRATION_FIELDS = {
    "facility_id": "Facility ID",
    "facility_name": "Facility name",
    "bridge_id": "Bridge ID",
    "hip_name": "HIP name",
}


class HrpRegistrationError(Exception):
    pass


def _registration_body(config: dict) -> dict:
    missing = [label for field, label in REQUIRED_REGISTRATION_FIELDS.items() if not (config.get(field) or "").strip()]
    if missing:
        raise HrpRegistrationError(f"Fill these fields on the ABDM setup page first: {', '.join(missing)}.")
    return {
        "facilityId": config.get("facility_id", ""),
        "facilityName": config.get("facility_name", ""),
        "HRP": [
            {
                "bridgeId": config.get("bridge_id", ""),
                "hipName": config.get("hip_name", ""),
                "type": "HIP",
                "active": True,
            }
        ],
    }


def _result(row):
    if row.status != row.Status.SUCCEEDED:
        raise HrpRegistrationError(failure_detail(row))
    return {"status_code": row.http_status, "request_id": row.request_id, "response": row.response_json}


def register_bridge_services(facility) -> dict:
    config = (facility.extensions or {}).get("abdm") or {}
    body = _registration_body(config)
    url = f"{plugin_settings.HSP_URL.rstrip('/')}{REGISTER_BRIDGE_SERVICES_PATH}"
    row = send("gateway-register-bridge-services", url, body, facility=facility)
    return _result(row)


def list_bridge_services(facility=None) -> dict:
    row = send("gateway-list-bridge-services", LIST_BRIDGE_SERVICES_PATH, None, method="GET", facility=facility)
    return _result(row)


def get_bridge_service(service_id: str, facility=None) -> dict:
    row = send(
        "gateway-get-bridge-service-by-id",
        GET_BRIDGE_SERVICE_PATH.format(service_id=service_id),
        None,
        method="GET",
        facility=facility,
    )
    return _result(row)
