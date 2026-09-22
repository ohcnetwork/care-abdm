"""
Pure tests for abdm/nhpr/rules.py. The example bodies are copied from the docs mirror pages under
docs/abdm-docs-mirror/pages/hiecm/v3/api/m4/endpoints/, so every parser is proven against its page.
"""

import base64
import unittest
from datetime import UTC, datetime

from abdm.nhpr import rules


class FormatTests(unittest.TestCase):
    def test_hpr_id_kinds(self):
        self.assertEqual(rules.hpr_id_kind("71-2665-5777-1234"), "number")
        self.assertEqual(rules.hpr_id_kind("71266557771234"), "number")
        self.assertEqual(rules.hpr_id_kind("ana.ray@hpr.abdm"), "address")
        self.assertEqual(rules.hpr_id_kind("ana.ray"), "username")
        self.assertEqual(rules.hpr_id_kind("ana@gmail.com"), "")
        self.assertEqual(rules.hpr_id_kind(""), "")

    def test_normalise_and_format(self):
        self.assertEqual(rules.normalise_hpr_address("ana.ray"), "ana.ray@hpr.abdm")
        self.assertEqual(rules.normalise_hpr_address("ana.ray@hpr.abdm"), "ana.ray@hpr.abdm")
        self.assertEqual(rules.normalise_hpr_address("71266557771234"), "71266557771234")
        self.assertEqual(rules.format_hpr_id_number("71266557771234"), "71-2665-5777-1234")
        self.assertEqual(rules.format_hpr_id_number("71-2665-5777-1234"), "71-2665-5777-1234")
        self.assertEqual(rules.format_hpr_id_number("abc"), "abc")

    def test_facility_id_and_hip_name(self):
        self.assertTrue(rules.facility_id_ok("IN1410000232"))
        self.assertFalse(rules.facility_id_ok("IN1410000232_1"))
        self.assertFalse(rules.facility_id_ok("1410000232"))
        self.assertTrue(rules.hip_name_ok("Smoke Hospital"))
        self.assertFalse(rules.hip_name_ok("Smoke Hospital & Sons"))
        self.assertFalse(rules.hip_name_ok("A" * 16))
        self.assertEqual(rules.default_hip_name("Sahyadri Super-Speciality Hospital, Pune"), "Sahyadri SuperS")
        self.assertEqual(rules.default_hip_name("Care Hospital"), "Care Hospital")


