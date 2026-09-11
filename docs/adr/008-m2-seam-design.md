# ADR-008 — M2 seam design

Status: Accepted (Rithvik, 2026-09-10)
Date: 2026-09-10

## Context
M2 makes CARE an HIP for linked care contexts and consented record share. M1 already stores ABHA state on a Patient. M2 adds facility identity, callbacks, link tokens, care context state, FHIR output, and data push jobs. The design must keep ABDM secrets and many-row state in plug tables. It must keep display state in Care extensions. Source facts below come only from the ABDM docs site and local ABDM docs artefacts.

Docs say these facts:

| Fact | Source |
|---|---|
| M2 attaches records to an ABHA address. It has HIP link, SMS deep link, discovery, and data transfer flows. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m2/index.md |
| M2 needs M1 and a valid facility ID with HIP role from M4. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m2/index.md |
| The care context has a reference number and a display name. It must not expose clinical detail. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/linking/index.md |
| One care context maps to 1 OPD visit or 1 IPD admission. Link when the record is ready. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/linking/index.md |
| A link token is per patient and valid for 6 months. The endpoint page also says short-lived. Treat this as a docs conflict. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/linking/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m2/endpoints/m2-generate-link-token/index.md |
| Discovery returns metadata only. Verified identifiers have more weight than unverified identifiers. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/linking/index.md |
| Data push must complete in 20 minutes. Use a background job. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/data-flow/index.md |
| Data push uses ECDH Curve25519, AES-GCM, HKDF, and 32-byte nonces. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/data-flow/index.md |
| FHIR output is FHIR R4 with NRCES profiles. HMIS must implement 8 record types. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/fhir/index.md |
| Callback authenticity uses gateway JWKS and RS256. The callback signature header is not published. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/callback-authenticity/index.md |
| The sandbox needs a public callback URL. M2 and M3 replies arrive as POST callbacks with `REQUEST-ID`. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/getting-started/sandbox/index.md |
| MCP `list_fhir_profiles` returns 7 record profiles and `DocumentBundle`. It does not return `Invoice`. | https://abdm-docs-mcp.dev.eka.care/mcp |

## ABDM operation matrix

The bridge URL is `${ABDM_CALLBACK_BASE_URL}/api/abdm` per ADR-005. A callback path that starts with `/api/...` therefore lands at `/api/abdm/api/...` in Care. The docs also name some older `/v0.5/...` callback paths inside endpoint prose. The receiver must accept both until the sandbox proves the one true path.

