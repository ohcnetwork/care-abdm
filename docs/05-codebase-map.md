# 05 — Codebase map (as of 2026-09-10, M2 steps 1-2 code)

Read this before touching code. Every module has one job; keep it that way.

## Backend — `backend/src/abdm/` (Django app, label `abdm`, mounted at `/api/abdm/`)

| Module | Job | Invariant |
|---|---|---|
| `__init__.py` | Package marker | No runtime code |
| `apps.py` | `AppConfig`; `ready()` imports `care_seams` and `signals` | Only place side-effect imports happen |
| `settings.py` | Reads `ABDM_*` env into a `PluginSettings` (pattern from `care_token_display`) | Names have no env marker; sandbox vs prod differ by value only |
| `care_seams.py` | Registers with Care: `Patient.extensions["abdm"]`, `Facility.extensions["abdm"]`, and two `auto_maintained` identifier configs (`abdm/abha-number`, `abdm/abha-address`) | Extension fields carry `x-ui.render_blacklist`; host forms never render them, the plug's own panel does |
| `callbacks/__init__.py` | Callback package marker | No runtime code |
| `callbacks/receiver.py` | Stores each callback before verification, derives idempotency keys, and maps paths to operation IDs | Never dispatch an unverified callback |
| `callbacks/signature.py` | Verifies callback JWT signatures with gateway JWKS and pinned RS256 | Fail closed in every environment |
| `callbacks/views.py` | Generic callback view plus callback list and detail probes | Callback list hides raw body and headers; detail is superuser-only |
| `facility/__init__.py` | Facility package marker | No runtime code |
| `facility/service.py` | Reads and writes `Facility.extensions["abdm"]`; records bridge and HRP timestamps | Store only config and operational status in the extension |
| `facility/views.py` | Thin DRF views for facility ABDM setup and bridge actions | Uses `can_update_facility_obj` from Care |
| `gateway/__init__.py` | Gateway package marker | No runtime code |
| `gateway/session.py` | Gateway session token (`POST /api/hiecm/gateway/v3/sessions`), Redis-cached, 60 s margin | Token never leaves the server |
| `gateway/bridge.py` | Bridge URL PATCH (accepts 200 and 202) | Uses `gateway/outbound.py` |
| `gateway/certs.py` | Fetches and caches gateway JWKS from `gateway-get-gateway-certs` | Certs endpoint has no bearer token |
| `gateway/hrp.py` | Registers HRP bridge services and reads bridge service lookup endpoints | Register body uses the docs page shape |
| `gateway/outbound.py` | Sends gateway calls with `REQUEST-ID`, `TIMESTAMP`, `Authorization`, and `X-CM-ID`; records `AbdmOutboundRequest` | Never store bearer tokens in request JSON |
| `abha/__init__.py` | ABHA package marker | No runtime code |
| `abha/crypto.py` | RSA-OAEP(SHA-1) encryption of Aadhaar/OTP/mobile with the pinned public key (cert endpoint 404s — `findings.md`). Optional `public_key` parameter is only for unit tests | Plaintext PII never logged or stored |
| `abha/checksums.py` | Luhn (ABHA number) / Verhoeff (Aadhaar) | Pure functions |
| `abha/client.py` | 1:1 wrappers over ABHA service endpoints; `_call` returns parsed JSON or the raw response for binary endpoints | No business logic; one method per docs page |
| `abha/service.py` | Orchestration: one function per journey step; records `AbhaTransaction` after each step; strips `tokens` before returning to a view. `ensure_x_token()` refreshes an expired X-token with the stored R-token; `_finalize_login()` fetches `GET /v3/profile/account` after any login; `existing_patient_for()` answers "is this ABHA already on a Care patient" | **Only** module that reads/writes X/T/R-tokens |
| `abha/views.py` | Thin DRF views. Enrol/login views are facility-agnostic; patient-scoped views check `can_view_patient_obj` / `can_write_patient_obj` (`care/security/authorization/patient.py`) | No ABDM calls outside `service` |
| `models.py` | `AbhaTransaction`, `AbdmOutboundRequest`, and `AbdmCallback` | Aadhaar/OTP never stored; callbacks store raw data only in the table |
| `migrations/` | `0001` creates `AbhaTransaction`; `0002` adds refresh state; `0003` adds M2 request and callback tables | Migrations must match `models.py` |
| `signals.py` | `post_save(Patient)` consumes `extensions.abdm.txn_id`; `link_patient_to_transaction(patient, txn)` is the **single writer** of ABHA identifiers + extension + `instance_identifiers` rebuild; used by both the signal and `POST .../abha/link` | Unknown txn → stripped + logged; txn/ABHA already bound elsewhere → `LinkError` |
| `urls.py` | Route table; see `frontend/src/lib/careApi.ts` for the mirror | Paths are the contract with the MFE — change both |
| `tasks.py` | Celery tasks for callback dispatch | Current M2 step marks verified callbacks as unhandled |

