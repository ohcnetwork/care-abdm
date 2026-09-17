"""
ADR-012. The catalogue comes from /docs/hiecm/v3/reference/error-codes.md, which the docs page
getting-started/build-it-well tells every HIP to key its handling to. These tests hold the
behaviour the desk depends on: what happened, what to do, and whether a repeat can help.
"""

import unittest
from datetime import UTC, datetime, timedelta

from abdm import errors

NOW = datetime(2026, 9, 17, 15, 47, 35, tzinfo=UTC)


class NormalizeTests(unittest.TestCase):
    def test_punctuation_and_case_are_removed(self):
        # Observed 2026-09-17 on an on-generate-token error callback: {"code": "ABDM-1027: "}.
        self.assertEqual(errors.normalize_code("ABDM-1027: "), "ABDM-1027")
        self.assertEqual(errors.normalize_code(" abdm-1092 "), "ABDM-1092")
        self.assertEqual(errors.normalize_code(None), "")
        self.assertEqual(errors.normalize_code(1092), "1092")


class CatalogueTests(unittest.TestCase):
    def test_the_generated_catalogue_is_large_and_holds_the_codes_the_plug_meets(self):
        self.assertGreater(len(errors.ERROR_ACTIONS), 700)
        for code in ("ABDM-1026", "ABDM-1027", "ABDM-1035", "ABDM-1038", "ABDM-1063", "ABDM-1092"):
            self.assertIn(code, errors.ERROR_ACTIONS, code)

    def test_an_unknown_code_is_unclassified_and_asks_for_support(self):
        failure = errors.classify(code="ABDM-0000", request_id="REQ-1")
        self.assertEqual(failure.action, errors.UNCLASSIFIED)
        self.assertEqual(failure.retry, errors.NEVER)
        self.assertIn("REQ-1", failure.next_step)

    def test_a_code_the_docs_give_only_as_a_group_falls_back_to_the_group(self):
        # The docs list "HIS-1xxx" and "HIS-400 to HIS-504" instead of each code.
        self.assertEqual(errors.action_for("HIS-1500"), errors.ERROR_ACTIONS["HIS-1xxx"])
        self.assertEqual(errors.action_for("HIS-450"), errors.ERROR_ACTIONS["HIS-400 to HIS-504"])


class DuplicateTokenRequestTests(unittest.TestCase):
    """ABDM-1092. Measured 2026-09-17: 11 refusals from 4 s to 362 s after the accepted request,
    12 acceptances from 374 s on. The window runs from the accepted request, not from a refusal."""

    def test_the_window_closes_after_the_measured_boundary(self):
        self.assertTrue(errors.window_open(NOW, NOW + timedelta(seconds=362)))
        self.assertFalse(errors.window_open(NOW, NOW + timedelta(seconds=421)))
        self.assertFalse(errors.window_open(None, NOW))
        self.assertGreater(errors.TOKEN_REQUEST_WINDOW, timedelta(seconds=374))

    def test_the_desk_gets_a_time_to_try_again(self):
        failure = errors.classify(code="ABDM-1092", message="Duplicate Link token request", since=NOW)
        self.assertEqual(failure.action, errors.WAIT)
        self.assertEqual(failure.retry, errors.AFTER)
        self.assertEqual(failure.retry_at, errors.window_ends(NOW))
        self.assertFalse(failure.retry_now)

    def test_abdm_wording_stays_out_of_the_desk_sentence(self):
        # ADR-011: the desk never reads gateway, callback, care context, bridge or token.
        failure = errors.classify(code="ABDM-1092", message="Duplicate Link token request", since=NOW)
        for word in ("gateway", "callback", "care context", "bridge", "token", "probe"):
            self.assertNotIn(word, f"{failure.what} {failure.next_step}".lower(), word)
        self.assertEqual(failure.detail, "Duplicate Link token request")


