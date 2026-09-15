# 05 — Codebase map (as of 2026-09-15, ADR-011 rebuild)

Read this before touching code. Every module has one job; keep it that way.

## Backend — `backend/src/abdm/` (Django app, label `abdm`, mounted at `/api/abdm/`)

| Module | Job | Invariant |
|---|---|---|
| `apps.py` | `AppConfig`; `ready()` imports `care_seams` and `signals` | Only place side-effect imports happen |
| `settings.py` | Reads `ABDM_*` env into `plugin_settings` (pattern from `care_token_display`) | Names carry no environment marker; sandbox and production differ by value only |
| `care_seams.py` | Registers with Care: `Patient.extensions["abdm"]`, `Facility.extensions["abdm"]` (`facility_id`, `facility_name`, `hip_name`, `counters`, `hrp_registered_at`, `last_error`), and the 2 `auto_maintained` identifier configs (`abdm/abha-number`, `abdm/abha-address`) | Extension fields carry `x-ui.render_blacklist`; host forms never render them |
| `models.py` | M1: `AbhaTransaction`, `AbdmProfileShare`. Audit: `AbdmOutboundRequest`, `AbdmCallback`. M2: `AbdmLinkToken`, `AbdmCareContext`, `AbdmLinkSession`, `AbdmConsent`, `AbdmDataRequest` | Secrets (X-token, link token, OTP hash) stay here, never in an extension. Ciphertext is never stored |
| `migrations/0001_initial.py` | The whole schema (restarted 2026-09-15) | Must match `models.py` |
| `signals.py` | `post_save(Patient)`: consume `extensions.abdm.txn_id` → identifiers (M1). `post_save(Encounter)`: queue `tasks.sync_encounter` after commit when the facility is set up and the save touched `status`, `encounter_class` or `period` | `link_patient_to_transaction` is the single writer of ABHA identifiers |
| `tasks.py` | `dispatch_callback` routes a verified callback by operation id through `CALLBACK_HANDLERS`; `sync_encounter` runs the HIP-initiated link | A Celery worker must run for M2 and for Scan and Share |
| `urls.py` | Route table. Mirrors: `frontend/src/lib/careApi.ts`, `bruno/` | Change all 3 together |
| `gateway/session.py` | Gateway session token, Redis-cached, 60 s margin | The token never leaves the server |
| `gateway/outbound.py` | `send()`: every call to ABDM or to an HIU push URL; adds `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID`, `Authorization`, `X-HIP-ID` (from the facility); records `AbdmOutboundRequest`; reads all 3 error envelopes | A 2xx with an `{"error": {...}}` body is a failure |
| `gateway/certs.py` | Gateway JWKS, cached 6 h | No bearer token on the certs call |
| `gateway/bridge.py` | Callback URL derivation, `PATCH bridge/url`, live `GET bridge-services` (caches the bridge id 1 h), HRP service registration on `ABDM_HSP_URL` | The gateway is the source of truth for bridge state; nothing is snapshotted |
| `gateway/views.py` | `GET gateway/status`, `GET bridge`, `POST bridge/register-url` (superuser) | Probes never return tokens |
| `callbacks/receiver.py` | Stores each callback before verification; idempotency key; path → operation id map (every path variant the docs name) | Never dispatch an unverified callback |
| `callbacks/signature.py` | RS256 JWT against the gateway JWKS; header from `ABDM_CALLBACK_SIGNATURE_HEADER` | Fails closed in every environment |
| `callbacks/views.py` | Generic callback view (`AllowAny`, `202 {}` after verification) plus the superuser callback log | The list hides raw body and headers |
| `facility/rules.py` | Pure format rules for HFR ID, facility name, HIP name | No Django import |
| `facility/service.py` | Reads and writes `Facility.extensions["abdm"]`; `hip_id_for()` derives HIP ID = HFR facility ID; `register_hrp_service()` | `hip_id_for()` is the single source of HIP ID |
| `facility/views.py` | `GET/PUT facilities/<id>/abdm`, `POST .../hrp-services` | Gate `can_update_facility_obj` |
| `abha/*` | M1: `crypto` (RSA-OAEP SHA-1), `checksums` (Luhn, Verhoeff), `client` (1:1 endpoint wrappers), `service` (journeys, X/T/R-token lifecycle), `views` | `service` is the only module that reads or writes user tokens |
| `share/*` | M1 Scan and Share: `rules` (pure), `service` (`handle_profile_share` → token → `on-share` ack), `views` (desk inbox) | Always sends an acknowledgement, SUCCESS or FAILURE |
| `hip/rules.py` | Pure M2 rules: care-context display, gender code, link-token expiry (`exp` or 6 months), OTP hash, date-range check, every request body builder, parsers for the consent and health-information callbacks | No Django import |
| `hip/crypto.py` | Pure data-transfer crypto: X25519 → XOR nonces → HKDF-SHA256 → AES-256-GCM; `decrypt()` for tests and M3 | No Django import |
| `hip/contexts.py` | HIP-initiated route: `ensure_care_context`, `ensure_link_token`, `sync_encounter`, `request_link`, `notify_context`, `send_sms_deep_link`, and the 4 result-callback handlers | A context becomes `linked` only in `handle_carecontext_result` |
| `hip/discovery.py` | User-initiated route: `handle_discover` (verified ABHA match only), `handle_link_init` (OTP by Care SMS), `handle_link_confirm` | The OTP is stored as a hash; fixed value outside production |
| `hip/consent.py` | `handle_consent_notify`: store GRANTED / REVOKED / EXPIRED, send `on-notify` ack | The artefact signature is stored, not verified |
| `hip/transfer.py` | `handle_health_information_request`: validate consent, range and key material → ack → `transfer()`: build, encrypt, push, notify inside the 20-minute window | Ciphertext leaves `entries` before the row is saved |
| `hip/views.py` | `GET/POST encounters/<id>/care-context[/link]`, `POST patients/<id>/abha/sms-link`, `GET patients/<id>/abha/consents` | Gates from `care/security/authorization/{encounter,patient}.py` |
| `fhir/__init__.py` | `HI_TYPE_PROFILES`, `available_hi_types(encounter)`, `build_bundle(encounter, hi_type)` | Add a builder module and register it in `_builders()` |
| `fhir/bundle.py` | Pure bundle helpers: DocumentBundle skeleton, Composition, Patient, Organization, Practitioner, Encounter, MedicationRequest, Condition, AllergyIntolerance, DocumentReference | Every `fullUrl` is `urn:uuid:`; every resource carries the NRCES `meta.profile` |
| `fhir/{op_consult,prescription,health_document}.py` | `has_data(encounter)` and `build(encounter)` per record type | `has_data` must guarantee `build` succeeds |
| `management/commands/abdm_register_bridge_url.py` | Registers `ABDM_CALLBACK_BASE_URL/api/abdm`; prints the live bridge state | Run before HRP registration |