class LinkageAndSearchTests(unittest.TestCase):
    def test_hrp_linkage_body_names_both_roles(self):
        body = rules.hrp_linkage_body("IN0610090166", "Singla Eye Center", "SBX_00XXXX", "Singla Eye")
        self.assertEqual(body["facilityId"], "IN0610090166")
        self.assertEqual(body["facilityName"], "Singla Eye Center")
        self.assertEqual([h["type"] for h in body["HRP"]], ["HIP", "HIU"])
        self.assertEqual(
            body["HRP"][0], {"bridgeId": "SBX_00XXXX", "hipName": "Singla Eye", "type": "HIP", "active": True}
        )
        with self.assertRaises(ValueError):
            rules.hrp_linkage_body("bad", "x", "b", "Singla Eye")
        with self.assertRaises(ValueError):
            rules.hrp_linkage_body("IN0610090166", "x", "b", "Too long a hip name!")
        with self.assertRaises(ValueError):
            rules.hrp_linkage_body("IN0610090166", "x", "b", "ok", types=("PHR",))

    def test_facility_search_body_matches_the_page(self):
        body = rules.facility_search_body(name="hospital", state_lgd="27", ownership="P")
        self.assertEqual(
            body,
            {
                "ownershipCode": "P",
                "subDistrictLGDCode": "",
                "pincode": "",
                "facilityName": "hospital",
                "facilityId": "",
                "page": 1,
                "resultsPerPage": 10,
                "stateLGDCode": "27",
                "districtLGDCode": "",
            },
        )
        self.assertEqual(rules.facility_search_body(facility_id="IN1410000232", per_page=500)["resultsPerPage"], 15)
        self.assertEqual(rules.facility_search_body(facility_id="IN1410000232", per_page=5)["resultsPerPage"], 10)

    def test_parse_facility_search_page_example(self):
        parsed = rules.parse_facility_search(
            {
                "facilities": [
                    {
                        "ownership": "GOVERNMENT",
                        "systemOfMedicineCode": "P,M",
                        "systemOfMedicine": "Physiotherapy,Modern Medicine(Allopathy)",
                        "facilityType": "Hospital",
                        "stateName": "Bihar",
                        "stateLGDCode": "10",
                        "districtName": "Patna",
                        "districtLGDCode": "212",
                        "subDistrictName": "Patna Sadar",
                        "subDistrictLGDCode": "1400",
                        "address": "Kankarbagh",
                        "pincode": "800020",
                        "latitude": "25.635802000000098",
                        "longitude": "85.10391099999993",
                        "facilityId": "IN1010000001",
                        "facilityName": "Asian City Hospital",
                        "facilityStatus": "Submitted",
                        "ownershipCode": "G",
                        "facilityTypeCode": "H",
                    }
                ],
                "message": "Request processed successfully",
                "totalFacilities": 1,
                "numberOfPages": 1,
            }
        )
        self.assertEqual(parsed["total"], 1)
        self.assertEqual(parsed["facilities"][0]["facilityId"], "IN1010000001")
        self.assertEqual(parsed["facilities"][0]["facilityStatus"], "Submitted")
        self.assertEqual(parsed["facilities"][0]["stateLGDCode"], "10")
        self.assertEqual(rules.parse_facility_search("nope"), {"facilities": [], "message": "", "total": 0, "pages": 0})

    def test_facility_otp_bodies(self):
        self.assertEqual(rules.facility_otp_send_body("IN2810002702"), {"facilityId": "IN2810002702"})
        self.assertEqual(
            rules.facility_otp_validate_body("IN2810002702", "2ddfc7ec", "885210", "AB-PMJAY", "AB-PMJAY"),
            {
                "facilityId": "IN2810002702",
                "sourceId": "AB-PMJAY",
                "otp": "885210",
                "source": "AB-PMJAY",
                "transactionId": "2ddfc7ec",
            },
        )


class LoginTests(unittest.TestCase):
    def test_password_body_for_address_and_number(self):
        self.assertEqual(
            rules.login_password_body("ana.ray", "XXXX@992"),
            {"idType": "hpr_id", "domainName": "@hpr.abdm", "hprId": "ana.ray@hpr.abdm", "password": "XXXX@992"},
        )
        body = rules.login_password_body("71266557771234", "p")
        self.assertEqual((body["idType"], body["domainName"], body["hprId"]), ("", "", "71266557771234"))

    def test_init_body_matches_the_page(self):
        body = rules.login_init_body("ana.ray@hpr.abdm", "AADHAAR_OTP")
        self.assertEqual(
            body,
            {"idType": "hpr_id", "domainName": "@hpr.abdm", "hprId": "ana.ray@hpr.abdm", "authMethod": "AADHAAR_OTP"},
        )
        with self.assertRaises(ValueError):
            rules.login_init_body("ana.ray", "CARRIER_PIGEON")
        self.assertEqual(rules.login_confirm_body("txn", "308709"), {"otp": "308709", "txnId": "txn"})

    def test_token_response_reads_epoch_and_duration(self):
        parsed = rules.parse_token_response(
            {"token": "T", "expiresIn": 1733639805, "refreshToken": None, "refreshExpiresIn": 0}
        )
        self.assertEqual(parsed["token"], "T")
        self.assertEqual(parsed["expires_at"], datetime.fromtimestamp(1733639805, tz=UTC))
        self.assertEqual(parsed["refresh_token"], "")
        self.assertIsNone(parsed["refresh_expires_at"])
        soon = rules.parse_token_response({"token": "T", "expiresIn": 1200})["expires_at"]
        self.assertTrue(1100 < (soon - datetime.now(UTC)).total_seconds() <= 1200)
        self.assertEqual(rules.parse_token_response("junk")["token"], "")

    def test_login_init_and_hpr_search_parsers(self):
        self.assertEqual(
            rules.parse_login_init({"transactionId": "227654a1", "mobileNumber": "******1234"}),
            {"txn_id": "227654a1", "mobile_masked": "******1234"},
        )
        parsed = rules.parse_hpr_search(
            {
                "hprIdNumber": "71-2665-5777-1234",
                "name": "Ayushman Bharat Mission",
                "authMethods": ["PASSWORD", "MOBILE_OTP"],
                "hprId": "abm@hpr.abdm",
                "categoryId": "1",
                "subCategoryId": "1",
            }
        )
        self.assertEqual(parsed["hpr_id"], "abm@hpr.abdm")
        self.assertEqual(parsed["auth_methods"], ["PASSWORD", "MOBILE_OTP"])

    def test_account_information_drops_photos(self):
        parsed = rules.parse_account_information(
            {
                "hprIdNumber": "71-2665-5777-1234",
                "hprId": "abm@hpr.abdm",
                "name": "A B M",
                "profilePhoto": "AAAA",
                "kycPhoto": "BBBB",
                "email": None,
            }
        )
        self.assertEqual(parsed, {"hprIdNumber": "71-2665-5777-1234", "hprId": "abm@hpr.abdm", "name": "A B M"})


