"""
RSA encryption for the NHPR (M4). Pure except for the certificate fetch.

registries/nhpr/hpr §What your system has to hold: "the public certificate from `v4/int/api/v1/auth/cert`.
Three fields are encrypted with it, cipher `RSA/ECB/PKCS1Padding`: the mobile number in mobile match,
the OTP in mobile login, and the email and password in create HPID. That cipher and that certificate
belong to the NHPR. M1 encrypts with RSA-OAEP and SHA-1 under the ABHA certificate, so the two paths
are not interchangeable."

The certificate page (m4-authentication/02) publishes no response shape, so `load_public_key()` reads
PEM (certificate or key), base64 DER (SubjectPublicKeyInfo or X.509) and a JSON wrapper with a
`publicKey` / `certificate` / `key` field. `docs/findings.md` N4.
"""

import base64
import json
import re

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

_PADDING = padding.PKCS1v15()
_PEM_RE = re.compile(r"-----BEGIN [A-Z ]+-----.*?-----END [A-Z ]+-----", re.S)


class CertificateError(ValueError):
    pass


def _from_pem(text: str):
    block = _PEM_RE.search(text)
    if not block:
        raise CertificateError("no PEM block")
    pem = block.group(0).encode("ascii")
    if b"CERTIFICATE" in pem:
        return x509.load_pem_x509_certificate(pem).public_key()
    return serialization.load_pem_public_key(pem)


def _from_der(raw: bytes):
    try:
        return serialization.load_der_public_key(raw)
    except ValueError:
        return x509.load_der_x509_certificate(raw).public_key()


def load_public_key(body: str | bytes | dict):
    """The RSA public key behind whatever `GET /api/v1/auth/cert` answers."""
    text = body.decode("utf-8", errors="replace") if isinstance(body, bytes) else body
    if isinstance(text, dict):
        payload = text
    else:
        payload = None
        stripped = (text or "").strip()
        if stripped.startswith("{"):
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                payload = None
    if isinstance(payload, dict):
        for key in ("publicKey", "certificate", "cert", "key", "publicCertificate"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return load_public_key(value)
        raise CertificateError("certificate JSON carries no publicKey, certificate, cert or key field")
    stripped = (text or "").strip()
    if not stripped:
        raise CertificateError("empty certificate response")
    if "-----BEGIN" in stripped:
        key = _from_pem(stripped)
    else:
        try:
            raw = base64.b64decode(re.sub(r"\s+", "", stripped), validate=True)
        except (ValueError, TypeError) as exc:
            raise CertificateError("certificate is neither PEM nor base64") from exc
        try:
            key = _from_der(raw)
        except ValueError as exc:
            raise CertificateError("certificate bytes are neither SubjectPublicKeyInfo nor X.509") from exc
    if not isinstance(key, rsa.RSAPublicKey):
        raise CertificateError("the NHPR certificate is not an RSA key")
    return key


def encrypt(value: str, public_key) -> str:
    """RSA/ECB/PKCS1Padding, base64: the shape the mobile-match, mobile-OTP and create-HPID fields take."""
    return base64.b64encode(public_key.encrypt(value.encode("utf-8"), _PADDING)).decode("ascii")
