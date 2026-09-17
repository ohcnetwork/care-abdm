# 05 — Codebase map (as of 2026-09-17, ADR-011 with its 2026-09-17 amendments)

Read this before touching code. Every module has one job; keep it that way.

## Backend — `backend/src/abdm/` (Django app, label `abdm`, mounted at `/api/abdm/`)

| Module | Job | Invariant |
|---|---|---|
| `apps.py` | `AppConfig`; `ready()` imports `care_seams` and `signals` | Only place side-effect imports happen |
| `settings.py` | Reads `ABDM_*` env into `plugin_settings` (pattern from `care_token_display`) | Names carry no environment marker; sandbox and production differ by value only |
| `care_seams.py` | Registers with Care: `Patient.extensions["abdm"]`, `Facility.extensions["abdm"]` (`facility_id`, `facility_name`, `hip_name`, `counters`; server-written `hip_id`, `hrp_registered_at`, `last_error`), and the 2 `auto_maintained` identifier configs (`abdm/abha-number`, `abdm/abha-address`) | Extension fields carry `x-ui.render_blacklist`; host forms never render them |
| `models.py` | M1: `AbhaTransaction`, `AbdmProfileShare`. Audit: `AbdmOutboundRequest`, `AbdmCallback`. M2: `AbdmLinkToken`, `AbdmCareContext`, `AbdmLinkSession`, `AbdmConsent`, `AbdmDataRequest` | Secrets (X-token, link token, OTP hash) stay here, never in an extension. Ciphertext is never stored |
| `migrations/` | `0001_initial` (schema restarted 2026-09-15), `0002` adds `AbdmCallback.signature_header` and `signature_error` | Must match `models.py` |
| `signals.py` | `post_save(Patient)`: consume `extensions.abdm.txn_id` → identifiers (M1). `post_save(Encounter)`: queue `tasks.sync_encounter` after commit when the facility is set up and the save touched `status`, `encounter_class` or `period` | `link_patient_to_transaction` is the single writer of ABHA identifiers |
| `tasks.py` | `dispatch_callback` routes a verified callback by operation id through `CALLBACK_HANDLERS`; `sync_encounter` runs the HIP-initiated link and repeats only what `errors.classify()` calls repeatable | A Celery worker must run for M2 and for Scan and Share. A refusal is never repeated: it earns `ABDM-1092` |
| `urls.py` | Route table. One catch-all POST route (last) receives every gateway callback: the bridge URL is `<base>/api/abdm`, so a callback lands at `/api/abdm/<callback path>` whatever the path. Mirrors: `frontend/src/lib/careApi.ts`, `bruno/` | Change all 3 together |
| `gateway/session.py` | Gateway session token, Redis-cached, 60 s margin | The token never leaves the server |
| `gateway/outbound.py` | `send()`: every call to ABDM or to an HIU push URL; adds `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID`, `Authorization`, `X-HIP-ID` (from the facility); records `AbdmOutboundRequest`; reads all 3 error envelopes; `failure(row)` gives the `errors.Failure`; keeps the response headers of a refusal in `response_headers` | A 2xx with an `{"error": {...}}` body is a failure. `send()` never raises: a transport failure is recorded and returned, so every caller reads 1 shape. ABDM answers some refusals with an empty body, so the headers are the only evidence (E11) |
| `gateway/certs.py` | Gateway JWKS, cached 6 h, fetched with the gateway bearer token (the sandbox answers 401 without it) | Raises `GatewayCertsError`; the receiver turns it into a 503 |
| `gateway/bridge.py` | Callback URL derivation, `PATCH bridge/url`, live `GET bridge-services` (caches the bridge id 1 h), HRP service registration on `ABDM_HSP_URL` | The gateway is the source of truth for bridge state; nothing is snapshotted |
| `gateway/views.py` | `GET gateway/status`, `GET bridge` (staff), `POST bridge/register-url` and `GET admin/overview` (superuser: gateway status, live bridge and services, HIP facilities) | Probes never return tokens |
| `callbacks/paths.py` | Pure: callback path → operation id. The real paths carry an `/api` prefix the docs omit (observed 2026-09-17: `{bridgeUrl}/api/v3/hip/token/on-generate-token`); `operation_for_path()` drops it, and the `/v0.5/...` spellings are aliases | No Django import; a path the docs never named maps to `""` and is still stored |
| `callbacks/receiver.py` | Stores each callback before verification; idempotency key; resolves the operation id through `paths.py` | Never dispatch an unverified callback |
| `callbacks/signature.py` | JWT against the gateway JWKS: configured header first, then any JWT-shaped header; algorithm from the matching JWK (RS256 or RS512); returns the header name; `seconds_late()` reports how late the token was | Fails closed in every environment, but accepts a token that expired inside `ABDM_CALLBACK_SIGNATURE_LEEWAY_SECONDS` (default 3600). The gateway repeats a refused delivery about 16 minutes later with the same, dead token (finding E10) |
| `callbacks/views.py` | Generic callback view (`AllowAny`): store, verify, `202 {}`; 401 on a bad signature, 503 when the verifier cannot run; never raises (Care's `ATOMIC_REQUESTS` would roll the row back). Plus the superuser callback log | The row always survives; `signature_header` and `signature_error` are the evidence |
| `facility/rules.py` | Pure format rules for HFR ID, facility name, HIP name; `find_hip_service()` picks the gateway service row for an HFR id | No Django import |
| `facility/service.py` | Reads and writes `Facility.extensions["abdm"]`. **HIP ID is not the HFR facility ID on the sandbox**: the registry issues `<facilityId>_<n>` (`IN1410000232_1`), the link token names it, and a call sent with the bare HFR id never gets its callback (2026-09-17). `sync_hip_id()` stores the service id read from `gateway-list-bridge-services` (after HRP registration and on every setup-page load); `hip_id_for()` returns it and is empty until a service exists, so an unregistered facility never sends a call the gateway would accept and drop; `facility_for_hip_id()` resolves an inbound HIP ID in any of the 3 forms | `hip_id_for()` and `facility_for_hip_id()` are the only HIP ID logic |
| `facility/views.py` | `GET/PUT facilities/<id>/abdm`, `POST .../hrp-services` | Gate `can_update_facility_obj` |
| `abha/*` | M1: `crypto` (RSA-OAEP SHA-1), `checksums` (Luhn, Verhoeff), `client` (1:1 endpoint wrappers), `service` (journeys, X/T/R-token lifecycle), `views` | `service` is the only module that reads or writes user tokens |
| `share/*` | M1 Scan and Share: `rules` (pure), `service` (`handle_profile_share` → token → `on-share` ack), `views` (desk inbox) | Always sends an acknowledgement, SUCCESS or FAILURE |
| `errors.py` | **Pure.** 1 catalogue and 1 `classify()` that turns any failure into what happened, what to do, and whether a repeat helps now, later (with the time) or not at all. Holds `TOKEN_REQUEST_WINDOW` (7 min, finding F6), `CALLBACK_DEADLINE`, the sandbox `OVERRIDES` and the plug's own codes (`NO_ABHA`, `NO_ANSWER`, …). Read ADR-012 first | No Django import. Nothing else may keep a hand-written list of ABDM codes |
| `error_catalogue.py` | **Generated**, do not edit. 818 codes from `/docs/hiecm/v3/reference/error-codes.md`. Rebuild: `python3 scripts/generate-error-catalogue.py` | `getting-started/build-it-well` tells every HIP to key its handling to this table |
| `hip/rules.py` | Pure M2 rules: care-context display, gender code, link-token expiry (`exp` or 6 months), OTP hash, date-range check, every request body builder, parsers for the consent and health-information callbacks | No Django import |
| `hip/crypto.py` | Pure data-transfer crypto: X25519 → XOR nonces → HKDF-SHA256 → AES-256-GCM; `decrypt()` for tests and M3 | No Django import |
| `hip/contexts.py` | HIP-initiated route: `ensure_care_context`, `ensure_link_token` (a token older than `rules.LINK_TOKEN_FRESHNESS` is regenerated; the link goes out from its callback), `sync_encounter`, `request_link`, `notify_context`, `send_sms_deep_link`, and the 4 result-callback handlers (error codes through `rules.normalize_error_code`) | A context becomes `linked` only in `handle_carecontext_result` |
| `hip/discovery.py` | User-initiated route: `handle_discover` (verified ABHA match only), `handle_link_init` (OTP by Care SMS), `handle_link_confirm` | The OTP is stored as a hash; fixed value outside production |
| `hip/consent.py` | `handle_consent_notify`: store GRANTED / REVOKED / EXPIRED, send `on-notify` ack | The artefact signature is stored, not verified |
| `hip/transfer.py` | `handle_health_information_request`: validate consent, range and key material → ack → `transfer()`: build, encrypt, push, notify inside the 20-minute window | Ciphertext leaves `entries` before the row is saved |
| `hip/views.py` | `GET/POST encounters/<id>/care-context[/link]`, `POST patients/<id>/abha/sms-link`, `GET patients/<id>/abha/consents`. `_failure_block()` adds the classified `failure` to the state | Gates from `care/security/authorization/{encounter,patient}.py`. Care runs no beat schedule for plugs, so the "ABDM never answered" rule is applied here, at read time (ADR-012 D6) |
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
| `manifest.tsx` | Routes `/facility/:facilityId/abdm/setup` and `/admin/abdm` (+ `adminNavItems` entry "ABDM"); slots `FacilityHomeActions`, `PatientRegistrationForm`, `PatientDetailsTabDemographyGeneralInfo`, `PatientHomeActions`, `PatientSearchActions`, `EncounterActions`, `EncounterOverviewTop` |
| `lib/request.ts` | Host-aware fetch (auth header, `CARE_API_URL`); `apiRoutes`; `fetchBlob` for the card |
| `lib/careApi.ts` | Every plug route + TS types. Mirrors `backend/src/abdm/urls.py`. `hip_id` (facility config and admin overview rows) is the gateway-issued service id, empty until the HRP service is registered |
| `components/abdm/abha-wizard.tsx` | The M1 dialog: Create (Aadhaar OTP → mobile OTP → address) or Link (mobile / ABHA number / ABHA address / Aadhaar). A login that finds no ABHA (`ABDM-1114` or an empty account list) shows one action, "Create a new ABHA", that starts the create journey with the typed Aadhaar and mobile |
| `components/abdm/field-help.tsx` | ABDM-docs-sourced help icon for manual fields |
| `components/abdm/facility-home-actions.tsx` | Slot: one dropdown row that links to the setup page (ADR-009) |
| `components/abdm/admin-dashboard.tsx` | `/admin/abdm` (superuser, the only place technical detail is shown): gateway session badge, bridge card (callback URL vs registered URL, register button), live bridge services table, HIP facilities table (HFR facility ID, gateway-issued `hip_id`, Registered / Not registered) with links to their setup pages, last 20 callbacks. All values read live |
| `components/abdm/facility-setup-page.tsx` | 2 cards, copy written for a hospital administrator: facility identity (HFR ID from the NHPR record, read-only "HIP ID (issued by ABDM)" that is empty until the HRP service is registered) + HRP registration (with a 1-line bridge status that links to `/admin/abdm`); Scan and Share counters with QR codes |
| `components/abdm/patient-registration-form.tsx` | Slot: runs the wizard, sets `extensions.abdm.txn_id`, prefills demographics; consumes `?abdm_txn=` |
| `components/abdm/patient-abha-panel.tsx` | Slot on the Demography tab: status, copy, link, card |
| `components/abdm/patient-home-actions.tsx` | Sidebar chip |
| `components/abdm/patient-search-actions.tsx` | Find by ABHA; Scan and Share inbox |
| `components/abdm/profile-share-inbox.tsx` | Desk inbox dialog (polls 10 s) |
| `components/abdm/care-context-state.ts` | Shared query for the encounter slots; `viewFor()` folds the backend state into 7 desk views (`no_abha`, `no_records`, `ready`, `in_progress`, `waiting`, `shared`, `failed`), polls 5 s while `in_progress` and 15 s while `waiting`; `retryAfter()` gives the moment the button frees itself; `hiTypeLabel()` maps record types to human labels. The `activity` log is never rendered for the desk | Reads `failure.retry` only. **It must never test an ABDM code**: the backend classifies once (ADR-012) |
| `components/abdm/encounter-actions.tsx` | Slot: "Share with ABHA" / "Shared with ABHA" button → compact dialog (max-w-md): one sentence per view, spinner while waiting, what was shared as human labels, backend `errorMessage` on failure; actions "Share with ABHA" / "Try again" / "Send update" (linked only). No codes, no REQUEST-IDs |
| `components/abdm/encounter-overview-top.tsx` | Slot: one stable row with the visit's display name and a plain sharing-status badge (`abdm_cc_status_<view>`) |
| `components/ui/*` | Vendored UI primitives (legacy from the reference plug) |
| `public/locale/en.json` | All `abdm_*` keys, sorted (217). Dynamic families: `abdm_hint_*`, `abdm_step_*`, `abdm_link_step_*`, `abdm_otp_system_*`, `abdm_share_status_*`, `abdm_source_*`, `abdm_cc_status_*` (one per `CareContextView`), `abdm_hi_type_*` (one per ABDM record type), `abdm_facility_help_*`. Desk-facing keys (`abdm_cc_*`, `abdm_hi_type_*`) never say gateway, callback, care context, HRP, bridge, token or probe |

## Bruno collection — `bruno/`

Folders: `auth`, `probes`, `bridge`, `facility`, `abha-enrol`, `abha-login`, `transactions`, `patient`, `encounters`, `callbacks`, `scan-share`. 47 requests; every route in `urls.py` has one. Secrets and personal data are secret variables.

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
- Inbound gateway callbacks and the link token: 2026-09-17 (2 real `on-generate-token` callbacks, one with a token, one with `ABDM-1027`).
- Not yet observed: a link result (`on_carecontext`; the link call answers an empty 400, findings E11), notify, discovery, consent, data transfer. The in-process smoke covers these with the network mocked (`03-roadmap.md`).
