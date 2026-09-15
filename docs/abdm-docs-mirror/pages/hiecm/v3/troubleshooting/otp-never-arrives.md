# The OTP never arrives

You called the request OTP operation, got back a `txnId`, and the phone you are watching has not received an [OTP](/docs/hiecm/v3/getting-started/glossary#otp).

Before working through the checks, confirm the request call itself succeeded and returned a `txnId`. If it failed, work through [Everything returns 401](/docs/hiecm/v3/troubleshooting/everything-returns-401) or the code the response names on the [error codes reference](/docs/hiecm/v3/reference/error-codes) instead.

## Work through these in order

1. **Is this the Aadhaar mobile, and are you holding it?** In the Aadhaar OTP enrolment flow, only the mobile number registered against that Aadhaar number receives the OTP. That is not necessarily the phone the person is holding while they enrol. See the [M1 user journey](/docs/hiecm/v3/milestones/m1) for the full enrolment sequence, and confirm which number Aadhaar has on file before assuming delivery failed.
2. **Have you requested an OTP for this transaction more than a few times in a short window?** You may have been rate limited. A retry loop that fires the request call again on every failure can trigger this without the failure showing clearly in your own logs, because a rate limit response can read like a plain timeout depending on how your client surfaces it.
3. **Has the transaction expired before you tried to verify it?** How long a `txnId` stays valid is not documented yet. A failed enrolment call should not be retried blindly: start a fresh OTP request rather than reuse an old `txnId` if enough time has passed that you are unsure it is still live.

## How you know it worked

The phone registered against the identifier you sent receives an SMS carrying an OTP, and verifying it with that `txnId` succeeds. Receiving a `txnId` from the request call alone does not confirm the SMS was sent.

## When it goes wrong

If you have confirmed the receiving number, are not rate limited, and the transaction is fresh, and the OTP still has not arrived, escalate on the [developer forum](https://devforum.abdm.gov.in) rather than requesting again. Report the API you called, the `REQUEST-ID`, the `TIMESTAMP`, and the full response body including the `txnId`. See [Support](/docs/support) for the full report format.

This symptom can surface as a rate limit code or the catch-all failure code, both on the [error codes reference](/docs/hiecm/v3/reference/error-codes).

[Next Still stuck? Walk the M1 user journey See exactly where the OTP request sits among the calls that create an ABHA.](/docs/hiecm/v3/milestones/m1)