| Operation | Direction | ABDM URL or callback path | Required headers from page | Body fields from page | Correlation | Answer or result | Timing |
|---|---|---|---|---|---|---|---|
| `m2-generate-link-token` | Care calls gateway | `POST /hiecm/v3/token/generate-token` | `Authorization`, `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID`, `X-HIP-ID` | `abhaNumber`, `abhaAddress`, `name`, `gender`, `yearOfBirth` | header `REQUEST-ID` | `m2-on-generate-token-result` | Token validity conflict. |
| `m2-on-generate-token-result` | Gateway calls Care | `POST /v3/hip/token/on-generate-token` | `REQUEST-ID`, `TIMESTAMP`, `X-HIP-ID`; auth header name not settled | `abhaAddress`, `linkToken`, `error`, `response.requestId` | `response.requestId` | Store token or error. | Callback timeout not published. |
| `m2-hip-link-care-context` | Care calls gateway | `POST /hiecm/hip/v3/link/carecontext` | `Authorization`, `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID`, `X-HIP-ID`, `X-Link-Token` | `abhaNumber`, `abhaAddress`, `patient[].referenceNumber`, `patient[].display`, `patient[].careContexts`, `patient[].hiType`, `patient[].count` | header `REQUEST-ID` | `m2-on-carecontext-result` | No timeout published. |
| `m2-on-carecontext-result` | Gateway calls Care | `POST /v3/link/on_carecontext` | `REQUEST-ID`, `TIMESTAMP`, `X-HIP-ID`; auth header name not settled | `abhaAddress`, `status`, `error`, `response.requestId` | `response.requestId` | Mark link success or error. | No timeout published. |
| `m2-link-care-context-notify` | Care calls gateway | `POST /hiecm/hip/v3/link/context/notify` | `Authorization`, `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID`, `X-HIP-ID` | `notification.patient.id`, `notification.careContext.*`, `notification.hiTypes`, `notification.date`, `notification.hip.*` | header `REQUEST-ID` | `m2-on-context-notify-result` | No timeout published. |
| `m2-on-context-notify-result` | Gateway calls Care | `POST /v3/links/context/on-notify` | `REQUEST-ID`, `TIMESTAMP`, `X-HIP-ID`; auth header name not settled | `acknowledgement.status`, `error`, `response.requestId` | `response.requestId` | Mark notify success or error. | No timeout published. |
| `m2-sms-deep-link-notify` | Care calls gateway | `POST /hiecm/hip/v3/link/patient/links/sms/notify2` | `Authorization`, `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID` | `requestId`, `timestamp`, `notification.phoneNo`, `notification.hip.name`, `notification.hip.id` | header `REQUEST-ID` and body `requestId` | `m2-on-sms-notify-result` | No timeout published. |
| `m2-on-sms-notify-result` | Gateway calls Care | `POST /v3/patients/sms/on-notify` | `REQUEST-ID`, `TIMESTAMP`, `X-HIP-ID`; auth header name not settled | `acknowledgement.status`, `error`, `response.requestId` | `response.requestId` | Mark SMS success or error. | No timeout published. |
| `m2-on-discovery-request` | Gateway calls Care | `POST /api/v3/hip/patient/care-context/discover`; prose also says `/v0.5/care-contexts/discover` | `REQUEST-ID`, `TIMESTAMP`, `X-HIP-ID`; auth header name not settled | `transactionId`, `patient.id`, `patient.verifiedIdentifiers`, `patient.unverifiedIdentifiers`, `patient.name`, `patient.gender`, `patient.yearOfBirth` | header `REQUEST-ID` and `transactionId` | `m2-on-discover-care-contexts` | Retry and timeout not stated. |
| `m2-on-discover-care-contexts` | Care calls gateway | `POST /hiecm/user-initiated-linking/v3/patient/care-context/on-discover` | `Authorization`, `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID` | `transactionId`, `patient[]`, `response.requestId` | body `response.requestId` echoes callback `REQUEST-ID` | Gateway accepts context list. | No timeout published. |
| `m2-on-link-init` | Gateway calls Care | `POST /api/v3/hip/link/care-context/init`; prose also says `/v0.5/links/link/init` | `REQUEST-ID`, `TIMESTAMP`, `X-HIP-ID`; auth header name not settled | `transactionId`, `abhaAddress`, `patient[]` | header `REQUEST-ID` and `transactionId` | `m2-receive-link-init` | Retry and timeout not stated. |
| `m2-receive-link-init` | Care calls gateway | `POST /hiecm/user-initiated-linking/v3/link/care-context/on-init` | `Authorization`, `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID` | `transactionId`, `link.referenceNumber`, `link.authenticationType`, `link.meta.*`, `response.requestId` | body `response.requestId` echoes callback `REQUEST-ID` | Gateway asks patient for token. | No timeout published. |
| `m2-on-link-confirm` | Gateway calls Care | `POST /api/v3/hip/link/care-context/confirm`; prose also says `/v0.5/links/link/confirm` | `REQUEST-ID`, `TIMESTAMP`, `X-HIP-ID`; auth header name not settled | `confirmation.token`, `confirmation.linkRefNumber` | header `REQUEST-ID` | `m2-receive-link-confirm` | Retry and timeout not stated. |
| `m2-receive-link-confirm` | Care calls gateway | `POST /hiecm/user-initiated-linking/v3/link/care-context/on-confirm` | `Authorization`, `REQUEST-ID`, `TIMESTAMP`, `X-CM-ID` | `patient[]`, `response.requestId` | body `response.requestId` echoes callback `REQUEST-ID` | Gateway accepts link result. | No timeout published. |
| `m2-consent-hip-on-notify` | Care calls gateway | `POST /hiecm/consent/v3/request/hip/on-notify` | `Authorization` only on page | `acknowledgement.status`, `acknowledgement.consentId`, `response.requestId` | body `response.requestId` echoes consent callback | Gateway accepts consent ack. | No timeout published. |
| HIP consent callback | Gateway calls Care | Prose says `POST /v0.5/consents/hip/notify`; no endpoint page found | Header and body not fully listed | Consent detail, care contexts, HI types, date range, signature are named in prose | header `REQUEST-ID` if present | `m2-consent-hip-on-notify` | No timeout published. |
| `m2-on-health-information-request` | Gateway calls Care | `POST /api/v3/hip/health-information/request`; prose also says `/v0.5/health-information/hip/request` | Auth header only on page; header name not settled | Page omits the body. Prose says consent id, date range, data push URL, key material. | header `REQUEST-ID` if present; `transactionId` if present | `m2-hip-health-information-on-request`, data push, then notify | 20 minutes for data push. |
| `m2-hip-health-information-on-request` | Care calls gateway | `POST /hiecm/data-flow/v3/health-information/hip/on-request` | `Authorization` only on page | `hiRequest.transactionId`, `hiRequest.sessionStatus`, `response.requestId` | `response.requestId` echoes callback `REQUEST-ID` | Gateway accepts ack. | Immediate ack. |
| Data push to HIU | Care calls HIU URL | The request supplies `dataPushUrl`; endpoint page is not the HIP call | Request body shape is not on M2 HIP page | Encrypted FHIR bundles plus HIP public key and nonce per concept page | `transactionId` | HIU receives encrypted records. | 20 minutes. |
| `m2-hip-data-flow-notify` | Care calls gateway | `POST /hiecm/data-flow/v3/health-information/notify` | `Authorization` only on page | `notification.consentId`, `transactionId`, `doneAt`, `notifier`, `statusNotification.*` | body `transactionId` | Gateway closes transfer. | Within 20 minutes. |
| `m2-on-consent-notify-hiu` | Gateway calls HIU | `POST /v0.5/consents/hiu/notify` | Auth header only on page | No body documented | unknown | M3 only. No Phase 3 route. | No timeout published. |
| `m2-on-data-notification` | HIU receives data push | `POST /api-hiu/data/notification` | Auth header only on page | No body documented | unknown | M3 only. No Phase 3 route. | Acknowledge fast. |

