# ADR-018 — Developer mode: an audit explorer for integrators

Status: Accepted (Rithvik, 2026-09-21: "this plug is a reference integration for other integrators …
amazing UI/UX experience to explore audit tables for developers/integrators. this feature should be
enabled only with a flag")
Date: 2026-09-21
Depends on: ADR-011 (1 table per ABDM object; `AbdmOutboundRequest` and `AbdmCallback` as the audit),
ADR-012 (1 failure shape), ADR-017 (long flows in a side sheet).

## Context

The plug records every exchange with ABDM (`AbdmOutboundRequest`, `AbdmCallback`) and 15 domain
tables, but a developer read them only through `manage.py shell` and 2 superuser JSON routes. An
integrator who uses this plug as the reference could not see what was sent, what came back, when the
callback landed, or why a handler failed.

The docs' `abdm-m2/references/design.md` (new on 2026-09-21) names the surface, in "What the
integrator needs on screen, separately from the patient":

| Rule | Source words |
|---|---|
| 1 exchange = call + wait + callback, keyed by REQUEST-ID | "an outbound call, its wait, and the callback answering it read as one exchange with a timeline" |
| 5 outcomes held apart | sent; accepted, waiting; answered; refused before waiting; no answer in the window |
| Redaction | "Redact by name and length, never by value. Show that an `Authorization` header was sent and how long it was. Never its contents. The panel is a browser." |
| Readiness | "A readiness check that names what is missing"; a missing facility id is a blocker, a missing callback URL a warning: "send anyway" |
| Inbound | "Inbound is a surface, and silence there is a failure state … give the interface a state for ABDM asked and this desk has not replied" |

3 gaps in the stored evidence blocked the screen: the M1 ABHA-service calls left no audit row
(`abha/client.py` used `requests` directly); a failed callback handler kept a log line and
`processed_status=failed` only; an outbound row held no request header names.

## Decisions (Rithvik, 2026-09-21)

1. **Switch: the env var `ABDM_DEVELOPER_MODE=true`**, instance-wide, read as
   `plugin_settings.DEVELOPER_MODE`. No environment marker in the name; a production deployment
   leaves it unset. Care's `UserFlag` system was offered and declined.
2. **Gate: any authenticated Care user when the var is on.** Off: every `dev/*` route answers HTTP 403
   with the sentence that names the var; `GET dev/status` answers `{enabled: false}` to every user,
   so a screen can learn whether the explorer exists.
3. **M1 joins the audit table.** `abha/client._call` records 1 `AbdmOutboundRequest` per call through
   `outbound.record()`, with the body and the answer through `dev.redact.redact()` **before the save**:
   the row never holds an X-token or a ciphertext. The service still receives the raw body. The
   gateway session call and the JWKS read are recorded the same way (`clientSecret`, `accessToken`
   redacted).
4. **JSON explorer written in the plug**: Care UI tokens, monospace, light and dark, redaction badges,
   search, copy path and value, raw toggle. No dependency.
5. **Core first.** Replay a callback, copy as curl, a docs link per operation and a request preview
   before send are a 2nd pass.

## Design

### Backend `abdm/dev/`

| Module | Job |
|---|---|
| `redact.py` (pure) | `redact(value)`: a value under a secret key (token, accessToken, refreshToken, linkToken, hprToken, X-token, T-token, R-token, x-hprid-auth, authorization, cookie, clientId, clientSecret, password, otp, otp_hash, privateKey, photo, kycPhoto, profilePhoto, …) → `<redacted, N chars>`; a ciphertext under an encrypted-field key (loginId, otpValue, mobile, mobileNumber, …; base64 of 200+ chars) → `<encrypted, N chars>`; a base64 blob of 512+ chars under any key → `<N chars, base64>`. `header_names(headers)` → `{name: length}`. `redact_fields(row, secret_fields)` for a table row |
| `exchange.py` (pure) | `EXPECTS_CALLBACK` (8 operation ids), `ACKS` (9), `PUSHES` (1); `kind_of()` → call, ack, push, sync; `state_of()` → the 5 states; `reason_of()`, `http_ms()`, `callback_seconds()`, `path_of()`, `summarize_error()` (the 3 envelopes) |
| `table_specs.py` (pure) | 17 specs: list columns, secret columns, heavy columns (`AbdmFetchedRecord.bundle`, `AbdmCallback.raw_body`), the request and callback foreign keys, filters |
| `tables.py` | Binds the specs to the models; `serialize_row` (a foreign key as a small reference: a plug row by table and id, a Care row by kind and id), `list_rows` (newest first, `before` cursor), `rows_naming_request`, `rows_naming_callback` |
| `readiness.py` | 8 checks: env, gateway session (cached token and its TTL, never the token), bridge URL (live read; mismatch = warning), facilities (linked, with a HIP service; else blocker), gateway JWKS, NHPR certificate, **Celery worker heartbeat** (blocker after 15 min of silence), traffic (queued callbacks, last callback). Each `{id, status, what, nextStep, …}` |
| `views.py` | `dev/status`; `dev/exchanges` (filters `module`, `operation`, `state`, `status`, `facility`, `patient`, `encounter`, `request_id`, `since`, `until`; `before` cursor; the state filter is derived after the read); `dev/exchanges/<request_id>` (request with header names + lengths, response, every callback with its traceback, the inbound it answers, the rows that name it, the ADR-012 failure block); `dev/inbound` (callbacks the gateway started, each with our ack joined through `request_json.body.response.requestId`); `dev/callbacks/<id>`; `dev/tables`, `dev/tables/<name>`, `dev/tables/<name>/<id>`; `dev/readiness` |

Storage, migration `0005_developer_mode`: `AbdmOutboundRequest.request_headers` (names → lengths,
written by `outbound.send()` and `outbound.record()`); `AbdmCallback.processing_error` (the traceback,
last 20 KB, written by `tasks.dispatch_callback`) and `processed_at`. The periodic tasks and every
dispatched callback set `cache["abdm:worker:last_seen"]`.

### Frontend `components/abdm/dev/`

`developer-page.tsx` at `/abdm/developer` (an app route, not `/admin`: the gate is any user, and a
move between the 2 layouts crashes the host, J7). 4 URL-addressed tabs: Exchanges (1 row per
exchange, filters in the URL, 5 s poll, new rows wait behind a "N new exchanges" button so the list
does not move under a reader), Inbound (each gateway-started callback with its ack, or "No
acknowledgement was sent"), Tables (17 tables by module with counts; rows newest first; "Load more"
appends), Readiness. A chosen exchange or row opens in a side sheet over the tab (`exchange-sheet.tsx`,
`RowSheet`): timeline (sent → HTTP → callback, elapsed figures, the state as the last word), request,
answer, every callback with signature, headers by length, body tree, traceback block. `json-tree.tsx`
is the explorer. `dev-footer.tsx` is the contextual entry: a collapsed "Developer" disclosure appended
last on the encounter ABDM tab, the patient ABHA panel, the facility setup page and the HPR section,
rendered only when `dev/status` says on. The admin dashboard gains a "Developer explorer" card.

## Consequences

- 3 new columns, 9 routes, 0 writes. Every answer passes `redact()`; header values never leave the
  server; a token string cannot appear in any explorer answer (the smoke counts them: 0).
- Every call the plug makes is in 1 table now, M1 and the gateway session included. `outbound.record()`
  is the 1 way another transport joins it, and it redacts at write.
- A handler that raises leaves its traceback on the callback row, beside the body it failed on.
- The worker heartbeat turns "nothing happens" into a named blocker with the start command.
- The flag is instance-wide: on, every logged-in user sees every exchange, patient identifiers
  included. A production deployment leaves it unset; the off page explains the var.
- 2nd pass: replay a stored callback through current code (superuser, dry run first), copy as curl
  (redacted `Authorization`), a docs page per operation (an id → page map generated from the mirror),
  a request preview before a call is sent.
