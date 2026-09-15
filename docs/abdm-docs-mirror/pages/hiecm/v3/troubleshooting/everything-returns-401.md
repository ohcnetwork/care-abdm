# Everything returns 401

Every call fails the same way, on every endpoint, not just one. That pattern points at your session or your headers, not at any single operation.

Before working through the checks, confirm more than one endpoint is actually failing. If only one call fails while others succeed, read that call's own error code on the [error codes reference](/docs/hiecm/v3/reference/error-codes) instead. Read the response body too, not only the status: the gateway returns a code that names the real reason.

## Work through these in order

1. **Has your session token expired?** Session tokens are short lived. Read `expiresIn` from the sessions call response rather than assuming a duration, and re-run it for a fresh token instead of retrying the failing call with the old one. See [authentication](/docs/hiecm/v3/reference/authentication).
2. **Are you calling the wrong environment's base URL?** A sandbox token is not valid against a production base URL, or the reverse. Look at the host in the failing request and the host you requested the session token from, side by side. If they differ, point every call at the same host you authenticated against.
3. **Is your clock wrong?** The `TIMESTAMP` header has to be close to the gateway's own clock, in ISO 8601 UTC. A container host that was suspended and resumed is the usual cause, because its clock resumes behind. See [authentication](/docs/hiecm/v3/reference/authentication).
4. **Is `X-CM-ID` missing or wrong for this environment?** Look at the literal value you sent, not the value you meant to send: `sbx` on the sandbox, `abdm` in production. This header names the consent manager you are pointed at, and the wrong value fails every call the same way a missing session token does.

## How you know it worked

A call that was returning 401 now returns its normal response, and stays that way across more than one call in a row. A single success right after several failures can be a token that was about to expire anyway; confirm with a second call a minute or more later.

## When it goes wrong

If you have re-run the session call, confirmed the environment, fixed the clock, and confirmed `X-CM-ID`, and calls still return 401 with no matching code, escalate on the [NHA dev forum](https://devforum.abdm.gov.in). Report the API you called, the `REQUEST-ID`, the `TIMESTAMP`, and the full response body. See [Support](/docs/support) for the full report format.

The codes this symptom can surface are on the [error codes reference](/docs/hiecm/v3/reference/error-codes): an invalid timestamp, the wrong consent manager id, a missing session token, or a required header that is absent or malformed.

[Next Still stuck? Read authentication end to end Every header a call needs, and what the gateway does when one is wrong.](/docs/hiecm/v3/reference/authentication)