## Route table

### Callback receivers that the gateway can POST

All rows use `AllowAny` plus ABDM callback signature verification. The receiver stores raw data before any verification. It dispatches only after signature success. The HTTP response is fast. Celery does all slow work.

| Care path | Method | Auth | Purpose | ABDM operation | Work mode |
|---|---|---|---|---|---|
| `/api/abdm/v3/hip/token/on-generate-token` | POST | Gateway callback | Store link token result. | `m2-on-generate-token-result` | Sync store, Celery dispatch. |
| `/api/abdm/v3/link/on_carecontext` | POST | Gateway callback | Store HIP link result. | `m2-on-carecontext-result` | Sync store, Celery state update. |
| `/api/abdm/v3/links/context/on-notify` | POST | Gateway callback | Store link-notify result. | `m2-on-context-notify-result` | Sync store, Celery state update. |
| `/api/abdm/v3/patients/sms/on-notify` | POST | Gateway callback | Store SMS result. | `m2-on-sms-notify-result` | Sync store, Celery state update. |
| `/api/abdm/api/v3/hip/patient/care-context/discover` | POST | Gateway callback | Receive discovery. | `m2-on-discovery-request` | Sync store, Celery reply. |
| `/api/abdm/v0.5/care-contexts/discover` | POST | Gateway callback | Compatibility path from endpoint prose. | `m2-on-discovery-request` | Sync store, Celery reply. |
| `/api/abdm/api/v3/hip/link/care-context/init` | POST | Gateway callback | Receive user link init. | `m2-on-link-init` | Sync store, Celery reply. |
| `/api/abdm/v0.5/links/link/init` | POST | Gateway callback | Compatibility path from endpoint prose. | `m2-on-link-init` | Sync store, Celery reply. |
| `/api/abdm/api/v3/hip/link/care-context/confirm` | POST | Gateway callback | Receive user link confirm. | `m2-on-link-confirm` | Sync store, Celery reply. |
| `/api/abdm/v0.5/links/link/confirm` | POST | Gateway callback | Compatibility path from endpoint prose. | `m2-on-link-confirm` | Sync store, Celery reply. |
| `/api/abdm/v0.5/consents/hip/notify` | POST | Gateway callback | Receive HIP consent artefact. | Inbound leg for `m2-consent-hip-on-notify` | Sync store, Celery ack and save. |
| `/api/abdm/api/v3/hip/health-information/request` | POST | Gateway callback | Receive consented record request. | `m2-on-health-information-request` | Sync store, Celery data job. |
| `/api/abdm/v0.5/health-information/hip/request` | POST | Gateway callback | Compatibility path from endpoint prose. | `m2-on-health-information-request` | Sync store, Celery data job. |

