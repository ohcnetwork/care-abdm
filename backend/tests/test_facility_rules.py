import unittest

from abdm.facility.rules import validate_facility_id, validate_facility_name, validate_hip_name


class FacilityRulesTests(unittest.TestCase):
    def test_facility_id_must_start_with_in_and_have_12_characters(self):
        validate_facility_id("")
        validate_facility_id("IN1410000232")

        for bad in ("in1410000232", "IN141000023", "IN14100002320", "AB1410000232", "IN14100002--"):
            with (
                self.subTest(bad=bad),
                self.assertRaisesRegex(
                    ValueError,
                    "HFR facility ID must start with IN and have 12 characters.",
                ),
            ):
                validate_facility_id(bad)

    def test_facility_name_allows_docs_characters_and_space(self):
        validate_facility_name("")
        validate_facility_name("Care Health-1_2.3(4),/Unit")

        with self.assertRaisesRegex(ValueError, "Facility name can use only letters, digits, space, and -_.\\(\\),/."):
            validate_facility_name("Care Health #1")

    def test_hip_name_has_15_character_limit_and_no_special_characters(self):
        validate_hip_name("")
        validate_hip_name("Care Health 123")

        for bad in ("Care Health 1234", "Care-Health"):
            with (
                self.subTest(bad=bad),
                self.assertRaisesRegex(
                    ValueError,
                    "HIP name must be 15 characters or fewer with no special characters.",
                ),
            ):
                validate_hip_name(bad)


class AlreadyAssociatedTests(unittest.TestCase):
    # Real sandbox refusal (findings B20), HTTP 200 with the error envelope.
    LINE = (
        "2500 Bridge-Id=SBXID_035123 is already associated with Hfr-Id=IN3210000772 for "
        "Service-Id=IN3210000772, Service-Name=SECONDARY FACIL"
    )

    def test_service_id_is_read_when_the_refusal_names_our_facility(self):
        from abdm.facility.rules import already_associated_service

        self.assertEqual(already_associated_service([self.LINE], "IN3210000772"), "IN3210000772")

    def test_suffixed_service_form_is_read(self):
        from abdm.facility.rules import already_associated_service

        line = "2500 Bridge-Id=SBXID_1 is already associated with Hfr-Id=IN1410000232_1 for Service-Id=IN1410000232_1"
        self.assertEqual(already_associated_service([line], "IN1410000232"), "IN1410000232_1")

    def test_another_facility_or_another_refusal_is_still_a_failure(self):
        from abdm.facility.rules import already_associated_service

        self.assertEqual(already_associated_service([self.LINE], "IN1410000232"), "")
        self.assertEqual(already_associated_service([self.LINE], ""), "")
        self.assertEqual(already_associated_service(["2500 Provided facility name is not matched"], "IN3210000772"), "")
        self.assertEqual(already_associated_service([], "IN3210000772"), "")


class HipServiceLookupTests(unittest.TestCase):
    # Real sandbox row (findings B18): the registry suffixes the HFR id and tags both roles.
    SANDBOX = [{"id": "IN1410000232_1", "name": "FACILITY WITH P", "types": ["HIP", "HIU"], "active": True}]

    def test_sandbox_service_id_is_the_hfr_id_with_a_suffix(self):
        from abdm.facility.rules import find_hip_service

        self.assertEqual(find_hip_service("IN1410000232", self.SANDBOX), "IN1410000232_1")
        self.assertEqual(find_hip_service("IN9999999999", self.SANDBOX), "")
        self.assertEqual(find_hip_service("", self.SANDBOX), "")

    def test_exact_match_wins_and_docs_shape_is_read(self):
        from abdm.facility.rules import find_hip_service

        services = [
            {"serviceId": "IN1410000232_1", "isHip": True},
            {"serviceId": "IN1410000232", "isHip": True},
            {"serviceId": "IN1410000232_2", "isHip": False, "isHiu": True},
        ]
        self.assertEqual(find_hip_service("IN1410000232", services), "IN1410000232")

    def test_inactive_and_hiu_only_services_are_skipped(self):
        from abdm.facility.rules import find_hip_service

        self.assertEqual(find_hip_service("IN1", [{"id": "IN1_1", "types": ["HIU"]}]), "")
        self.assertEqual(find_hip_service("IN1", [{"id": "IN1_1", "types": ["HIP"], "active": False}]), "")
        self.assertEqual(find_hip_service("IN1", [{"id": "IN1_1"}]), "IN1_1")
