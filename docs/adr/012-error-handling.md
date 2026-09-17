# ADR-012 — Error handling: one catalogue, one failure shape, no endless spinner

Status: Accepted (2026-09-17)
Supersedes: the `ABDM-1092` handling added in `81e18ca`, and `rules.LINK_TOKEN_FRESHNESS` from
ADR-011's 2026-09-17 amendment.

## Context

The happy path is built. Every failure path is not. The evidence below comes from the plug's own
audit tables (`abdm_abdmoutboundrequest`, `abdm_abdmcallback`) on 2026-09-17, read with `psql`.

### 1. The desk sees nothing

`{"error": {"code": "ABDM-1092", "message": "Duplicate Link token request"}}` is recorded on the
outbound row. `care-context-state.ts` maps that code to `in_progress`, so the dialog shows a
spinner that never stops. 3 care-context rows were in that state when this ADR was written.

Every other failure has the same gap. The audit table holds the answer. The desk does not.

### 2. The plug causes the `ABDM-1092` itself

The gateway refuses a second link-token request for the same ABHA address at the same HIP inside a
time window. The window is measured from the last **accepted** request:

| Gap after the last accepted request | Result | Count |
|---|---|---|
| 4 s, 156 s, 181 s, 186 s, 198 s, 214 s, 217 s, 246 s, 321 s, 350 s, 362 s | `ABDM-1092` | 11 |
| 374 s, 685 s, 776 s, 825 s, 884 s, 921 s, 1277 s, 8357 s, 151488 s | accepted | 12 |

The boundary is between **362 s and 374 s**, so the window is about 6 minutes. A delivered answer
does not close it: patient 77 received a token at 15:47:40 and was still refused at 15:53:37.

`LINK_TOKEN_FRESHNESS = 5 minutes` makes the plug ask again 5 to 6 minutes after the last request.
That is inside the window, so the refusal is certain.

The 5-minute rule also has no evidence behind it. It came from finding F1: a link call 8 minutes
after its token was refused with an empty HTTP 400. On 2026-09-17 the token callback arrived at
15:47:40.032 and the link call went out at 15:47:40.128 with a token 2 seconds old. It was refused
with the same empty HTTP 400. Token age is not the cause. The rule only causes `ABDM-1092`.

### 3. The plug throws real answers away

2 genuine callbacks failed the signature check and were lost:

| Received | Content lost | Bearer token `exp` |
|---|---|---|
| 07:31:50 Z | a valid link token | 07:26:27 Z |
| 10:16:16 Z | an `ABDM-1027` block | 10:14:26 Z |

The gateway mints its 20-minute session token up to 9 minutes before it builds the callback. It
then retries a failed delivery about **16 minutes** later (965 s and 963 s, measured from the
callback `TIMESTAMP` header) with the same token. By then the token `exp` has passed, `jwt.decode`
refuses it, and the plug answers 401 and drops the row. The patient's visit then waits for an
answer that already came. This answers open finding E10.

### 4. Transient failures are treated as permanent

`303001 Runtime Error ... [ State : SUSPENDED ]` (HTTP 500) failed twice at 13:29 and succeeded at
13:32. The plug marked the visit failed. `outbound.send()` also raises on a network error, which
reaches the desk as an HTTP 500 with no message.

### 5. There is no hand-written catalogue to maintain

`docs/abdm-docs-mirror/pages/hiecm/v3/reference/error-codes.md` holds 928 rows and 818 codes. Each
row carries a "What to do" value. `getting-started/build-it-well` says: "Key your handling to that
column rather than to a list of codes you maintain by hand." Only 39 codes (4.8 %) publish more
than 1 action.

## Decision

### D1 — Generate the catalogue; override only what the sandbox disproved

`scripts/generate-error-catalogue.py` reads the docs mirror and writes
`backend/src/abdm/error_catalogue.py`: `ERROR_ACTIONS`, a map of code to action. A code with more
than 1 published action resolves by a fixed precedence that prefers the action which does not
retry. Regenerate the file when the mirror is refreshed.

`abdm/errors.py` holds the overrides. An override needs observed sandbox evidence and a line in
`docs/findings.md`. There are 2 today:

