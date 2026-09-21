"""
Callback signature verification (/docs/hiecm/v3/concepts/callback-authenticity).

The docs say the gateway signs callbacks and publishes a JWKS, and that "which header carries
the signed token is not published". So:
- The configured header (`ABDM_CALLBACK_SIGNATURE_HEADER`, default `Authorization`) is read first.
  When it holds no JWT, every header is scanned for a JWT-shaped value. The header name is not a
  security property: only the gateway's private key can produce a signature that verifies.
- The algorithm is taken from the JWK that matches the token `kid`, never from the token header
  alone, and only RSA signatures (RS256, RS512: the 2 algorithms in the gateway's set) pass.
- Verification fails closed. `verify_callback_signature` raises `CallbackSignatureError` for a
  bad or missing signature and lets `GatewayCertsError` through when the JWKS cannot be read.
- An expired token is accepted for `ABDM_CALLBACK_SIGNATURE_LEEWAY_SECONDS` after its `exp`
  (ADR-012 D4). The gateway repeats a failed delivery about 16 minutes later with the same token,
  so a strict check throws genuine answers away. The signature is still verified in full.
"""

import re
from datetime import UTC, datetime

import jwt
from jwt import InvalidTokenError

from abdm.gateway.certs import get_jwks
from abdm.settings import plugin_settings

ALLOWED_ALGORITHMS = ("RS256", "RS512")
_JWT_RE = re.compile(r"^[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}$")


class CallbackSignatureError(Exception):
    pass


def _bare(value: str) -> str:
    value = (value or "").strip()
    return value.split(" ", 1)[1].strip() if value.lower().startswith("bearer ") else value


SECRET_HEADERS = ("authorization", "cookie", "x-token", "x-hprid-auth", "x-link-token")


def redact_headers(headers: dict) -> dict:
    """Header names and lengths, never values, for the browser (abdm-m2 design.md: "Redact by name
    and length, never by value"). A credential header, or any JWT-shaped value, becomes
    `<redacted, N characters>`; the plain routing headers (REQUEST-ID, TIMESTAMP, X-HIP-ID, ...)
    stay readable."""
    out = {}
    for name, value in (headers or {}).items():
        text = str(value or "")
        if name.lower() in SECRET_HEADERS or _JWT_RE.match(_bare(text)):
            out[name] = f"<redacted, {len(text)} characters>"
        else:
            out[name] = text
    return out


def find_token(headers: dict[str, str]) -> tuple[str, str]:
    """(header name, bare JWT). The configured header wins; otherwise the first JWT-shaped header."""
    wanted = plugin_settings.CALLBACK_SIGNATURE_HEADER.lower()
    for name, value in headers.items():
        if name.lower() == wanted and _JWT_RE.match(_bare(value)):
            return name, _bare(value)
    for name, value in headers.items():
        if _JWT_RE.match(_bare(value)):
            return name, _bare(value)
    raise CallbackSignatureError(f"No JWT in header {plugin_settings.CALLBACK_SIGNATURE_HEADER} or any other header")


def _candidate_keys(token: str, jwks: dict) -> list[tuple[object, str]]:
    try:
        header = jwt.get_unverified_header(token)
    except InvalidTokenError as exc:
        raise CallbackSignatureError(f"Unreadable token header: {exc}") from exc
    alg = header.get("alg")
    if alg not in ALLOWED_ALGORITHMS:
        raise CallbackSignatureError(f"Token algorithm {alg!r} is not RS256 or RS512")
    kid = header.get("kid")
    keys = [k for k in jwks.get("keys", []) if k.get("kty") == "RSA" and k.get("alg", alg) == alg]
    if kid:
        keys = [k for k in keys if k.get("kid") == kid]
        if not keys:
            raise KeyError(kid)
    return [(jwt.PyJWK.from_dict(k, algorithm=alg).key, alg) for k in keys]


def verify_callback_signature(headers: dict[str, str]) -> tuple[dict, str]:
    """Return (claims, header name) or raise CallbackSignatureError. GatewayCertsError propagates."""
    header_name, token = find_token(headers)
    try:
        candidates = _candidate_keys(token, get_jwks())
    except KeyError:
        try:
            candidates = _candidate_keys(token, get_jwks(force_refresh=True))
        except KeyError as exc:
            raise CallbackSignatureError(f"Unknown signing key kid={exc.args[0]}") from exc
    last = "no RSA key matched"
    leeway = max(0, int(plugin_settings.CALLBACK_SIGNATURE_LEEWAY_SECONDS or 0))
    for key, alg in candidates:
        try:
            claims = jwt.decode(token, key=key, algorithms=[alg], leeway=leeway, options={"verify_aud": False})
            return claims, header_name
        except InvalidTokenError as exc:
            last = str(exc)
    raise CallbackSignatureError(f"Signature did not verify: {last}")


def seconds_late(claims: dict, now: datetime | None = None) -> int:
    """How many seconds after its `exp` the token arrived. 0 when it was still valid."""
    expiry = claims.get("exp")
    if not isinstance(expiry, (int, float)):
        return 0
    moment = now or datetime.now(UTC)
    return max(0, int(moment.timestamp() - float(expiry)))