### Care-user-facing endpoints that the MFE can call

All rows require a Care user. Use the existing Care permission checks for the named Facility, Patient, or Encounter. Never return ABDM tokens.

| Care path | Method | Auth | Purpose | ABDM operation | Work mode |
|---|---|---|---|---|---|
| `/api/abdm/facilities/{facility_id}/abdm` | GET | Care user | Read facility ABDM state for ADR-007. | Gateway list/get bridge services | Sync read. |
| `/api/abdm/facilities/{facility_id}/abdm` | PUT | Care facility admin | Save manual facility link fields. | none | Sync write to extension. |
| `/api/abdm/facilities/{facility_id}/abdm/bridge-url` | POST | Care facility admin | Register or re-register callback URL. | `gateway-update-bridge-url` | Sync gateway call. |
| `/api/abdm/facilities/{facility_id}/abdm/hrp-services` | POST | Care facility admin | Register or update HIP HRP service. | `gateway-register-bridge-services` | Sync gateway call. |
| `/api/abdm/patients/{patient_id}/link-token` | POST | Care user with patient write | Generate or refresh the patient link token. | `m2-generate-link-token` | Celery, callback result. |
| `/api/abdm/patients/{patient_id}/sms-link` | POST | Care user with patient write | Ask ABDM to send a deep-link SMS. | `m2-sms-deep-link-notify` | Celery, callback result. |
| `/api/abdm/encounters/{encounter_id}/care-context` | GET | Care user with encounter read | Read link state and transfer log. | none | Sync read. |
| `/api/abdm/encounters/{encounter_id}/care-context/link` | POST | Care user with encounter write | Link this Encounter as a care context. | `m2-hip-link-care-context` | Celery, callback result. |
| `/api/abdm/encounters/{encounter_id}/care-context/notify` | POST | Care user with encounter write | Notify after a linked context gains records. | `m2-link-care-context-notify` | Celery, callback result. |
| `/api/abdm/encounters/{encounter_id}/abdm-log` | GET | Care user with encounter read | Show consent, request, and transfer events. | none | Sync read. |

## Data model

### Plug tables

| Table | Purpose | Key fields | Indexes and constraints |
|---|---|---|---|
| `AbdmOutboundRequest` | One row for each call that Care sends to ABDM. | `request_id`, `operation_id`, `facility`, `patient`, `encounter`, `status`, `request_json`, `http_status`, `response_json`, `error_code`, `sent_at`, `completed_at` | unique `request_id`; index `operation_id,status`; index `facility,status`; index `patient,status`; index `encounter,status`. |
| `AbdmCallback` | Raw callback log and dispatch state. | `path`, `request_id_header`, `timestamp_header`, `hip_id_header`, `signature_status`, `raw_body`, `parsed_json`, `response_request_id`, `transaction_id`, `idempotency_key`, `shape_status`, `processed_status`, `received_at` | unique `idempotency_key`; index `response_request_id`; index `transaction_id`; index `path,received_at`; index `signature_status`. |
| `AbdmPatientLinkToken` | Secret link token per patient and facility. | `patient`, `facility`, `abha_address`, `abha_number`, `link_token`, `expires_at`, `status`, `last_request`, `last_error`, `created_at` | unique active row on `patient,facility,abha_address`; index `expires_at`; index `status`. |
| `AbdmCareContext` | Lifecycle row for 1 Encounter as 1 care context. | `encounter`, `patient`, `facility`, `reference_number`, `display`, `hi_types`, `status`, `linked_at`, `last_link_request`, `last_notify_request`, `last_error` | unique `encounter`; unique `facility,reference_number`; index `patient,status`; index `facility,status`. |
| `AbdmDiscoveryFlow` | State for PHR discovery and user link. | `transaction_id`, `callback`, `patient_match`, `abha_address`, `verified_identifiers`, `unverified_identifiers`, `candidate_contexts`, `status`, `link_reference_number`, `expires_at` | unique `transaction_id`; index `status`; index `link_reference_number`. |
| `AbdmSmsNotification` | State for SMS deep-link requests. | `request_id`, `patient`, `facility`, `phone_no`, `hip_id`, `status`, `last_callback`, `last_error` | unique `request_id`; index `patient,status`. |
| `AbdmConsentArtefact` | HIP consent state and raw artefact. | `consent_id`, `facility`, `patient`, `abha_address`, `hiu_id`, `status`, `hi_types`, `care_context_references`, `date_from`, `date_to`, `raw_json`, `signature_status`, `notified_at` | unique `consent_id`; index `patient,status`; index `facility,status`; index `date_to`. |
| `AbdmHealthInformationRequest` | Data-push state with the 20-minute deadline. | `transaction_id`, `consent`, `facility`, `patient`, `data_push_url`, `date_from`, `date_to`, `key_material`, `status`, `deadline_at`, `ack_request`, `notify_request`, `received_at` | unique `transaction_id`; index `deadline_at,status`; index `consent,status`. |
| `AbdmHealthInformationTransfer` | One transfer part or bundle result. | `request`, `care_context`, `record_type`, `bundle_identifier`, `bundle_sha256`, `validation_status`, `push_status`, `pushed_at`, `status_description` | unique `request,care_context,record_type,bundle_identifier`; index `request,push_status`. |

