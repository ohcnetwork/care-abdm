import base64
import json
import unittest
from datetime import UTC, datetime, timedelta

from abdm.hip import rules


def _jwt(exp: int) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"exp": exp}).encode()).decode().rstrip("=")
    return f"eyJhbGciOiJSUzI1NiJ9.{payload}.sig"


class CareContextRulesTests(unittest.TestCase):
    def test_display_names_the_visit_kind_and_day_only(self):
        when = datetime(2026, 9, 10, 9, 30, tzinfo=UTC)
        self.assertEqual(rules.care_context_display("amb", when), "OPD records for 10 Sep 2026")
        self.assertEqual(rules.care_context_display("imp", when), "IPD records for 10 Sep 2026")
        self.assertEqual(rules.care_context_display("emer", None), "Emergency records for an unknown date")

    def test_gender_code_maps_care_values_to_abdm(self):
        self.assertEqual(rules.gender_code("male"), "M")
        self.assertEqual(rules.gender_code("female"), "F")
        self.assertEqual(rules.gender_code("transgender"), "O")
        self.assertEqual(rules.gender_code(None), "O")

    def test_link_token_expiry_reads_jwt_exp_or_defaults_to_six_months(self):
        now = datetime(2026, 9, 15, tzinfo=UTC)
        exp = int(datetime(2027, 1, 1, tzinfo=UTC).timestamp())
        self.assertEqual(rules.link_token_expiry(_jwt(exp), now), datetime(2027, 1, 1, tzinfo=UTC))
        self.assertEqual(rules.link_token_expiry("opaque-token", now), now + timedelta(days=180))

    def test_generate_token_body_types_abha_number_as_integer(self):
        body = rules.generate_token_body("k@sbx", "91-1234-5678-9012", "K", "male", 1990)
        self.assertEqual(
            body,
            {"abhaAddress": "k@sbx", "name": "K", "gender": "M", "yearOfBirth": 1990, "abhaNumber": 91123456789012},
        )
        self.assertNotIn("abhaNumber", rules.generate_token_body("k@sbx", "", "K", "male", 1990))

    def test_link_body_types_abha_number_as_string_and_counts_contexts(self):
        blocks = rules.link_patient_blocks("PAT", "K", [{"referenceNumber": "V1", "display": "OPD"}], ["Prescription"])
        body = rules.link_body("k@sbx", "91123456789012", blocks)
        self.assertEqual(body["abhaNumber"], "91123456789012")
        self.assertEqual(body["patient"][0]["count"], 1)
        self.assertEqual(body["patient"][0]["hiType"], "Prescription")

    def test_link_patient_blocks_sends_1_block_for_each_hi_type(self):
        blocks = rules.link_patient_blocks(
            "PAT", "K", [{"referenceNumber": "V1", "display": "OPD"}], ["OPConsultation", "Prescription"]
        )
        self.assertEqual([b["hiType"] for b in blocks], ["OPConsultation", "Prescription"])
        self.assertEqual([b["count"] for b in blocks], [1, 1])
        self.assertEqual(blocks[0]["careContexts"], blocks[1]["careContexts"])

    def test_link_patient_blocks_is_empty_without_an_hi_type(self):
        self.assertEqual(rules.link_patient_blocks("PAT", "K", [{"referenceNumber": "V1", "display": "OPD"}], []), [])

    def test_discovery_patient_block_keeps_the_hi_type_array(self):
        block = rules.patient_block("PAT", "K", [{"referenceNumber": "V1", "display": "OPD"}], ["Prescription"])
        self.assertEqual(block["hiType"], ["Prescription"])


class DiscoveryRulesTests(unittest.TestCase):
    def test_abha_candidates_reads_patient_id_and_verified_identifiers(self):
        address, number = rules.abha_candidates(
            {"id": "kiran@sbx", "verifiedIdentifiers": [{"type": "ABHA_NUMBER", "value": "91-1234-5678-9012"}]}
        )
        self.assertEqual((address, number), ("kiran@sbx", "91123456789012"))

    def test_abha_candidates_ignores_unverified_and_demographics(self):
        address, number = rules.abha_candidates(
            {"id": "MRN-1", "name": "Kiran", "unverifiedIdentifiers": [{"type": "MR", "value": "MRN-1"}]}
        )
        self.assertEqual((address, number), ("", ""))

    def test_otp_hash_roundtrip_and_mask(self):
        h = rules.otp_hash("123456", "ref")
        self.assertTrue(rules.otp_matches("123456", "ref", h))
        self.assertFalse(rules.otp_matches("123457", "ref", h))
        self.assertEqual(rules.mask_mobile("+91 98765 43210"), "******3210")
        self.assertEqual(len(rules.new_otp()), 6)

    def test_on_confirm_body_adds_error_block_only_on_failure(self):
        ok = rules.on_confirm_body([], "req")
        bad = rules.on_confirm_body([], "req", ("HIP_OTP_INVALID", "wrong"))
        self.assertNotIn("error", ok)
        self.assertEqual(bad["error"], {"code": "HIP_OTP_INVALID", "message": "wrong"})


