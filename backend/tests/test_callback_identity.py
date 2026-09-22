"""The callback idempotency key (`callbacks/receiver.py`).

A gateway-initiated notify is redelivered with a fresh REQUEST-ID and a fresh `timestamp`, so the
default key (which hashes the raw body and the header) sees every copy as new. `IDENTITY_FIELDS`
names the fields that identify such a callback instead.
"""

import json
import unittest

from abdm.callbacks.identity import idempotency_key as _idempotency_key
from abdm.callbacks.identity import identity as _identity


def notify_body(
    status: str = "GRANTED", artefacts: tuple[str, ...] = ("a1",), timestamp: str = "2026-09-22T06:00:00"
) -> dict:
    """`05-m3-post-v3-hiu-consent-request-notify` shape, with the fields ABDM varies per delivery."""
    return {
        "timestamp": timestamp,
        "notification": {
            "consentRequestId": "43bdc247-8909-40c5-81c1-a6dcde03351e",
            "status": status,
            "consentArtefacts": [{"id": a} for a in artefacts],
        },
    }


def key_for(
    body: dict,
    request_id: str,
    operation_id: str = "m3-hiu-consent-notify",
    path: str = "/v3/hiu/consent/request/notify",
) -> str:
    raw = json.dumps(body).encode("utf-8")
    return _idempotency_key(path, request_id, "", "", raw, _identity(operation_id, body))


class ConsentNotifyIdentityTests(unittest.TestCase):
    def test_redelivery_with_a_new_request_id_and_timestamp_is_the_same_callback(self):
        # The bug this guards: ABDM rotates REQUEST-ID per delivery, so keying on it (or on the
        # raw body, which carries `timestamp`) let every redelivery through as new work.
        first = key_for(notify_body(), "11111111-1111-1111-1111-111111111111")
        again = key_for(notify_body(timestamp="2026-09-22T06:04:31"), "22222222-2222-2222-2222-222222222222")
        self.assertEqual(first, again)

    def test_a_later_decision_on_the_same_request_is_not_a_duplicate(self):
        granted = key_for(notify_body("GRANTED"), "11111111-1111-1111-1111-111111111111")
        revoked = key_for(notify_body("REVOKED"), "11111111-1111-1111-1111-111111111111")
        self.assertNotEqual(granted, revoked)

    def test_a_revoke_naming_other_artefacts_is_not_a_duplicate(self):
        one = key_for(notify_body("REVOKED", ("a1",)), "11111111-1111-1111-1111-111111111111")
        two = key_for(notify_body("REVOKED", ("a1", "a2")), "11111111-1111-1111-1111-111111111111")
        self.assertNotEqual(one, two)

    def test_artefact_order_does_not_change_the_identity(self):
        one = key_for(notify_body("REVOKED", ("a1", "a2")), "11111111-1111-1111-1111-111111111111")
        two = key_for(notify_body("REVOKED", ("a2", "a1")), "33333333-3333-3333-3333-333333333333")
        self.assertEqual(one, two)

    def test_two_requests_are_never_confused(self):
        other = notify_body()
        other["notification"]["consentRequestId"] = "00000000-0000-0000-0000-000000000000"
        self.assertNotEqual(
            key_for(notify_body(), "11111111-1111-1111-1111-111111111111"),
            key_for(other, "11111111-1111-1111-1111-111111111111"),
        )


class DefaultKeyTests(unittest.TestCase):
    def test_an_operation_without_an_identity_still_keys_on_the_body(self):
        body = {"response": {"requestId": "r1"}, "consentRequest": {"id": "c1"}}
        self.assertEqual(_identity("m3-on-consent-request-init", body), "")
        same = key_for(body, "r1", "m3-on-consent-request-init", "/v3/hiu/consent/request/on-init")
        again = key_for(body, "r1", "m3-on-consent-request-init", "/v3/hiu/consent/request/on-init")
        differs = key_for(body, "r2", "m3-on-consent-request-init", "/v3/hiu/consent/request/on-init")
        self.assertEqual(same, again)
        self.assertNotEqual(same, differs)

    def test_a_notify_missing_its_identifying_fields_falls_back_to_the_body(self):
        # Never key an empty identity: every malformed notify would collapse onto one row.
        self.assertEqual(_identity("m3-hiu-consent-notify", {"notification": {}}), "")


if __name__ == "__main__":
    unittest.main()
