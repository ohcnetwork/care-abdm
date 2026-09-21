"""
Redaction for the developer explorer (ADR-018). Pure: no Django import, so backend/tests can import it.

Rule (abdm-m2/references/design.md, "What the integrator needs on screen"): "Redact by name and
length, never by value. Show that an `Authorization` header was sent and how long it was. Never its
contents. The panel is a browser."

3 kinds of value are hidden:
  - a secret (a token, a password, an OTP, a key, a photo): `<redacted, N chars>`;
  - an RSA ciphertext the plug made (an encrypted Aadhaar, mobile, OTP or password on its way to
    ABDM): `<encrypted, N chars>`, so a reader sees that the field went out encrypted;
  - a long base64 blob under any other key (an attachment, a certificate body): `<N chars, base64>`.
Everything else is shown as it came. Key matching is case-insensitive and ignores `-` and `_`.
"""

import re

SECRET_KEYS = frozenset(
    key.lower().replace("-", "").replace("_", "")
    for key in (
        # tokens of every kind the docs name
        "token",
        "accessToken",
        "refreshToken",
        "linkToken",
        "hprToken",
        "X-token",
        "T-token",
        "R-token",
        "x-hprid-auth",
        "authorization",
        "cookie",
        "set-cookie",
        "clientId",
        "clientSecret",
        "client_secret",
        # credentials a person typed
        "password",
        "otp",
        "otp_hash",
        # key material a row holds
        "privateKey",
        "private_key",
        # pictures of a person
        "photo",
        "kycPhoto",
        "profilePhoto",
        "kyc_photo",
        "profile_photo",
        # the plug's own column names for the same things
        "x_token",
        "refresh_token",
        "link_token",
    )
)

# Fields the plug sends RSA-encrypted (M1: loginId, otpValue; M4: mobile, otp, password). The same
# keys come back plain and masked in answers (`mobileNumber: "******6128"`), so a value under one of
# these keys is marked encrypted only when it is a ciphertext: base64, and at least as long as an
# RSA-2048 block (344 chars).
ENCRYPTED_KEYS = frozenset(
    key.lower()
    for key in ("loginId", "otpValue", "encryptedData", "mobile", "mobileNumber", "aadhaar", "aadhaarNumber")
)
CIPHERTEXT_CHARS = 200

# A base64 blob this long is an attachment or a certificate, not a value a reader compares.
LONG_BASE64_CHARS = 512
_BASE64_RE = re.compile(r"^[A-Za-z0-9+/=_\-]+$")
_REDACTED_RE = re.compile(r"^<(redacted|encrypted), \d+ chars>$|^<\d+ chars, base64>$")


def _norm(key) -> str:
    return str(key).lower().replace("-", "").replace("_", "")


def is_secret_key(key) -> bool:
    return _norm(key) in SECRET_KEYS


def is_encrypted_key(key) -> bool:
    return str(key).lower() in ENCRYPTED_KEYS


def is_redaction_marker(value) -> bool:
    return isinstance(value, str) and bool(_REDACTED_RE.match(value))


def _looks_base64(value: str, at_least: int = LONG_BASE64_CHARS) -> bool:
    return len(value) >= at_least and bool(_BASE64_RE.match(value))


def redact(value, key=None):
    """A copy of `value` with every secret replaced by its kind and length. Safe on any JSON shape."""
    if isinstance(value, dict):
        return {k: redact(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v, key) for v in value]
    if isinstance(value, str):
        if is_redaction_marker(value):
            return value
        if key is not None and is_secret_key(key) and value:
            return f"<redacted, {len(value)} chars>"
        if key is not None and is_encrypted_key(key) and _looks_base64(value, CIPHERTEXT_CHARS):
            return f"<encrypted, {len(value)} chars>"
        if _looks_base64(value):
            return f"<{len(value)} chars, base64>"
        return value
    return value


def header_names(headers) -> dict:
    """`{name: length}` for a header set: the names are the finding, the values are credentials."""
    out = {}
    for name, value in (headers or {}).items():
        out[str(name)] = len(str(value if value is not None else ""))
    return out


def redact_fields(row: dict, secret_fields=()) -> dict:
    """A table row as a dict: the named fields become `<redacted, N chars>` (an empty one stays
    empty), and every JSON field goes through `redact()`."""
    out = {}
    for name, value in row.items():
        if name in secret_fields:
            text = "" if value in (None, "") else str(value)
            out[name] = f"<redacted, {len(text)} chars>" if text else value
        else:
            out[name] = redact(value, name)
    return out
