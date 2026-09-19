# 03 — Roadmap

Status legend: [ ] not started · [~] in progress · [x] done (with evidence link)

Order (Rithvik, 2026-09-09): M1 → M2 → M3 → M4. Since 2026-09-15 the docs say the NHPR portal route is sanctioned and "a product that registers its facilities there by hand never builds M4" (`milestones/m4`). The ADR-007 facility setup is therefore the route, not a workaround; Phase 5 shrinks to the API extras. Every phase ends on
an **observed sandbox result**, per the docs' own scaffold loops
(`.agent/skills/abdm-m*/references/scaffold.md`).

## Phase 0 — Knowledge base and environment  [x]
- [x] Mirror docs (`docs/abdm-docs-mirror/`), download the nine skills (`.agent/skills/`).
- [x] Register the docs MCP server in the Hermes profile (`hermes config set mcp_servers.abdm-docs.url …`). Needs a Hermes restart to expose tools.
- [x] Read CARE host contract, write `02-care-host-contract.md`.
- [x] Sandbox `clientId`/`clientSecret` received → `.env.local` (ignored; verified `git check-ignore`).
- [x] Dev callback exposure: cloudflared named tunnel `care-abdm-sbx` → https://care-abdm-sbx.rithviknishad.dev → localhost:8000 (ADR-005). Bridge URL registered 2026-09-09 via `abdm.gateway.bridge.update_bridge_url()` → HTTP 202.
- [x] ADR-004 data model drafted (identifiers + extensions first; Facility has no extension surface — flagged).
- [x] Skeleton repos: `backend/` from `care_token_display`, `frontend/` from `care_token_display_fe`. Evidence 2026-09-10: code exists. `npm run build` produced `dist/assets/remoteEntry.js`. `manage.py check` passed with the plug. Roadmap records `remoteEntry.js` served with CORS `*` on :4174.
- [x] 2026-09-15 Docs mirror rebuilt from the sitemap by `scripts/refresh-docs-mirror.py`: 382 pages (was 55), 9 skills at the 2026-09-14 build, `MANIFEST.json`. Observed: `pages in sitemap: 382`, `pages_failed: []`, `skill_files_failed: []`. 42 of the 55 old pages had changed; the code-relevant changes are in `findings.md` rows A8, B6, B17, C11, C12, E1, F3.
- [x] 2026-09-14 Bruno collection (`bruno/`) — 47 files that cover every route in `backend/src/abdm/urls.py`: Care login and refresh, 2 probes, 5 facility routes, 6 enrol steps, 3 login steps, the transaction read-back, 3 patient routes, the 2 callback probes, and all 13 callback receiver paths. Bodies come from the docs mirror; the 3 bodies that the docs do not publish are marked as placeholders (see `docs/findings.md`, 2026-09-10). Observed: `@usebruno/lang` parsed 47/47 files with 0 failures; `bru run probes --env local` gave `health 200` with the assertion passed and `gateway-status 403` without a token; `bru run callbacks/link-on-carecontext.bru --env-var careUrl=http://localhost:8099` reached a local echo server on path `/api/abdm/v3/link/on_carecontext` with a fresh `REQUEST-ID` UUID and a UTC `TIMESTAMP` with milliseconds. Not yet run against the sandbox with real credentials (user-driven).
- [x] 2026-09-15 Bruno collection updated to the ADR-011 routes: 58 files parse (`@usebruno/lang`), 46 requests; the route diff against `backend/src/abdm/urls.py` is empty both ways. The 7 files that carried a pasted `Authorization: ******` were fixed; the 2 Care JWTs that sat in `environments/local.bru` were removed and the variables are now secret.

## Phase 1 — Gateway session (prerequisite to everything)  [~]
Docs: `/docs/hiecm/v3/api/gateway`, `/concepts/gateway`, `/getting-started/first-fifteen-minutes`.
- Backend: `abdm/gateway/session.py` — `POST sessions` with clientId/secret, cache token until expiry, refresh. Header set (`X-CM-ID`, `REQUEST-ID`, `TIMESTAMP`, `Authorization`) exactly as `get_operation gateway-sessions-create` says.
- Backend: fetch RSA public certificate (M1 encryption) and gateway JWKS (`gateway-get-gateway-certs`) for callback signature verification (`/concepts/callback-authenticity`).
- [x] 2026-09-09 verified by curl from the workdir: `POST https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions` → HTTP 200, `{accessToken, expiresIn: 1200, refreshExpiresIn: 1800, refreshToken, tokenType: "bearer"}` — shape identical to the docs example. Token lifetime is 20 min; refresh path via `m1-token-refresh` still to confirm.
- [x] 2026-09-09 from inside Care: `abdm.gateway.session.get_access_token()` → token, Redis TTL 1140s (=1200−60 margin), second call served from cache. Exposed as `GET /api/abdm/gateway/status` (auth required, token never returned).
- [x] 2026-09-14 Gateway token refresh: not built, by design. `m1-token-refresh` is the ABHA user X-token refresh (`GET /v3/profile/account/request/token`, `R-token` header), already done in Phase 2. The docs publish no refresh endpoint for the gateway session token. The plug creates a new session on expiry (Redis TTL 1140 s); the docs allow this. Recorded in `findings.md` (2026-09-14, M1 gap review).

