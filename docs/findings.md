# Findings about the docs site (for the documentation team)

This file is a register. Each finding has 1 row: an ID, the date it was raised, a status, the
statement, and the URL that should have answered the question. Statuses:

- **Open** — the docs still do not answer it.
- **Resolved** — the docs now answer it, or the sandbox settled it. The row says how and when.
- **Positive** — the docs were right and the sandbox agreed.
- **Withdrawn** — the entry was a design question for this plug, not a docs gap.

Scrubbed 2026-09-15 against the live site (docs mirror rebuilt the same day). Duplicates were merged
and 3 entries were corrected. The pre-scrub file is kept in the session archive, not in the repo.
Base URL for every source: `https://abdm-docs.dev.eka.care/docs/hiecm/v3/`.

## A. Site and tooling

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| A1 | 2026-09-09 | Resolved 2026-09-15 | `/getting-started/index.md` and `build-with-ai/index.md` rendered MDX components as raw JSX (`<SandboxAction>`). The live pages now render plain links. | `getting-started`, `getting-started/build-with-ai` |
| A2 | 2026-09-09 | Open | `<url>.md` returns 404; only `<url>/index.md` works. `llms.txt` still says "add `.md` to any link". | `/llms.txt` |
| A3 | 2026-09-09 | Open | `/reference/hiecm-*` pages are JS-only. MCP `get_operation` covers them. | `/reference/hiecm-m1` |
| A4 | 2026-09-09 | Open | MCP `get_operation gateway_sessions_create` returns unresolved `$ref`s. Operation ids differ between MCP (`gateway_sessions_create`) and URLs (`gateway-sessions-create`). | MCP `get_operation` |
| A5 | 2026-09-09 | Open | `catalogue_info`: 311 of 319 atoms are `unverified`. | MCP `catalogue_info` |
| A6 | 2026-09-10 | Open | `/api/m2/apis` does not exist. M1 has an `apis` conventions page; M2 does not. | `api/m2` |
| A7 | 2026-09-14 | Open | The docs give no scope words ("instance level", "facility level") for configuration fields. A multi-facility HMIS derives each scope from the shape of the call. The 2026-09-15 update added "one bridge, many facilities" prose, but no field-by-field table. | `getting-started/sandbox`, `concepts/how-it-fits#one-bridge-many-facilities` |
| A8 | 2026-09-15 | Positive | `build-it-well` (new page) documents the 4 error shapes, the "format vs not-found" split, the ABHA number plaintext `NN-NNNN-NNNN-NNNN`, and "Invalid LoginId" (padding) vs "LoginId is invalid" (format). These match the plug's 2026-09-11 sandbox findings. | `getting-started/build-it-well` |
| A9 | 2026-09-15 | Positive | MCP `get_fhir_example`, `get_fhir_profile` and `validate_fhir` were enough to build 3 record types. `validate_fhir` returned 0 findings for the plug's OPConsultation, Prescription and HealthDocumentRecord bundles. | MCP `validate_fhir` |