Why `txn_id` and not the ABHA number from the client: a client-supplied ABHA would be forgeable.
Why `post_save` and not a post-create callback: core drops `auto_maintained` identifiers on create
(`care/emr/api/viewsets/patient.py:138`) and the `PatientRegistrationForm` slot has no post-create hook.

## Frontend — `frontend/src/` (Vite MF remote, name from `manifest.tsx`)

| File | Job |
|---|---|
| `manifest.tsx` | Route `/facility/:facilityId/abdm/setup`; slots `FacilityHomeActions`, `PatientRegistrationForm`, `PatientDetailsTabDemographyGeneralInfo`, `PatientHomeActions`, `PatientSearchActions`, `EncounterActions`, `EncounterOverviewTop` |
| `lib/request.ts` | Host-aware fetch (auth header, `CARE_API_URL`); `apiRoutes`; `fetchBlob` for the card |
| `lib/careApi.ts` | Every plug route + TS types. Mirrors `backend/src/abdm/urls.py` |
| `components/abdm/abha-wizard.tsx` | The M1 dialog: Create (Aadhaar OTP → mobile OTP → address) or Link (mobile / ABHA number / ABHA address / Aadhaar) |
| `components/abdm/field-help.tsx` | ABDM-docs-sourced help icon for manual fields |
| `components/abdm/facility-home-actions.tsx` | Slot: one dropdown row that links to the setup page (ADR-009) |
| `components/abdm/facility-setup-page.tsx` | 3 cards: facility identity + HRP registration; bridge (live state, superuser register button); Scan and Share counters with QR codes |
| `components/abdm/patient-registration-form.tsx` | Slot: runs the wizard, sets `extensions.abdm.txn_id`, prefills demographics; consumes `?abdm_txn=` |
| `components/abdm/patient-abha-panel.tsx` | Slot on the Demography tab: status, copy, link, card |
| `components/abdm/patient-home-actions.tsx` | Sidebar chip |
| `components/abdm/patient-search-actions.tsx` | Find by ABHA; Scan and Share inbox |
| `components/abdm/profile-share-inbox.tsx` | Desk inbox dialog (polls 10 s) |
| `components/abdm/care-context-state.ts` | Shared query for the encounter slots (polls 5 s while a gateway answer is pending); status → i18n key |
| `components/abdm/encounter-actions.tsx` | Slot: "Link to ABHA" button → dialog with state, error, gateway activity, "Link now" / "Send update" |
| `components/abdm/encounter-overview-top.tsx` | Slot: one stable row with the care-context display and a status badge |
| `components/ui/*` | Vendored UI primitives (legacy from the reference plug) |
| `public/locale/en.json` | All `abdm_*` keys, sorted (180). Dynamic families: `abdm_hint_*`, `abdm_step_*`, `abdm_link_step_*`, `abdm_otp_system_*`, `abdm_share_status_*`, `abdm_source_*`, `abdm_cc_status_*`, `abdm_facility_help_*` |

