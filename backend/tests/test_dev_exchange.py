"""The exchange model of the developer explorer (ADR-018): the docs' 5 states, kinds and timings."""

import re
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from abdm.callbacks.paths import CALLBACK_OPERATION_BY_PATH
from abdm.dev import exchange as x
from abdm.errors import CALLBACK_DEADLINE

T0 = datetime(2026, 9, 21, 10, 0, 0, tzinfo=UTC)
SRC = Path(__file__).resolve().parents[1] / "src" / "abdm"


def _sent_operation_ids() -> set[str]:
    """Every operation id the plug sends, read from the source (1-line and 2-line send() calls)."""
    ids = set()
    for path in SRC.rglob("*.py"):
        if "/dev/" in str(path) or path.name.startswith("test"):
            continue
        text = path.read_text()
        ids |= set(re.findall(r'outbound\.send\(\s*"([a-z0-9-]+)"', text))
        ids |= set(re.findall(r'ACK_OPERATION_ID = "([a-z0-9-]+)"', text))
    return ids


class StateTests(unittest.TestCase):
    def state(self, **kw):
        base = {
            "operation_id": "m2-generate-link-token",
            "status": "succeeded",
            "http_status": 202,
            "sent_at": T0,
            "callbacks_received": 0,
            "now": T0 + timedelta(seconds=1),
            "window": CALLBACK_DEADLINE,
        }
        base.update(kw)
        return x.state_of(**base)

    def test_the_5_states_with_the_docs_figures(self):
        # design.md: "accepted, waiting: 202, nothing back yet — real patient, 340 ms"
        self.assertEqual(self.state(now=T0 + timedelta(milliseconds=340)), "accepted_waiting")
        # "refused before waiting: a synchronous 400, nothing was ever pending — 91 ms"
        self.assertEqual(self.state(status="failed", http_status=400), "refused")
        # "answered: the callback arrived"
        self.assertEqual(self.state(callbacks_received=1), "answered")
        # "no answer in the window: accepted, then silence" — the plug's window is 10 minutes
        self.assertEqual(self.state(now=T0 + timedelta(seconds=60)), "accepted_waiting")
        self.assertEqual(self.state(now=T0 + CALLBACK_DEADLINE + timedelta(seconds=1)), "no_answer")
        # in the air
        self.assertEqual(self.state(status="sent", http_status=None), "sent")

    def test_a_synchronous_call_is_answered_by_its_http_body(self):
        for op in ("gateway-list-bridge-services", "m4-facility-search", "m1-post-v3-profile-login-request-otp"):
            self.assertEqual(self.state(operation_id=op, http_status=200), "answered")
        # an ack and a push are synchronous too
        self.assertEqual(self.state(operation_id="m2-consent-hip-on-notify"), "answered")
        self.assertEqual(self.state(operation_id="m2-data-push", http_status=202), "answered")
        # a transport failure is a refusal with a reason
        self.assertEqual(self.state(operation_id="m4-auth-cert", status="failed", http_status=None), "refused")
        self.assertEqual(
            x.reason_of(status="failed", http_status=None, error_code="ConnectTimeout"), "unreachable: ConnectTimeout"
        )
        self.assertEqual(x.reason_of(status="failed", http_status=400, error_code="ABDM-1092"), "ABDM-1092")
        self.assertEqual(x.reason_of(status="failed", http_status=400, error_code=""), "HTTP 400")
        self.assertEqual(x.reason_of(status="succeeded", http_status=202, error_code=""), "")

    def test_kinds_and_modules(self):
        self.assertEqual(x.kind_of("m2-generate-link-token"), "call")
        self.assertEqual(x.kind_of("m3-consent-notify-ack"), "ack")
        self.assertEqual(x.kind_of("m2-data-push"), "push")
        self.assertEqual(x.kind_of("m4-hfr-basic-information"), "sync")
        for op, module in (
            ("gateway-sessions-create", "gateway"),
            ("m1-post-v3-enrollment-request-otp", "m1"),
            ("m2-hip-link-care-context", "m2"),
            ("m3-consent-fetch", "m3"),
            ("m4-master-lgd-states", "m4"),
            ("probe-response-headers", "probe"),
            ("", "other"),
        ):
            self.assertEqual(x.module_of(op), module)

    def test_every_sent_operation_has_a_kind_and_every_callback_call_is_listed(self):
        sent = _sent_operation_ids()
        self.assertGreaterEqual(len(sent), 20)
        for op in sent:
            self.assertIn(x.kind_of(op), x.KINDS)
        # Every operation that expects a callback maps to a callback path the plug knows.
        answered = set(CALLBACK_OPERATION_BY_PATH.values())
        self.assertGreater(len(answered), 10)
        # Every ack is an operation the plug really sends.
        for op in x.ACKS:
            self.assertIn(op, sent, op)
        for op in x.EXPECTS_CALLBACK:
            self.assertIn(op, sent, op)

    def test_timings_and_paths(self):
        self.assertEqual(x.http_ms(T0, T0 + timedelta(milliseconds=340)), 340)
        self.assertEqual(x.http_ms(T0, None), None)
        self.assertEqual(x.callback_seconds(T0, T0 + timedelta(seconds=1.94)), 1.9)
        self.assertEqual(x.callback_seconds(T0, T0 + timedelta(seconds=968)), 968.0)
        self.assertEqual(
            x.path_of("https://dev.abdm.gov.in/api/hiecm/hip/v3/link/carecontext"), "/api/hiecm/hip/v3/link/carecontext"
        )
        self.assertEqual(x.path_of("https://host"), "/")
        self.assertEqual(x.path_of("/relative"), "/relative")

    def test_summarize_error_reads_the_3_envelopes(self):
        self.assertEqual(
            x.summarize_error([{"error": {"code": "ABDM-9999: ", "message": "Invalid from/to date"}}]),
            "ABDM-9999:  Invalid from/to date",
        )
        self.assertEqual(
            x.summarize_error(
                {
                    "code": "HIS-422",
                    "message": "wrong data",
                    "details": [{"code": "HIS-1070", "message": "Required OwnershipCode Field is empty."}],
                }
            ),
            "HIS-1070 Required OwnershipCode Field is empty.",
        )
        self.assertEqual(x.summarize_error({"message": "Invalid OTP"}), "Invalid OTP")
        self.assertEqual(x.summarize_error({"text": "Please make a valid request."}), "Please make a valid request.")
        self.assertEqual(x.summarize_error({}), "")
        self.assertEqual(x.summarize_error(None), "")


if __name__ == "__main__":
    unittest.main()