## B. Gateway and bridge

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| B1 | 2026-09-09 | Positive | The session call built from the endpoint page worked first time (HTTP 200); response keys matched the example. | `api/gateway/endpoints/gateway-sessions-create` |
| B2 | 2026-09-09 | Open | The sessions example shows `expiresIn: 0`. The sandbox returns 1200 (20 minutes). | `api/gateway/endpoints/gateway-sessions-create` |
| B3 | 2026-09-14 | Open | No endpoint refreshes the gateway session token. The response carries `refreshToken` and `refreshExpiresIn`, but no call consumes them. `m1-token-refresh` is the ABHA user token. The plug creates a new session on expiry. | `gateway-sessions-create`, `api/m1/endpoints/m1-token-refresh` |
| B4 | 2026-09-09 | Open | `gateway-update-bridge-url` documents `200 {"message"}`. The sandbox returned **HTTP 202 with an empty body** for a valid PATCH. | `api/gateway/endpoints/gateway-update-bridge-url` |
| B5 | 2026-09-09 | Open in part | Whether the bridge `url` may carry a path prefix is unstated. The sandbox accepted `https://care-abdm-sbx.rithviknishad.dev/api/abdm` and `gateway-list-bridge-services` returns it as the bridge URL. **Whether the gateway delivers callbacks to that URL with the prefix is not yet observed**: 3 accepted `m2-generate-link-token` calls on 2026-09-15 produced no callback on `{bridgeUrl}/v3/hip/token/on-generate-token` within 6 to 70 minutes. | `gateway-update-bridge-url` |
| B6 | 2026-09-14 | Positive | The bridge URL is 1 per integrator, never per facility. The 2026-09-15 update says it in words: "One URL covers your whole integration ... It belongs to your bridge, never to a facility". The plug's earlier per-facility bridge URL input was a design over-reach, since removed. | `getting-started/sandbox` |
| B7 | 2026-09-10 | Resolved 2026-09-14 (sandbox) | `gateway-register-bridge-services` names 4 hosts across prose and curl: `apihspsbx.abdm.gov.in`, `dev.abdm.gov.in`, `facilitysbx.abdm.gov.in`, `abhasbx.abdm.gov.in`. Observed: the gateway host answers HTTP 503 "Please make a valid request."; `apihspsbx` answers HTTP 200. The prose host is right; the curl is wrong. | `api/gateway/endpoints/gateway-register-bridge-services` |
| B8 | 2026-09-10 | Open | `gateway-register-bridge-services` lists no `REQUEST-ID`, `TIMESTAMP` or `X-CM-ID` headers. Other gateway pages require them. The plug sends them. | same |
| B9 | 2026-09-14 | Open | The HSP Registry reports a failure with **HTTP 200** and an error envelope: `[{"error": {"code": "2500", "message": "Provided facility name is not matched with registered name"}}]`. The page does not warn about this. Error `2500` is absent from the error pages and collides with the documented `ABDM-2500` meanings. | same; `reference/error-codes` |
| B10 | 2026-09-14 | Open | The HSP Registry uses a 2nd error envelope: `{"code": "HIS-400", "message", "details": [{"code": "HIS-1070", "message": "Bridge ID cannot be blank", "attribute": {"key", "value"}}]}`. The error-codes page shows only `{"error": {"code", "message"}}`. | `reference/error-codes` |
| B11 | 2026-09-14 | Open | `gateway-list-bridge-services` does not say which host serves it. Both `dev.abdm.gov.in` and `apihspsbx.abdm.gov.in` answer HTTP 200. | `api/gateway/endpoints/gateway-list-bridge-services` |
| B12 | 2026-09-14 | Open | The docs do not say how a bridge id is issued. `gateway-list-bridge-services` returns `bridge.id` for an existing bridge; HRP registration needs it as `HRP.bridgeId`. | same |
| B13 | 2026-09-14 | Open | The docs do not say how a user learns a `serviceId`. `gateway-get-bridge-service-by-id` needs it as a path parameter and returns it. The list page shows the services array as a placeholder. | `api/gateway/endpoints/gateway-get-bridge-service-by-id` |
| B14 | 2026-09-10 | Resolved 2026-09-15 (sandbox) | `gateway-get-gateway-certs` shows a placeholder JWKS and lists no bearer token. Observed: **401 without `Authorization`, 200 with the gateway session token.** The set holds 2 RSA keys, `alg` RS256 (kid `AlRb5W…`) and RS512 (kid `oc-l6O…`), each with `x5c`, `x5t`, `x5t2`, `use`. The RS256 kid is the one that signs the gateway's own session tokens (`iss` `https://dev.abdm.gov.in/auth/realms/central-registry`). `gateway-get-oidc-config` also needs the token and returns `jwks_uri` = the certs URL. The page should state the bearer requirement and show a captured key. | `api/gateway/endpoints/gateway-get-gateway-certs`, `gateway-get-oidc-config` |
| B15 | 2026-09-14 | Open | HFR search by `facilityId` exists but the path is not published, so an HMIS cannot prefill the registered facility name. The user must type the exact HFR name. | `api/m4/undocumented` |
| B16 | 2026-09-14 | Open | The docs do not say whether `facilityName` or `hipName` may contain spaces. The bridge-linkage table allows `-_.(),/` in the name and "no special characters" in the HIP name. The plug allows spaces in both. | `api/m4/undocumented` |
| B18 | 2026-09-15 | Open | The real `gateway-list-bridge-services` service row is `{"id": "IN1410000232_1", "name": "FACILITY WITH P", "types": ["HIP", "HIU"], "active": true}`. The docs give `serviceId`, `isHip`, `isHiu`, `registerTime` (on `gateway-get-bridge-service-by-id`) and a placeholder list. Two observations for the docs: the service id is `<HFR facility ID>_<n>`, and a service registered with `type: "HIP"` came back with both `HIP` and `HIU`. | `api/gateway/endpoints/gateway-list-bridge-services`, `gateway-get-bridge-service-by-id` |
| B17 | 2026-09-15 | Positive | M4 is optional: "a product that registers its facilities [on the NHPR portal] by hand never builds M4". M2 still needs a facility ID and a linked HIP bridge. This settles the plug's ADR-007 "workaround" as the sanctioned route. | `milestones/m4` |

