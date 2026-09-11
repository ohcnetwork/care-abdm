import base64
import unittest

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from abdm.abha.crypto import encrypt


class CryptoTests(unittest.TestCase):
    def test_encrypt_uses_rsa_oaep_sha1_and_base64(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        plaintext = "synthetic-secret"

        ciphertext = base64.b64decode(encrypt(plaintext, public_key=private_key.public_key()))

        decrypted = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None,
            ),
        )
        self.assertEqual(decrypted.decode("utf-8"), plaintext)


if __name__ == "__main__":
    unittest.main()
