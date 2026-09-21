"""Redaction for the developer explorer (ADR-018): by name and length, never by value."""

import unittest

from abdm.dev import redact as r

TOKEN = "eyJhbGciOiJSUzI1NiJ9." + "a" * 700
CIPHERTEXT = "Q" * 344  # an RSA-2048 block in base64


class RedactTests(unittest.TestCase):
    def test_secret_keys_by_name_and_length(self):
        body = {
            "tokens": {"token": TOKEN, "refreshToken": TOKEN, "expiresIn": 1800},
            "linkToken": TOKEN,
            "password": "Secret@123",
            "otp": "123456",
            "Authorization": f"Bearer {TOKEN}",
            "x-hprid-auth": TOKEN,
            "photo": "/9j/" + "A" * 100,
            "kycPhoto": "x",
            "privateKey": "k" * 44,
        }
        out = r.redact(body)
        self.assertEqual(out["tokens"]["token"], f"<redacted, {len(TOKEN)} chars>")
        self.assertEqual(out["tokens"]["refreshToken"], f"<redacted, {len(TOKEN)} chars>")
        self.assertEqual(out["tokens"]["expiresIn"], 1800)
        self.assertEqual(out["linkToken"], f"<redacted, {len(TOKEN)} chars>")
        self.assertEqual(out["password"], "<redacted, 10 chars>")
        self.assertEqual(out["otp"], "<redacted, 6 chars>")
        self.assertEqual(out["Authorization"], f"<redacted, {len(TOKEN) + 7} chars>")
        self.assertEqual(out["x-hprid-auth"], f"<redacted, {len(TOKEN)} chars>")
        self.assertEqual(out["photo"], "<redacted, 104 chars>")
        self.assertEqual(out["kycPhoto"], "<redacted, 1 chars>")
        self.assertEqual(out["privateKey"], "<redacted, 44 chars>")
        # The input is not touched.
        self.assertEqual(body["password"], "Secret@123")

    def test_encrypted_fields_only_when_the_value_is_a_ciphertext(self):
        out = r.redact(
            {
                "loginId": CIPHERTEXT,
                "otp": {"txnId": "t", "otpValue": CIPHERTEXT, "mobile": "9876543210"},
                "mobileNumber": "******6128",
                "mobile": CIPHERTEXT,
            }
        )
        self.assertEqual(out["loginId"], "<encrypted, 344 chars>")
        self.assertEqual(out["otp"]["otpValue"], "<encrypted, 344 chars>")
        # A plain or masked number under the same keys stays readable.
        self.assertEqual(out["otp"]["mobile"], "9876543210")
        self.assertEqual(out["mobileNumber"], "******6128")
        self.assertEqual(out["mobile"], "<encrypted, 344 chars>")

    def test_long_base64_under_any_key(self):
        blob = "A" * 600
        out = r.redact({"facilityUploads": {"facilityBoardPhoto": {"name": "board.jpg", "value": blob}}})
        self.assertEqual(out["facilityUploads"]["facilityBoardPhoto"]["value"], "<600 chars, base64>")
        self.assertEqual(out["facilityUploads"]["facilityBoardPhoto"]["name"], "board.jpg")
        # A long sentence is not base64.
        text = "word " * 200
        self.assertEqual(r.redact({"message": text})["message"], text)

    def test_lists_nulls_numbers_and_markers(self):
        out = r.redact([{"token": "abc"}, {"code": "ABDM-1092"}, None, 7, "plain"])
        self.assertEqual(out, [{"token": "<redacted, 3 chars>"}, {"code": "ABDM-1092"}, None, 7, "plain"])
        # A value already redacted is left alone, so a second pass does not grow the length.
        once = r.redact({"token": TOKEN})
        self.assertEqual(r.redact(once), once)
        # An empty secret stays empty: the reader sees that nothing was sent.
        self.assertEqual(r.redact({"token": ""}), {"token": ""})

    def test_header_names(self):
        names = r.header_names({"Authorization": f"Bearer {TOKEN}", "REQUEST-ID": "abc", "X-HIP-ID": None})
        self.assertEqual(names, {"Authorization": len(TOKEN) + 7, "REQUEST-ID": 3, "X-HIP-ID": 0})
        self.assertEqual(r.header_names(None), {})

    def test_redact_fields_for_a_table_row(self):
        row = {"x_token": TOKEN, "refresh_token": "", "abha_address": "nihal_99@sbx", "profile": {"kycPhoto": "zz"}}
        out = r.redact_fields(row, secret_fields=("x_token", "refresh_token"))
        self.assertEqual(out["x_token"], f"<redacted, {len(TOKEN)} chars>")
        self.assertEqual(out["refresh_token"], "")
        self.assertEqual(out["abha_address"], "nihal_99@sbx")
        self.assertEqual(out["profile"]["kycPhoto"], "<redacted, 2 chars>")


if __name__ == "__main__":
    unittest.main()
