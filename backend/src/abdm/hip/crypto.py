"""
Data-transfer encryption for the HIP side (pure: no Django imports).

Docs (/docs/hiecm/v3/concepts/data-flow, "The encryption"):
  1. Generate a key pair DHSK(P), DHPK(P) in the group the HIU specified (Curve25519).
  2. Generate a 32-byte random value RAND(P).
  3. Compute the shared key DHK(U,P) from the HIU public key and the HIP private key.
  4. Derive the salt and IV by XOR of RAND(P) and RAND(U): first 20 bytes salt, last 12 bytes IV.
  5. Compute a 256-bit AES-GCM session key with HKDF from the shared key and that salt.
  6. Encrypt the data with that key and that IV.
The HIP sends DHPK(P), RAND(P) and the encrypted data.

Wire format (/docs/hiecm/v3/api/m3/endpoints/m3-on-health-information-transfer):
  keyMaterial.dhPublicKey.keyValue  base64 ECDH public key, "32 bytes for Curve25519"
  keyMaterial.nonce                 base64 random nonce, 32 bytes
  entries[].content                 the encrypted bundle
  entries[].checksum                MD5 of the content before encryption

Assumptions the docs leave open (docs/findings.md): HKDF hash = SHA-256, HKDF info empty,
content = base64(ciphertext || GCM tag). A key value that is not 32 raw bytes is read as
DER SubjectPublicKeyInfo.
"""

import base64
import hashlib
import secrets
from dataclasses import dataclass

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

NONCE_BYTES = 32
SALT_BYTES = 20
IV_BYTES = 12
KEY_BYTES = 32


class KeyMaterialError(ValueError):
    pass


@dataclass(frozen=True)
class SessionKeys:
    private_key: X25519PrivateKey
    nonce: bytes  # RAND(P)

    @property
    def public_key_b64(self) -> str:
        raw = self.private_key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        return base64.b64encode(raw).decode("ascii")

    @property
    def nonce_b64(self) -> str:
        return base64.b64encode(self.nonce).decode("ascii")


def new_session_keys() -> SessionKeys:
    return SessionKeys(private_key=X25519PrivateKey.generate(), nonce=secrets.token_bytes(NONCE_BYTES))


def load_public_key(key_value_b64: str) -> X25519PublicKey:
    try:
        raw = base64.b64decode(key_value_b64 or "", validate=False)
    except (ValueError, TypeError) as exc:
        raise KeyMaterialError("dhPublicKey.keyValue is not base64") from exc
    if len(raw) == KEY_BYTES:
        return X25519PublicKey.from_public_bytes(raw)
    try:
        key = serialization.load_der_public_key(raw)
    except (ValueError, TypeError) as exc:
        raise KeyMaterialError("dhPublicKey.keyValue is neither 32 raw bytes nor DER") from exc
    if not isinstance(key, X25519PublicKey):
        raise KeyMaterialError("dhPublicKey.keyValue is not a Curve25519 key")
    return key


def load_nonce(nonce_b64: str) -> bytes:
    try:
        nonce = base64.b64decode(nonce_b64 or "", validate=False)
    except (ValueError, TypeError) as exc:
        raise KeyMaterialError("nonce is not base64") from exc
    if len(nonce) != NONCE_BYTES:
        raise KeyMaterialError(f"nonce must be {NONCE_BYTES} bytes, got {len(nonce)}")
    return nonce


def check_key_material(key_material: dict) -> tuple[X25519PublicKey, bytes]:
    """Step 'check the encryption parameters': algorithm, curve, public key and nonce."""
    if not isinstance(key_material, dict):
        raise KeyMaterialError("keyMaterial missing")
    if str(key_material.get("cryptoAlg") or "").rstrip(".").upper() != "ECDH":
        raise KeyMaterialError(f"cryptoAlg must be ECDH, got {key_material.get('cryptoAlg')!r}")
    if str(key_material.get("curve") or "").lower() != "curve25519":
        raise KeyMaterialError(f"curve must be Curve25519, got {key_material.get('curve')!r}")
    public = key_material.get("dhPublicKey") if isinstance(key_material.get("dhPublicKey"), dict) else {}
    return load_public_key(str(public.get("keyValue") or "")), load_nonce(str(key_material.get("nonce") or ""))


def derive_key_and_iv(private_key: X25519PrivateKey, peer_public: X25519PublicKey, own_nonce: bytes, peer_nonce: bytes):
    shared = private_key.exchange(peer_public)
    mixed = bytes(a ^ b for a, b in zip(own_nonce, peer_nonce, strict=True))
    salt, iv = mixed[:SALT_BYTES], mixed[-IV_BYTES:]
    key = HKDF(algorithm=hashes.SHA256(), length=KEY_BYTES, salt=salt, info=b"").derive(shared)
    return key, iv


def encrypt(plaintext: bytes, keys: SessionKeys, peer_public: X25519PublicKey, peer_nonce: bytes) -> str:
    key, iv = derive_key_and_iv(keys.private_key, peer_public, keys.nonce, peer_nonce)
    return base64.b64encode(AESGCM(key).encrypt(iv, plaintext, None)).decode("ascii")


def decrypt(
    content_b64: str, private_key: X25519PrivateKey, own_nonce: bytes, peer_public: X25519PublicKey, peer_nonce: bytes
) -> bytes:
    """The HIU side of the same derivation. Used by the tests and later by M3."""
    key, iv = derive_key_and_iv(private_key, peer_public, own_nonce, peer_nonce)
    return AESGCM(key).decrypt(iv, base64.b64decode(content_b64), None)


def md5_checksum(plaintext: bytes) -> str:
    return hashlib.md5(plaintext, usedforsecurity=False).hexdigest()


def key_material_block(keys: SessionKeys, expiry_iso: str) -> dict:
    return {
        "cryptoAlg": "ECDH",
        "curve": "Curve25519",
        "dhPublicKey": {"expiry": expiry_iso, "parameters": "Curve25519/32byte", "keyValue": keys.public_key_b64},
        "nonce": keys.nonce_b64,
    }