class BlockAndPermissionTests(unittest.TestCase):
    def test_a_block_waits_24_hours(self):
        failure = errors.classify(code="ABDM-1027", since=NOW)
        self.assertEqual(failure.action, errors.BLOCKED)
        self.assertEqual(failure.retry_at, NOW + timedelta(hours=24))

    def test_already_linked_counts_as_success(self):
        # The catalogue lists ABDM-1056 twice; the plug only ever meets "already linked".
        failure = errors.classify(code="ABDM-1056", message="This care contexts has been already linked")
        self.assertTrue(failure.succeeded)
        self.assertEqual(failure.retry, errors.NEVER)

    def test_an_invalid_permission_is_renewed_and_repeated_at_once(self):
        for code in ("ABDM-1026", "ABDM-1038", "ABDM-1063"):
            failure = errors.classify(code=code)
            self.assertTrue(failure.renew_permission, code)
            self.assertTrue(failure.retry_now, code)

    def test_an_unregistered_facility_points_at_the_setup_page(self):
        failure = errors.classify(code="ABDM-1035")
        self.assertEqual(failure.action, errors.FIX_REQUEST)
        self.assertEqual(failure.retry, errors.NEVER)
        self.assertIn("setup", failure.next_step.lower())


class TransientTests(unittest.TestCase):
    def test_a_5xx_is_repeated(self):
        # Observed 2026-09-17: 303001 "Address endpoint [State : SUSPENDED]" twice, then success.
        failure = errors.classify(code="303001", message="Runtime Error", http_status=500)
        self.assertTrue(failure.retry_now)

    def test_a_transport_failure_is_repeated(self):
        failure = errors.classify(exception="ConnectTimeout")
        self.assertTrue(failure.retry_now)
        self.assertEqual(failure.code, "")

    def test_a_refusal_with_no_reason_asks_for_the_reference(self):
        # Observed 2026-09-17: 9 of 9 link calls answered with an empty HTTP 400 (finding E11).
        failure = errors.classify(http_status=400, request_id="REQ-7")
        self.assertEqual(failure.action, errors.ASK_SUPPORT)
        self.assertFalse(failure.retry_now)
        self.assertIn("REQ-7", failure.next_step)

    def test_a_refusal_with_no_reason_and_no_reference_points_at_the_admin_page(self):
        failure = errors.classify(http_status=400)
        self.assertNotIn("none", failure.next_step)

    def test_a_stored_http_code_keeps_its_meaning(self):
        # outbound.send() stores "HTTP_400" when ABDM refuses with no code of its own.
        self.assertFalse(errors.classify(code="HTTP_400").retry_now)
        self.assertEqual(errors.classify(code="HTTP_400", request_id="R1").action, errors.ASK_SUPPORT)
        self.assertTrue(errors.classify(code="HTTP_503").retry_now)


class NoAnswerTests(unittest.TestCase):
    """Care runs no beat schedule for plugs, so the rule is applied when the desk reads (D6)."""

    def test_a_wait_becomes_a_failure_after_the_deadline(self):
        self.assertFalse(errors.answer_overdue(NOW, NOW + errors.CALLBACK_DEADLINE))
        self.assertTrue(errors.answer_overdue(NOW, NOW + errors.CALLBACK_DEADLINE + timedelta(seconds=1)))
        self.assertFalse(errors.answer_overdue(None, NOW))

    def test_the_desk_is_told_to_try_again(self):
        failure = errors.no_answer(request_id="REQ-3")
        self.assertEqual(failure.code, "NO_ANSWER")
        self.assertTrue(failure.retry_now)


class PlugCodeTests(unittest.TestCase):
    def test_every_plug_code_gives_a_sentence_and_a_next_step(self):
        for code in errors.PLUG_CODES:
            failure = errors.classify(code=code)
            self.assertTrue(failure.what, code)
            self.assertTrue(failure.next_step, code)

    def test_no_abha_cannot_proceed(self):
        failure = errors.classify(code="NO_ABHA")
        self.assertEqual(failure.action, errors.CANNOT_PROCEED)
        self.assertEqual(failure.retry, errors.NEVER)


class ApiShapeTests(unittest.TestCase):
    def test_the_block_the_mfe_reads_holds_every_field(self):
        block = errors.classify(code="ABDM-1092", since=NOW).as_dict()
        self.assertEqual(
            sorted(block),
            ["action", "code", "detail", "nextStep", "retry", "retryAt", "supportReference", "what"],
        )
        self.assertEqual(block["retryAt"], errors.window_ends(NOW))

    def test_the_summary_is_1_line_for_the_audit_row(self):
        summary = errors.classify(code="ABDM-1092", message="Duplicate Link token request", request_id="R1").summary()
        self.assertNotIn("\n", summary)
        self.assertIn("R1", summary)
        self.assertIn("Duplicate Link token request", summary)


if __name__ == "__main__":
    unittest.main()
