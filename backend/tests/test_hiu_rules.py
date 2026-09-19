"""
Pure tests for abdm/hiu/rules.py. Every example body below is copied from the docs mirror page it
names (docs/abdm-docs-mirror/pages/hiecm/v3/api/m3/endpoints/m3-consent-management-data-flow-hiu/),
so a parser is proven against the page and not against an assumed shape.
"""

import unittest
from datetime import UTC, datetime, timedelta

from abdm.hiu import rules

NOW = datetime(2026, 9, 19, 12, 0, 0, tzinfo=UTC)


class DefaultsAndValidationTests(unittest.TestCase):
    def test_defaults_follow_the_2026_09_19_decisions(self):
        d = rules.default_request(NOW)
        self.assertEqual(d["purpose_code"], "CAREMGT")
        self.assertEqual(d["hi_types"], list(rules.HI_TYPES[:-1]))
        self.assertNotIn("Invoice", d["hi_types"])
        self.assertEqual(d["date_to"] - d["date_from"], timedelta(days=365))
        self.assertEqual(d["data_erase_at"] - NOW, timedelta(days=30))

    def test_eight_hi_types_match_the_schema_enum(self):
        self.assertEqual(
            set(rules.HI_TYPES),
            {
                "DiagnosticReport",
                "DischargeSummary",
                "HealthDocumentRecord",
                "ImmunizationRecord",
                "OPConsultation",
                "Prescription",
                "WellnessRecord",
                "Invoice",
            },
        )

    def test_validate_accepts_the_defaults_and_normalises_the_purpose(self):
        clean = rules.validate_request({"purpose_code": "caremgt"}, NOW)
        self.assertEqual(clean["purpose_code"], "CAREMGT")
        self.assertEqual(clean["hi_types"], list(rules.DEFAULT_HI_TYPES))

    def test_validate_refuses_bad_input_with_a_desk_sentence(self):
        with self.assertRaisesRegex(ValueError, "Purpose"):
            rules.validate_request({"purpose_code": "FUN"}, NOW)
        with self.assertRaisesRegex(ValueError, "Unknown record type"):
            rules.validate_request({"hi_types": ["Selfie"]}, NOW)
        with self.assertRaisesRegex(ValueError, "after its end"):
            rules.validate_request({"date_from": "2026-09-19T00:00:00Z", "date_to": "2026-09-01T00:00:00Z"}, NOW)
        with self.assertRaisesRegex(ValueError, "future"):
            rules.validate_request({"data_erase_at": "2026-09-01T00:00:00Z"}, NOW)
        with self.assertRaisesRegex(ValueError, "id and a name"):
            rules.validate_request({"hip_id": "IN123"}, NOW)

    def test_validate_dedupes_hi_types_and_keeps_order(self):
        clean = rules.validate_request({"hi_types": ["Prescription", "OPConsultation", "Prescription"]}, NOW)
        self.assertEqual(clean["hi_types"], ["Prescription", "OPConsultation"])