## C. M1 — ABHA identity

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| C1 | 2026-09-09 | Open | `m1-get-public-certificate` documents `GET /profile/public/certificate`, which returns **404** on the sandbox. The working path is `/v3/profile/public/certificate`, answering `{"publicKey": "<base64 DER SPKI, RSA-4096>"}`. The pages call the key "PEM"; it is base64 DER without armour. | `api/m1/endpoints/m1-get-public-certificate`, `concepts/encryption` |
| C2 | 2026-09-09 | Open | RSA padding: only the encryption atom summary (MCP search) says "OAEP with SHA-1". The page text says "confirm which padding". Sandbox: OAEP-SHA1 reached UIDAI; PKCS1v15 and OAEP-SHA256 returned `400 {"loginId": "Invalid LoginId"}`. State OAEP/SHA-1 + base64 on the page and on every `<RSA_ENCRYPTED_*>` placeholder. | `concepts/encryption` |
| C3 | 2026-09-09 | Resolved 2026-09-15 | ABHA service error shapes (`422 {"error": {...}}` vs flat `400 {"<field>": "<msg>"}`) were undocumented. `build-it-well` now documents the 4 shapes. | `getting-started/build-it-well` |
| C4 | 2026-09-09 | Resolved 2026-09-09 (sandbox) | `m1-encrypt-value` body "not described": it is `{"encryptedData": "<base64>"}` and returns `{"encryptedData"}`. | `api/m1/endpoints/m1-encrypt-value` |
| C5 | 2026-09-09 | Open | `X-CM-ID` is documented for gateway calls. ABHA-service calls work without it. Not tested whether sending it hurts. | `api/m1/apis` |
| C6 | 2026-09-09 | Open | `m1-profile-get-abha-card` documents no 200 body or content type ("Send the call with Try it"). The plug passes the upstream `Content-Type` through. | `api/m1/endpoints/m1-profile-get-abha-card` |
| C7 | 2026-09-09 | Open | `m1-login-verify` says the returned `token` is a T-token that `m1-login-select-account` consumes with a `Bearer` prefix. Sandbox-confirmed for mobile login on 2026-09-09; the page still gives no schema for the X-token case. | `api/m1/endpoints/m1-login-verify` |
| C8 | 2026-09-10 | Resolved 2026-09-15 | `m1-token-refresh`: the curl sent `R-token` bare while a header table said "prefixed". The live page now describes `R-token` as "The refresh token" with a bare value in the curl. Not yet run against the sandbox; the plug now sends the bare form first and falls back to the prefixed form. | `api/m1/endpoints/m1-token-refresh` |
| C9 | 2026-09-10 | Resolved 2026-09-15 | `loginHint: aadhaar` had no request example and `otpSystem` showed the placeholder `"abdm, aadhaar"`. The page now states the plaintext shape per hint (12 digits for Aadhaar). The `otpSystem` placeholder remains on `m1-phr-request-otp`. | `api/m1/endpoints/m1-login-request-otp`, `m1-phr-request-otp` |
| C10 | 2026-09-10 | Open | Whether a non-mobile `login/verify` response (X-token directly) also carries `accounts[]` is unstated. The plug decides X- vs T-token from the body fields, not the hint. | `api/m1/endpoints/m1-login-verify` |
| C11 | 2026-09-11 | Resolved 2026-09-15 | An ABHA number sent as 14 bare digits fails with `400 {"loginId": "LoginId is invalid"}`; `NN-NNNN-NNNN-NNNN` is accepted. `build-it-well` and `m1-login-request-otp` now state the dashed shape. | `getting-started/build-it-well` |
| C12 | 2026-09-15 | Positive | The M1 page was rewritten after NHA's review of 11 September 2026: Aadhaar OTP is the only mandatory creation route for a private integrator; face and biometric are optional; demographic auth and child ABHA are not for private integrators; enrol-by-document is "not recommended". Login token lifetimes are now stated (X-token 1800 s, R-token 1296000 s). | `milestones/m1` |
| C13 | 2026-09-09 | Withdrawn | "No identifier-system URI is prescribed for ABHA number / ABHA address as FHIR identifiers." The plug chose its own systems (`abdm/abha-number`, `abdm/abha-address`, ADR-004). The NRCES Patient profile is the place to look; not an HIE-CM docs gap. | — |

