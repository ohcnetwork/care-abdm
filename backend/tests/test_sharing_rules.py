import unittest
from datetime import UTC, datetime, timedelta

from abdm.hip import rules


class StagingRulesTests(unittest.TestCase):
    def test_prescription_is_shareable_unless_draft_cancelled_or_error(self):
        for status in ("active", "on_hold", "ended", "stopped", "completed"):
            self.assertTrue(rules.prescription_is_shareable(status), status)
        for status in ("draft", "cancelled", "entered_in_error", "", None):
            self.assertFalse(rules.prescription_is_shareable(status), status)

    def test_diagnostic_report_is_shareable_only_when_final(self):
        self.assertTrue(rules.diagnostic_report_is_shareable("final"))
        for status in ("registered", "partial", "preliminary", None):
            self.assertFalse(rules.diagnostic_report_is_shareable(status), status)

    def test_discharge_summary_needs_type_completed_and_not_archived(self):
        self.assertTrue(rules.discharge_summary_is_shareable("discharge_summary", True, False))
        self.assertFalse(rules.discharge_summary_is_shareable("discharge_summary", False, False))
        self.assertFalse(rules.discharge_summary_is_shareable("discharge_summary", True, True))
        self.assertFalse(rules.discharge_summary_is_shareable("encounter_report", True, False))

    def test_op_consultation_is_outpatient_only(self):
        self.assertTrue(rules.op_consultation_applies("amb"))
        for cls in ("imp", "emer", "obsenc", "vr", "hh", None):
            self.assertFalse(rules.op_consultation_applies(cls), cls)

    def test_encounter_closes_on_completed_or_discharged(self):
        self.assertTrue(rules.encounter_closes("completed"))
        self.assertTrue(rules.encounter_closes("discharged"))
        for status in ("planned", "in_progress", "on_hold", "cancelled", "entered_in_error", None):
            self.assertFalse(rules.encounter_closes(status), status)

    def test_item_label_has_no_clinical_detail(self):
        when = datetime(2026, 9, 18, 10, 42, tzinfo=UTC)
        self.assertEqual(rules.item_label("Prescription", when), "Prescription · 18 Sep 2026 10:42")
        self.assertEqual(rules.item_label("DiagnosticReport", when, "CBC"), "Diagnostic report CBC · 18 Sep 2026 10:42")
        self.assertEqual(rules.item_label("OPConsultation", None), "OP consultation")


class RetryRulesTests(unittest.TestCase):
    def test_next_attempt_stops_after_max_retries(self):
        now = datetime(2026, 9, 18, 12, 0, tzinfo=UTC)
        hour = timedelta(hours=1)
        # attempts counts the attempts made so far: 1 first try + up to 3 retries.
        self.assertEqual(rules.next_attempt(now, 1, hour, 3), now + hour)
        self.assertEqual(rules.next_attempt(now, 3, hour, 3), now + hour)
        self.assertIsNone(rules.next_attempt(now, 4, hour, 3))
        self.assertIsNone(rules.next_attempt(now, 1, hour, 0))
