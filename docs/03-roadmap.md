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

Pending sandbox observations (user-driven):
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

### Sandbox proofs (user-driven; each ends on an observed gateway answer)
- [~] 1. Facility and bridge.
  - [x] Observed 2026-09-14: `GET bridge-services` → HTTP 200, bridge `SBXID_035123`, url `https://care-abdm-sbx.rithviknishad.dev/api/abdm`, `services: []`.
  - [x] Observed 2026-09-14: HRP register → HTTP 200 error 2500 "Provided facility name is not matched with registered name" (user screenshot). Host fixed to `ABDM_HSP_URL`.
  - [x] Observed 2026-09-15 (user): bridge URL registered; HRP register → HTTP 200, `hrp_registered_at` 16:02 IST. `GET /api/abdm/admin/overview` shows the service `{"id": "IN1410000232_1", "name": "FACILITY WITH P", "types": ["HIP", "HIU"], "active": true}` (findings B18: the real row shape differs from the docs).
  - [ ] USER screenshot: `/admin/abdm` shows the gateway badge, the bridge card and the services table after registration.
  - [ ] USER screenshot: `/facility/<id>/abdm/setup` shows the 2 cards and saves.
- [~] 2. Callback receiver: the first real gateway callback row shows the signature header name (`GET /api/abdm/callbacks/<id>`, superuser). Update `ABDM_CALLBACK_SIGNATURE_HEADER` if it is not `Authorization`; close findings E2.
  - [x] Added 2026-09-15: a catch-all POST route under `/api/abdm/` stores a callback to any path the docs did not name (row with empty operation id, `unhandled`), so a path mismatch shows as a row and not as an invisible Care 404. Smoke: stored and `unhandled`; GET on an unknown path is 405.
- [~] 3. Link token: `on-generate-token` lands for a patient with ABHA → `AbdmLinkToken.status=active`; record the token's `exp` claim (findings F2).
  - [x] Observed 2026-09-15 16:20:52 IST (diagnosis agent, 1 manual `POST .../care-context/link`): `m2-generate-link-token` → HTTP 202, REQUEST-ID `f250c4b6-31fd-45b2-8d36-e4dc295c7465`, `X-HIP-ID: IN1410000232`. Care and the tunnel answered 200 on the public health URL. **No callback reached any known path within 120 s.** The docs give no delivery window (troubleshooting "The callback never arrives", check 3). Cause not yet known; the encounter had pre-existed the setup, so nothing had fired before the manual trigger (a medication request does not trigger the link — known limitation).
  - [x] Observed 2026-09-15 17:37 IST (user, runserver log): `Internal Server Error: /api/abdm/v3/hip/token/on-generate-token` — a POST **did reach the documented callback path** on the bridge. The receiver crashed: `GatewayCertsError: gateway certs failed: HTTP 401` (the certs endpoint needs the bearer token, findings B14), and Care's `ATOMIC_REQUESTS` rolled the stored row back (J6). Fixed the same hour: certs fetch carries the token; the receiver never raises (401 bad signature, 503 verifier unavailable, row kept with `signature_error`); the verifier accepts the JWK's own RS256/RS512 and auto-detects the header (migration 0002). Smoke: 503 + row kept; real verifier 202 with auto-detected header; bad signature 401 with reason. Whether that POST was the gateway or the diagnosis agent's probe is not yet settled; the agent's report will say.
  - [ ] USER: check the Care `runserver` and `cloudflared` terminals for any inbound POST after 16:20 IST. A 404 means a path outside `/api/abdm/`; a 401 means the signature check refused it (a row would exist). Nothing means the gateway did not call. Then re-check `GET /api/abdm/callbacks` after a longer wait.
  - [ ] If nothing arrives: 1 experiment — send `X-HIP-ID` = the gateway service id (`IN1410000232_1`) instead of the HFR facility id, since the docs' claim "HIP ID = HFR facility ID" is unproven against the sandbox (findings E1). Then escalate per the docs' report format (API, REQUEST-ID, TIMESTAMP, response).
- [ ] 4. HIP link: create an Encounter with a prescription → `on_carecontext` lands → `AbdmCareContext.status=linked`; record the real `status` value (findings F4).
- [ ] 5. Notify: `on-notify` acknowledgement SUCCESS.
- [ ] 6. Discovery from a PHR app → `on-discover` 202 → the PHR app shows the visit. Record the real `verifiedIdentifiers` shape (findings G1).
- [ ] 7. User link: PHR app selects the visit → OTP SMS → confirm → linked. Confirm the docs-inbound init body and the confirm `token` type.
- [ ] 8. SMS deep link: sandbox SMS received; `on-notify` SUCCESS.
- [ ] 9. Consent granted in the PHR app → `AbdmConsent GRANTED`; record the real path and body (findings E3, H1).
- [ ] 10. Data transfer: PHR app requests records → push → notify TRANSFERRED → **record readable in the PHR app**. This is the docs' end-to-end loop (`/concepts/hip-hiu`).

### Known limitations after this pass
- Notify-on-new-records runs on Encounter status change or on the desk "Send update" action, not on every clinical write (ADR-011 consequence).
- Record types: OPConsultation, Prescription, HealthDocumentRecord. DiagnosticReport, DischargeSummary, WellnessRecord, ImmunizationRecord, Invoice are deferred (findings I4).
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
