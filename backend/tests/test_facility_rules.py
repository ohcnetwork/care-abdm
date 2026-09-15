import unittest

from abdm.facility.rules import validate_facility_id, validate_facility_name, validate_hip_name


class FacilityRulesTests(unittest.TestCase):
    def test_facility_id_must_start_with_in_and_have_12_characters(self):
        validate_facility_id("")
        validate_facility_id("IN1410000232")

        for bad in ("in1410000232", "IN141000023", "IN14100002320", "AB1410000232", "IN14100002--"):
            with self.subTest(bad=bad), self.assertRaisesRegex(
                ValueError,
                "HFR facility ID must start with IN and have 12 characters.",
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
            with self.subTest(bad=bad), self.assertRaisesRegex(
                ValueError,
                "HIP name must be 15 characters or fewer with no special characters.",
            ):
                validate_hip_name(bad)
