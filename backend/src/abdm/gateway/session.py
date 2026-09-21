"""
Gateway session: obtain and cache the bearer token every HIE-CM module call needs.

Contract source (read 2026-09-09):
  https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-sessions-create/index.md
  POST {GATEWAY_URL}/api/hiecm/gateway/v3/sessions
  headers: REQUEST-ID (fresh uuid), TIMESTAMP (ISO-8601 UTC ms + Z), X-CM-ID (sbx|abdm)
  body:    {clientId, clientSecret, grantType: "client_credentials"}
  200:     {accessToken, expiresIn, refreshExpiresIn, refreshToken, tokenType}
Observed against the sandbox 2026-09-09: HTTP 200, expiresIn=1200, refreshExpiresIn=1800.

The docs say: read `expiresIn` from the response rather than assuming, and
refresh before it runs out instead of waiting for a 401. We cache in Django's
cache (Redis in Care) with a TTL shortened by a safety margin.
"""

import logging
import uuid
from datetime import UTC, datetime

import requests
from django.core.cache import cache
from django.utils import timezone

from abdm.settings import plugin_settings

logger = logging.getLogger(__name__)

SESSIONS_PATH = "/api/hiecm/gateway/v3/sessions"
CACHE_KEY = "abdm:gateway:access_token"
# Seconds subtracted from expiresIn so we never present a token at the edge of expiry.
EXPIRY_SAFETY_MARGIN = 60


class GatewaySessionError(Exception):
    def __init__(self, status_code, body, request_id):
        self.status_code = status_code
        self.body = body
        self.request_id = request_id
        super().__init__(f"gateway session failed: HTTP {status_code} (REQUEST-ID {request_id}): {body}")


def utc_timestamp() -> str:
    """ISO 8601 UTC with milliseconds and Z suffix, as the docs require for TIMESTAMP."""
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now(UTC).microsecond // 1000:03d}Z"


def new_request_id() -> str:
    return str(uuid.uuid4())


def gateway_headers(access_token: str | None = None) -> dict:
    """The three mandatory gateway headers (+ Authorization when a token is given)."""
    headers = {
        "REQUEST-ID": new_request_id(),
        "TIMESTAMP": utc_timestamp(),
        "X-CM-ID": plugin_settings.CM_ID,
        "Content-Type": "application/json",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers


def create_session() -> dict:
    """Call the sessions endpoint and return the raw response body."""
    from abdm.gateway import outbound  # lazy: outbound imports this module

    plugin_settings.validate()
    headers = gateway_headers()
    url = f"{plugin_settings.GATEWAY_URL}{SESSIONS_PATH}"
    body = {
        "clientId": plugin_settings.CLIENT_ID,
        "clientSecret": plugin_settings.CLIENT_SECRET,
        "grantType": "client_credentials",
    }
    sent_at = timezone.now()
    response = requests.post(url, headers=headers, json=body, timeout=plugin_settings.REQUEST_TIMEOUT_SECONDS)
    try:
        answer = response.json() if response.text else {}
    except ValueError:
        answer = {"text": response.text}
    # ADR-018: the session call is the first thing an integrator debugs ("everything returns 401").
    # `record()` redacts `clientSecret` and the tokens before the save.
    outbound.record(
        "gateway-sessions-create",
        method="POST",
        url=url,
        request_id=headers["REQUEST-ID"],
        headers=headers,
        body=body,
        http_status=response.status_code,
        response_body=answer,
        sent_at=sent_at,
    )
    if response.status_code != 200:
        raise GatewaySessionError(response.status_code, response.text, headers["REQUEST-ID"])
    return answer


def get_access_token(force_refresh: bool = False) -> str:
    """Return a cached bearer token, creating a new session when missing/expired."""
    if not force_refresh:
        token = cache.get(CACHE_KEY)
        if token:
            return token
    body = create_session()
    token = body["accessToken"]
    ttl = max(int(body.get("expiresIn", 0)) - EXPIRY_SAFETY_MARGIN, 1)
    cache.set(CACHE_KEY, token, timeout=ttl)
    logger.info("abdm gateway session created; cached for %ss", ttl)
    return token


def invalidate_access_token() -> None:
    cache.delete(CACHE_KEY)