## D. M1 — Scan and Share

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| D1 | 2026-09-14 | Open | The counter QR code content is not published. The pages say only "a URL with two parameters: your HIP id and a counter context". No host, path or parameter names. The plug reads the format from `ABDM_SHARE_QR_URL_TEMPLATE`. | `milestones/m1#a-patient-shares-their-profile-at-your-counter` |
| D2 | 2026-09-14 | Open | `m1-on-share-acknowledgement` has 2 bodies. The M1 page: `{acknowledgement: {status, abhaAddress, profile: {context, tokenNumber}, error}}` on `dev.abdm.gov.in/api/hiecm`. The PHR page `onpatientshare` adds `profile.expiry` and `response.requestId` and uses `phrsbx.abdm.gov.in`. The `m1-receive-patient-share` curl shows `abhasbx.../patient-share/v3/share`, which is the HIP's own bridge path. The plug sends the union on the gateway host. | `api/m1/endpoints/m1-on-share-acknowledgement`, `m1-receive-patient-share` |
| D3 | 2026-09-14 | Open | The token number format is not specified (examples show `TKN-0042`). Two time limits are given as untested (60 minutes between tokens; token valid 30 minutes). The plug uses `<context>-<nnn>` per counter per day and sends `expiry: "1800"`. | `milestones/p2#scan-and-share-at-a-facility` |
| D4 | 2026-09-14 | Open | The callback signature for `patient-share/v3/share` is described only as `Authorization: <bearer>`. The plug verifies it with the gateway JWKS like every other callback. No real gateway callback observed yet. | `api/m1/endpoints/m1-receive-patient-share` |