class HpidCreationTests(unittest.TestCase):
    def test_aadhaar_link_body_and_parser(self):
        self.assertEqual(rules.aadhaar_link_body(), {"scopes": ["nhpr-register"], "source": "NHPR"})
        parsed = rules.parse_aadhaar_link({"txnId": "de4ff682", "mobileNumber": "******1234"})
        self.assertEqual(parsed, {"txn_id": "de4ff682", "url": "", "mobile_masked": "******1234"})
        self.assertEqual(rules.parse_aadhaar_link({"txnId": "t", "url": "https://x/y"})["url"], "https://x/y")

    def test_boolean_parser(self):
        self.assertTrue(rules.parse_boolean(True))
        self.assertTrue(rules.parse_boolean("true"))
        self.assertFalse(rules.parse_boolean("false"))
        self.assertTrue(rules.parse_boolean({"verified": True, "errorCode": None, "reason": None, "uidaiToken": None}))
        self.assertFalse(rules.parse_boolean({"status": "false"}))
        self.assertFalse(rules.parse_boolean(None))

    def test_aadhaar_details_keeps_photo_apart(self):
        parsed = rules.parse_aadhaar_details(
            {
                "txnId": "951b",
                "photo": "PHOTO==",
                "gender": "M",
                "name": "Ayushman Bharat Mission",
                "email": None,
                "pincode": "110001",
                "district": "Ghaziabad",
                "state": "Uttar Pradesh",
            }
        )
        self.assertEqual(parsed["photo"], "PHOTO==")
        self.assertNotIn("photo", parsed["details"])
        self.assertEqual(parsed["details"]["state"], "Uttar Pradesh")
        self.assertNotIn("email", parsed["details"])
        self.assertEqual(rules.split_name("Ayushman Bharat Mission"), ("Ayushman", "Bharat", "Mission"))
        self.assertEqual(rules.split_name("Ana Ray"), ("Ana", "", "Ray"))
        self.assertEqual(rules.split_name("Ana"), ("Ana", "", ""))

    def test_account_exists_page_example(self):
        parsed = rules.parse_account_exists(
            {
                "token": "JWT",
                "hprIdNumber": "71-2665-5777-1234",
                "categoryId": 100,
                "subCategoryId": 85,
                "txnId": "79dbf65d",
                "name": "Ayushman Bharat Mission",
                "hprId": "abm@hpr.abdm",
                "new": False,
            }
        )
        self.assertTrue(parsed["exists"])
        self.assertEqual(parsed["token"], "JWT")
        self.assertEqual(parsed["category_id"], "100")
        self.assertFalse(rules.parse_account_exists({"new": True})["exists"])
        self.assertFalse(rules.parse_account_exists({})["exists"])
        self.assertEqual(rules.account_exists_body("t"), {"txnId": "t", "preverifiedCheck": True})

    def test_mobile_bodies(self):
        self.assertEqual(rules.mobile_auth_body("t", "ENC=="), {"txnId": "t", "mobileNumber": "ENC=="})
        self.assertEqual(rules.mobile_otp_body("t", "9810651234"), {"mobile": "9810651234", "txnId": "t"})
        self.assertEqual(rules.mobile_otp_verify_body("t", "ENC=="), {"otp": "ENC==", "txnId": "t"})
        self.assertEqual(rules.parse_suggestions(["anujsharma"]), ["anujsharma"])
        self.assertEqual(rules.parse_suggestions({"suggestions": ["a", "b"]}), ["a", "b"])

    def test_create_body_matches_the_page(self):
        body = rules.create_hpid_body(
            txn_id="c3b0",
            username="ayushman.bharat",
            email="abm@example.com",
            encrypted_password="ENC==",
            first_name="Ayushman",
            middle_name="Bharat",
            last_name="Mission",
            profile_photo_b64="PHOTO==",
            category_code=1,
            sub_category_code=1,
            state_code="9",
            district_code="145",
            role=2,
        )
        self.assertEqual(body["idType"], "hpr_id")
        self.assertEqual(body["domainName"], "@hpr.abdm")
        self.assertEqual(body["hprId"], "ayushman.bharat")
        self.assertEqual(body["password"], "ENC==")
        self.assertEqual(body["sourceType"], "AADHAAR")
        self.assertEqual(body["clientId"], "V4")
        self.assertEqual((body["hpCategoryCode"], body["hpSubCategoryCode"], body["role"]), (1, 1, 2))
        self.assertIs(body["council"], False)
        with self.assertRaises(ValueError):
            rules.create_hpid_body(
                txn_id="t",
                username="a b",
                email="e",
                encrypted_password="p",
                first_name="f",
                middle_name="",
                last_name="l",
                profile_photo_b64="",
                category_code=1,
                sub_category_code=1,
                state_code="9",
                district_code="1",
                role=1,
            )
        with self.assertRaises(ValueError):
            rules.create_hpid_body(
                txn_id="t",
                username="abc",
                email="e",
                encrypted_password="p",
                first_name="f",
                middle_name="",
                last_name="l",
                profile_photo_b64="",
                category_code=1,
                sub_category_code=1,
                state_code="9",
                district_code="1",
                role=9,
            )


