# ADR-014 — M3 Retrieve: CARE as an HIU

Status: Accepted (Rithvik, 2026-09-19)
Date: 2026-09-19
Depends on: ADR-011 (lean M2: 1 table per ABDM object, callbacks drive state), ADR-012 (1 failure
shape), ADR-013 (the ABDM Records encounter tab).

## Context

M3 lets a facility act as a Health Information User: ask a patient, through the HIE-CM, for the
records other facilities hold against their ABHA address, and receive them encrypted at a URL the
HIU names. The docs mirror of 2026-09-19 (catalogue 2026.09.16) publishes 7 HIU calls and 5 HIU
callbacks on 12 flow pages under `api/m3/endpoints/m3-consent-management-data-flow-hiu/`, the
push body on the M2 page `m2-consent-management-data-flow-hip/05-m2-post-health-information-transfer`,
and the state model on `concepts/consent`. The M3 skill says: "Nothing here has been run against
the ABDM sandbox."

The plug already holds the pieces the HIU side re-uses: the gateway session, `outbound.send()`,
the signed callback catch-all, the X25519 + HKDF-SHA256 + AES-256-GCM implementation with a
`decrypt()` written for this purpose (`hip/crypto.py`), and the ADR-012 failure classifier.

Facts that shape the design:

| Fact | Source |
|---|---|
| Consent request and consent artefact are 2 objects with 2 ids. A grant can produce several artefacts. Store the request id and every artefact id. | `concepts/consent` §Two objects, not one |
| 5 states: Requested, Granted, Denied, Expired, Revoked. On Revoked or Expired, stop. | `concepts/consent` §The states a consent moves through |
| The HIU names any https `dataPushUrl`; the HIP posts there directly, not through the gateway, with a bearer token. | `m3 .../09`, `m2 .../05` |
| The HIU generates a short-term key pair and a 32-byte nonce per request; the HIP answers with its own; both derive the session key. 20 minutes from the request. | `concepts/data-flow` |
| `consent.hip` is nullable in the init schema, so a request can go to every HIP. | MCP `get_operation m3_post_consent_v3_request_init` |
| The sandbox issued 1 service id with `types: ["HIP", "HIU"]` for the facility. | findings B18 |
| "Decide your retention policy for data you already hold." | `concepts/consent` §Expiry and revocation |
| The HIU must "discontinue access upon consent expiry or revocation". | `milestones/m3` §What you build, in order, step 6 |

## Decisions (Rithvik, 2026-09-19)

1. **UI seam: the 3rd card of the existing "ABDM Records" encounter tab.** No care_fe change. A
   consent request is per patient and facility; the visit is where the doctor is. care_fe has no
   patient-level tab slot, and a second encounter tab needs a host label.
2. **Retention: store the decrypted bundle; erase its content at the consent `dataEraseAt`**, or at
   once when the consent is revoked, denied or expires. The row stays as the audit trail. The plug
   sends `accessMode: VIEW` as the endpoint example does; the docs define no mode (findings L2).
3. **Target: every HIP by default, with an optional provider picker** backed by
   `GET gateway/v3/providers?name=`. With no provider the `hip` block is omitted.
4. **Defaults, editable in the dialog:** purpose `CAREMGT` (6 codes), the 7 clinical record types
   (`Invoice` off), records of the last 12 months, permission valid 30 days, `frequency` as the
   example (`HOUR`, 1, 0).
5. **Automatic journey 3.** A GRANTED notify is acknowledged, every artefact is fetched, a live
   artefact starts the health-information request with a fresh key pair, the push is decrypted and
   stored, and the gateway is told RECEIVED. The desk has "Fetch again" for a lapsed window.

## Design

**Backend `abdm/hiu/`** mirrors `abdm/hip/`: `rules.py` (pure builders, parsers, defaults,
validation), `service.py` (rows, the 6 callback handlers, the chain, housekeeping, summaries),
`views.py` (desk routes). 4 tables, 1 per ABDM object the HIU must remember:

| Table | 1 row per | Why |
|---|---|---|
| `AbdmConsentRequest` | consent request | The ask. `consent_request_id` arrives on `on-init`; the notify names it. |
| `AbdmConsentArtefact` | consent artefact | The permission. Ids from the GRANTED notify; detail from `on-fetch`; signature stored, not verified. |
| `AbdmFetchRequest` | health-information request | Holds the X25519 private key and our nonce until the push is decrypted or 20 minutes pass, then blanks them. `transaction_id` from `on-request`. |
| `AbdmFetchedRecord` | decrypted bundle | The record: HI type from `Composition.meta.profile`, title, date, HIP, MD5 result, `erase_at`. |

**Headers.** `outbound.send(..., role="hiu")` sends the facility's gateway service id as `X-HIU-ID`
and omits `X-HIP-ID`. The value is the one id the sandbox issued (B18); confirm on the first call.

**Callbacks.** 6 paths in `callbacks/paths.py`; handlers in `tasks.CALLBACK_HANDLERS`. Correlation
is by `response.requestId` (the receiver links the outbound row), by `consentRequestId` (notify) or
by `transactionId` (push). No header is used for routing. The data push URL is
`${ABDM_CALLBACK_BASE_URL}/api/abdm/v3/hiu/health-information/transfer`, so the push goes through
the same signed catch-all: the HIP's bearer token must verify against the gateway JWKS, which is
what the M2 side sends (findings L6 records the assumption).

**Requester.** `consent.requester.name` is the logged-in user; `identifier` is the medical council
registration (`User.doctor_medical_council_registration`) or the Care username, with the callback
base URL as `system`. The docs define no type list (L3).

**Acknowledgement.** `acknowledgement[].consentId` names each artefact id for GRANTED and REVOKED.
A DENIED or EXPIRED notify carries no artefact, so the consent request id goes in that field, as the
page example does (L4).

**Checksum.** AES-GCM authenticates the content, so an MD5 mismatch is recorded on the row and in
the notify description, not refused (L5).

**Housekeeping.** `abdm.tasks.hiu_housekeeping` every 15 minutes: a request with no push inside
its window is failed, its key blanked and the gateway told FAILED ("FAILED when data was not
sent", the notify page); a bundle past `erase_at` is emptied.

**Desk routes.** `GET/POST patients/<id>/abha/consent-requests?facility=`,
`POST .../consent-requests/<id>/refresh|fetch`, `GET patients/<id>/abha/records/<id>`,
`GET providers?name=`. All gated on `can_view_clinical_data` for the patient.

**Frontend.** `fetch-records-card.tsx` (list, actions, polling every 10 s while something may
arrive), `consent-request-dialog.tsx` (the 5 fields and the picker), `fhir-record-viewer.tsx`
(Composition sections, per-resource summaries, attachments, raw JSON, download), `hiu-state.ts`.
The card is append-only and shows every failure block (ADR-012 D7).

## Consequences

- 4 tables, 1 periodic task, 6 callback paths, 4 desk routes; no host change.
- The plug holds decrypted health data of other facilities for the length of the consent. The
  erase rule is enforced by the periodic task and by the revoke, deny and expire handlers.
- Nothing has been observed against the sandbox yet. The first real run must confirm: the
  `X-HIU-ID` value, the `hip`-less init, the ack body for a denial, and which token the HIP sends on
  the push (`03-roadmap.md` Phase 4).