## E. M2 — headers, paths, callbacks

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| E1 | 2026-09-10 | Resolved 2026-09-15 | `X-HIP-ID` scope. The docs did not say which value it carries or that it identifies the facility on an inbound callback. The live pages now say: "This is per facility, and it is what a callback arriving at your one bridge URL is routed on." The docs team confirmed on 2026-09-14 that HIP ID = HFR facility ID. **Still open in part:** no page says in words that `X-HIP-ID` equals the HFR `facilityId`; `m2-link-care-context-notify` shows `hip.id` as `HIP_SERVICE_ID`. Experiment 2026-09-15: `m2-generate-link-token` was accepted (202) both with `X-HIP-ID: IN1410000232` (HFR id) and with `IN1410000232_1` (the gateway service id); neither produced a callback in the observed window, so the sandbox has not settled it. The plug sends the HFR id and accepts both forms on inbound callbacks. | `reference/authentication`, `api/m2/endpoints/m2-hip-link-care-context`, `m2-link-care-context-notify` |
| E2 | 2026-09-10 | Open | Callback authenticity: the gateway signs callbacks (JWKS, RS256) but "which header carries the signed token is not published". Callback pages show `Authorization` prose that reads like the outbound gateway bearer. The plug reads the configured header first, then any JWT-shaped header, verifies against the JWKS (RS256 or RS512 as the JWK declares) and records the header name on the row (`signature_header`). 2026-09-15 17:37: a POST reached `/api/abdm/v3/hip/token/on-generate-token` (runserver log) but the receiver crashed on the JWKS fetch (B14) and the row rolled back (J6); the header name is still unobserved. | `concepts/callback-authenticity` |
| E3 | 2026-09-10 | Open | Callback paths conflict. Discovery: `/api/v3/hip/patient/care-context/discover` (inbound page) vs `{bridgeUrl}/v0.5/care-contexts/discover` (on-discover page). Link init/confirm: `/api/v3/hip/link/care-context/{init,confirm}` vs `{bridgeUrl}/v0.5/links/link/{init,confirm}`. Health information: `/api/v3/hip/health-information/request` vs `{bridgeUrl}/v0.5/health-information/hip/request`. Consent: `{bridgeUrl}/v0.5/consents/hip/notify` (M2) vs `/api/v3/consent/request/hip/notify` (M3 page). The plug serves every variant. | `api/m2/endpoints/m2-on-discovery-request`, `m2-on-discover-care-contexts`, `m2-on-link-init`, `m2-receive-link-init`, `m2-on-link-confirm`, `m2-receive-link-confirm`, `m2-on-health-information-request`, `m2-hip-health-information-on-request`, `m2-consent-hip-on-notify`, `api/m3/endpoints/m3-on-consent-request-notify-hip` |
| E4 | 2026-09-10 | Open | Callback curl examples render bridge-relative paths on the ABDM host, e.g. `https://dev.abdm.gov.in/api/api/v3/hip/...`. | `api/m2/endpoints/m2-on-health-information-request` |
| E5 | 2026-09-10 | Open | `m2-hip-health-information-on-request`, `m2-hip-data-flow-notify` and `m2-consent-hip-on-notify` list only `Authorization`. Other M2 pages require `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID`. The plug sends them. | those 3 pages |
| E6 | 2026-09-10 | Open | Retry count, backoff and timeout for inbound discovery, link init and link confirm are "not stated in NHA's material". No page gives a callback timeout for the result legs either. | `m2-on-discovery-request`, `m2-on-link-init`, `m2-on-link-confirm` |
| E7 | 2026-09-10 | Open | Ack body for inbound callbacks: the pages say "202" or "200" and "a 202 carrying the wrong body is still a failure", but do not say what the right body is. The plug returns `202 {}`. | same |
| E8 | 2026-09-15 | Open | `milestones/m2` says "Four callbacks name a path and carry no documented payload: discovery, link init, link confirm, and consent notify. Do not assume a body." The endpoint pages `m2-on-discovery-request`, `m2-on-link-init` and `m2-on-link-confirm` do list body fields. The 2 statements contradict each other. | `milestones/m2`, the 3 pages |
| E9 | 2026-09-15 | Open | `m2-sms-deep-link-notify` lists no `X-HIP-ID` header, but the body carries `notification.hip.id`, and the page does not say whether the body `requestId` must equal the `REQUEST-ID` header. The plug sends the same UUID in both. | `api/m2/endpoints/m2-sms-deep-link-notify` |

## F. M2 — link token and care contexts

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| F1 | 2026-09-10 | Open | Link token lifetime conflict. `concepts/linking`, `milestones/m2`, the glossary and `how-it-fits` say "valid six months, stored at registration". `m2-generate-link-token` says "short-lived ... must be called immediately before the linking call, tokens expire quickly". The 2026-09-15 update strengthened the 6-month wording and left the endpoint page unchanged. | `concepts/linking`, `api/m2/endpoints/m2-generate-link-token` |
| F2 | 2026-09-15 | Open | The link token is a JWT ("validate it with a tool such as JWT.io") but its claims are not published. The plug reads `exp` when present and otherwise assumes 6 months. | `concepts/linking` |
| F3 | 2026-09-15 | Positive | "A care context is linked when the callback says so, not when the call returns" (whats-new 2026-09-10). The plug keys `linked` on `/v3/link/on_carecontext`. | `whats-new/2026-09-10`, `api/m2/endpoints/m2-on-carecontext-result` |
| F4 | 2026-09-15 | Open | `m2-on-carecontext-result` keeps `status` as free text ("one observed value, `invalid   [invalid request]`"). No success value is named. The plug treats "no `error` block" as success and `ABDM-1056` (already linked) as success. | `api/m2/endpoints/m2-on-carecontext-result`, `api/m2/errors` |
| F5 | 2026-09-10 | Open | `m2-generate-link-token` types `abhaNumber` as integer; `m2-hip-link-care-context` types it as string. | both pages |