Why `txn_id` and not the ABHA number from the client: a client-supplied ABHA would be forgeable.
Why `post_save` and not a post-create callback: core drops `auto_maintained` identifiers on create
(`care/emr/api/viewsets/patient.py:138`) and the `PatientRegistrationForm` slot has no post-create
hook. See `adr/004` amendment.

## Frontend — `frontend/src/` (Vite MF remote, name from `manifest.tsx`)

| File | Job |
|---|---|
| `manifest.tsx` | Registers the route `/facility/:facilityId/abdm/setup` and the slots: `FacilityHomeActions`, `PatientRegistrationForm`, `PatientDetailsTabDemographyGeneralInfo`, `PatientHomeActions`, `PatientSearchActions`. The route node carries its own `Suspense`, because the host does not add one |
| `lib/request.ts` | Host-aware fetch (auth header, `CARE_API_URL`); `apiRoutes`/`HttpMethod`; `fetchBlob` for the card |
| `lib/careApi.ts` | Every plug route + TS types. Mirrors `backend/src/abdm/urls.py`. `hostFacility` is the one host route the MFE calls |
| `lib/types/facility.ts` | Minimal host `FacilityHomeActions` prop type | Keep only fields the plug reads |
| `components/abdm/abha-wizard.tsx` | The one dialog: chooser → Create (Aadhaar OTP → mobile OTP → address) or Link (identify by mobile / ABHA number / ABHA address / Aadhaar → OTP → account picker only for mobile). Emits `AbhaWizardResult {txnId, profile, source, existingPatient}`. `renderDone` lets a caller replace the final step |
| `components/abdm/facility-home-actions.tsx` | Slot: one dropdown row only. Shows the gateway status dot and links to the setup page. Never opens a dialog — see ADR-009 |
| `components/abdm/facility-setup-page.tsx` | The ADR-007 setup form as a full page at `/facility/:facilityId/abdm/setup`. Three cards (facility identity, HIP identity, bridge and services), a sticky save bar, and the two register actions. The form writes through Care only |
| `components/abdm/patient-registration-form.tsx` | Slot: runs the wizard, `form.setValue("extensions.abdm.txn_id")`, prefills demographics. Also consumes `?abdm_txn=` (handoff from Find by ABHA) via `GET abha/transactions/<txnId>` |
| `components/abdm/patient-abha-panel.tsx` | Slot on Demography tab: status, copy, link, card dialog (`fetchBlob` → object URL) |
| `components/abdm/patient-home-actions.tsx` | Sidebar chip |
| `components/abdm/patient-search-actions.tsx` | Slot next to "Add patient": Find by ABHA → open existing patient or register with prefill |
| `components/ui/*` | Vendored from careui.ohc.network registry (`input-otp` added 2026-09-09). Legacy shadcn copies from the reference plug otherwise |
| `public/locale/en.json` | All `abdm_*` keys, sorted. Missing keys render as raw key strings, silently |

## Data flow — registration

1. Wizard completes at ABDM → `service` stores `AbhaTransaction(txn_id, abha_number, tokens…)`.
2. Slot sets `extensions.abdm.txn_id`; host POSTs `/api/v1/patient/`.
3. `signals.post_save` → `link_patient_to_transaction` → identifiers + extension rewritten to
   `{abha_number, abha_address, abha_linked_at, abha_source, kyc_verified}`.
4. Panel reads `patientData.extensions.abdm`; the card goes through `GET /api/abdm/patients/<id>/abha/card` using the stored X-token (409 when none).

## Planned M2 data flow — steps 3-5

This flow is planned. Steps 1 and 2 only add the required seams.

1. `post_save(Encounter)` checks that the Patient has ABHA and the Facility has ABDM config.
2. Celery gets or refreshes the link token for the patient.
3. Celery sends `m2-hip-link-care-context` with `Encounter.external_id`.
4. The callback receiver stores `/v3/link/on_carecontext` and dispatches it after signature success.
5. Celery sends `m2-link-care-context-notify` when the link is active or the Encounter status changes.

## Observed against the real sandbox (not just docs)

- Gateway session, bridge PATCH — 2026-09-09.
- Journey 1/2 request-otp reaches ABDM validation (real Aadhaar run is user-driven).
- **Journey 5 login-by-mobile end to end, including select-account and link to an existing
  patient — 2026-09-09 (user screenshot: KYC verified, card button rendered).**
- Not yet observed: card bytes (content-type), token refresh against sandbox, login by
  ABHA number / address / Aadhaar against sandbox (implemented 2026-09-10; in-process smoke only).
- M2 steps 1-2 observed in-process on 2026-09-10. Facility setup round-trip passed. Unsigned callback failed closed. Local signed callback reached Celery.
