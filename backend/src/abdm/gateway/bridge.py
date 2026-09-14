"""
Bridge (callback URL) registration.

Contract source (read 2026-09-09):
  https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-update-bridge-url/index.md
  PATCH {GATEWAY_URL}/api/hiecm/gateway/v3/bridge/url
  headers: Authorization Bearer, REQUEST-ID, TIMESTAMP, X-CM-ID
  body:    {"url": "<HTTPS callback URL>"}
  200:     {"message": "..."}

The docs do not state whether `url` is a bare host or may carry a path prefix.
We register CALLBACK_BASE_URL + "/api/abdm" (Care mounts plug routes under
api/<plug>/, care/config/urls.py:111-112) and confirm with the first real callback.
"""

import logging

from abdm.gateway.outbound import failure_detail, send
from abdm.settings import plugin_settings

logger = logging.getLogger(__name__)

BRIDGE_URL_PATH = "/api/hiecm/gateway/v3/bridge/url"
CALLBACK_PREFIX = "/api/abdm"


class BridgeError(Exception):
    pass


def callback_url() -> str:
    base = plugin_settings.CALLBACK_BASE_URL.rstrip("/")
    if not base.startswith("https://"):
        raise BridgeError("CALLBACK_BASE_URL must be an https URL (docs: `url` is an HTTPS callback URL)")
    return f"{base}{CALLBACK_PREFIX}"


def update_bridge_url(url: str | None = None, *, facility=None) -> dict:
    url = url or callback_url()
    row = send(
        "gateway-update-bridge-url",
        BRIDGE_URL_PATH,
        {"url": url},
        method="PATCH",
        facility=facility,
    )
    if row.status != row.Status.SUCCEEDED:
        raise BridgeError(failure_detail(row))
    return {
        "url": url,
        "status_code": row.http_status,
        "request_id": row.request_id,
        "response": row.response_json,
    }