class RegisterProfessionalTests(unittest.TestCase):
    PRACTITIONER = {
        "healthProfessionalType": "doctor",
        "personalInformation": {"salutation": "1", "firstName": "Ayushman", "lastName": "Mission", "gender": "M"},
        "registrationAcademic": {
            "category": "1",
            "registrationData": [{"registeredWithCouncil": "47", "registrationNumber": "REG12032"}],
        },
        "currentWorkDetails": {"currentlyWorking": "0"},
    }

    def test_register_body_wraps_the_form_with_the_token(self):
        body = rules.register_professional_body("HPRTOKEN", self.PRACTITIONER)
        self.assertEqual(body["hprToken"], "HPRTOKEN")
        self.assertEqual(body["practitioner"]["personalInformation"]["firstName"], "Ayushman")
        self.assertEqual(
            set(body["practitioner"]),
            {"healthProfessionalType", "personalInformation", "registrationAcademic", "currentWorkDetails"},
        )

    def test_register_body_refuses_stray_and_missing_blocks(self):
        with self.assertRaisesRegex(ValueError, "Unknown profile block"):
            rules.register_professional_body("T", {**self.PRACTITIONER, "hprToken": "leak"})
        with self.assertRaisesRegex(ValueError, "firstName"):
            rules.register_professional_body(
                "T", {"personalInformation": {}, "registrationAcademic": {"registrationData": [{}]}}
            )
        with self.assertRaisesRegex(ValueError, "registrationData"):
            rules.register_professional_body(
                "T", {"personalInformation": {"firstName": "A"}, "registrationAcademic": {}}
            )
        with self.assertRaises(ValueError):
            rules.register_professional_body("T", {})

    def test_documents_bodies_and_limits(self):
        self.assertEqual(rules.documents_list_body("abm@hpr.abdm"), {"hprid": "abm@hpr.abdm"})
        small = base64.b64encode(b"%PDF-1.3").decode()
        body = rules.upload_documents_body(
            "T",
            [{"document_id": "21021", "document_type": "registrationCertificate", "fileType": "PDF", "data": small}],
        )
        self.assertEqual(body["hpr_token"], "T")
        self.assertEqual(
            body["document"][0],
            {"document_id": 21021, "document_type": "registrationCertificate", "fileType": "pdf", "data": small},
        )
        big = "A" * (int(1.2 * 1024 * 1024 * 4 / 3) + 4)
        with self.assertRaisesRegex(ValueError, "1 MB"):
            rules.upload_documents_body(
                "T", [{"document_id": 1, "document_type": "profilePhoto", "fileType": "png", "data": big}]
            )
        with self.assertRaisesRegex(ValueError, "document_type"):
            rules.upload_documents_body(
                "T", [{"document_id": 1, "document_type": "selfie", "fileType": "png", "data": small}]
            )
        with self.assertRaisesRegex(ValueError, "fileType"):
            rules.upload_documents_body(
                "T", [{"document_id": 1, "document_type": "profilePhoto", "fileType": "gif", "data": small}]
            )
        with self.assertRaises(ValueError):
            rules.upload_documents_body("T", [])
        self.assertEqual(rules.base64_size(base64.b64encode(b"x" * 100).decode()), 100)

    def test_professional_info_body(self):
        body = rules.professional_info_body(hpr_id="abm@hpr.abdm", name="A B M")
        self.assertEqual(
            set(body["practitioner"]),
            {"id", "name", "contactNumber", "state", "registrationNumber", "stateCouncilName"},
        )