Store `link_token` as a secret. Do not put it in a Care extension. Store raw consent and key material only in the plug tables. Store only hashes for large encrypted payloads unless a debug flag keeps a short-lived copy.

### Care extensions

Use ADR-004. Secrets and many rows stay in plug tables. Display state can stay in `extensions`. All server-owned fields use `x-ui.render_blacklist` for host forms.

#### `Encounter.extensions["abdm"]`

```json
{
  "care_context_reference": "Encounter.external_id or stable plug reference",
  "care_context_display": "OPD records for 10-Sep-2026",
  "hi_types": ["OPConsultation", "Prescription"],
  "link_status": "not_linked | token_requested | link_requested | linked | failed",
  "linked_at": "2026-09-10T12:00:00Z",
  "last_link_request_id": "uuid",
  "last_notify_request_id": "uuid",
  "last_error_code": "ABDM-1056",
  "last_error_message": "This care contexts has been already linked"
}
```

`care_context_reference` must be stable. Use `Encounter.external_id`.

#### `Facility.extensions["abdm"]`

Keep the field names that the docs use. Add plug fields only where the docs have no name.

```json
{
  "facilityId": "IN07100XXXXX",
  "facilityName": "City Health HIP",
  "url": "https://care-abdm-sbx.rithviknishad.dev/api/abdm",
  "HRP": [
    {
      "bridgeId": "BRIDGE_HIP_001",
      "hipName": "City Health HIP",
      "type": "HIP",
      "active": true,
      "serviceId": "HIP_SERVICE_ID"
    }
  ],
  "hip": {
    "id": "HIP_SERVICE_ID",
    "name": "City Health HIP",
    "type": "HIP"
  },
  "bridge": {
    "id": "bridge id from list",
    "name": "bridge name from list",
    "url": "callback URL from list",
    "active": true,
    "blocklisted": false
  },
  "verified_at": "2026-09-10T12:00:00Z"
}
```

The docs do not say whether `X-HIP-ID` must equal `HRP.bridgeId`, `serviceId`, or `hip.id`. Use `hip.id` in plug code after Rithvik fills it. Verify it against the first successful M2 call.

#### `Patient.extensions["abdm"]` additions

```json
{
  "link_token_status": "missing | requested | active | expired | failed",
  "link_token_expires_at": "2027-03-10T12:00:00Z",
  "last_link_token_request_id": "uuid",
  "last_sms_request_id": "uuid"
}
```

The token itself stays in `AbdmPatientLinkToken`. The existing ABHA number, address, source, and KYC fields stay as ADR-004 defines them.

## Celery tasks

Use Care's `@shared_task` pattern. Care autodiscovers tasks from apps. Source: `~/ohc.network/care/config/celery_app.py:8-18`. Use `retry_kwargs`, `expires`, and clear logs like `care/emr/tasks/report_generation.py:12-78`.

