# Findings about the docs site (for the documentation team)

Append-only. Each entry: date, what we needed, where we looked, what happened.

- 2026-09-09 — `/docs/hiecm/v3/getting-started/index.md` and
  `/getting-started/build-with-ai/index.md` render MDX components as raw JSX
  (`<SandboxAction>`, `export const ReadAsAgent = …`). The markdown form of
  Build with AI contains none of the install commands; those are only at
  `/agent-setup/prompt.md`, which is not linked from the markdown.
- 2026-09-09 — `<url>.md` 404s; only `<url>/index.md` works. `llms.txt` says
  "add `.md` to any link", build-with-ai says "add `/index.md`". Inconsistent.
- 2026-09-09 — No identifier-system URI is prescribed for ABHA number / ABHA
  address when an HMIS stores them as FHIR-style identifiers. We invented our
  own (ADR-004).
- 2026-09-09 — `/reference/hiecm-*` pages are JS-only; not readable without a
  browser. MCP `get_operation` covers it.
- 2026-09-09 — MCP `get_operation gateway_sessions_create` returns `$ref`s
  (`#/components/parameters/RequestId`, `#/components/schemas/SessionRequest`)
  unresolved; the endpoint page `/api/gateway/endpoints/gateway-sessions-create/index.md`
  has the full headers/body. Operation ids differ in casing/separator between
  MCP (`gateway_sessions_create`) and URLs (`gateway-sessions-create`).
- 2026-09-09 — POSITIVE: session call built purely from the endpoint page
  worked first time against the sandbox (HTTP 200); response keys matched the
  documented example exactly. `expiresIn` came back 1200 (docs example shows 0).
- 2026-09-09 — `catalogue_info`: 311/319 atoms are `unverified`, 4 verified.
- 2026-09-09 — `gateway-update-bridge-url` docs say `200` with `{"message"}`;
  sandbox returned **HTTP 202 with an empty body** for a valid PATCH. Also
  unstated: whether `url` may include a path prefix (we sent
  `https://care-abdm-sbx.rithviknishad.dev/api/abdm`; to be confirmed by the
  first callback actually arriving).
- 2026-09-09 — `m1-get-public-certificate` documents `GET /profile/public/certificate`
  (server `https://abhasbx.abdm.gov.in/abha/api`) → sandbox **404**. The working
  path is **`/v3/profile/public/certificate`** → 200 `{"publicKey": "<base64 DER SPKI, RSA-4096>"}`.
  The concepts/encryption page itself says the URL "is not yet published"; the
  endpoint page contradicts that with a wrong URL. Also, the docs pages describing
  the key as "PEM" are inaccurate: it is base64 DER without PEM armour.
- 2026-09-09 — Padding: only the concepts/encryption *atom summary* (via MCP
  search) says "RSA OAEP with SHA-1 for the V3 flows"; the rendered page text says
  merely "confirm which padding". Verified on sandbox with `/v3/enrollment/request/otp`:
  OAEP-SHA1 → reached UIDAI (`422 ABDM-1204 Aadhaar number is incorrect`, expected for a
  fake number); PKCS1v15 and OAEP-SHA256 → `400 {"loginId":"Invalid LoginId"}`.
  Suggest stating OAEP/SHA-1 + base64 explicitly on both the encryption page and every
  `<RSA_ENCRYPTED_*>` placeholder.
- 2026-09-09 — Error body shapes observed on ABHA service: `422` → `{"error":{"code","message"}}`;
  `400` → flat `{"<field>": "<message>", "timestamp": ...}`. The M1 errors page should
  show both shapes.
- 2026-09-09 — `m1-encrypt-value` helper (`POST /v3/phr/app/enrollment/encrypt`) works
  (200 `{"encryptedData"}`); docs say body "not described" — it is `{"encryptedData": "<base64>"}`.
- 2026-09-09 — `X-CM-ID` is documented for gateway calls; ABHA-service calls work
  without it (not tested whether sending it hurts).

## 2026-09-09 — M1 Journeys 5 & 7 + Care linkage