class OnboardingTests(unittest.TestCase):
    BASIC = {
        "facilityName": "Sahyadri Hospital",
        "facilityAddressDetails": {
            "country": "India",
            "stateLGDCode": "24",
            "districtLGDCode": "438",
            "subDistrictLGDCode": "6512",
            "pincode": "411001",
        },
        "facilityContactInformation": {"facilityEmailId": "x@y.com"},
        "ownershipCode": "G",
        "systemOfMedicineCode": "M",
        "facilityTypeCode": "5",
        "facilityUploads": {
            "facilityBoardPhoto": {"name": "board.jpg", "value": "AAAA"},
            "facilityBuildingPhoto": {"name": "", "value": ""},
        },
        "timingsOfFacility": [{"workingDays": "MON", "openingHours": "9:00 AM - 6:00 PM"}],
    }

    def test_dedup_body_matches_the_page(self):
        body = rules.dedup_body(name="Jethana", address="Main road", district_lgd="511", sub_district_lgd="5271")
        self.assertEqual(
            body,
            {
                "name": "Jethana",
                "address": "Main road",
                "district": "511",
                "subDistrict": "5271",
                "village": "",
                "geolocation": "",
                "facilityId": "",
            },
        )

    def test_basic_information_creates_then_updates(self):
        body = rules.basic_information_body(self.BASIC)
        self.assertEqual(body["trackingId"], "")
        self.assertEqual(body["facilityInformation"]["facilityName"], "Sahyadri Hospital")
        self.assertEqual(rules.basic_information_body(self.BASIC, "76803")["trackingId"], "76803")
        with self.assertRaisesRegex(ValueError, "Unknown facilityInformation field"):
            rules.basic_information_body({**self.BASIC, "trackingId": "x"})
        with self.assertRaisesRegex(ValueError, "facilityName"):
            rules.basic_information_body({**self.BASIC, "facilityName": ""})
        with self.assertRaisesRegex(ValueError, "stateLGDCode"):
            rules.basic_information_body({**self.BASIC, "facilityAddressDetails": {}})

    def test_basic_information_shortens_the_coordinates(self):
        """HIS-4019 and HIS-4020: 1 to 6 decimal places. Care holds 16 (Rithvik, 2026-09-21)."""
        address = {**self.BASIC["facilityAddressDetails"], "latitude": "10.0400000000000000"}
        body = rules.basic_information_body({**self.BASIC, "facilityAddressDetails": address})
        self.assertEqual(body["facilityInformation"]["facilityAddressDetails"]["latitude"], "10.04")
        with self.assertRaisesRegex(ValueError, "latitude must be between"):
            rules.basic_information_body({**self.BASIC, "facilityAddressDetails": {**address, "latitude": "99"}})
        with self.assertRaisesRegex(ValueError, "longitude must be a number"):
            rules.basic_information_body({**self.BASIC, "facilityAddressDetails": {**address, "longitude": "east"}})

    def test_coordinate_keeps_1_to_6_decimal_places(self):
        self.assertEqual(rules.coordinate("25.635802000000098", "latitude"), "25.635802")
        self.assertEqual(rules.coordinate("10", "latitude"), "10.0")
        self.assertEqual(rules.coordinate("-76.2811119", "longitude"), "-76.281112")
        self.assertEqual(rules.coordinate(None, "latitude"), "")
        self.assertEqual(rules.coordinate("", "longitude"), "")
        self.assertEqual(rules.coordinate("north", "latitude"), "")
        self.assertEqual(rules.coordinate("91", "latitude"), "")
        self.assertEqual(rules.coordinate("181", "longitude"), "")

    def test_later_steps_need_the_tracking_id(self):
        with self.assertRaisesRegex(ValueError, "tracking id"):
            rules.additional_information_body({"generalInformation": {}}, "")
        body = rules.additional_information_body(
            {"linkedProgramIds": {"nin": "1234"}, "generalInformation": {"hasPharmacy": "YALL"}}, "80266"
        )
        self.assertEqual(body["trackingId"], "80266")
        with self.assertRaisesRegex(ValueError, "Unknown additional"):
            rules.additional_information_body({"beds": 4}, "80266")
        body = rules.detailed_information_body(
            {"specialities": [], "medicalInfrastructure": {"countIPDBedsWithOxygen": 4}}, "80266"
        )
        self.assertEqual(set(body), {"specialities", "medicalInfrastructure", "trackingId"})
        self.assertEqual(rules.submit_body({}, "80266"), {"trackingId": "80266"})
        self.assertEqual(
            rules.submit_body({"sourceOfInformation": "HRP_SUB_1"}, "80266")["sourceOfInformation"], "HRP_SUB_1"
        )

    def test_speciality_codes_are_sent_without_the_system_of_medicine_prefix(self):
        # get-specialities answers "UN-S68"; the detailed body takes "S68" (findings N30).
        body = rules.detailed_information_body(
            {
                "specialities": [
                    {
                        "systemOfMedicineCode": "UN",
                        "isSpecializationAvalaible": "Y",
                        "specialities": ["UN-S68", "S100", " UN-S168 "],
                    },
                    {"systemOfMedicineCode": "D", "isSpecializationAvalaible": "Y", "specialities": ["D-S44"]},
                ]
            },
            "80266",
        )
        self.assertEqual(body["specialities"][0]["specialities"], ["S68", "S100", "S168"])
        self.assertEqual(body["specialities"][1]["specialities"], ["S44"])
        # A row with no specialities keeps its shape; unknown fields are refused.
        self.assertEqual(
            rules.specialities([{"systemOfMedicineCode": "M"}]),
            [{"systemOfMedicineCode": "M", "isSpecializationAvalaible": "N", "specialities": []}],
        )
        with self.assertRaisesRegex(ValueError, "Unknown speciality field"):
            rules.specialities([{"systemOfMedicineCode": "M", "codes": []}])

    def test_bed_total_is_derived_from_the_6_counts_the_registry_sums(self):
        # The page example sends totalNumberOfBeds 4 with categories that sum to 33 (findings N27).
        example = {
            "countIPDBedsWithoutOxygen": 2,
            "countIPDBedsWithOxygen": 3,
            "countICUBedsWithVentilators": 4,
            "countICUBedsWithoutVentilators": 1,
            "countHDUBedsWithVentilators": 5,
            "countHDUBedsWithoutVentilators": 6,
            "totalNumberOfVentilators": 7,
            "countDayCareBedsWithoutOxygen": 8,
            "countDayCareBedsWithOxygen": 9,
            "countDentalChairs": 1,
            "totalNumberOfBeds": 4,
        }
        infra = rules.medical_infrastructure(example)
        self.assertEqual(infra["totalNumberOfBeds"], 33)
        self.assertEqual(infra["countICUBedsWithVentilators"], 4)
        # Absent and empty counts are 0; strings are read as numbers; the total follows.
        infra = rules.medical_infrastructure({"countIPDBedsWithOxygen": "5", "countDentalChairs": ""})
        self.assertEqual(infra["totalNumberOfBeds"], 5)
        self.assertEqual(infra["countDentalChairs"], 0)
        self.assertEqual(set(infra), set(rules.INFRASTRUCTURE_FIELDS) | {"totalNumberOfBeds"})
        body = rules.detailed_information_body({"medicalInfrastructure": {}}, "80266")
        self.assertEqual(body["medicalInfrastructure"]["totalNumberOfBeds"], 0)
        with self.assertRaises(ValueError):
            rules.medical_infrastructure({"countIPDBedsWithOxygen": -1})
        with self.assertRaises(ValueError):
            rules.medical_infrastructure({"countIPDBedsWithOxygen": "five"})
        with self.assertRaises(ValueError):
            rules.medical_infrastructure({"beds": 1})

    def test_onboarding_result_and_photo_strip(self):
        parsed = rules.parse_onboarding_result(
            {
                "trackingId": "76803",
                "status": "success",
                "message": "Facility is saved successfully",
                "errorStatus": None,
            }
        )
        self.assertEqual(
            parsed,
            {
                "tracking_id": "76803",
                "status": "success",
                "message": "Facility is saved successfully",
                "error": "",
                "facility_id": "",
            },
        )
        stripped = rules.strip_photos(self.BASIC)
        self.assertEqual(stripped["facilityUploads"]["facilityBoardPhoto"], {"name": "board.jpg", "value": ""})
        self.assertEqual(self.BASIC["facilityUploads"]["facilityBoardPhoto"]["value"], "AAAA")


