import unittest

from abdm.share.rules import ack_body, prefill_profile, token_number, validate_counters

CONFIG = {"facility_id": "IN0810000177", "hip_id": "CARE_SBX_HIP", "hip_name": "Care Sandbox"}


class CounterRulesTests(unittest.TestCase):
    def test_accepts_alphanumeric_up_to_20(self):
        self.assertEqual(validate_counters(["OPD1", " Pharmacy ", "", "A" * 20], CONFIG), ["OPD1", "Pharmacy", "A" * 20])

    def test_rejects_symbols_and_length(self):
        with self.assertRaises(ValueError):
            validate_counters(["OPD cardio"], CONFIG)
        with self.assertRaises(ValueError):
            validate_counters(["A" * 21], CONFIG)

    def test_rejects_identity_values_and_duplicates(self):
        for bad in ("IN0810000177", "care_sbx_hip"):
            with self.assertRaises(ValueError):
                validate_counters([bad], CONFIG)
        with self.assertRaises(ValueError):
            validate_counters(["OPD1", "opd1"], CONFIG)


class AckBodyTests(unittest.TestCase):
    def test_success_body(self):
        body = ack_body(abha_address="john@sbx", context="OPD1", token=token_number("OPD1", 7), request_id="req-1")
        self.assertEqual(
            body,
            {
                "acknowledgement": {
                    "abhaAddress": "john@sbx",
                    "status": "SUCCESS",
                    "profile": {"context": "OPD1", "tokenNumber": "OPD1-007", "expiry": "1800"},
                },
                "response": {"requestId": "req-1"},
            },
        )

    def test_failure_body_has_error_and_no_profile(self):
        body = ack_body(abha_address="john@sbx", context="X", token="", request_id="", error=("HIP_UNKNOWN", "no"))
        ack = body["acknowledgement"]
        self.assertEqual(ack["status"], "FAILURE")
        self.assertEqual(ack["error"], {"code": "HIP_UNKNOWN", "message": "no"})
        self.assertNotIn("profile", ack)
        self.assertNotIn("response", body)


class PrefillTests(unittest.TestCase):
    def test_maps_shared_patient_to_account_profile_keys(self):
        shared = {
            "abhaNumber": "91-1234-5678-9012",
            "abhaAddress": "johnkumar@sbx",
            "name": "John Kumar",
            "gender": "M",
            "dob": "1990-01-15",
            "mobile": "9876543210",
            "kycPhoto": "AAAA",
            "address": {"line": "123 Main Street", "district": "Mumbai", "state": "Maharashtra", "pinCode": "400001"},
        }
        profile = prefill_profile(shared, "2026-09-14T00:00:00+00:00")
        self.assertEqual(profile["ABHANumber"], "91-1234-5678-9012")
        self.assertEqual(profile["address"], "123 Main Street")
        self.assertEqual(profile["districtName"], "Mumbai")
        self.assertEqual(profile["pinCode"], "400001")
        self.assertNotIn("kycPhoto", profile)