| Task | Trigger | Retry and timeout | Outcome |
|---|---|---|---|
| `abdm.tasks.generate_link_token` | Patient link, encounter auto-link, or token expiry. | Retry 5xx, `ABDM-9999`, and rate limit with backoff. Do not retry 4xx. `expires=5m`. | Sends `m2-generate-link-token`. Waits for callback. |
| `abdm.tasks.link_care_context` | `post_save(Encounter)` in `signals.py`, at create and status change. Run only when the Patient has ABHA and the Facility has ABDM config. | Retry only transport and 5xx. Do not retry duplicate link as failure. | Sends `m2-hip-link-care-context`. Updates `AbdmCareContext`. |
| `abdm.tasks.notify_linked_context` | Link success, or linked context gains a new record. | Retry transport and 5xx. `expires=10m`. | Sends `m2-link-care-context-notify`. |
| `abdm.tasks.send_sms_deep_link` | User clicks SMS link route for a patient without ABHA. | Retry transport and 5xx. `expires=10m`. | Sends `m2-sms-deep-link-notify`. |
| `abdm.tasks.reply_to_discovery` | Verified callback for discovery. | One fast attempt, then retry transport. | Sends `m2-on-discover-care-contexts`. |
| `abdm.tasks.reply_to_link_init` | Verified callback for link init. | One fast attempt, then retry transport. | Sends `m2-receive-link-init`. |
| `abdm.tasks.reply_to_link_confirm` | Verified callback for link confirm. | One fast attempt, then retry transport. | Sends `m2-receive-link-confirm`. |
| `abdm.tasks.ack_consent_notification` | Verified consent callback. | Retry transport and 5xx. | Sends `m2-consent-hip-on-notify`; saves consent artefact. |
| `abdm.tasks.process_health_information_request` | Verified health information request. | `expires=20m`. No retry after `deadline_at`. | Ack, validate consent/date/key data, build FHIR, encrypt, push to `dataPushUrl`, then notify. |
| `abdm.tasks.expire_pending_m2_work` | Periodic task. | No retry. | Marks missed callbacks and data jobs after their deadline. |

The 20-minute window starts when Care receives `m2-on-health-information-request`. Store `deadline_at = received_at + 20 minutes`. Each retry must check the deadline before it starts.

## Callback handling

Use one generic receiver behind a path whitelist.

1. Read the path, headers, raw body, and arrival time.
2. Build `idempotency_key = sha256(path + REQUEST-ID + response.requestId + transactionId + raw_body)`.
3. Insert `AbdmCallback`. If the key already exists, return the same ack status.
4. Verify the callback signature with gateway JWKS from `gateway-get-gateway-certs`.
5. Pin `RS256`. Refetch JWKS 1 time if `kid` is unknown.
6. Do not dispatch if signature verification fails.
7. Verification fails closed in every environment.
8. Match the callback to `AbdmOutboundRequest.request_id` via `response.requestId` when present.
9. Fall back to `transactionId` only for inbound flows that did not answer our request.
10. Dispatch by callback path and operation id.
11. If the body shape does not match the docs, set `shape_status="mismatch"` and save a finding row.
12. Still return 200 or 202 for a verified shape mismatch, because the raw payload is useful evidence.
13. Do not mutate patient, encounter, consent, or transfer state from an unverified callback.

The docs say the callback signature header is not published. Log the first real callback headers as a finding. Do not log tokens or clinical payload bytes outside `AbdmCallback.raw_body`.

## FHIR bundle builder

MCP `list_fhir_profiles` returned these profiles on 2026-09-10: `DiagnosticReportRecord`, `DischargeSummaryRecord`, `DocumentBundle`, `HealthDocumentRecord`, `ImmunizationRecord`, `OPConsultRecord`, `PrescriptionRecord`, and `WellnessRecord`. It did not return `Invoice`.

Common rules from the docs and MCP:

- Use FHIR R4.
- Use `Bundle.type = "document"`.
- Put a `Composition` as the first bundle entry.
- Set `Bundle.meta`, `Bundle.meta.versionId`, `Bundle.identifier.system`, `Bundle.identifier.value`, and `Bundle.timestamp`.
- Use logical `entry[].fullUrl` values.
- Put the facility HIP ID in `Composition.attester.party` through an `Organization` resource.
- Validate first with MCP `validate_fhir`.
- Then use the HL7 validator recipe from `.agent/skills/abdm-fhir/references/generate.md` if Rithvik wants a second tier.

