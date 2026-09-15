# ADR-011 — Lean M2: one table per ABDM object, the gateway as the source of truth

Status: Accepted (Rithvik, 2026-09-15)
Date: 2026-09-15
Supersedes: ADR-008 §Data model, §Celery tasks, §Build order; ADR-010 §`AbdmBridge`.
Keeps: ADR-008 decisions 1–8 (auto-link at Encounter create, class map, verified-only discovery
match, reference = `Encounter.external_id`, day-1 record types, in-process crypto, HIP ID = HFR
facility ID, fail-closed signatures). ADR-007 stays as the facility setup route: the docs now say
the NHPR portal route is sanctioned and "a product that registers its facilities there by hand
never builds M4" (`milestones/m4`, 2026-09-15).

## Context

ADR-008 planned 8 new tables and 10 Celery tasks. ADR-010 added a bridge snapshot table, an
admin page, and 3 admin routes. On 2026-09-15 Rithvik asked for the M2 design to be rebuilt with
less code. The docs update of the same day fixed 3 facts that shape the design:

| Fact | Source |
|---|---|
| The bridge URL is 1 per integration. `X-HIP-ID` is per facility and is the key a callback is routed on. | `getting-started/sandbox`, `reference/authentication` |
| A care context is linked only when the `/v3/link/on_carecontext` callback says so. | `whats-new/2026-09-10` |
| M4 is optional when the facility is registered on the NHPR portal by hand. | `milestones/m4` |

## Decision

1. **The gateway is the source of truth for bridge state.** No `AbdmBridge` table. `gateway/bridge.py`
   reads `GET /api/hiecm/gateway/v3/bridge-services` live and caches only the bridge id (1 hour).
   Bridge URL registration is `manage.py abdm_register_bridge_url` or `POST /api/abdm/bridge/register-url`
   (superuser). The facility setup page shows the live bridge state; there is no admin page.
2. **One table per ABDM object the HIP must remember**, all in `abdm/models.py`:

   | Table | 1 row per | Why a table |
   |---|---|---|
   | `AbdmLinkToken` | patient × facility | The token is a secret valid 6 months. |
   | `AbdmCareContext` | Encounter | Link status keyed on callbacks; reference number must resolve later. |
   | `AbdmLinkSession` | gateway `transactionId` | Discover → init (OTP hash) → confirm spans 3 callbacks. |
   | `AbdmConsent` | consent artefact | GRANTED / REVOKED / EXPIRED must be "seen in HMIS" (certification). |
   | `AbdmDataRequest` | health-information `transactionId` | 20-minute deadline; ack, push and notify audit. |

   `AbdmOutboundRequest` and `AbdmCallback` stay as the audit log. `AbdmCallback.shape_status` is gone
   (never written). No `Encounter.extensions["abdm"]`: the MFE reads `GET encounters/<id>/care-context`.
3. **Callbacks drive state.** `tasks.dispatch_callback` routes a verified callback by operation id to
   1 handler in `abdm/hip/{contexts,discovery,consent,transfer}.py`. Handlers correlate through
   `AbdmCallback.outbound_request` (`response.requestId`) or the flow's transaction id.
4. **One Celery task for the HIP-initiated route.** `tasks.sync_encounter` runs `hip.contexts.sync_encounter()`:
   create or refresh the care context, then link, or notify when a linked context gained record types.
   `post_save(Encounter)` queues it after commit for saves that touch `status`, `encounter_class` or
   `period`. The desk can run it now from the `EncounterActions` slot.
5. **Discovery matches on verified ABHA identifiers only**; the OTP for user-initiated linking is the
   plug's own, sent with Care's SMS backend, hashed at rest, fixed outside production like Care core.
6. **Data transfer** validates consent state, date range and key material before any record is read,
   builds 1 bundle per (care context, HI type), encrypts each with ECDH X25519 + HKDF-SHA256 +
   AES-256-GCM (`hip/crypto.py`), pushes once to `dataPushUrl`, then notifies. Ciphertext is not stored.
7. **Record types this pass:** `OPConsultation`, `Prescription`, `HealthDocumentRecord` (`abdm/fhir/`).
   `available_hi_types(encounter)` decides both the advertised `hiType` list and what is pushed.
8. **Migrations restart at `0001_initial`.** Local data is test data (Rithvik, 2026-09-15).

## Consequences

- 5 new tables instead of 8; 2 Celery tasks instead of 10; no admin page, nav item or snapshot table.
- The setup page keeps 3 cards: facility identity + HRP registration, bridge (read-only + register), Scan and Share counters.
- Notify-on-new-records fires on Encounter status change or on the desk action, not on every clinical write. Recorded as a limitation in `03-roadmap.md`.
- Every docs gap met on the way is a row in `findings.md` sections E–I.
