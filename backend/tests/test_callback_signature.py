import unittest
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.utils import base64url_encode

from abdm.callbacks.signature import CallbackSignatureError, find_token, verify_callback_signature
from abdm.settings import plugin_settings


def _jwk(public_key, kid: str, alg: str = "RS256") -> dict:
    numbers = public_key.public_numbers()
    return {
        "kty": "RSA",
        "kid": kid,
        "use": "sig",
        "alg": alg,
        "n": base64url_encode(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")).decode("ascii"),
        "e": base64url_encode(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")).decode("ascii"),
    }


class CallbackSignatureTests(unittest.TestCase):
    def setUp(self):
        plugin_settings.CALLBACK_SIGNATURE_HEADER = "Authorization"
        plugin_settings.CALLBACK_SIGNATURE_LEEWAY_SECONDS = 3600
        self.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        # The sandbox set (2026-09-15) holds an RS256 key and an RS512 key.
        self.jwks = {"keys": [_jwk(self.key.public_key(), "k256"), _jwk(self.other.public_key(), "k512", "RS512")]}

    def _token(self, key=None, alg="RS256", kid="k256", claims=None):
        return jwt.encode(claims or {"iss": "abdm-gateway"}, key or self.key, algorithm=alg, headers={"kid": kid})

    def test_accepts_rs256_bearer_in_the_configured_header(self):
        with patch("abdm.callbacks.signature.get_jwks", return_value=self.jwks):
            claims, header = verify_callback_signature({"Authorization": f"Bearer {self._token()}"})
        self.assertEqual((claims["iss"], header), ("abdm-gateway", "Authorization"))

    def test_accepts_rs512_when_the_jwk_declares_it(self):
        token = self._token(key=self.other, alg="RS512", kid="k512")
        with patch("abdm.callbacks.signature.get_jwks", return_value=self.jwks):
            claims, _ = verify_callback_signature({"Authorization": token})
        self.assertEqual(claims["iss"], "abdm-gateway")

    def test_finds_the_token_in_an_unnamed_header(self):
        headers = {"Authorization": "Bearer not-a-jwt", "X-Gateway-Signature": self._token()}
        with patch("abdm.callbacks.signature.get_jwks", return_value=self.jwks):
            _, header = verify_callback_signature(headers)
        self.assertEqual(header, "X-Gateway-Signature")

    def test_rejects_tampered_token(self):
        token = self._token()
        head, payload, sig = token.split(".")
        tampered = f"{head}.{payload[:-2]}AA.{sig}"
        with patch("abdm.callbacks.signature.get_jwks", return_value=self.jwks):
            with self.assertRaises(CallbackSignatureError):
                verify_callback_signature({"Authorization": f"Bearer {tampered}"})

    def test_rejects_token_signed_by_an_unknown_key(self):
        stranger = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        token = self._token(key=stranger, kid="k256")
        with patch("abdm.callbacks.signature.get_jwks", return_value=self.jwks):
            with self.assertRaises(CallbackSignatureError):
                verify_callback_signature({"Authorization": token})

    def test_rejects_non_rsa_algorithm(self):
        token = jwt.encode({"iss": "x"}, "secret", algorithm="HS256", headers={"kid": "k256"})
        with patch("abdm.callbacks.signature.get_jwks", return_value=self.jwks):
            with self.assertRaises(CallbackSignatureError):
                verify_callback_signature({"Authorization": token})

    def test_unknown_kid_refreshes_the_jwks_once_then_fails(self):
        token = self._token(kid="rotated")
        with patch("abdm.callbacks.signature.get_jwks", return_value=self.jwks) as get:
            with self.assertRaises(CallbackSignatureError):
                verify_callback_signature({"Authorization": token})
        self.assertEqual(get.call_count, 2)

    def test_missing_signature_names_the_configured_header(self):
        with self.assertRaises(CallbackSignatureError) as ctx:
            find_token({"Content-Type": "application/json", "REQUEST-ID": "abc"})
        self.assertIn("Authorization", str(ctx.exception))
