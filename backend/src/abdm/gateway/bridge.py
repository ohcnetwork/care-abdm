"""
The bridge: this ABDM client's callback URL and the HIP services linked to it.

Scope (ADR-010, ADR-011): the bridge is instance-level. 1 callback URL per clientId
(/getting-started/sandbox: "One URL covers your whole integration, however many
facilities it serves"). The gateway is the source of truth for the bridge id and the
services list, so the plug reads them live and caches only the bridge id.

Docs (read 2026-09-15):
  gateway-update-bridge-url        PATCH {GATEWAY_URL}/api/hiecm/gateway/v3/bridge/url  {"url"}
                                   docs say 200 {"message"}; sandbox returned 202 with no body.
  gateway-list-bridge-services     GET   {GATEWAY_URL}/api/hiecm/gateway/v3/bridge-services
                                   -> {"bridge": {id, name, url, active, blocklisted}, "services": [...]}
  gateway-register-bridge-services POST  {HSP_URL}/v4/int/v1/bridges/MutipleHRPAddUpdateServices
                                   The page conflicts on the host. Observed 2026-09-14: the
                                   gateway host answers 503; the prose host (HSP) answers 200.
                                   HSP reports failures with HTTP 200 and an error envelope.
"""

import logging

from django.core.cache import cache

from abdm.gateway.outbound import failure_detail, send
from abdm.settings import plugin_settings

logger = logging.getLogger(__name__)

BRIDGE_URL_PATH = "/api/hiecm/gateway/v3/bridge/url"
LIST_BRIDGE_SERVICES_PATH = "/api/hiecm/gateway/v3/bridge-services"
REGISTER_BRIDGE_SERVICES_PATH = "/v4/int/v1/bridges/MutipleHRPAddUpdateServices"
# Care mounts plug routes at api/<plug>/ (care/config/urls.py:111-112).
CALLBACK_PREFIX = "/api/abdm"
BRIDGE_ID_CACHE_KEY = "abdm:gateway:bridge_id"
BRIDGE_ID_CACHE_TTL = 60 * 60


class BridgeError(Exception):
    pass


def callback_url() -> str:
    base = plugin_settings.CALLBACK_BASE_URL.rstrip("/")
    if not base.startswith("https://"):
        raise BridgeError("ABDM_CALLBACK_BASE_URL must be an https URL (docs: the bridge URL is an HTTPS URL).")
    return f"{base}{CALLBACK_PREFIX}"


def _ok(row, error_cls=BridgeError):
    if row.status != row.Status.SUCCEEDED:
        raise error_cls(failure_detail(row))
    return row


def register_callback_url() -> dict:
    """PATCH the bridge URL. Returns the URL and the request id for the audit row."""
    url = callback_url()
    row = _ok(send("gateway-update-bridge-url", BRIDGE_URL_PATH, {"url": url}, method="PATCH"))
    cache.delete(BRIDGE_ID_CACHE_KEY)
    return {"url": url, "status_code": row.http_status, "request_id": row.request_id}


def bridge_services() -> dict:
    """Live read of the bridge and its services. Caches the bridge id."""
    row = _ok(send("gateway-list-bridge-services", LIST_BRIDGE_SERVICES_PATH, None, method="GET"))
    body = row.response_json if isinstance(row.response_json, dict) else {}
    bridge = body.get("bridge") if isinstance(body.get("bridge"), dict) else {}
    found = str(bridge.get("id") or bridge.get("bridgeId") or "")
    if found:
        cache.set(BRIDGE_ID_CACHE_KEY, found, timeout=BRIDGE_ID_CACHE_TTL)
    return {
        "bridge": {
            "id": found,
            "name": str(bridge.get("name") or ""),
            "url": str(bridge.get("url") or ""),
            "active": bridge.get("active"),
            "blocklisted": bridge.get("blocklisted"),
        },
        "services": body.get("services") if isinstance(body.get("services"), list) else [],
        "request_id": row.request_id,
    }


def bridge_id() -> str:
    """The gateway-issued bridge id, needed as HRP.bridgeId. Cached for 1 hour."""
    cached = cache.get(BRIDGE_ID_CACHE_KEY)
    if cached:
        return cached
    found = bridge_services()["bridge"]["id"]
    if not found:
        raise BridgeError("The gateway returned no bridge id. Register the callback URL first.")
    return found


def bridge_state() -> dict:
    """What the admin and setup pages show: the derived callback URL plus the live gateway view.
    Never raises: a missing ABDM_CALLBACK_BASE_URL or a gateway failure lands in `error`."""
    state = {"callback_url": "", "bridge": None, "services": [], "error": ""}
    try:
        state["callback_url"] = callback_url()
        live = bridge_services()
    except BridgeError as exc:
        state["error"] = str(exc)
        return state
    state["bridge"] = live["bridge"]
    state["services"] = live["services"]
    return state


# --- HRP service registration (facility-level) ---------------------------------------


class HrpRegistrationError(Exception):
    pass


REQUIRED_HRP_FIELDS = {"facility_id": "HFR facility ID", "facility_name": "Facility name", "hip_name": "HIP name"}


def hrp_registration_body(config: dict, bridge: str) -> dict:
    """Body of gateway-register-bridge-services for 1 facility, in the HIP and the HIU role.

    ADR-015: M3 needs the HIU role, so both types are named (`m4-multiple-hrp-api/01`, 1 HRP entry
    per type). The sandbox returned both types for a HIP-only registration (findings B18)."""
    missing = [label for field, label in REQUIRED_HRP_FIELDS.items() if not str(config.get(field) or "").strip()]
    if missing:
        raise HrpRegistrationError(f"Fill these fields on the ABDM setup page first: {', '.join(missing)}.")
    from abdm.nhpr.rules import hrp_linkage_body

    try:
        return hrp_linkage_body(config["facility_id"], config["facility_name"], bridge, config["hip_name"])
    except ValueError as exc:
        raise HrpRegistrationError(str(exc)) from exc


def register_hrp_service(facility, config: dict) -> dict:
    try:
        bridge = bridge_id()
    except BridgeError as exc:
        raise HrpRegistrationError(f"Register the bridge URL first. {exc}") from exc
    body = hrp_registration_body(config, bridge)
    url = f"{plugin_settings.HSP_URL.rstrip('/')}{REGISTER_BRIDGE_SERVICES_PATH}"
    row = _ok(send("gateway-register-bridge-services", url, body, facility=facility), HrpRegistrationError)
    return {"status_code": row.http_status, "request_id": row.request_id, "response": row.response_json}