## G. M2 — discovery and user-initiated linking

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| G1 | 2026-09-15 | Open | `patient.verifiedIdentifiers[]` and `unverifiedIdentifiers[]` are typed `object[]` with no element shape. The plug reads `{type, value}` pairs. | `api/m2/endpoints/m2-on-discovery-request` |
| G2 | 2026-09-15 | Open | The docs do not say how to answer discovery when no patient matches, or when several match. The plug sends `patient: []`. `ABDM-1012 no records found against ABHA address` exists in the error table but no page ties it to this reply. | `m2-on-discover-care-contexts`, `api/m2/errors` |
| G3 | 2026-09-10 | Open | The docs do not say how the HIP must create, deliver, store or validate the 6-digit OTP for link init and confirm. Only `confirmation.token` and the `link.meta` fields appear. The plug sends its own OTP over Care's SMS backend and stores a hash. | `m2-receive-link-confirm`, `m2-on-link-confirm` |
| G4 | 2026-09-15 | Open | `m2-receive-link-init` and `m2-receive-link-confirm` list no `error` field. The docs do not say how the HIP reports "no such patient" or "wrong OTP". The plug adds `error {code, message}` like every other callback answer. | those 2 pages |

## H. M2 — consent and data transfer

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| H1 | 2026-09-10 | Resolved in part 2026-09-15 | The HIP consent notification has no M2 endpoint page and no body on `m2-consent-hip-on-notify`. **The body is published** on the M3 page `m3-on-consent-request-notify-hip` (`status`, `consentId`, `consentDetail{...}`, `signature`, `grantAcknowledgement`). The M2 pages do not link to it. | `api/m2/endpoints/m2-consent-hip-on-notify`, `api/m3/endpoints/m3-on-consent-request-notify-hip` |
| H2 | 2026-09-15 | Open | The consent artefact `signature` is "for validation", but no page gives the algorithm, the signed bytes, or the key. The plug stores it and does not verify it. | `m3-on-consent-request-notify-hip` |
| H3 | 2026-09-10 | Resolved in part 2026-09-15 | `m2-on-health-information-request` has no body section. **The body is inferable** from `m3-hiu-health-information-request` (`hiRequest{consent{id}, dateRange{from,to}, dataPushUrl, keyMaterial}`) and `p2-as-record-on-share` (`transactionId`). The HIP page should carry it. | `api/m2/endpoints/m2-on-health-information-request`, `api/m3/endpoints/m3-hiu-health-information-request`, `api/p2/endpoints/p2-as-record-on-share` |
| H4 | 2026-09-15 | Resolved in part 2026-09-15 | The data-push body the HIP must send is not on any M2 page. It is on the M3 receive page `m3-on-health-information-transfer`: `{pageNumber, pageCount, transactionId, entries[{content, media, checksum, careContextReference}], keyMaterial}`. Link it from `concepts/data-flow`. | `api/m3/endpoints/m3-on-health-information-transfer` |
| H5 | 2026-09-15 | Open | Encryption details the docs leave open: the HKDF hash (the plug uses SHA-256) and `info` (empty); the `content` encoding (the plug sends base64 of ciphertext + GCM tag); `keyValue` encoding (the M3 page says "32 bytes"; the plug also accepts DER). "Sign with its long-term private key" has no field in the push body. | `concepts/data-flow`, `m3-on-health-information-transfer` |
| H6 | 2026-09-10 | Open | `/concepts/fhir` says an HMIS must implement 8 record types including `Invoice`. MCP `list_fhir_profiles` returns 7 record profiles plus `DocumentBundle`; `get_fhir_profile Invoice` says not found. `consent.md` omits `Invoice` from the HI type list. | `concepts/fhir`, `concepts/consent`, MCP |
| H7 | 2026-09-15 | Open | The docs do not say which records a HIP must include when the consent names a date range: records dated in the range, or records of care contexts whose visit falls in the range. The plug filters by the encounter start date. | `concepts/data-flow` |