| ABDM record type | Profile URL | CARE source today | Phase 3 plan |
|---|---|---|---|
| `OPConsultation` | `https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord` | `Encounter` has status, class, patient, period, facility, and extensions. `Observation`, `Condition`, `AllergyIntolerance`, `MedicationRequest`, `ServiceRequest`, `FormSubmission`, and `QuestionnaireResponse` point at Encounter. | Day-1 record type. Build a first structured bundle from Encounter data. Defer procedure detail because no `Procedure` model was found. |
| `Prescription` | `https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord` | `MedicationRequestPrescription` and `MedicationRequest` point at Encounter and Patient. | Day-1 record type. Build structured prescription bundles. |
| `DiagnosticReport` | `https://nrces.in/ndhm/fhir/r4/StructureDefinition/DiagnosticReportRecord` | `DiagnosticReport`, `Observation`, `Specimen`, and `ServiceRequest` point at Encounter or Patient. `FileUpload` can attach diagnostic files. | Day-1 record type. Build structured reports when rows exist. Use a simple bundle for report files. |
| `DischargeSummary` | `https://nrces.in/ndhm/fhir/r4/StructureDefinition/DischargeSummaryRecord` | `Encounter.discharge_summary_advice` exists. Care registers a discharge summary report for Encounter. | Day-1 record type. Start with a simple bundle around the discharge summary report. Add structured fields later. |
| `HealthDocumentRecord` | `https://nrces.in/ndhm/fhir/r4/StructureDefinition/HealthDocumentRecord` | `FileUpload` has `associating_id`, `file_type`, and `file_category`. It supports patient and encounter files. | Day-1 record type. Build simple bundles for uploaded documents. |
| `WellnessRecord` | `https://nrces.in/ndhm/fhir/r4/StructureDefinition/WellnessRecord` | `Observation` points at Encounter and Patient. | Recorded gap. Not a blocker. |
| `ImmunizationRecord` | `https://nrces.in/ndhm/fhir/r4/StructureDefinition/ImmunizationRecord` | No model named Immunization was found. | Recorded gap. Not a blocker. |
| `Invoice` | Docs list this as mandatory, but MCP has no profile. | CARE has billing modules, but no ABDM Invoice profile was returned. | Recorded gap. Not a blocker. |

CARE model citations: `~/ohc.network/care/care/emr/models/encounter.py:8-37`, `observation.py:6-15`, `medication_request.py:9-41`, `diagnostic_report.py:6-20`, `condition.py:6-14`, `allergy_intolerance.py:6-13`, `service_request.py:7-22`, `questionnaire.py:47-72`, `file_upload.py:13-18`, `emr/reports/report_types.py:12-18`.

## Encryption

The data-flow page specifies this design:

| Item | Docs term | Rule |
|---|---|---|
| Curve | Curve25519 | Use ECDH over Curve25519. |
| HIU short-term public key | `DHPK(U)` | The HIU sends it in the request. |
| HIP short-term public key | `DHPK(P)` | CARE sends it with encrypted data. |
| HIU nonce | `RAND(U)` | 32 bytes. The HIU sends it in the request. |
| HIP nonce | `RAND(P)` | 32 bytes. CARE sends it with encrypted data. |
| Shared key | `DHK(U,P)` | CARE computes it from `DHPK(U)` and the HIP private key. |
| Salt and IV | XOR of nonces | First 20 bytes are salt. Last 12 bytes are IV. |
| Session key | `SK(U,P)` | Derive a 256-bit AES-GCM key with HKDF. |
| Payload cipher | AES-GCM | Encrypt the FHIR bundle bytes. |
| Long-term HIP private key | not named as a field | It signs the encrypted payload. |

Use the Python `cryptography` library in-process. It implements the documented ECDH Curve25519, HKDF, and AES-GCM algorithm. Do not add an external crypto service.

## Frontend slots

No care_fe slot is missing for Phase 3. A facility settings page slot does not exist. Use `FacilityHomeActions` for ADR-007. It already receives the `facility` object.

| Need | Slot | Host source | Proposed plug surface |
|---|---|---|---|
| Encounter "Link to ABHA" action | `EncounterActions` | `~/ohc.network/care_fe/src/pluginTypes.ts:36-39`; `summary-panel-actions.tab.tsx:93-101`; `EncounterCommandDialog.tsx:519-529` | Button in the encounter action area and command dialog. |
| Quick link action on patient card | `PatientInfoCardQuickActions` | `pluginTypes.ts:41-44`; `EncounterShow.tsx:238-248` | Primary button when selected encounter exists. |
| Link status on encounter overview | `EncounterOverviewTop` | `pluginTypes.ts:93-97`; `pages/Encounters/tabs/overview.tsx:54-60` | Compact status card with care context reference and last error. |
| Consent and transfer log tab | `encounterTabs` | `pluginTypes.ts:212-215`; `EncounterShow.tsx:80` | Tab that lists callbacks, consent state, health requests, and transfers. |
| ADR-007 facility link form | `FacilityHomeActions` | `pluginTypes.ts:50-53`; `FacilityHome.tsx:253-257` | Form for `facilityId`, `facilityName`, `HRP`, `hip`, and `url`. |

