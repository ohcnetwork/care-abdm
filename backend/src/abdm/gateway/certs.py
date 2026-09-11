import requests
from django.core.cache import cache

from abdm.gateway.session import new_request_id, utc_timestamp
from abdm.settings import plugin_settings

CERTS_PATH = "/api/hiecm/gateway/v3/certs"
CACHE_KEY = "abdm:gateway:jwks"
CACHE_TTL = 6 * 60 * 60


class GatewayCertsError(Exception):
    pass


def fetch_jwks() -> dict:
    response = requests.get(
        f"{plugin_settings.GATEWAY_URL}{CERTS_PATH}",
        headers={"REQUEST-ID": new_request_id(), "TIMESTAMP": utc_timestamp()},
        timeout=plugin_settings.REQUEST_TIMEOUT_SECONDS,
    )
    if response.status_code != 200:
        raise GatewayCertsError(f"gateway certs failed: HTTP {response.status_code}")
    body = response.json()
    if not isinstance(body, dict) or not isinstance(body.get("keys"), list):
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