## Bruno collection — `bruno/`

Folders: `auth`, `probes`, `bridge`, `facility`, `abha-enrol`, `abha-login`, `transactions`, `patient`, `encounters`, `callbacks`, `scan-share`. 46 requests; every route in `urls.py` has one. Secrets and personal data are secret variables.

## Data flow — HIP-initiated link (M2 journey 1)

1. Encounter saved → `signals.sync_encounter_care_context` → `tasks.sync_encounter` after commit.
2. `hip.contexts.sync_encounter`: facility set up? patient has ABHA? `available_hi_types` non-empty? → `AbdmCareContext` row.
3. No usable link token → `m2-generate-link-token` (202); the token lands on `/v3/hip/token/on-generate-token` → `AbdmLinkToken.active` → `link_pending_contexts`.
4. `m2-hip-link-care-context` with `X-Link-Token` (202) → `link_requested`.
5. `/v3/link/on_carecontext` → `linked` (or `failed` with the gateway code) → `m2-link-care-context-notify` → `/v3/links/context/on-notify` → `notified_at`.

## Data flow — consent and transfer (M2 journey 4)

1. `/v0.5/consents/hip/notify` (or `/api/v3/consent/request/hip/notify`) → `AbdmConsent` → `m2-consent-hip-on-notify` ack.
2. `/v0.5/health-information/hip/request` → `AbdmDataRequest` (deadline = received + 20 min) → validate → `m2-hip-health-information-on-request` ACKNOWLEDGED or ERRORED.
3. `transfer()`: for each linked care context of the consent in the requested range × each consented HI type with data → `build_bundle` → MD5 → encrypt → 1 push to `dataPushUrl` → `m2-hip-data-flow-notify` TRANSFERRED or FAILED.

## Observed against the real sandbox (not just docs)

- Gateway session, bridge PATCH, bridge-services read — 2026-09-09 / 2026-09-14.
- M1 login by mobile end to end, real Aadhaar enrol, login by ABHA number / address / Aadhaar — 2026-09-09 to 2026-09-11 (user-driven).
- HRP registration reaches the HSP Registry and returns the HFR name-mismatch error — 2026-09-14.
- Not yet observed: any inbound gateway callback (signature header unknown), link token, link result, discovery, consent, data transfer. The in-process smoke covers these with the network mocked (`03-roadmap.md`).