class FormattingTests(unittest.TestCase):
    def test_abdm_iso_has_milliseconds_and_z(self):
        self.assertEqual(
            rules.to_abdm_iso(datetime(2021, 9, 28, 12, 30, 8, 573000, tzinfo=UTC)), "2021-09-28T12:30:08.573Z"
        )
        self.assertRegex(rules.to_abdm_iso(NOW), r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")

    def test_safe_text_keeps_only_what_the_fields_accept(self):
        self.assertEqual(rules.safe_text("Dr. Ana <b>Ray</b>"), "Dr. Ana b Ray /b")
        self.assertEqual(rules.safe_text("", "fallback"), "fallback")
        self.assertEqual(len(rules.safe_text("x" * 300)), 255)

    def test_abha_address_pattern_from_the_init_page(self):
        self.assertTrue(rules.abha_address_ok("nihal_99@sbx"))
        self.assertTrue(rules.abha_address_ok("ana.ray@abdm"))
        self.assertFalse(rules.abha_address_ok("ana@gmail.com"))
        self.assertFalse(rules.abha_address_ok("@sbx"))


class BodyBuilderTests(unittest.TestCase):
    def _body(self, **extra):
        return rules.consent_request_body(
            abha_address="nihal_99@sbx",
            hiu_id="IN1410000232_1",
            hiu_name="FACILITY WITH P",
            requester_name="Dr Ana Ray",
            requester_identifier=rules.requester_identifier(
                registration="KMC12345", username="ana", system="https://care.example"
            ),
            purpose_code="CAREMGT",
            hi_types=["Prescription", "OPConsultation"],
            date_from=NOW - timedelta(days=365),
            date_to=NOW,
            data_erase_at=NOW + timedelta(days=30),
            **extra,
        )

    def test_consent_request_body_carries_every_required_field_of_the_init_page(self):
        consent = self._body()["consent"]
        self.assertEqual(
            consent["purpose"], {"text": "Care Management", "code": "CAREMGT", "refUri": rules.PURPOSE_REF_URI}
        )
        self.assertEqual(consent["patient"], {"id": "nihal_99@sbx"})
        self.assertEqual(consent["hiu"], {"id": "IN1410000232_1", "name": "FACILITY WITH P", "type": "HIU"})
        self.assertEqual(consent["requester"]["name"], "Dr Ana Ray")
        self.assertEqual(
            consent["requester"]["identifier"],
            {"value": "KMC12345", "type": "MEDICAL_COUNCIL_REGISTRATION", "system": "https://care.example"},
        )
        self.assertEqual(consent["hiTypes"], ["Prescription", "OPConsultation"])
        permission = consent["permission"]
        self.assertEqual(permission["accessMode"], "VIEW")
        self.assertEqual(permission["frequency"], {"unit": "HOUR", "value": 1, "repeats": 0})
        for key in ("from", "to"):
            self.assertRegex(permission["dateRange"][key], r"\.\d{3}Z$")
        self.assertRegex(permission["dataEraseAt"], r"\.\d{3}Z$")
        # `hip` is nullable: omitted for "every HIP"; `careContexts` is never sent.
        self.assertNotIn("hip", consent)
        self.assertNotIn("careContexts", consent)

    def test_consent_request_body_names_the_picked_provider(self):
        consent = self._body(hip_id="IN2810014366_1", hip_name="Other Hospital")["consent"]
        self.assertEqual(consent["hip"], {"id": "IN2810014366_1", "name": "Other Hospital", "type": "HIP"})

    def test_requester_identifier_falls_back_to_the_username(self):
        ident = rules.requester_identifier(registration="", username="ana.ray", system="")
        self.assertEqual(ident, {"value": "ana.ray", "type": "CARE_USERNAME", "system": "care"})

    def test_status_fetch_and_ack_bodies(self):
        self.assertEqual(rules.consent_status_body("5f7a"), {"consentRequestId": "5f7a"})
        self.assertEqual(rules.consent_fetch_body("5f7a"), {"consentId": "5f7a"})
        ack = rules.consent_notify_ack_body(["a1", "a2"], "req-1")
        self.assertEqual(
            ack,
            {
                "acknowledgement": [{"status": "OK", "consentId": "a1"}, {"status": "OK", "consentId": "a2"}],
                "response": {"requestId": "req-1"},
            },
        )
        self.assertEqual(rules.consent_notify_ack_body(["a1"], "r", ok=False)["acknowledgement"][0]["status"], "ERROR")

    def test_hi_request_body_matches_the_request_page(self):
        km = rules.key_material_block("PUBKEY==", "NONCE==", NOW + timedelta(minutes=20))
        body = rules.hi_request_body(
            artefact_id="art-1",
            date_from=NOW - timedelta(days=30),
            date_to=NOW,
            data_push_url="https://care.example/api/abdm/v3/hiu/health-information/transfer",
            key_material=km,
        )["hiRequest"]
        self.assertEqual(body["consent"], {"id": "art-1"})
        self.assertEqual(body["dataPushUrl"], "https://care.example/api/abdm/v3/hiu/health-information/transfer")
        self.assertEqual(body["keyMaterial"]["cryptoAlg"], "ECDH")
        self.assertEqual(body["keyMaterial"]["curve"], "curve25519")
        self.assertEqual(body["keyMaterial"]["dhPublicKey"]["keyValue"], "PUBKEY==")
        self.assertEqual(body["keyMaterial"]["dhPublicKey"]["parameters"], "Ephemeral public key")
        self.assertEqual(body["keyMaterial"]["nonce"], "NONCE==")
        self.assertRegex(body["keyMaterial"]["dhPublicKey"]["expiry"], r"\.\d{3}Z$")

    def test_data_push_url_fits_the_255_character_pattern(self):
        url = "https://care-abdm-sbx.rithviknishad.dev/api/abdm" + rules.DATA_PUSH_PATH
        self.assertRegex(url, r'^[a-zA-Z0-9_\-@,. ":=?/&]{0,255}$')

    def test_hiu_notify_body_reports_received_or_failed(self):
        entries = [
            {"careContextReference": "cc-1", "hiStatus": "OK", "description": "Data received successfully"},
            {"careContextReference": "cc-2", "hiStatus": "ERRORED", "description": "Decryption failed: tag"},
        ]
        body = rules.hiu_notify_body(
            artefact_id="art-1",
            transaction_id="txn-1",
            done_at="2026-09-19T12:00:00.000Z",
            hiu_id="IN1410000232_1",
            hip_id="IN2810014366_1",
            entries=entries,
        )["notification"]
        self.assertEqual(body["notifier"], {"type": "HIU", "id": "IN1410000232_1"})
        self.assertEqual(body["statusNotification"]["sessionStatus"], "RECEIVED")
        self.assertEqual(body["statusNotification"]["hipId"], "IN2810014366_1")
        self.assertEqual(len(body["statusNotification"]["statusResponses"]), 2)
        failed = rules.hiu_notify_body(
            artefact_id="a", transaction_id="t", done_at="d", hiu_id="u", hip_id="p", entries=[]
        )["notification"]["statusNotification"]
        self.assertEqual(failed["sessionStatus"], "FAILED")
        self.assertEqual(failed["statusResponses"], [])


class ParserTests(unittest.TestCase):
    def test_on_init_page_example(self):
        parsed = rules.parse_on_init(
            {
                "consentRequest": {"id": "f29f0e59-8388-4698-9fe6-05db67aeac46"},
                "error": {"code": "ABDM-1001", "message": "unable to connect database"},
                "response": {"requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"},
            }
        )
        self.assertEqual(parsed["consent_request_id"], "f29f0e59-8388-4698-9fe6-05db67aeac46")
        self.assertEqual(parsed["request_id"], "6f0b4665-a915-4c92-aa36-65afb4a2cd71")
        self.assertEqual(parsed["error_code"], "ABDM-1001")

    def test_on_init_tolerates_null_error_and_trailing_separator(self):
        self.assertEqual(rules.parse_on_init({"consentRequest": {"id": "x"}, "error": None})["error_code"], "")
        self.assertEqual(rules.parse_on_init({"error": {"code": "ABDM-1001: "}})["error_code"], "ABDM-1001")

    def test_on_status_page_example(self):
        parsed = rules.parse_on_status(
            {
                "consentRequest": {"id": "e5ec415f-c098-40f6-a0db-faa162fc5295", "status": "REQUESTED"},
                "error": None,
                "response": {"requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"},
                "resp": None,
            }
        )
        self.assertEqual(parsed["status"], "REQUESTED")
        self.assertEqual(parsed["consent_request_id"], "e5ec415f-c098-40f6-a0db-faa162fc5295")

    def test_consent_notify_page_example(self):
        parsed = rules.parse_consent_notify(
            {
                "notification": {
                    "consentRequestId": "e3c74829-3f82-4f94-959e-e10f57bcd57b",
                    "status": "GRANTED",
                    "reason": None,
                    "consentArtefacts": [{"id": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"}],
                }
            }
        )
        self.assertEqual(parsed["status"], "GRANTED")
        self.assertEqual(parsed["consent_request_id"], "e3c74829-3f82-4f94-959e-e10f57bcd57b")
        self.assertEqual(parsed["artefact_ids"], ["6f0b4665-a915-4c92-aa36-65afb4a2cd71"])
        self.assertEqual(parsed["reason"], "")

    def test_on_fetch_page_example(self):
        parsed = rules.parse_on_fetch(
            {
                "consent": {
                    "status": "GRANTED",
                    "consentDetail": {
                        "consentId": "e5ec415f-c098-40f6-a0db-faa162fc5295",
                        "hip": {"id": "cowin_hip_01", "name": "Cowin", "type": "HIP"},
                        "hiu": {"id": "cowin_hiu_01", "name": "Cowin", "type": "HIU"},
                        "hiTypes": ["Prescription"],
                        "patient": {"id": "<ABHA_ADDRESS>"},
                        "purpose": {"text": "Care Management", "code": "CAREMGT", "refUri": "www.abc.com"},
                        "createdAt": "2021-09-28T12:30:08.573Z",
                        "requester": {
                            "name": "<ABHA_ADDRESS>",
                            "identifier": {"value": "REG1", "type": "MH1001", "system": "https://www.sample.com"},
                        },
                        "permission": {
                            "accessMode": "VIEW",
                            "dateRange": {"from": "2021-09-28T12:30:08.573Z", "to": "2021-09-28T12:30:08.573Z"},
                        },
                        "dataEraseAt": "2021-09-28T12:30:08.573Z",
                        "frequency": {"unit": "HOUR", "value": 1, "repeats": 0},
                        "lastUpdated": "2021-09-28T12:30:08.573Z",
                        "careContexts": [{"patientReference": "batman@tmh", "careContextReference": "Episode1"}],
                        "schemaVersion": "v3",
                        "consentManager": {"id": "abdm"},
                    },
                    "signature": "Signature of CM as defined in W3C standards; Base64 encoded",
                },
                "error": None,
                "response": {"requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"},
                "resp": None,
            }
        )
        self.assertEqual(parsed["status"], "GRANTED")
        self.assertEqual(parsed["artefact_id"], "e5ec415f-c098-40f6-a0db-faa162fc5295")
        self.assertEqual(parsed["hip_id"], "cowin_hip_01")
        self.assertEqual(parsed["hip_name"], "Cowin")
        self.assertEqual(parsed["hi_types"], ["Prescription"])
        self.assertEqual(parsed["care_context_references"], ["Episode1"])
        self.assertEqual(parsed["date_from"], datetime(2021, 9, 28, 12, 30, 8, 573000, tzinfo=UTC))
        # `dataEraseAt` sits beside `permission` on this page and inside it on the init page.
        self.assertEqual(parsed["data_erase_at"], datetime(2021, 9, 28, 12, 30, 8, 573000, tzinfo=UTC))
        self.assertTrue(parsed["signature"].startswith("Signature"))
        self.assertEqual(parsed["error_code"], "")

    def test_on_fetch_reads_data_erase_at_inside_permission_too(self):
        parsed = rules.parse_on_fetch(
            {
                "consent": {
                    "status": "GRANTED",
                    "consentDetail": {"consentId": "a", "permission": {"dataEraseAt": "2027-01-01T00:00:00.000Z"}},
                }
            }
        )
        self.assertEqual(parsed["data_erase_at"], datetime(2027, 1, 1, tzinfo=UTC))

    def test_hi_on_request_page_example(self):
        parsed = rules.parse_hi_on_request(
            {
                "hiRequest": {"transactionId": "18235d89-cb13-479d-ad71-7a57d5f669a8", "sessionStatus": "REQUESTED"},
                "error": {"code": "ABDM-1001", "message": "unable to connect database"},
                "response": {"requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"},
            }
        )
        self.assertEqual(parsed["transaction_id"], "18235d89-cb13-479d-ad71-7a57d5f669a8")
        self.assertEqual(parsed["session_status"], "REQUESTED")
        self.assertEqual(parsed["error_code"], "ABDM-1001")

    def test_transfer_page_example(self):
        parsed = rules.parse_transfer(
            {
                "pageNumber": 0,
                "pageCount": 1,
                "transactionId": "<TRANSACTION_ID>",
                "entries": [
                    {
                        "content": "Encrypted content of data packaged in FHIR bundle",
                        "media": "application/fhir+json",
                        "checksum": "string",
                        "careContextReference": "1931-nd2",
                    }
                ],
                "keyMaterial": {
                    "cryptoAlg": "ECDH",
                    "curve": "Curve25519",
                    "dhPublicKey": {
                        "expiry": "<EXPIRY>",
                        "parameters": "Curve25519/32byte random key",
                        "keyValue": "<KEY_VALUE>",
                    },
                    "nonce": "<NONCE>",
                },
            }
        )
        self.assertEqual(parsed["transaction_id"], "<TRANSACTION_ID>")
        self.assertEqual(parsed["page_count"], 1)
        self.assertEqual(parsed["entries"][0]["careContextReference"], "1931-nd2")
        self.assertEqual(parsed["entries"][0]["content"], "Encrypted content of data packaged in FHIR bundle")
        self.assertEqual(parsed["key_material"]["curve"], "Curve25519")

    def test_transfer_tolerates_garbage(self):
        parsed = rules.parse_transfer({"entries": [1, "x", {"link": "https://x"}], "pageCount": "many"})
        self.assertEqual(len(parsed["entries"]), 1)
        self.assertEqual(parsed["entries"][0]["link"], "https://x")
        self.assertEqual(parsed["page_count"], 1)


class BundleSummaryTests(unittest.TestCase):
    def test_reads_the_hi_type_off_the_composition_profile(self):
        bundle = {
            "resourceType": "Bundle",
            "entry": [
                {
                    "resource": {
                        "resourceType": "Composition",
                        "meta": {"profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord"]},
                        "title": "OP Consultation Record",
                        "date": "2026-09-18T10:00:00+05:30",
                    }
                },
                {"resource": {"resourceType": "Patient"}},
            ],
        }
        summary = rules.bundle_summary(bundle)
        self.assertEqual(summary["hi_type"], "OPConsultation")
        self.assertEqual(summary["title"], "OP Consultation Record")
        self.assertEqual(summary["authored_at"], datetime(2026, 9, 18, 4, 30, tzinfo=UTC))
        self.assertEqual(summary["resource_count"], 2)

    def test_unknown_bundle_gives_empty_fields(self):
        self.assertEqual(
            rules.bundle_summary({"resourceType": "Bundle"}),
            {"hi_type": "", "title": "", "authored_at": None, "resource_count": 0},
        )
        self.assertEqual(rules.bundle_summary("nope")["resource_count"], 0)


class StateRuleTests(unittest.TestCase):
    def test_artefact_is_live_until_data_erase_at(self):
        self.assertTrue(rules.artefact_is_live("GRANTED", NOW + timedelta(days=1), NOW))
        self.assertTrue(rules.artefact_is_live("GRANTED", None, NOW))
        self.assertFalse(rules.artefact_is_live("GRANTED", NOW - timedelta(seconds=1), NOW))
        self.assertFalse(rules.artefact_is_live("REVOKED", NOW + timedelta(days=1), NOW))

    def test_request_is_open_only_while_requested(self):
        self.assertTrue(rules.request_is_open("REQUESTED"))
        for status in ("GRANTED", "DENIED", "EXPIRED", "REVOKED", "failed"):
            self.assertFalse(rules.request_is_open(status))


if __name__ == "__main__":
    unittest.main()
