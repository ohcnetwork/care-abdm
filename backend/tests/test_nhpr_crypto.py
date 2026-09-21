import base64
import json
import unittest

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509.oid import NameOID

from abdm.nhpr import crypto


def _key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def _cert_pem(private):
    import datetime

    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "nhpr-test")])
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private.public_key())
        .serial_number(1)
        .not_valid_before(datetime.datetime(2026, 1, 1))
        .not_valid_after(datetime.datetime(2030, 1, 1))
        .sign(private, hashes.SHA256())
    )
    return cert.public_bytes(serialization.Encoding.PEM).decode()


class NhprCryptoTests(unittest.TestCase):
    def test_pkcs1_ciphertext_decrypts_with_the_private_key(self):
        private = _key()
        pem = (
            private.public_key()
            .public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
            .decode()
        )
        encrypted = crypto.encrypt("9810651234", crypto.load_public_key(pem))
        plain = private.decrypt(base64.b64decode(encrypted), padding.PKCS1v15())
        self.assertEqual(plain, b"9810651234")

    def test_load_every_documented_and_undocumented_shape(self):
        private = _key()
        spki_der = private.public_key().public_bytes(
            serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo
        )
        spki_pem = (
            private.public_key()
            .public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
            .decode()
        )
        cert_pem = _cert_pem(private)
        for body in (
            spki_pem,
            cert_pem,
            base64.b64encode(spki_der).decode(),
            json.dumps({"publicKey": base64.b64encode(spki_der).decode()}),
            {"certificate": cert_pem},
            spki_pem.encode(),
        ):
            with self.subTest(body=type(body).__name__):
                key = crypto.load_public_key(body)
                self.assertEqual(key.public_numbers(), private.public_key().public_numbers())

    def test_garbage_is_refused(self):
        with self.assertRaises(crypto.CertificateError):
            crypto.load_public_key("")
        with self.assertRaises(crypto.CertificateError):
            crypto.load_public_key("not a key")
        with self.assertRaises(crypto.CertificateError):
            crypto.load_public_key({"message": "no key here"})


if __name__ == "__main__":
    unittest.main()
