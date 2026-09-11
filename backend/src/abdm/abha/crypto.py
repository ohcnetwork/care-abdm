"""
RSA encryption of sensitive M1 inputs (Aadhaar, mobile, OTP, ...).

Docs: /docs/hiecm/v3/concepts/encryption — "encrypt against the ABDM public key,
base64 of the ciphertext goes in the field". Padding is only stated in the
catalogue summary: RSA-OAEP with SHA-1.

Verified on sandbox 2026-09-09 (docs/findings.md): OAEP-SHA1 accepted; PKCS1v15
and OAEP-SHA256 rejected with `400 Invalid LoginId`.
Public key: GET {ABHA_URL}/v3/profile/public/certificate -> {"publicKey": base64 DER SPKI}
(the documented `/profile/public/certificate` returns 404).
"""

import base64

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from django.core.cache import cache

from abdm.gateway.session import gateway_headers, get_access_token
from abdm.settings import plugin_settings

PUBLIC_CERT_PATH = "/v3/profile/public/certificate"
CACHE_KEY = "abdm:abha:public_key_der"
CACHE_TTL = 6 * 60 * 60  # NHA rotates rarely; a bad key surfaces as 400 Invalid LoginId -> invalidate

_PADDING = padding.OAEP(mgf=padding.MGF1(hashes.SHA1()), algorithm=hashes.SHA1(), label=None)


def fetch_public_key_der() -> bytes:
    headers = gateway_headers(get_access_token())
    headers.pop("X-CM-ID", None)
    response = requests.get(
        f"{plugin_settings.ABHA_URL}{PUBLIC_CERT_PATH}",
        headers=headers,
        timeout=plugin_settings.REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return base64.b64decode(response.json()["publicKey"])


def get_public_key():
    der = cache.get(CACHE_KEY)
    if der is None:
        der = fetch_public_key_der()
        cache.set(CACHE_KEY, der, timeout=CACHE_TTL)
    return serialization.load_der_public_key(der)


def invalidate_public_key() -> None:
    cache.delete(CACHE_KEY)


def encrypt(value: str, public_key=None) -> str:
    """RSA-OAEP(SHA-1) encrypt `value`, return base64 ciphertext for `loginId`/`otpValue`/... fields."""
    key = public_key or get_public_key()
    return base64.b64encode(key.encrypt(value.encode("utf-8"), _PADDING)).decode("ascii")
