import base64
import unittest

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

from abdm.hip import crypto


class DataTransferCryptoTests(unittest.TestCase):
    def _hiu(self):
        priv = X25519PrivateKey.generate()
        raw = priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        nonce = crypto.secrets.token_bytes(32)
        material = {
            "cryptoAlg": "ECDH",
            "curve": "Curve25519",
            "dhPublicKey": {"expiry": "2027-01-01T00:00:00.000Z", "parameters": "Curve25519/32byte", "keyValue": base64.b64encode(raw).decode()},
            "nonce": base64.b64encode(nonce).decode(),
        }
        return priv, nonce, material

    def test_hiu_decrypts_what_the_hip_encrypted(self):
        hiu_priv, hiu_nonce, material = self._hiu()
        hip = crypto.new_session_keys()
        peer_public, peer_nonce = crypto.check_key_material(material)
        content = crypto.encrypt(b'{"resourceType":"Bundle"}', hip, peer_public, peer_nonce)
        block = crypto.key_material_block(hip, "2027-01-01T00:00:00.000Z")
        hip_public = crypto.load_public_key(block["dhPublicKey"]["keyValue"])
        plain = crypto.decrypt(content, hiu_priv, hiu_nonce, hip_public, crypto.load_nonce(block["nonce"]))
        self.assertEqual(plain, b'{"resourceType":"Bundle"}')

    def test_key_material_checks_reject_wrong_algorithm_curve_and_sizes(self):
        _, _, material = self._hiu()
        with self.assertRaises(crypto.KeyMaterialError):
            crypto.check_key_material({**material, "cryptoAlg": "RSA"})
        with self.assertRaises(crypto.KeyMaterialError):
            crypto.check_key_material({**material, "curve": "P-256"})
        with self.assertRaises(crypto.KeyMaterialError):
            crypto.check_key_material({**material, "nonce": base64.b64encode(b"short").decode()})
        with self.assertRaises(crypto.KeyMaterialError):
            crypto.check_key_material({**material, "dhPublicKey": {**material["dhPublicKey"], "keyValue": "not-a-key"}})

    def test_der_encoded_public_key_is_accepted(self):
        priv = X25519PrivateKey.generate()
        der = priv.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        self.assertIsNotNone(crypto.load_public_key(base64.b64encode(der).decode()))

    def test_checksum_is_md5_of_plaintext(self):
        self.assertEqual(crypto.md5_checksum(b""), "d41d8cd98f00b204e9800998ecf8427e")