## I. FHIR mapping gaps (CARE data → NRCES profiles)

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| I1 | 2026-09-15 | Open | CARE `Condition.category` has no "chief complaint" value. The plug maps `problem_list_item` to the OPConsultRecord "Chief complaints" section and other categories to "Medical history". | `care/emr/resources/condition/spec.py`; MCP `get_fhir_profile OPConsultation` |
| I2 | 2026-09-15 | Open | `HealthDocumentRecord` attachments: the plug inlines file bytes when the object store answers; otherwise it falls back to a signed URL that expires in 1 hour. The docs do not say whether `attachment.url` is acceptable. | `concepts/fhir` |
| I3 | 2026-09-15 | Open | NRCES `Practitioner` examples carry an HPR identifier. CARE users have none. The plug sends the CARE user id as the identifier. The docs do not say whether HPR is required for a valid bundle. | MCP `get_fhir_example` |
| I4 | 2026-09-15 | Open | No CARE model exists for `Immunization`, `Procedure` or wellness vitals grouping. `ImmunizationRecord`, `WellnessRecord`, `DiagnosticReport`, `DischargeSummary` and `Invoice` builders are deferred (ADR-011). | — |

## J. Care core caveats (for the plug, not for the docs team)

| ID | Raised | Status | Finding | Source |
|---|---|---|---|---|
| J1 | 2026-09-09 | Handled | `PatientIdentifier` rows are invisible until `Patient.instance_identifiers` is rebuilt; only the patient viewset rebuilds it. The plug calls `patient.build_instance_identifiers()` in `abdm/signals.py`. | `care/emr/resources/patient/spec.py:275`, `care/emr/api/viewsets/patient.py:147,190` |
| J2 | 2026-09-09 | Handled | Auto-maintained identifier configs are dropped from create payloads, so the ABHA cannot arrive as an identifier from the form. Hence `extensions.abdm.txn_id` → `post_save`. | `care/emr/api/viewsets/patient.py:138` |
| J3 | 2026-09-14 | Handled | The desk inbox and the ABHA wizard use `can_create_patient`, which is organisation-scoped, not facility-scoped. | `care/security/authorization/patient.py:87` |
| J4 | 2026-09-15 | Handled | `Encounter.save()` runs for cache-only updates (`sync_organization_cache`). The plug's `post_save` skips saves whose `update_fields` touch neither `status`, `encounter_class` nor `period`. | `care/emr/models/encounter.py` |
| J6 | 2026-09-15 | Handled | Care runs every request in a transaction (`ATOMIC_REQUESTS = True`, `config/settings/base.py:73`). An exception in the callback view rolled back the stored callback row, so a real gateway POST on 2026-09-15 17:37 left no evidence (only a 500 in the runserver log). The receiver now catches everything after the insert: 401 for a bad signature, 503 when the JWKS cannot be read, and the row keeps `signature_error`. | `config/settings/base.py:73` |
| J5 | 2026-09-15 | Handled | Care sends a fixed OTP outside production (`care/emr/api/otp_viewsets/login.py`). The plug uses the same rule for the user-initiated link OTP (`123456` when `IS_PRODUCTION` is false). | `care/emr/api/otp_viewsets/login.py:98` |

## K. Product decisions recorded here (durable)

- 2026-09-10 — Find by ABHA does not use core's `?identifier=` search. ABDM verifies the ABHA by OTP before Care looks it up.
- 2026-09-10 — Care-context reference number = `Encounter.external_id`; display = `<OPD|IPD|class> records for <day>`; discovery matches on verified ABHA address or number only (ADR-008 decisions 2-4).
- 2026-09-14 — `X-HIP-ID` is always the HFR facility ID; the plug derives it and ignores any client-supplied HIP ID.
- 2026-09-15 — The bridge id is read live from the gateway and cached; no snapshot table (ADR-011). The bridge UI is instance-level at `/admin/abdm`, not on a facility page (Rithvik).
- 2026-09-15 — Day-1 record types: OPConsultation, Prescription, HealthDocumentRecord (ADR-011).