class CarePrefillTests(unittest.TestCase):
    """ADR-016: a registry record fills the Care facility form; the type is a suggestion."""

    RECORD = {
        "facilityId": "IN0110009999",
        "facilityName": "Sahyadri Hospital",
        "facilityType": "Hospital",
        "ownership": "Private",
        "ownershipCode": "P",
        "address": "MG Road",
        "pincode": "682001",
        "stateName": "Kerala",
        "districtName": "Ernakulam",
        "latitude": "9.98",
        "longitude": "76.28",
    }

    def test_prefill_fields(self):
        out = rules.care_prefill(self.RECORD)
        self.assertEqual(out["name"], "Sahyadri Hospital")
        self.assertEqual(out["pincode"], 682001)
        self.assertAlmostEqual(out["latitude"], 9.98)
        self.assertAlmostEqual(out["longitude"], 76.28)
        self.assertEqual(out["facility_type"], "Private Hospital")
        self.assertEqual((out["state_name"], out["district_name"]), ("Kerala", "Ernakulam"))

    def test_prefill_rounds_to_6_decimal_places(self):
        """The registry answers with 15 decimal places; Care must not store more than 6, or the
        HFR basic step refuses the value it filled itself (HIS-4019)."""
        out = rules.care_prefill({**self.RECORD, "latitude": "25.635802000000098"})
        self.assertEqual(out["latitude"], 25.635802)

    def test_prefill_drops_bad_values(self):
        out = rules.care_prefill({**self.RECORD, "pincode": "0123", "latitude": "north", "longitude": "999"})
        self.assertIsNone(out["pincode"])
        self.assertIsNone(out["latitude"])
        self.assertIsNone(out["longitude"])

    def test_type_suggestions(self):
        cases = [
            ({"facilityType": "Diagnostic Center", "ownershipCode": "P"}, "Private Labs"),
            ({"facilityType": "Laboratory", "ownershipCode": "G"}, "Govt Labs"),
            ({"facilityType": "Telemedicine Centre", "ownershipCode": "P"}, "TeleMedicine"),
            (
                {"facilityType": "Hospital", "ownershipCode": "G", "facilityName": "District Hospital Kollam"},
                "District Hospitals",
            ),
            ({"facilityType": "Primary Health Centre", "ownership": "Government"}, "Primary Health Centres"),
            ({"facilityType": "Hospital", "ownershipCode": "G", "facilityName": "GH Alappuzha"}, "Other"),
            ({"facilityType": "Clinic", "ownershipCode": "P"}, "Private Hospital"),
            ({"facilityType": "Pharmacy", "ownershipCode": "P"}, "Other"),
            ({}, "Other"),
        ]
        for record, expected in cases:
            with self.subTest(record=record):
                self.assertEqual(rules.suggest_care_facility_type(record), expected)


