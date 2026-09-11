import jwt
from jwt import InvalidTokenError

from abdm.gateway.certs import get_jwks
from abdm.settings import plugin_settings


class CallbackSignatureError(Exception):
    pass


def _extract_token(headers: dict[str, str]) -> str:
    name = plugin_settings.CALLBACK_SIGNATURE_HEADER
    value = ""
    for key, header_value in headers.items():
        if key.lower() == name.lower():
            value = header_value
            break
    if not value:
        raise CallbackSignatureError(f"Missing callback signature header: {name}")
    if value.lower().startswith("bearer "):
        return value.split(" ", 1)[1].strip()
    return value.strip()


def _key_for_token(token: str, jwks: dict) -> object:
    try:
        header = jwt.get_unverified_header(token)
    except InvalidTokenError as exc:
        raise CallbackSignatureError(str(exc)) from exc
    if header.get("alg") != "RS256":
        raise CallbackSignatureError("Callback signature algorithm must be RS256")
    kid = header.get("kid")
    if not kid:
        raise CallbackSignatureError("Callback signature has no kid")
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return jwt.PyJWK.from_dict(key, algorithm="RS256").key
    raise KeyError(kid)


def verify_callback_signature(headers: dict[str, str], *, force_jwks_refresh: bool = False) -> dict:
    token = _extract_token(headers)
    jwks = get_jwks(force_refresh=force_jwks_refresh)
    try:
        key = _key_for_token(token, jwks)
    except KeyError as exc:
        try:
            key = _key_for_token(token, get_jwks(force_refresh=True))
        except KeyError as refresh_exc:
            raise CallbackSignatureError(f"Unknown callback signature key: {exc.args[0]}") from refresh_exc
    try:
        return jwt.decode(token, key=key, algorithms=["RS256"], options={"verify_aud": False})
    except InvalidTokenError as exc:
        raise CallbackSignatureError(str(exc)) from exc
