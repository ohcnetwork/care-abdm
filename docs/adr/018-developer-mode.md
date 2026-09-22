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

## Amendment 2026-09-22 — the console skin (Rithvik: "something that looks more like developers thing")

A developer surface looks like a terminal; a clinical surface never does. The reference is the
terminal block of the ABDM docs site (screenshot 2026-09-22: a deep navy block, `$` and the command,
a grey `→` annotation line, an outline "Copy command" button). The site was unreachable from this
machine at that moment, so the palette values are chosen by eye, not read from its CSS.

Decisions:

1. **Tokens, not components.** `style/index.css` gains 1 block, `.dark.abdm-console`, with the same
   token names careui uses and a navy palette. The wrapper (`Console` in `dev/console.tsx`, and
   `SheetContent` for a portalled sheet) carries `dark abdm-console`: `.dark` makes every `dark:`
   utility fire and sets `color-scheme: dark`; `.abdm-console` swaps the palette. Every Card, Badge,
   Button, Sheet, Input and Table keeps working; nothing is re-implemented. Surfaces are plain
   `oklch` (no colour-blind remap touches navy); every semantic colour stays on the Tailwind palette
   variables, so the `[data-theme]` remaps still apply inside. The accent is cyan, not careui's
   emerald: emerald is the "answered" state inside the console, and an accent must not read as a
   state. Radii are tighter (`--radius: 0.375rem`).
2. **Dark in both host themes.** A code block is dark in a light document too. (The host mounts no
   theme provider today; see `02-care-host-contract.md`.)
3. **Geist Mono, from careui.** The plug restores careui's `@import "@fontsource-variable/geist-mono"`
   and its `--font-mono`; the host loads no monospace face, so `font-mono` fell back to the system
   stack. The `@font-face` registers a family the host does not have, so it collides with nothing.
   Vite writes asset URLs inside CSS relative to the stylesheet (`experimental.renderBuiltUrl`,
   `hostType === "css"`), because the federation runtime appends the stylesheet as a `<link>` from
   the remote origin and an absolute `/assets/…` path would resolve against the host and 404 (the
   modulepreload case, J8). The woff2 is 1 more asset the remote must serve with
   `Access-Control-Allow-Origin: *` (fonts are CORS-restricted).
4. **Terminal furniture in 1 file.** `dev/console.tsx`: `Console`, `Label` (small caps caption),
   `Prompt` (`$`), `Dot` and `Status` (a state as a dot and a word; pulses while
   something is still expected, hollow when nothing arrived), `Kbd`, `CopyButton` (the label never
   changes, only the icon: no layout shift), `Command` (the docs' block: `$`, the command, `→` note,
   "Copy command"), `NextStep` (a backend sentence with commands in backticks → 1 `Command` per
   span), `Pairs` (`name: value` rows, the shape of an HTTP header block). The non-component parts
   (`CONSOLE_CLASS`, the tones, `useCopy`) live in `dev-state.ts`.
5. **Keys.** In the explorer, when no field has the focus and no sheet is open: `1`–`4` switch the
   tab, `/` focuses the operation filter. A modifier click on a tab is left to the browser.
6. **What each surface became.** The page is 1 console panel: a status line (`● abdm / developer`,
   gateway host, X-CM-ID, the redaction caption), a `→` intro line, the 4 tabs with key caps.
   Exchanges are log lines (time and day, module and kind, operation and `METHOD path`, the state
   as a dot and a word, HTTP status coloured by class, callbacks, REQUEST-ID). The sheet
   (superseded the same day by amendment 2 below: the inspector views) shows the headers as
   `name: <1448 chars>` rows, a request line `→ POST url` and a callback line `← POST path`. The JSON tree has
   an editor's 4 value hues (`--console-key/string/number/keyword`), a guide line per depth, a
   dashed lock chip for a redaction marker. The timeline is a rail (`●──340 ms──●──1.2 s──●`, a
   dashed line to a stop not reached). Tables are a file tree (`m2/` then `abdm_outbound_requests
   1204`). Readiness rows carry `[ ok ]`, `[ !! ]`, `[FAIL]` marks, and a next step with a command
   renders as a command block with its copy button. The off page and the admin card show
   `$ ABDM_DEVELOPER_MODE=true` with "Copy command". The footer on a clinical page is a thin console
   strip (`● abdm / developer … Open in the explorer`): a dark strip says "developer mode is on
   here" at a glance.

## Amendment 2026-09-22 (2) — the exchange sheet as a network inspector (Rithvik: "like browser's inspector tab")

The exchange sheet stacked everything on 1 scroll (timeline, request, answer, callbacks, rows). It
is now laid out like a browser's Network panel, 5 views under a tab strip (`TabStrip` in
`console.tsx`), the chosen view in the URL as `?view=` so a link can point at the response of an
exchange, and 1–5 switch the view while the sheet is open (the page's 1–4 stand down then):

| View | Content |
|---|---|
| General | the ADR-012 failure notice when refused; `Request URL` (copy), method, status code with its RFC 9110 reason phrase and ms, operation (module, kind), REQUEST-ID (copy), state, reason; **Timing** — sent, HTTP answer (+ms), first callback (+s, count) or the honest words for the wait, and the rail; **Scope** — facility, patient (link), encounter; **Request headers** and **Answer headers** as `name: <N chars>` rows |
| Request | `→ METHOD url`, the query string parameters as rows when the URL has any, the body tree |
| Response | `← 202 Accepted · 340 ms`; for a `call`, the reminder that the HTTP answer is the gateway's acceptance and the answer arrives as a callback; the body tree |
| Callbacks (n) | the inbound this exchange answers first, then every callback. Each `CallbackBlock` keeps its header line (`← POST path`, time, +s) and its status line (signature, handler, X-HIP-ID, "answers …"), and gets its own small strip: Headers (n), Body, Traceback (only when the handler raised; red dot on the tab), Rows (n). The block opens on Traceback when the handler raised, on Body otherwise. The Callbacks tab carries a red dot when any callback has a traceback |
| Rows (n) | the plug rows that name this exchange |

The sheet header always shows the summary line (state, status and reason phrase, ms, `METHOD path`)
in a reserved height, so the tab strip does not move when the detail lands. The view survives a move
to another exchange, as an inspector's tab does; closing the sheet clears `?view=`.

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