- **Docs gap #4:** `m1-profile-get-abha-card` documents no 200 body or
  content-type. Plug passes upstream `Content-Type` through verbatim
  (`abdm/abha/views.py::_PatientAbhaBinary`). Verify against sandbox once a real X-token exists.
- **Docs gap #5:** `m1-login-verify` says the returned `token` is a *T-token* consumed by
  `m1-login-select-account` with a `Bearer ` prefix. Not verified against sandbox yet.
- **Care core caveat:** `PatientIdentifier` rows are not what the API returns. Core reads the
  denormalised `Patient.instance_identifiers` JSON (`care/emr/resources/patient/spec.py:275`),
  which only the patient viewset rebuilds (`care/emr/api/viewsets/patient.py:147,190`). A plug
  writing identifiers must call `patient.build_instance_identifiers()` and persist it, or the
  identifiers silently never show. Done in `abdm/signals.py::link_patient_to_transaction`.
- **Care core caveat:** auto-maintained identifier configs are skipped on create
  (`viewsets/patient.py:138`), so the ABHA cannot be sent as an identifier from the form. Hence
  the `extensions.abdm.txn_id` → `post_save` design (ADR-004 amendment).

## 2026-09-10 — M1 login variants, token refresh, Find by ABHA

- **Docs conflict #6:** `m1-token-refresh` — the curl example sends `R-token: <token>` bare.
  The old header table said to use a token prefix.
  Plug tries the prefixed form first and retries bare on `AS-1358`/`AS-1360`.
  Code: `abdm/abha/client.py::refresh_token`.
  Confirm against sandbox and drop the fallback.
  2026-09-10 live re-check: the page still sends `R-token: <R_TOKEN>`.
  The header table says "refresh token" and gives no prefix.
  The 200 schema still has `token`, `expiresIn`, `refreshToken`, and `refreshExpiresIn`.
  Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m1/endpoints/m1-token-refresh/index.md.
- **Docs gap #7:** `m1-login-request-otp` lists `loginHint: aadhaar` in the description but has no
  request example for it; `otpSystem` example for `m1-phr-request-otp` is the placeholder
  `"abdm, aadhaar"`. Plug sends `aadhaar` / `abdm` singly. Hypothesis until observed.
- **Docs gap #8:** whether non-mobile `login/verify` responses (X-token directly) also carry an
  `accounts[]` entry is unstated; `service.login_verify` decides X- vs T-token from the body
  (`refreshToken`/`expiresIn` present and ≤1 account ⇒ X-token), not from the hint.
- **Product decision:** Find by ABHA does not use core's `?identifier=` search. The ABHA is
  verified by ABDM (OTP) before Care looks it up, so a mistyped/borrowed card cannot open the
  wrong record. Lookup is plug-side via `AbhaNumberIdentifier.find_patient` (then address).
- **Care host contract used:** `PatientSearchActions` slot (`care_fe/src/pluginTypes.ts:73-76`,
  mounted `PatientIndex.tsx:259-266`, host passes a primary-button `className`); registration
  route `/facility/:facilityId/patient/create` (`Routers/routes/PatientRoutes.tsx:86`) reads
  query params with raviger `useQueryParams` (`PatientRegistration.tsx:92`) — plug adds
  `abdm_txn`. Form fields prefilled: `name`, `date_of_birth`, `age_or_dob`, `gender`,
  `phone_number`, `address`, `pincode` (numeric) — `PatientRegistration.tsx:530,796,859`.

## 2026-09-10 — M2 research

