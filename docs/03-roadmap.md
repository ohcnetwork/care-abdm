# 03 — Roadmap

Status legend: [ ] not started · [~] in progress · [x] done (with evidence link)

Order (Rithvik, 2026-09-09): M1 → M2 → M3 → M4. The docs say M4's facility ID blocks M2; we bridge that with the manual facility-link workaround (ADR-007) until M4 lands. Every phase ends on
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
- [x] 2026-09-14 Bruno collection (`bruno/`) — 47 files that cover every route in `backend/src/abdm/urls.py`: Care login and refresh, 2 probes, 5 facility routes, 6 enrol steps, 3 login steps, the transaction read-back, 3 patient routes, the 2 callback probes, and all 13 callback receiver paths. Bodies come from the docs mirror; the 3 bodies that the docs do not publish are marked as placeholders (see `docs/findings.md`, 2026-09-10). Observed: `@usebruno/lang` parsed 47/47 files with 0 failures; `bru run probes --env local` gave `health 200` with the assertion passed and `gateway-status 403` without a token; `bru run callbacks/link-on-carecontext.bru --env-var careUrl=http://localhost:8099` reached a local echo server on path `/api/abdm/v3/link/on_carecontext` with a fresh `REQUEST-ID` UUID and a UTC `TIMESTAMP` with milliseconds. Not yet run against the sandbox with real credentials (user-driven).

## Phase 1 — Gateway session (prerequisite to everything)  [~]
Docs: `/docs/hiecm/v3/api/gateway`, `/concepts/gateway`, `/getting-started/first-fifteen-minutes`.
- Backend: `abdm/gateway/session.py` — `POST sessions` with clientId/secret, cache token until expiry, refresh. Header set (`X-CM-ID`, `REQUEST-ID`, `TIMESTAMP`, `Authorization`) exactly as `get_operation gateway-sessions-create` says.
- Backend: fetch RSA public certificate (M1 encryption) and gateway JWKS (`gateway-get-gateway-certs`) for callback signature verification (`/concepts/callback-authenticity`).
- [x] 2026-09-09 verified by curl from the workdir: `POST https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions` → HTTP 200, `{accessToken, expiresIn: 1200, refreshExpiresIn: 1800, refreshToken, tokenType: "bearer"}` — shape identical to the docs example. Token lifetime is 20 min; refresh path via `m1-token-refresh` still to confirm.
- [x] 2026-09-09 from inside Care: `abdm.gateway.session.get_access_token()` → token, Redis TTL 1140s (=1200−60 margin), second call served from cache. Exposed as `GET /api/abdm/gateway/status` (auth required, token never returned).
- [ ] refresh via refreshToken (docs `m1-token-refresh`) — currently we just create a new session on expiry, which the docs allow.

## Phase 2 — M1 Create: ABHA identity  [~]
Docs: `/milestones/m1`, `/api/m1`, `/api/m1/apis`, skill `abdm-m1`.
Mandatory set (from `/concepts/hip-hiu` capability table, private integrator):
1. ABHA creation by Aadhaar OTP (request otp → verify → address suggestions → claim address → enrol byAadhaar).
2. Login by mobile / Aadhaar / ABHA number / ABHA address (request → verify → select account).
3. Fetch profile, download ABHA card.
4. Communication mobile number (post-enrol).
5. Local Luhn (ABHA number) and Verhoeff (Aadhaar) validators.
Skip: face auth, biometrics, demographic auth, benefits, re-KYC (optional for private).

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
- [x] 2026-09-10 X-token refresh — `AbhaTransaction.refresh_token_expires_at` (migration 0002), `service.ensure_x_token()` refreshes via `GET /v3/profile/account/request/token` (`R-token` header) when the X-token is expired and the R-token is not; the card uses it. Observed in-process: expired X + valid R → refreshed + rotated; both expired → `NoUserSession` (409). The `R-token` prefix is a docs conflict (see findings). The plug tried prefixed first, then bare on AS-1358/1360.
- [x] 2026-09-11 Aadhaar login always uses the Aadhaar-linked mobile — the "Send the OTP to" selector stays only for the ABHA number and the ABHA address (`abha-wizard.tsx::canChooseOtpSystem`); `LoginOtpRequest` sets `otp_system="aadhaar"` for the `aadhaar` hint, because UIDAI sends that OTP. Observed: `manage.py shell` — `aadhaar`+`abdm` → `aadhaar`, `aadhaar` with no value → `aadhaar`, `abha-number` keeps both values; `npm run build` and `npx eslint src` clean (0 errors); 8 backend tests OK.

