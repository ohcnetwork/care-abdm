"""
Gateway JWKS for callback signature verification.

Docs: gateway-get-gateway-certs (`GET /api/hiecm/gateway/v3/certs`) lists no bearer token.
Observed 2026-09-15: the sandbox answers 401 without `Authorization` and 200 with the gateway
session token (docs/findings.md B14). The set held 2 keys, RS256 and RS512, and the RS256 `kid`
was the one that signs the gateway's own session tokens (Keycloak realm `central-registry`).
"""

import requests
from django.core.cache import cache

from abdm.gateway.session import gateway_headers, get_access_token
from abdm.settings import plugin_settings

CERTS_PATH = "/api/hiecm/gateway/v3/certs"
CACHE_KEY = "abdm:gateway:jwks"
CACHE_TTL = 6 * 60 * 60


class GatewayCertsError(Exception):
    pass


def fetch_jwks() -> dict:
    response = requests.get(
        f"{plugin_settings.GATEWAY_URL}{CERTS_PATH}",
        headers=gateway_headers(get_access_token()),
        timeout=plugin_settings.REQUEST_TIMEOUT_SECONDS,
    )
    if response.status_code != 200:
        raise GatewayCertsError(f"gateway certs failed: HTTP {response.status_code}")
    body = response.json()
    if not isinstance(body, dict) or not isinstance(body.get("keys"), list) or not body["keys"]:
        raise GatewayCertsError("gateway certs response has no keys")
    return body


def get_jwks(*, force_refresh: bool = False) -> dict:
    if not force_refresh:
        jwks = cache.get(CACHE_KEY)
        if jwks:
            return jwks
    jwks = fetch_jwks()
    cache.set(CACHE_KEY, jwks, timeout=CACHE_TTL)
    return jwks