Minimal care_fe delta: none for Phase 3. Add a facility-settings slot later only if Rithvik wants the ADR-007 form away from Facility Home.

## Build order

Each step is a sandbox loop. A step ends only on observed output. The user runs servers, tunnel, OTP, and PHR app actions. The agent can run in-process checks, make ABDM docs-based calls through backend code, and inspect callback rows.

1. **Facility and bridge proof.** Add the ADR-007 form and save `facilityId`, `facilityName`, `HRP`, `hip`, and `url`. USER keeps the tunnel up and supplies sandbox facility values. Agent verifies `gateway-update-bridge-url`, `gateway-register-bridge-services`, and gateway service lookup output.
2. **Callback receiver proof.** Add the generic receiver, raw callback table, JWKS fetch, and signature mode. USER keeps Care public on the tunnel. Agent verifies JWKS fetch and that a sandbox callback inserts `AbdmCallback` before dispatch.
3. **Link token proof.** Add `generate_link_token`. USER registers or links a patient with ABHA. Agent sends `m2-generate-link-token`. Done when `/v3/hip/token/on-generate-token` lands and stores a token or a documented error.
4. **HIP link proof.** Add `AbdmCareContext` and the encounter auto-link path. USER creates an encounter with a shareable record. Agent sends `m2-hip-link-care-context`. Done when `/v3/link/on_carecontext` reports success or an already-linked code.
5. **Context notify proof.** Add `notify_linked_context`. Agent sends `m2-link-care-context-notify`. Done when `/v3/links/context/on-notify` reports success.
6. **Discovery proof.** Add discovery match and reply. USER starts discovery in a PHR app. Agent verifies the inbound discovery row and outbound `m2-on-discover-care-contexts` 202. Done when the PHR app shows only metadata for the encounter.
7. **User link proof.** Add link init and confirm handlers. USER selects the care context in the PHR app and completes the PHR action. Agent verifies init, confirm, and the final linked state in `AbdmCareContext`.
8. **SMS deep-link proof.** Add SMS path for a patient without ABHA. USER confirms the mobile can receive sandbox SMS and follows the link in a PHR app. Agent verifies `m2-sms-deep-link-notify` and `/v3/patients/sms/on-notify`.
9. **FHIR proof.** Add builders for `Prescription`, `DiagnosticReport`, `OPConsultation`, `DischargeSummary`, and `HealthDocumentRecord` first. Agent validates each bundle with MCP `validate_fhir`. Done when each selected type has 0 findings or a recorded mapping gap.
10. **Data transfer proof.** Add consent ack and health information job. USER grants consent from the PHR app. Agent verifies health request callback, immediate `m2-hip-health-information-on-request`, bundle build, encryption, data push, and `m2-hip-data-flow-notify` before `deadline_at`. Done when the record is readable in the PHR app.

## Decisions (Rithvik, 2026-09-10)

1. Auto-link at Encounter create. Auto-update when the Encounter status changes.
2. Encounter class map: FHIR `amb` -> "OPD", `imp` -> "IPD". Use class display text for other classes.
3. Discovery match uses verified ABHA address or ABHA number only. Do not use demographic match.
4. Care-context reference number = `Encounter.external_id`.
5. Day-1 record types: OPConsultation, Prescription, DiagnosticReport, DischargeSummary, HealthDocumentRecord. Wellness, Immunization, and Invoice are recorded gaps. They are not blockers.
6. Crypto: Python `cryptography` library in-process implements documented ECDH Curve25519, HKDF, and AES-GCM. Do not use an external service.
7. ADR-007 facility form stores `hip.id`, `HRP.bridgeId`, and `serviceId`. `X-HIP-ID` = `hip.id` by default. A facility config switch can select another value.
8. Callback signature verification fails closed from day 1 in every environment. The receiver stores the raw callback before verification. This lets the first real callback show the header name.

## Consequences

- Phase 3 can start without host code changes.
- Callback storage becomes the main evidence source for docs gaps.
- M2 state stays auditable and idempotent.
- The design accepts temporary duplicate callback paths because the docs conflict.
- FHIR work starts with record types that CARE can produce today.
- `Invoice` and full `ImmunizationRecord` remain blocked by docs or data gaps.
