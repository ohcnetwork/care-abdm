import unittest

from abdm.callbacks.paths import CALLBACK_OPERATION_BY_PATH, normalize_path, operation_for_path


class CallbackPathTests(unittest.TestCase):
    def test_real_gateway_path_carries_an_api_prefix_the_docs_omit(self):
        # Observed 2026-09-17: POST {bridgeUrl}/api/v3/hip/token/on-generate-token
        self.assertEqual(operation_for_path("/api/v3/hip/token/on-generate-token"), "m2-on-generate-token-result")
        self.assertEqual(operation_for_path("/v3/hip/token/on-generate-token"), "m2-on-generate-token-result")
        self.assertEqual(operation_for_path("api/v3/link/on_carecontext/"), "m2-on-carecontext-result")

    def test_every_documented_spelling_resolves(self):
        cases = {
            "/api/v3/hip/patient/care-context/discover": "m2-on-discovery-request",
            "/v0.5/care-contexts/discover": "m2-on-discovery-request",
            "/api/v3/hip/link/care-context/init": "m2-on-link-init",
            "/v0.5/links/link/confirm": "m2-on-link-confirm",
            "/api/v3/consent/request/hip/notify": "m2-consent-hip-notify",
            "/v0.5/consents/hip/notify": "m2-consent-hip-notify",
            "/api/v3/hip/health-information/request": "m2-on-health-information-request",
            "/patient-share/v3/share": "m1-receive-patient-share",
            "/api/v3/hip/patient/share": "m1-receive-patient-share",
        }
        for path, operation in cases.items():
            with self.subTest(path=path):
                self.assertEqual(operation_for_path(path), operation)

    def test_unknown_path_is_kept_but_unnamed(self):
        self.assertEqual(operation_for_path("/api/v9/something"), "")
        self.assertEqual(operation_for_path(""), "")

    def test_normalize_strips_only_a_leading_api_segment(self):
        self.assertEqual(normalize_path("/api/v3/x"), "/v3/x")
        self.assertEqual(normalize_path("/apiv3/x"), "/apiv3/x")
        self.assertEqual(normalize_path("/v3/api/x"), "/v3/api/x")

    def test_table_holds_no_api_prefixed_keys(self):
        for path in CALLBACK_OPERATION_BY_PATH:
            self.assertFalse(path.startswith("/api/"), path)