class TransferRulesTests(unittest.TestCase):
    def test_within_refuses_a_wider_window(self):
        a = datetime(2026, 1, 1, tzinfo=UTC)
        b = datetime(2026, 6, 1, tzinfo=UTC)
        self.assertTrue(rules.within(a, b, a, b))
        self.assertFalse(rules.within(a - timedelta(days=1), b, a, b))
        self.assertTrue(rules.within(a, b, None, None))

    def test_parse_hi_request_reads_nested_and_top_level_transaction_id(self):
        body = {
            "transactionId": "t1",
            "hiRequest": {
                "consent": {"id": "c1"},
                "dateRange": {"from": "2026-01-01T00:00:00.000Z", "to": "2026-02-01T00:00:00.000Z"},
                "dataPushUrl": "https://hiu/push",
                "keyMaterial": {"curve": "Curve25519"},
            },
        }
        data = rules.parse_hi_request(body)
        self.assertEqual(data["transaction_id"], "t1")
        self.assertEqual(data["consent_id"], "c1")
        self.assertEqual(data["date_from"], datetime(2026, 1, 1, tzinfo=UTC))
        self.assertEqual(data["key_material"], {"curve": "Curve25519"})
        self.assertEqual(rules.parse_hi_request({"hiRequest": {"transactionId": "t2"}})["transaction_id"], "t2")

    def test_parse_consent_notification_reads_m3_shape(self):
        body = {
            "status": "GRANTED",
            "consentId": "c1",
            "consentDetail": {
                "patient": {"id": "kiran@sbx"},
                "careContexts": [{"patientReference": "kiran@sbx", "careContextReference": "V1"}],
                "hiTypes": ["Prescription"],
                "hip": {"id": "IN0001"},
                "hiu": {"id": "HIU1", "name": "HIU"},
                "purpose": {"code": "CAREMGT"},
                "permission": {
                    "dateRange": {"from": "2026-01-01T00:00:00.000Z", "to": "2026-02-01T00:00:00.000Z"},
                    "dataEraseAt": "2027-01-01T00:00:00.000Z",
                },
            },
            "signature": "sig",
        }
        data = rules.parse_consent_notification(body)
        self.assertEqual(data["status"], "GRANTED")
        self.assertEqual(data["care_context_references"], ["V1"])
        self.assertEqual(data["hip_id"], "IN0001")
        self.assertEqual(data["data_erase_at"], datetime(2027, 1, 1, tzinfo=UTC))

    def test_notify_body_sends_the_internal_patient_reference(self):
        body = rules.notify_body("k@sbx", "V1", ["OPConsultation"], "now", "IN1", "H", patient_reference="PAT-1")[
            "notification"
        ]
        self.assertEqual(body["patient"]["id"], "k@sbx")
        self.assertEqual(body["careContext"]["patientReference"], "PAT-1")

    def test_notify_body_falls_back_to_the_abha_address(self):
        body = rules.notify_body("k@sbx", "V1", ["OPConsultation"], "now", "IN1", "H")["notification"]
        self.assertEqual(body["careContext"]["patientReference"], "k@sbx")

    def test_data_flow_notify_body_fails_when_any_entry_errored(self):
        ok = rules.data_flow_notify_body("c", "t", "now", "IN1", [{"careContextReference": "V1", "hiStatus": "OK"}])
        bad = rules.data_flow_notify_body(
            "c", "t", "now", "IN1", [{"careContextReference": "V1", "hiStatus": "ERRORED"}]
        )
        self.assertEqual(ok["notification"]["statusNotification"]["sessionStatus"], "TRANSFERRED")
        self.assertEqual(bad["notification"]["statusNotification"]["sessionStatus"], "FAILED")
        self.assertEqual(
            rules.data_flow_notify_body("c", "t", "now", "IN1", [])["notification"]["statusNotification"][
                "sessionStatus"
            ],
            "FAILED",
        )


class ErrorCodeTests(unittest.TestCase):
    def test_error_code_trailing_punctuation_is_stripped(self):
        # Observed 2026-09-17 on an on-generate-token error callback: {"code": "ABDM-1027: ", ...}
        self.assertEqual(rules.normalize_error_code("ABDM-1027: "), "ABDM-1027")
        self.assertEqual(rules.normalize_error_code(" ABDM-1056 "), "ABDM-1056")
        self.assertEqual(rules.normalize_error_code(None), "")

    def test_link_token_claims_and_expiry_are_read_from_the_jwt(self):
        now = datetime(2026, 9, 17, 7, 10, tzinfo=UTC)
        iat = int(datetime(2026, 9, 17, 7, 2, 47, tzinfo=UTC).timestamp())
        payload = (
            base64.urlsafe_b64encode(json.dumps({"iat": iat, "exp": iat + 15768000}).encode()).decode().rstrip("=")
        )
        token = f"eyJhbGciOiJSUzUxMiJ9.{payload}.sig"
        # The token is valid 6 months (concepts/linking). ADR-012 removed the freshness rule:
        # a link sent 96 ms after a token arrived failed the same way as 1 sent 8 minutes after.
        self.assertEqual(rules.jwt_claims(token)["exp"], iat + 15768000)
        self.assertEqual(rules.link_token_expiry(token, now), datetime.fromtimestamp(iat + 15768000, UTC))
        self.assertEqual(rules.link_token_expiry("opaque", now), now + rules.LINK_TOKEN_VALIDITY)