| Code | Docs say | Sandbox says | Override |
|---|---|---|---|
| `ABDM-1092` | New request id | A fresh REQUEST-ID is refused too (F6) | Wait for the window to end |
| `ABDM-1027` | Blocked, no retry | Scoped to the ABHA address, not to the client | Blocked for 24 hours |

### D2 — One failure shape

`errors.classify()` turns any failure into a `Failure`: the ABDM code, the action, a retry kind
(`now`, `after` or `never`), the seconds to wait, 1 sentence that says what happened, 1 sentence
that says what to do, and a support reference. The same shape covers a gateway refusal, a 5xx, a
timeout, a network error, an error block on a callback, and an answer that never came.

`classify()` is pure and lives in a module with no Django import, so `backend/tests` can import it.

### D3 — Never send a request inside the refusal window

`AbdmLinkToken` keeps the request that opened the window. `ensure_link_token()` refuses to send
again until `rules.TOKEN_REQUEST_WINDOW` (7 minutes, which is the observed 374 s plus margin) has
passed. Inside the window the plug returns the row as it stands:

- The answer has not come: the desk sees "waiting", with the time it can try again.
- The answer came and carried an error: the desk sees that error, with the same time.

The plug regenerates a link token only when the link call reports the token is wrong
(`ABDM-1026`, `ABDM-1038`, `ABDM-1063`) or when the token has expired. The token is valid 6 months
(`concepts/linking`, confirmed by the JWT `exp` in finding F2).

### D4 — Accept a late callback, and record how late

`verify_callback_signature()` verifies the signature against the gateway JWKS as before. It then
accepts a token whose `exp` has passed by up to `ABDM_CALLBACK_SIGNATURE_LEEWAY_SECONDS`
(default 3600). The signature still proves that the gateway minted the token, which is the only
thing this check can prove: finding E2 records that the token is a client-credentials JWT and that
nothing binds it to the body. The row keeps the evidence in `signature_error`, for example
`Accepted 323 s after exp`. Everything else still fails closed.

Rejected: keep the strict check. The cost is a lost clinical result and a spinner that never ends.
Rejected: drop `exp` entirely. A bounded leeway keeps a stale token from working for a day.

### D5 — Retry what is safe to retry, in the task, not at the desk

`outbound.send()` records a network error and returns the row. It no longer raises. Every caller
reads 1 shape.

`tasks.sync_encounter` retries only when `classify()` returns the retry kind `now`, with the
Celery backoff that is already configured. It does not retry a refusal. A retry of a refusal is
what produced the `ABDM-1027` block.

`build-it-well` lists the calls that must never repeat. The plug repeats none of them: the link
token, the link, and the notify are all safe, and every OTP call is user-driven.

### D6 — An answer that never comes is a failure, computed when it is read

Care gives a plug no Celery beat hook (`config/celery_app.py`), so there is no periodic sweep. A
request with no answer after `rules.CALLBACK_DEADLINE` (10 minutes; the observed latency is 1.9 s,
finding E12, and the observed retry is 16 minutes) is reported as "ABDM did not answer" when the
state is read. No spinner can outlive the deadline.

### D7 — The desk reads sentences; the admin page reads codes

The state endpoint carries a `failure` block with the 2 sentences, the retry kind, the time the
desk can try again, and the support reference. The desk dialog renders that block. It still shows
no code, no REQUEST-ID and no `activity` log, per ADR-011.

`/admin/abdm` gains the last failure per facility, so ops sees an `ABDM-1092` or a `303001`
without a database session.

## Consequences

- No migration. Every input already exists on the rows.
- `rules.LINK_TOKEN_FRESHNESS` and `rules.link_token_is_fresh()` are deleted. Finding F1 is closed
  by evidence, not by a workaround.
- A refusal inside the window costs no call at all, so the plug cannot walk itself into
  `ABDM-1027` again.
- The catalogue is 818 codes wide, so a code the plug has never met still produces an action.
- The empty HTTP 400 on `m2-hip-link-care-context` (finding E11) is unchanged by this ADR. It has
  no code, so it classifies as "ask support" and shows the REQUEST-ID. That failure is still open.
