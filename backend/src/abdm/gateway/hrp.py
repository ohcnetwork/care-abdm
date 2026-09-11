from abdm.gateway.outbound import send

REGISTER_BRIDGE_SERVICES_PATH = "/v4/int/v1/bridges/MutipleHRPAddUpdateServices"
LIST_BRIDGE_SERVICES_PATH = "/api/hiecm/gateway/v3/bridge-services"
GET_BRIDGE_SERVICE_PATH = "/api/hiecm/gateway/v3/bridge-service/serviceId/{service_id}"


class HrpRegistrationError(Exception):
    pass


def _registration_body(config: dict) -> dict:
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


def register_bridge_services(facility) -> dict:
    config = (facility.extensions or {}).get("abdm") or {}
    body = _registration_body(config)
    row = send("gateway-register-bridge-services", REGISTER_BRIDGE_SERVICES_PATH, body, facility=facility)
    if row.status != row.Status.SUCCEEDED:
        raise HrpRegistrationError(f"HTTP {row.http_status} (REQUEST-ID {row.request_id})")
    return {"status_code": row.http_status, "request_id": row.request_id, "response": row.response_json}


def list_bridge_services(facility=None) -> dict:
    row = send("gateway-list-bridge-services", LIST_BRIDGE_SERVICES_PATH, None, method="GET", facility=facility)
    if row.status != row.Status.SUCCEEDED:
        raise HrpRegistrationError(f"HTTP {row.http_status} (REQUEST-ID {row.request_id})")
    return {"status_code": row.http_status, "request_id": row.request_id, "response": row.response_json}


def get_bridge_service(service_id: str, facility=None) -> dict:
    row = send(
        "gateway-get-bridge-service-by-id",
        GET_BRIDGE_SERVICE_PATH.format(service_id=service_id),
        None,
        method="GET",
        facility=facility,
    )
    if row.status != row.Status.SUCCEEDED:
        raise HrpRegistrationError(f"HTTP {row.http_status} (REQUEST-ID {row.request_id})")
    return {"status_code": row.http_status, "request_id": row.request_id, "response": row.response_json}
