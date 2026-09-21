"""The M1 ABHA-service calls join the audit table (ADR-018): the operation id is the docs' page slug form."""

import unittest

from abdm.abha.client import operation_id_for


class OperationIdTests(unittest.TestCase):
    def test_docs_slug_form(self):
        self.assertEqual(operation_id_for("POST", "/v3/enrollment/request/otp"), "m1-post-v3-enrollment-request-otp")
        self.assertEqual(operation_id_for("GET", "/v3/profile/account"), "m1-get-v3-profile-account")
        self.assertEqual(
            operation_id_for("get", "/v3/profile/account/abha-card?x=1"), "m1-get-v3-profile-account-abha-card"
        )
        self.assertEqual(
            operation_id_for("POST", "/v3/phr/web/login/abha/request/otp"), "m1-post-v3-phr-web-login-abha-request-otp"
        )
        self.assertEqual(
            operation_id_for("GET", "/v3/profile/account/request/token"), "m1-get-v3-profile-account-request-token"
        )


if __name__ == "__main__":
    unittest.main()