- `/docs/hiecm/v3/api/m2/apis/index.md` returns 404. The M1 docs have an `apis` page. M2 does not.
- `m2-generate-link-token` conflicts with `/concepts/linking` and `/milestones/m2`. The concept and milestone pages say to store a per-patient link token for 6 months. The endpoint page says the token is short-lived and must be used immediately before the link call.
- `m2-on-health-information-request` names the body only in prose. The page has no `Body` section. It does not give field names for consent ID, date range, data push URL, or key material.
- The M2 endpoint pages for `m2-hip-health-information-on-request`, `m2-hip-data-flow-notify`, and `m2-consent-hip-on-notify` omit `REQUEST-ID`, `TIMESTAMP`, and `X-CM-ID` headers. Other M2 pages and the skill header table present these as module headers.
- Callback authenticity is incomplete. `/concepts/callback-authenticity` says ABDM signs callbacks and publishes JWKS. It also says the header that carries the signed token is not published. M2 callback endpoint pages instead show `Authorization` prose that looks like an outbound gateway bearer token.
- Callback paths conflict. The `m2-on-discovery-request` endpoint page says `/api/v3/hip/patient/care-context/discover`. The `m2-on-discover-care-contexts` page says the gateway sends discovery to `{bridgeUrl}/v0.5/care-contexts/discover`.
- Callback paths conflict for user link too. The inbound pages say `/api/v3/hip/link/care-context/init` and `/api/v3/hip/link/care-context/confirm`. The response pages say the gateway sends the earlier requests to `{bridgeUrl}/v0.5/links/link/init` and `{bridgeUrl}/v0.5/links/link/confirm`.
- The callback endpoint curl examples are misleading for bridge-hosted paths. Pages such as `m2-on-health-information-request` render `https://dev.abdm.gov.in/api/api/v3/...`. The text says the paths are bridge-relative, not ABDM-hosted.
- The HIP consent callback has no per-endpoint page in the 20 M2 endpoint list. `m2-consent-hip-on-notify` says the gateway sends it to `{bridgeUrl}/v0.5/consents/hip/notify`, and it says the callback contains consent details, care contexts, HI types, date range, and signature. It does not give the request schema.
- The docs do not say how a HIP must create, deliver, store, or validate the 6-digit token for user-initiated link init and confirm. The pages only show `confirmation.token` and the link metadata response.
- The docs do not say the retry count, backoff, or timeout for discovery, link init, or link confirm callbacks. The endpoint pages say to treat them as unknown.
- `/concepts/fhir` says an HMIS must implement 8 record types and includes `Invoice`. MCP `list_fhir_profiles` returns 7 record profiles plus `DocumentBundle`. MCP `get_fhir_profile` says `Invoice not found`.
- `/concepts/fhir` says the 8 record-type names and HI type codes are paired from multiple places, not from 1 published table. The page says `Invoice` appears only in an M2 error message and must be checked before use.
- `gateway-register-bridge-services` has a host conflict. The prose says base URL `https://apihspsbx.abdm.gov.in`, while the curl example uses `https://dev.abdm.gov.in/v4/int/v1/bridges/MutipleHRPAddUpdateServices`.
- The docs do not say whether the value for `X-HIP-ID` must be `HRP.bridgeId`, gateway service `serviceId`, or `notification.hip.id`. M2 pages only call it the HIP identifier.

## 2026-09-10 — M2 steps 1-2 build

- `https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/callback-authenticity/index.md`
  says callback authenticity uses gateway JWKS and RS256.
  It does not say which header carries the signed token.
  The code uses `Authorization` by default because callback pages show it.
  Verification fails closed.
- `https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m2/endpoints/m2-on-discovery-request/index.md`,
  `m2-on-link-init`, `m2-on-link-confirm`, and `m2-on-health-information-request`
  state only the accepted status.
  They do not say whether the callback ack body must be `{}` or another shape.
  The receiver returns `202 {}` after signature success.
- `https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md`
  does not list `REQUEST-ID`, `TIMESTAMP`, or `X-CM-ID` headers.
  Other gateway pages require them.
  The outbound helper sends them.
- `https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md`
  has a host conflict.
  The prose says `https://apihspsbx.abdm.gov.in`.
  The curl example uses `https://dev.abdm.gov.in/v4/int/v1/bridges/MutipleHRPAddUpdateServices`.
  The code uses the configured gateway URL and the curl path.
- `https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md`
  names `facilityId`, `facilityName`, `HRP.bridgeId`, `HRP.hipName`, `HRP.type`, and `HRP.active`.
  It does not name `serviceId` or `hip.id`.
  `gateway-get-bridge-service-by-id` returns `serviceId`.
  M2 pages require `X-HIP-ID`.
- `https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-get-gateway-certs/index.md`
  shows a placeholder JWKS response.
  It does not give a captured sandbox response.
  The code validates only the required `keys` array until sandbox confirms the shape.
