# When something breaks

Find the symptom you are seeing. Every page here walks the checks in the order this catalogue recommends checking, not a record of how often each has turned out to be the actual cause, so you do not need to know an error code to start.

- [The callback never arrives](/docs/hiecm/v3/troubleshooting/callback-never-arrives): a call returned 202, and nothing followed on your registered URL.
- [Everything returns 401](/docs/hiecm/v3/troubleshooting/everything-returns-401): every call fails the same way, not just one endpoint.
- [The OTP never arrives](/docs/hiecm/v3/troubleshooting/otp-never-arrives): you requested an OTP and nothing reached the phone.
- [Accepted, then nothing](/docs/hiecm/v3/troubleshooting/accepted-then-nothing): discovery or linking started and stalled somewhere in the middle.
- [Consent stuck in Requested](/docs/hiecm/v3/troubleshooting/consent-stuck-requested): a consent request never moved to Granted or Denied.

If your symptom is not here, or you already have an error code in hand, the [error codes reference](/docs/hiecm/v3/reference/error-codes) is organised the other way, by code.

## What to put in a support request

Raise it through [Support](/docs/support), with:

| Include                          | Example                                |
| -------------------------------- | -------------------------------------- |
| The API you called               | `POST /api/hiecm/gateway/v3/sessions`  |
| The `REQUEST-ID` header you sent | `4f8a1c62-6a3b-4d0e-9d7c-2b1f0a5e8d31` |
| The `TIMESTAMP` header you sent  | `2026-08-24T09:14:07.412Z`             |
| The response you received        | Status code and full body              |
| What you expected instead        | The behaviour the document describes   |

Add the callback body if the call is asynchronous and a callback arrived. Never post an access token, a client secret, or a real patient's identifiers. Replace them with a placeholder.

`REQUEST-ID` is a fresh UUID you generate per request. It is the one value that names the exact call you made, so log it and quote it.
