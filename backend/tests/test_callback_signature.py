import unittest
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.utils import base64url_encode

from abdm.callbacks.signature import CallbackSignatureError, verify_callback_signature
from abdm.settings import plugin_settings


def _jwk(public_key, kid: str) -> dict:
    numbers = public_key.public_numbers()
    return {
        "kty": "RSA",
        "kid": kid,
        "use": "sig",
        "alg": "RS256",
        "n": base64url_encode(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")).decode("ascii"),
        "e": base64url_encode(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")).decode("ascii"),
    }


class CallbackSignatureTests(unittest.TestCase):
    def setUp(self):
        plugin_settings.CALLBACK_SIGNATURE_HEADER = "Authorization"

    def test_verify_callback_signature_accepts_rs256_jwks(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        token = jwt.encode({"iss": "abdm-gateway"}, private_key, algorithm="RS256", headers={"kid": "test-key"})
        with patch(
            "abdm.callbacks.signature.get_jwks",
            return_value={"keys": [_jwk(private_key.public_key(), "test-key")]},
        ):
            claims = verify_callback_signature({"Authorization": f"Bearer {token}"})
        self.assertEqual(claims["iss"], "abdm-gateway")

    def test_verify_callback_signature_rejects_tampered_token(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        token = jwt.encode({"iss": "abdm-gateway"}, private_key, algorithm="RS256", headers={"kid": "test-key"})
        # Change the first character of the signature. The last character is
        # partly base64 padding, so a change there does not always alter the
        # signature bytes.
        header, payload, signature = token.split(".")
        bad_token = f"{header}.{payload}.{'A' if signature[0] != 'A' else 'B'}{signature[1:]}"
        with patch(
            "abdm.callbacks.signature.get_jwks",
            return_value={"keys": [_jwk(private_key.public_key(), "test-key")]},
        ):
            with self.assertRaises(CallbackSignatureError):
                verify_callback_signature({"Authorization": f"Bearer {bad_token}"})

    def test_verify_callback_signature_rejects_unknown_kid(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        token = jwt.encode({"iss": "abdm-gateway"}, private_key, algorithm="RS256", headers={"kid": "missing-key"})
        with patch("abdm.callbacks.signature.get_jwks", return_value={"keys": []}):
            with self.assertRaises(CallbackSignatureError):
                verify_callback_signature({"Authorization": f"Bearer {token}"})


if __name__ == "__main__":
    unittest.main()