class MastersTests(unittest.TestCase):
    def test_every_master_shape_becomes_code_name(self):
        self.assertEqual(
            rules.parse_code_values({"type": "MEDICINE", "data": [{"code": "H", "value": "Homeopathy"}]}),
            [{"code": "H", "name": "Homeopathy"}],
        )
        lgd = rules.parse_code_values(
            [{"code": "35", "name": "Andaman", "districts": [{"code": "603", "name": "Nicobars"}]}]
        )
        self.assertEqual(lgd[0]["children"], [{"code": "603", "name": "Nicobars"}])
        cats = rules.parse_code_values(
            [{"code": 1, "name": "Doctor", "subCategories": [{"code": "1", "name": "Modern Medicine"}]}]
        )
        self.assertEqual(cats[0]["code"], "1")
        self.assertEqual(cats[0]["children"][0]["name"], "Modern Medicine")
        hpr = rules.parse_code_values([{"id": 6046, "name": "Baba Farid University", "status": True}])
        self.assertEqual(hpr, [{"code": "6046", "name": "Baba Farid University"}])
        types = rules.parse_code_values({"masterTypes": [{"type": "OWNER", "desc": "Ownership Of Facility"}]})
        self.assertEqual(types, [{"code": "OWNER", "name": "Ownership Of Facility"}])
        self.assertEqual(rules.parse_code_values("x"), [])

    def test_courses_body(self):
        self.assertEqual(
            rules.courses_body("Modern Medicine", "doctor"),
            {"systemOfMedicine": "Modern Medicine", "hprType": "doctor", "qualificationCount": 0},
        )

    def test_sandbox_shapes_of_2026_09_21(self):
        # The OWNER master pads its codes and values; the languages pad their names.
        owner = rules.parse_code_values(
            {"type": "OWNER", "data": [{"code": "G         ", "value": "Government        "}]}
        )
        self.assertEqual(owner, [{"code": "G", "name": "Government"}])
        self.assertEqual(rules.parse_code_values([{"id": 1, "name": " English "}]), [{"code": "1", "name": "English"}])
        # HPR districts, sub-districts, countries and systems of medicine name their fields differently.
        rows = rules.parse_code_values(
            [{"id": 242, "stateId": 14, "districtName": "Bokaro", "isoCode": "322", "status": True}]
        )
        self.assertEqual(rows, [{"code": "242", "name": "Bokaro"}])
        rows = rules.parse_code_values([{"id": 193, "districtCode": 1, "subDistrictName": "Anantnag"}])
        self.assertEqual(rows, [{"code": "193", "name": "Anantnag"}])
        rows = rules.parse_code_values(
            [{"id": 356, "alpha_2_code": "IN", "enShortName": "India", "nationality": "Indian"}]
        )
        self.assertEqual(rows, [{"code": "356", "name": "India"}])
        # Systems of medicine carry both an `id` and a slug `code`; the register body takes the id.
        rows = rules.parse_code_values(
            [{"id": 1, "medicalSystem": "Modern Medicine", "code": "modern_medicine", "hprType": "doctor"}]
        )
        self.assertEqual(rows, [{"code": "1", "name": "Modern Medicine"}])
        # A text answer ("Data not available in database") is an empty list, not an error.
        self.assertEqual(rules.parse_code_values({"text": "Data not available in database"}), [])

    def test_owner_subtype_codes(self):
        self.assertEqual([r["code"] for r in rules.owner_subtypes_for("G")], ["C"])
        self.assertEqual([r["code"] for r in rules.owner_subtypes_for("P")], ["P", "NP"])
        self.assertEqual([r["code"] for r in rules.owner_subtypes_for("PP")], ["P", "NP"])
        self.assertEqual(rules.owner_subtypes_for(""), [])
        self.assertIn("FAC-STATUS", rules.MASTER_TYPES)
        self.assertIn("TYPE-SERVICE", rules.MASTER_TYPES)

    def test_parse_facility_search_keeps_the_sandbox_codes(self):
        row = rules.parse_facility_search(
            {
                "facilities": [
                    {
                        "facilityId": "IN1410000232",
                        "facilityName": "Manipur Test Facility",
                        "systemOfMedicineCode": "M",
                        "subDistrictLGDCode": "1881",
                        "villageCityTownName": None,
                        "villageCityTownLGDCode": None,
                        "workingInPsu": False,
                    }
                ],
                "totalFacilities": 1,
                "numberOfPages": 1,
            }
        )["facilities"][0]
        self.assertEqual(row["systemOfMedicineCode"], "M")
        self.assertEqual(row["subDistrictLGDCode"], "1881")
        self.assertEqual(row["villageCityTownLGDCode"], "")


if __name__ == "__main__":
    unittest.main()