## Phase 2 — M1 Create: ABHA identity  [~]
Docs: `/milestones/m1`, `/api/m1`, `/api/m1/apis`, skill `abdm-m1`.
Mandatory set (from `/concepts/hip-hiu` capability table, private integrator):
1. ABHA creation by Aadhaar OTP (request otp → verify → address suggestions → claim address → enrol byAadhaar).
2. Login by mobile / Aadhaar / ABHA number / ABHA address (request → verify → select account).
3. Fetch profile, download ABHA card.
4. Communication mobile number (post-enrol).
5. Local Luhn (ABHA number) and Verhoeff (Aadhaar) validators.
Also mandatory (MCP `x-abdm-requirement.level: mandatory`, case `SHARE_PATIENT_PROFILE_701`):
6. Scan and Share: receive `patient-share/v3/share`, answer `m1-on-share-acknowledgement` with a token number.
7. Consent record before enrolment (`CRT_ABHA_102`).
Optional for a private integrator (`milestones/m1`, rewritten after NHA's review of 11 September 2026): face authentication, fingerprint/iris, mobile/email update, find a forgotten ABHA. **None of these is built.** An earlier roadmap line said they were built on 2026-09-14; that was wrong and is corrected here (2026-09-15). Not for private integrators: demographic authentication, child ABHA. Not recommended by NHA: enrol by document. Decision (Rithvik, 2026-09-15): M2 first; optional M1 features later.

- Backend: `/api/abdm/abha/...` thin endpoints wrapping the ABHA service, doing RSA encryption server-side, holding the `X-token` server-side per transaction. Persist `AbhaNumber`-ish record linked to `Patient` (ADR-004).
- Frontend: `PatientRegistrationForm` slot — create/verify ABHA, then set fields on the host form; `PatientDetailsTabDemographyGeneralInfo` — show ABHA, card, status; `PatientSearchActions` — find by ABHA.
- Done when: sandbox test-data ABHA created/logged in from the CARE UI end to end; matrix in `.agent/skills/abdm-m1/references/test.md` mapped to observed results.
- [x] 2026-09-09 Journey 1+2 (Aadhaar enrol, mobile OTP, address claim) — backend + `AbhaWizard`; all six paths reach ABDM validation (real Aadhaar run pending, user-driven).
- [x] 2026-09-09 Journey 5 (login by mobile OTP → accounts → select) — backend `service.login_*`, wizard "Link existing ABHA" mode. Not yet run against sandbox with a real mobile.
- [x] 2026-09-09 Journey 7 (card) — proxied via stored X-token, `GET /api/abdm/patients/<id>/abha/card`; 409 when no valid token. Content-type undocumented; passthrough. The QR code (`/v3/profile/account/qrCode`) was built, then removed on 2026-09-10: the QR is a patient-held credential, so a staff panel is the wrong place for it. The staff-side use is a scan in `PatientSearchActions`, not a preview.
- [x] 2026-09-09 Linkage to Patient: `extensions.abdm.txn_id` → `post_save` → auto-maintained identifiers + `instance_identifiers` rebuild (ADR-004 amendment). Verified via in-process `POST /api/v1/patient/` and `PUT` (identifiers survive edit). Existing-patient link endpoint verified likewise.
- [x] 2026-09-09 UI: `AbhaPanel` on Demography tab (link / card / copy), status chip in `PatientHomeActions`. Not visually verified by the agent.
- [x] 2026-09-10 `PatientSearchActions` — "Find by ABHA" on the patient search page (`patient-search-actions.tsx`). Runs the link wizard (default tab ABHA number), then the backend reports `existingPatient` (lookup via `AbhaNumberIdentifier.find_patient` / address) → "Open patient" or "Register with ABHA" (`/patient/create?abdm_txn=<txnId>` → `patient-registration-form.tsx` reads `GET abha/transactions/<txnId>` and prefills name/DOB/gender/mobile/address/pincode). Core `?identifier=` search deliberately not used: ABHA is verified by ABDM before Care trusts it. Observed: tsc/eslint/build clean, `remoteEntry.js` 200 with CORS `*` on :4174; UI not visually verified by the agent.
- [x] 2026-09-10 Login by ABHA number / ABHA address / Aadhaar — one endpoint `POST abha/login/request-otp {hint, login_id, otp_system}` + `verify` (`abdm/abha/service.py::login_*`, `client.login_request_otp/login_verify_otp`; address goes via `/v3/phr/web/login/abha/*`). Non-mobile verify returns an X-token directly → `_finalize_login` also does `GET /v3/profile/account` for the full profile. Observed: in-process `APIClient` smoke (`/tmp/abdm_login_smoke.py`, ABDM client mocked) — validation 400s, txn kinds, `existingPatient` lookup. **Not yet run against sandbox with real OTPs (user-driven).**
- [x] 2026-09-10 X-token refresh — `AbhaTransaction.refresh_token_expires_at` (migration 0002), `service.ensure_x_token()` refreshes via `GET /v3/profile/account/request/token` (`R-token` header) when the X-token is expired and the R-token is not; the card uses it. Observed in-process: expired X + valid R → refreshed + rotated; both expired → `NoUserSession` (409). The `R-token` prefix was a docs conflict (findings C8). The live page (2026-09-15) sends it bare; the plug now sends bare first and retries with the prefix on 401.
- [x] 2026-09-11 Aadhaar login always uses the Aadhaar-linked mobile — the "Send the OTP to" selector stays only for the ABHA number and the ABHA address (`abha-wizard.tsx::canChooseOtpSystem`); `LoginOtpRequest` sets `otp_system="aadhaar"` for the `aadhaar` hint, because UIDAI sends that OTP. Observed: `manage.py shell` — `aadhaar`+`abdm` → `aadhaar`, `aadhaar` with no value → `aadhaar`, `abha-number` keeps both values; `npm run build` and `npx eslint src` clean (0 errors); 8 backend tests OK.

- [x] 2026-09-14 Consent record (`CRT_ABHA_102`) — the wizard has a consent checkbox (`abha-wizard.tsx`, id `abdm-consent`); "Send OTP" stays disabled until it is ticked. `POST abha/enrol/aadhaar/request-otp` needs `consent: true` (400 otherwise). `AbhaTransaction` stores `consent_recorded_at`, `consent_code`, `consent_version` (migration 0004); `GET abha/transactions/<txnId>` returns `consentRecordedAt`. Observed: `manage.py check` clean; `makemigrations --check` clean; 14 backend tests OK; `npm run build` + `eslint` 0 errors.
- [x] 2026-09-14 Scan and Share (`SHARE_PATIENT_PROFILE_701`) — callback route `patient-share/v3/share` → `AbdmCallback` (operation `m1-receive-patient-share`) → `tasks.dispatch_callback` → `share/service.py::handle_profile_share`: facility by `metaData.hipId` (fallback `facility_id`), counter check, patient match by ABHA identifiers, token `<context>-<nnn>` per counter per day, `AbhaTransaction` kind `profile_share` for the registration prefill, then `outbound.send("m1-on-share-acknowledgement", "/api/hiecm/patient-share/v3/on-share")` with SUCCESS or FAILURE. Model `AbdmProfileShare` (migration 0005 then; migrations restarted at 0001 on 2026-09-15). Facility config gains `counters`. Desk API `GET/POST facilities/<id>/abdm/profile-shares[...]`. UI: setup page card "Scan and Share counters" with one QR code per counter (`qrcode.react`, URL from `ABDM_SHARE_QR_URL_TEMPLATE`); patient search "Shared profiles" inbox (`profile-share-inbox.tsx`, polls 10 s) → open patient / register prefilled. Bruno `scan-share/`. Observed in-process (`share_smoke.py`, signature + gateway mocked): 5 shares → 202 each; tokens `OPD1-001`, `OPD1-002`, `Pharmacy-001`; unknown counter → FAILURE `HIP_UNKNOWN_COUNTER`; wrong intent → FAILURE `HIP_UNSUPPORTED_INTENT`; inbox hides `kycPhoto`, detail `?photo=1` returns it; prefill txn returns name/pincode; dismiss removes the row; callback `processed_status=handled`; bad counter `OPD 1` → 400. Frontend build + eslint clean.
  - [ ] sandbox: QR URL format. The docs do not publish it (findings). USER scans a known sandbox facility QR with a plain QR reader, reports the URL, and sets `ABDM_SHARE_QR_URL_TEMPLATE` (placeholders `{hip_id}`, `{context}`).
  - [ ] sandbox: real share from the PHR app → callback signature accepted, token shown in the app within 30 s, row in the inbox. Needs Celery worker running and the tunnel up.
  - [ ] sandbox: `on-share` host. The M1 page says `https://dev.abdm.gov.in/api/hiecm`; the callback page curl shows `abhasbx`. The plug uses the gateway host. Confirm by the `AbdmOutboundRequest` row.

- [x] 2026-09-17 A login with no ABHA offers the create journey — the desk sees `ABDM-1114` ("No ABHA user registered with this Aadhaar number.") or an empty account list, and the error now carries one action, "Create a new ABHA" (`abha-wizard.tsx::createFromLink`, `AlertAction` slot, so the dialog layout does not shift). The action drops the failed login transaction, moves to the create journey and carries what the desk typed: the Aadhaar for the `aadhaar` identifier, the mobile for the `mobile` identifier. The back arrow returns to the link step. The action shows for all 4 identifiers. Observed: `npm run build` → `dist/assets/remoteEntry.js`, built in 1.03 s; `npx eslint src` 0 errors (10 pre-existing warnings); locale check 217 keys, 158 used, 0 missing.
  - [ ] USER: on the sandbox, run a link by Aadhaar for an Aadhaar with no ABHA, press "Create a new ABHA", and confirm the Aadhaar is already filled and the create journey completes. Screenshot.

Pending sandbox observations (user-driven):
- [x] 2026-09-19 A refused ABHA link answers HTTP 400, never HTTP 500. The desk used to read
      "Something went wrong": `LinkError` was a plain exception, and the `post_save(Patient)`
      receiver raises it inside Care's own patient viewset. `LinkError` is now a DRF
      `ValidationError` that carries `{"errors": "<sentence>"}`, which Care passes through
      (`02-care-host-contract.md`, "Errors from a plug signal") and care_fe shows in a toast. The
      3 sentences say what failed and what to do, and name no other patient record. The rule
      itself stands: 1 ABHA number is 1 person (`/concepts/phr`), and `find_patient` answers with
      1 row, so a second patient record would break discovery and consent for both. The
      registration form now reads `existingPatient` from the transaction, keeps the ABHA prefill,
      sends no `txn_id`, and shows an amber card with the other patient's name and an "Open
      patient" button — so "Register as new" saves the patient without the ABHA instead of
      failing at save. The link wizard shows a refusal on its own done step (`finishError`).
      **Observed: `abha_link_conflict_smoke.py` → `LINK CONFLICT SMOKE OK — 14 checks passed, 0
      failed`, `cleanup done, rows left: 0`; the 400 body is `{"errors": "This ABHA is already
      linked to a different patient record. Open that patient record, or use a different ABHA."}`
      and patient B was rolled back; 90 backend tests OK; ruff clean; `npm run build` →
      `dist/assets/remoteEntry.js`, built in 1.01 s; `npx eslint src` 0 errors (10 pre-existing
      warnings).**
  - [ ] USER: on the sandbox, link an ABHA that another patient already holds, and confirm the
        message in the dialog. Then press "Register as new" from "Find by ABHA" and confirm the
        patient saves without the ABHA. Screenshot.

- [x] 2026-09-19 The ABHA dialog closes when the journey ends. The wizard never closes itself,
      so each caller must do it; 4 paths did not. The patient panel now closes the dialog when
      the link call succeeds (a refusal keeps it open and shows the reason). The registration
      form closes it as soon as the ABHA is applied, so the desk sees the card on the form.
      "Find by ABHA" and the Scan and Share inbox close before they open another page, so no
      dialog stays over the new page. The done step of "Find by ABHA" still waits, because it
      asks the desk to choose between "Open patient" and "Register as new".
      **Observed: `npm run build` → `dist/assets/remoteEntry.js`, built in 1.01 s; `tsc -b` exit
      0; `npx eslint src` 0 errors (10 pre-existing warnings).**
  - [ ] USER: on the sandbox, link an ABHA to a patient from the Demography tab and confirm the
        dialog closes and the panel shows the ABHA. Screenshot.

- [x] Real Aadhaar enrol run.
- [x] Login by ABHA number, ABHA address, and Aadhaar with real OTPs.
- [ ] X-token refresh, including the `R-token` prefix conflict (findings #6).
- [ ] Card response bytes and content-type (findings gap #4).

## Phase 3 — M2 Attach: linking and sharing (the bulk)  [~]
Design: ADR-011 (lean M2), which keeps ADR-008 decisions 1–8. Facility setup: ADR-007 (now the sanctioned route).
Docs: `/milestones/m2`, `/api/m2`, `/concepts/linking`, `/concepts/data-flow`, `/concepts/encryption`, `/concepts/fhir`, skills `abdm-m2`, `abdm-fhir`. Fact sheet from the 2026-09-15 mirror read: `findings.md` sections E–I.

### Code-complete 2026-09-15 (ADR-011 rebuild)
- [x] Backend: `AbdmBridge`, `abdm/instance/`, the admin routes and `gateway/hrp.py` removed; `gateway/bridge.py` reads the bridge live and caches the id. New `abdm/hip/` (`rules`, `crypto`, `contexts`, `discovery`, `consent`, `transfer`, `views`) and `abdm/fhir/` (`bundle`, `op_consult`, `prescription`, `health_document`). 5 new tables. Migrations restart at `0001_initial`.
- [x] Frontend: instance dashboard `/admin/abdm` (gateway, bridge, services, HIP facilities, recent callbacks; all live) with an admin nav item; setup page has 2 cards (facility identity + HRP with a bridge status line, Scan and Share); new slots `EncounterActions` ("Link to ABHA" dialog with gateway activity) and `EncounterOverviewTop` (status row). `careApi.ts` mirrors `urls.py`.
- [x] Observed 2026-09-15: `manage.py check` — no issues; `makemigrations abdm --check --dry-run` — no changes; ruff — all checks passed; `python -m unittest` — 41 tests OK (checksums, crypto, callback signature, facility rules, share rules, hip rules, hip crypto, fhir bundles); `npm run build` — `dist/assets/remoteEntry.js` built; `npx eslint src` — 0 errors, 9 existing fast-refresh warnings; i18n — 205 keys, no missing key, no empty value.
- [x] Observed 2026-09-15: `m2_smoke.py` (session files; real Care auth and DB, ABDM network and signature mocked) printed `M2 SMOKE OK — outbound calls: 19 callbacks: 14` with 0 failed or unhandled callbacks. It proved: facility PUT → HIP ID derived; bridge GET live; admin overview lists the HIP facility (superuser only, 403 for staff); HRP body carries the cached bridge id and goes to the HSP host; Encounter save → `generate-token` with `X-HIP-ID`; `on-generate-token` → token active ~6 months → link call with `X-Link-Token`, reference = encounter `external_id`, display without clinical detail; `on_carecontext` → linked → notify → `on-notify` acknowledged; duplicate callback deduped; discovery → `on-discover` with the care context, no match → `patient: []`; link init → OTP session, masked hint → wrong OTP error block → right OTP `on-confirm`; consent GRANTED stored and acked, revoked via the `/api/v3` path; health-information request → ACKNOWLEDGED → 2 bundles (OPConsultRecord, PrescriptionRecord) pushed encrypted → **decrypted by the HIU-side key in the test, checksum = MD5 of the plaintext** → notify TRANSFERRED; a wider date range refused with `ABDM-1063` and acked ERRORED; SMS deep link body; non-superuser 403 on bridge registration; Scan and Share token `OPD1-001`.
- [x] Observed 2026-09-15: MCP `validate_fhir` returned `findings: null` (0 findings) for the OPConsultation, Prescription and HealthDocumentRecord bundles built from fixture CARE data (`fhir_smoke.py`, session files).

### Code-complete 2026-09-18 (ADR-013 staged sharing)
- [x] Backend: `AbdmShareItem` (migration 0002; sandbox history kept as linked items); `post_save` stages prescriptions (not draft), final diagnostic reports and discharge summary uploads, plus 1 outpatient OP consultation with the first record; the desk links selected items or excludes one; a completed/discharged Encounter links every staged item; retries hourly × 3 (configurable) via Celery beat; `hi_types` derived from linked items; transfer builds only from linked items. FHIR: `DischargeSummaryRecord` added, `HealthDocumentRecord` removed, OP consult outpatient only, Prescription from prescriptions only.
- [x] Frontend: encounter tab "ABDM Records" (`encounterTabs.abdm`); the actions slot opens it.
- [x] Observed 2026-09-18: `manage.py check` clean; `makemigrations --check` clean; ruff clean; 90 unit tests OK (`test_sharing_rules.py` added); `m2_smoke.py` → `M2 SMOKE OK — outbound calls: 31 callbacks: 54` with the new stages 3 (stage, draft, cancel → excluded), 3b (select 1 → token), 4 (link carries only the queued type), 5 (item linked, `hi_types` derived, unselected item stays staged), 5a (completion → all staged linked in 1 call with linked + queued types; excluded item not sent), 5c (refusal → hourly retry → failed after 1 + 3 → desk re-select resets → linked), 5d (exclude/include; a linked item refuses). `fhir_smoke.py` + MCP `validate_fhir`: OPConsultation, Prescription, **DischargeSummary** → `findings: none`. `npm run build` OK; eslint 0 errors; i18n 250 keys, none missing or empty.
- [ ] USER: write a prescription on an outpatient encounter of an ABHA patient → the ABDM tab shows `Prescription` and `OP consultation` as Staged and no gateway call; select one → Link selected → callback → Shared; complete the encounter → the rest links by itself.
- [ ] Sandbox measurement for findings F10: does a second link with a new `hiType` add the type at ABDM? Link Prescription first, then OPConsultation for the same reference; read the `hiType` list in a PHR app discovery.
- [ ] Discharge summary: generate one from an inpatient encounter (a `Template` row is needed), check it is staged, link it, confirm the bundle in the PHR app.

### Sandbox proofs (user-driven; each ends on an observed gateway answer)
- [x] 1. Facility and bridge.
  - [x] Observed 2026-09-14: `GET bridge-services` → HTTP 200, bridge `SBXID_035123`, url `https://care-abdm-sbx.rithviknishad.dev/api/abdm`, `services: []`.
  - [x] Observed 2026-09-14: HRP register → HTTP 200 error 2500 "Provided facility name is not matched with registered name" (user screenshot). Host fixed to `ABDM_HSP_URL`.
  - [x] Observed 2026-09-15 (user): bridge URL registered; HRP register → HTTP 200, `hrp_registered_at` 16:02 IST. `GET /api/abdm/admin/overview` shows the service `{"id": "IN1410000232_1", "name": "FACILITY WITH P", "types": ["HIP", "HIU"], "active": true}` (findings B18: the real row shape differs from the docs).
  - [x] Observed 2026-09-15 (Playwright run, session files `dogfood-output/report.md`, 16 screenshots): `/admin/abdm` shows the gateway badge, bridge card (registered), 1 service `IN1410000232_1 HIP, HIU`, 1 HIP facility, "No callback received yet."; `/facility/<id>/abdm/setup` shows the 2 cards, `HIP ID IN1410000232`, `HRP service registered at 4:02:21 PM`, `Bridge registered`, the QR-template warning, save bar disabled; the encounter overview row reads `IPD records for 15 Sep 2026 · Waiting for the link token`; the dialog shows the ABDM-1092 waiting text; the patient panel shows `KYC verified`, number and address; patient search shows `Find by ABHA` and `Shared profiles`. Found and fixed the same day: "Open setup" from the admin page crashed the host (J7, now a full-page link); the dialog's Gateway activity missed the token requests (query widened); ~25 `modulepreload` 404s per page (J8, `modulePreload: false`). Not ours: `/facility/<id>` redirects home and `/admin` is Page Not Found in the host.
- [x] 2. Callback receiver. Observed 2026-09-17 07:02:47Z, the first real gateway callback: `POST /api/abdm/api/v3/hip/token/on-generate-token` (the docs omit the `/api`), 1.9 s after the 202, `Authorization: Bearer <RS256 JWT>` signed by the gateway's own RS256 key (`azp: gateway`), `X-HIP-ID`, `REQUEST-ID`, `TIMESTAMP`, `User-Agent: ReactorNetty/1.1.19`, source IP `13.203.243.253`. Row stored, signature `ok`, header name recorded (findings E2, E3, E12). The receiver had been proven reachable through Cloudflare with 7 User-Agents before that (no edge blocking).
- [x] 3. Link token. **Root cause of "no callbacks" found 2026-09-17:** every request since 2026-09-15 sent `X-HIP-ID: IN1410000232` (the HFR id, as the docs say) and the gateway accepts that with 202 but never delivers the callback. The gateway routes on the service id it issued at HRP registration, `IN1410000232_1`; with that header the callback arrived in 1.9 s and the token's own claims say `hipId: IN1410000232_1` (findings E1, B18). The plug now stores the service id read from `gateway-list-bridge-services` (after HRP registration and on every setup-page load) and a facility without one is not configured for M2. Token: RS512 JWT, `exp` = `iat` + 182.5 days (F2). The old 2026-09-15 sub-bullets are superseded by this one.
  - [x] 2026-09-17 07:10Z: the stored callback replayed through the fixed code → `AbdmLinkToken.active`, 4 `m2-hip-link-care-context` calls sent with `X-HIP-ID: IN1410000232_1` and `X-Link-Token` → **all HTTP 400 with an empty body** (findings E11). 20 controlled variants (docs example body, integer/absent ABHA number, single HI type, `Bearer` prefix, wrong HIP id, every header spelling) → the same empty 400; a missing header → empty 401 `Basic realm`, so the header names are right and the gateway's own link-token check is what fails. The token was 8 minutes old; the endpoint page says "must be called immediately before the linking call" (F1). The plug now regenerates a token older than 5 minutes and links from the callback that delivers it.
  - [x] 2026-09-17 07:27Z: fresh token request → error callback in 8.8 s: `ABDM-1027: You are blocked. Please try again after 24 hours.` (findings E14), caused by the burst of refused link calls. The plug recorded it on the token row and the 4 care contexts show the sentence on the desk. `gateway-list-bridge-services` and the session call keep working.
  - [x] 2026-09-17 11:19Z (16:49 IST): encounter `4ddc3e10-2354-4d86-9666-9d11505de359` created for patient 61 through the backend API alone (`POST /api/v1/auth/login/` then `POST /api/v1/encounter/`, class `amb`). The plug linked it without help: care context `OPD records for 17 Sep 2026`, hiType `OPConsultation`, `m2-generate-link-token` 202 at 11:19:55Z. The callback arrived 968 s later, exactly as E10 predicts. The ADR-012 leeway accepted it (signature `ok`, 447 s past the token `exp`, `processed_status=handled`), so the fix is proven against a real late callback. The body was `ABDM-1027` again, because the block follows the ABHA address (E14) and patient 61 is blocked until 2026-09-18 07:27Z.
  - [x] **2026-09-17 11:46Z to 11:56Z: check order on the link call (E11).** 9 controlled calls on `nihal_99@sbx` with the 6-month link token of row 13. (1) `patient: []` answers JSON `400 ABDM-9999: patient attribute required in the payload`, so ABDM reads our payload. (2) An invalid `hiType` answers the same empty 400 and not `ABDM-1006`, so a well formed request never reaches field validation. (3) The sibling endpoint `link/context/notify` reaches its backend with the same session token and the same `X-HIP-ID` and answers `ABDM-9999: User not found`, so our credentials and our HIP work next door. A `303001 ... SUSPENDED` answer was seen once here, but it carries little weight: rows 433 and 434 show the same state on the healthy `HIECM-LinkToken--vv3` endpoint at 13:29 IST, which worked again 3 minutes later. Every refusal comes from `server: istio-envoy` in 16-25 ms and carries `correlation-id` and `activityid`. The plug now stores the response headers of each refusal (`AbdmOutboundRequest.response_headers`, migration `0003`). Nothing on our side is left to vary. **Superseded 2026-09-18: the "ABDM fault" reading was wrong. The check order proves only that the token and the top-level shape pass; it does not cover the field that was the cause.**
  - [x] **2026-09-18: escalation is not needed. The cause was ours (E11): `hiType` must be a JSON string, not an array.** Measured with 1 variable changed at a time, same token and headers: the array answers the empty 400; the string answers **202**. Raise a docs defect instead, because the page types `hiType` as `object[]` and its example sends an array.
  - [x] **2026-09-18 09:52Z: the real link ran for encounter `4ddc3e10-2354-4d86-9666-9d11505de359`.** Link token → `m2-hip-link-care-context` **HTTP 202** → `on_carecontext` `Successfully Linked care context` → `AbdmCareContext.status=linked`. Care context 17 (2 HI types, 1 `patient` block for each, F7) also answered 202 and reached `linked`.
- [x] 4. HIP link: `on_carecontext` lands → `AbdmCareContext.status=linked`. **Observed 2026-09-18 on care contexts 20 and 17: the success `status` is `Successfully Linked care context` and the callback carries no `error` block (F4 answered).**
- [x] 5. Notify: `on-notify` acknowledgement **SUCCESS**, observed 2026-09-18 on care contexts 20 and 17. 2 defects were found and fixed on the way: `careContext.patientReference` must hold our internal patient reference, not the ABHA address (F8), and the notify must wait for ABDM to index the link (F9).
- [ ] 6. Discovery from a PHR app → `on-discover` 202 → the PHR app shows the visit. Record the real `verifiedIdentifiers` shape (findings G1).
- [ ] 7. User link: PHR app selects the visit → OTP SMS → confirm → linked. Confirm the docs-inbound init body and the confirm `token` type.
- [ ] 8. SMS deep link: sandbox SMS received; `on-notify` SUCCESS.
- [ ] 9. Consent granted in the PHR app → `AbdmConsent GRANTED`; record the real path and body (findings E3, H1).
- [ ] 10. Data transfer: PHR app requests records → push → notify TRANSFERRED → **record readable in the PHR app**. This is the docs' end-to-end loop (`/concepts/hip-hiu`).

### Error handling (ADR-012)  [x]
Every failure reaches the desk. Before this, `ABDM-1092` was shown as "Waiting for ABDM to confirm…"
and the spinner never stopped.
- [x] Generated catalogue: `python3 scripts/generate-error-catalogue.py` → 818 codes from 928 rows.
- [x] 1 pure classifier, `abdm/errors.py`. **Observed 2026-09-17: 78 backend tests, result OK**
      (`test_errors.py` added: 18 tests over the window, the block, the plug codes and the API shape).
- [x] The plug no longer causes `ABDM-1092`: the 5-minute freshness rule is gone and no link-token
      request goes out inside `TOKEN_REQUEST_WINDOW` (7 min; the measured boundary is 362–374 s, F6).
- [x] A late callback is no longer thrown away (`ABDM_CALLBACK_SIGNATURE_LEEWAY_SECONDS`, E10).
- [x] **Observed 2026-09-17 against the live database through the real state endpoint** (superuser,
      `APIClient`, no mocks). Every stuck row now carries a failure block:
      `ABDM-1092` → `wait`, `retryAt 10:07`, "ABDM refused a second request for this patient so soon
      after the last one."; a blank `pending` row → `NO_ANSWER`, `retry now`, "ABDM did not answer.";
      `HTTP_400` → `ask_support`, `retry never`, with the REQUEST-ID for support.
- [x] Desk: the `waiting` view holds the button until the time shown. Admin: the last failure per
      facility. **Observed: `npm run build` OK, `dist/assets/remoteEntry.js` written; `tsc --noEmit`
      clean; `eslint src` 0 errors.**
- [x] Closed 2026-09-18: `m2-hip-link-care-context` answers **202** and the context reaches `linked`. The empty 400 was an array `hiType` (E11). ADR-012 still gives support the reference when a call does fail.

### Known limitations after this pass
- A record is announced to ABDM only when the desk links it or the Encounter closes (ADR-013). ABDM's own "a linked context gained records" notify follows each link.
- Record types: OPConsultation (outpatient), Prescription, DischargeSummary (PDF). DiagnosticReport is staged and linked, but its structured `DiagnosticReportRecord` bundle is not built yet (a data request for it answers ERRORED for that entry). WellnessRecord, ImmunizationRecord, Invoice are deferred (findings I4).
- The consent artefact signature is stored, not verified (findings H2).
- The link-confirm OTP is fixed (`123456`) outside production, like Care core's login OTP.

## Phase 4 — M3 Retrieve (HIU)  [ ]
Consent request creation, status callbacks, fetch, decrypt, store, show in an `encounterTabs` tab. Docs: `/milestones/m3`, `/api/m3`, skill `abdm-m3`.

## Phase 5 — M4 Enrol: facility + bridge  [~]
Docs: `/milestones/m4`, `/api/m4`, `/api/m4/undocumented` (2 published endpoints; the rest "not yet published").
- [x] Facility ID and names on the Care facility (`Facility.extensions["abdm"]`, ADR-007). Bridge URL registration (`gateway-update-bridge-url`) and HRP service registration (`gateway-register-bridge-services`) exist in `gateway/bridge.py`.
- [x] 2026-09-15: the docs sanction the NHPR portal route; no M4 API build is required for M2. Remaining M4 work is optional: HFR search by facility ID to prefill the registered name (path not published, findings B15).

## Phase 6 — Hardening / publish  [ ]
- Security audit checklist from `/getting-started/security-audit`.
- README, `care-package.lock`, plug_config example, `ADDITIONAL_PLUGS` example.
- App Store enrolment only on explicit approval (skill `care-apps-registry-enrolment`).

## Cross-cutting decisions
- ADR-001 Scope: Proposed. See `adr/001-scope-hip-first.md`.
- ADR-002 Secrets and encryption boundary: Accepted. See `adr/002-secrets-and-encryption-boundary.md`.
- ADR-003 Host slots: Accepted for M1 slots. Proposed for M2/M3/M4 slots. See `adr/003-host-slots.md`.
- ADR-004 Data model: Proposed. See `adr/004-data-model.md`.
- ADR-005 Callback ingress in dev and prod: Accepted. See `adr/005-dev-callback-tunnel.md`.
- ADR-006 Sync/async boundary: Proposed. See `adr/006-sync-async-boundary.md`.
- ADR-007 Pre-M4 manual facility link: Accepted. See `adr/007-pre-m4-facility-link-workaround.md`.
- ADR-008 M2 seam design: Accepted. See `adr/008-m2-seam-design.md`.
- ADR-009 Facility setup page: Accepted. See `adr/009-facility-setup-page.md`.
- ADR-010 Instance and facility scope: Accepted; `AbdmBridge` removed by ADR-011. See `adr/010-instance-vs-facility-scope.md`.
- ADR-011 Lean M2: Accepted. See `adr/011-lean-m2.md`.
- ADR-012 Error handling: Accepted. See `adr/012-error-handling.md`.
- ADR-013 Staged sharing: Accepted. See `adr/013-staged-sharing.md`.