Pending sandbox observations (user-driven):
- [x] Real Aadhaar enrol run.
- [x] Login by ABHA number, ABHA address, and Aadhaar with real OTPs.
- [ ] X-token refresh, including the `R-token` prefix conflict (findings #6).
- [ ] Card response bytes and content-type (findings gap #4).

## Phase 3 — M2 Attach: linking and sharing (the bulk)  [~]
Prereq: ADR-007 manual facility link form (`FacilityHomeActions`) so a Care facility has an ABDM facility ID before M4.
Design: ADR-008.
Docs: `/milestones/m2`, `/api/m2`, `/concepts/linking`, `/concepts/data-flow`, `/concepts/encryption`, `/concepts/fhir`, skills `abdm-m2`, `abdm-fhir`.
- [~] 1. Facility and bridge proof — save `facilityId`, `facilityName`, `HRP`, `hip`, and `url`; verify bridge URL and HRP service output against sandbox. USER keeps the tunnel up and supplies sandbox facility values.
  - [x] Code-complete: `Facility.extensions["abdm"]`, the setup API, and the MFE setup page exist.
  - [x] Observed: `/tmp/abdm_m2_smoke.py` PUT and GET round-tripped the facility values.
  - [x] Observed: mocked bridge URL 202 and HRP service 200 wrote `AbdmOutboundRequest` rows and timestamps.
  - [x] Observed: `npm run build` made `dist/assets/remoteEntry.js`.
  - [x] Code-complete 2026-09-10: the form moved from a dropdown dialog to the page `/facility/:facilityId/abdm/setup` (ADR-009). `npm run build` made `dist/assets/facility-setup-page-*.js`.
  - [ ] USER screenshot: the "Configurations" dropdown shows one narrow ABDM row.
  - [ ] USER screenshot: `/facility/<id>/abdm/setup` renders the 3 cards and saves the values.
  - [x] Observed 2026-09-14: bridge services read returns HTTP 200 from the sandbox. Bridge `SBXID_035123`, url `https://care-abdm-sbx.rithviknishad.dev/api/abdm`, `services: []`.
  - [x] Fixed 2026-09-14: HRP registration returned HTTP 503 because the plug used the gateway host. The host moved to `ABDM_HSP_URL` (`https://apihspsbx.abdm.gov.in`). Observed: the same call now reaches the HSP Registry and returns a real answer.
  - [x] Fixed 2026-09-14: the HSP Registry reports a failure with HTTP 200 and an error envelope. `outbound.send()` now marks such a response as failed. Observed: HTTP 200 error 2500 wrote `status=failed`, `error_code=2500`.
  - [ ] sandbox: bridge PATCH returns 200 or 202 with the new form values.
  - [ ] sandbox: HRP registration succeeds. Blocked: the facility config needs `bridge_id` and `hip_name`. USER supplies them on the setup page.
- [~] 2. Callback receiver proof — store raw callbacks, fetch JWKS, fail closed on callback signature, and prove a sandbox callback inserts `AbdmCallback` before dispatch. USER keeps Care public on the tunnel.
  - [x] Code-complete: generic callback receiver, raw callback table, JWKS cache, and RS256 verifier exist.
  - [x] Observed: unsigned callback returned 401, stored headers, and set `signature_status="failed"`.
  - [x] Observed: duplicate unsigned callback returned 401 and did not add a second row.
  - [x] Observed: local RS256 JWT plus cached JWKS returned 202 and reached `dispatch_callback`.
  - [x] Observed: `python -m unittest` ran 8 tests. Result: OK.
  - [ ] sandbox: real gateway callback row shows `signature_status` and the header list.
- [ ] 3. Link token proof — send `m2-generate-link-token`; observe `/v3/hip/token/on-generate-token` and store the token or documented error. USER registers or links a patient with ABHA first.
- [ ] 4. HIP link proof — create one `AbdmCareContext` for an Encounter; send `m2-hip-link-care-context`; observe `/v3/link/on_carecontext` success or already-linked. USER creates an encounter with a shareable record.
- [ ] 5. Context notify proof — send `m2-link-care-context-notify`; observe `/v3/links/context/on-notify` success.
- [ ] 6. Discovery proof — answer an inbound PHR discovery with metadata only; observe outbound `m2-on-discover-care-contexts` 202 and PHR app context display. USER starts discovery in a PHR app.
- [ ] 7. User link proof — answer link init and confirm; observe final linked state. USER selects the care context and completes the PHR action.
- [ ] 8. SMS deep-link proof — send `m2-sms-deep-link-notify`; observe `/v3/patients/sms/on-notify`. USER confirms sandbox SMS and follows the link in a PHR app.
- [ ] 9. FHIR proof — build first bundles for `Prescription`, `DiagnosticReport`, `OPConsultation`, `DischargeSummary`, and `HealthDocumentRecord`; run MCP `validate_fhir` until 0 findings or a recorded mapping gap.
- [ ] 10. Data transfer proof — ack consent and health-information request, build and encrypt bundles, push to `dataPushUrl`, and call `m2-hip-data-flow-notify` before the 20-minute deadline. USER grants consent in a PHR app.
- Done when: the docs' single end-to-end sandbox loop (`/concepts/hip-hiu` "Testing the loop in sandbox") passes: record visible in a PHR app.

## Phase 4 — M3 Retrieve (HIU)  [ ]
Consent request creation, status callbacks, fetch, decrypt, store, show in an `encounterTabs` tab. Docs: `/milestones/m3`, `/api/m3`, skill `abdm-m3`.

## Phase 5 — M4 Enrol: facility + bridge  [ ]
Docs: `/milestones/m4`, `/api/m4`, `/api/m4/undocumented` (only 2 published endpoints; the rest are "not yet published").
- Store HFR facility ID on the Care facility (where — ADR).
- Register/update bridge callback URL (`gateway-update-bridge-url`, `m1-register-hrp-services`).
- Done when: bridge URL update returns success in sandbox and a test callback lands on `/api/abdm/...`.
- Replaces ADR-007 workaround with browse-and-link; delete the workaround.
- Expect documentation gaps here; log to `findings.md`.

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
