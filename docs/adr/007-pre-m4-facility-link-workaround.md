# ADR-007 — Pre-M4 workaround: manual facility ↔ ABDM facility linking

Status: Accepted (Rithvik, 2026-09-09)
Note: 2026-09-15: the docs now sanction this route. `milestones/m4` says a product that registers facilities on the NHPR portal by hand never builds M4. This is no longer a workaround; it is the facility setup.
Date: 2026-09-09

## Context
M2 (linking/sharing) needs a facility ID registered in the HIP role, which
comes from M4 (`/docs/hiecm/v3/milestones`, "M4 certifies last but blocks
M2"). We are building M1 → M2 → M3 → M4 in that order, so M2 will be built
before we have M4's browse-and-link flow.

## Decision
Until M4 ships, the MFE exposes a facility-admin form (host slot
`FacilityHomeActions`, `care_fe/src/pluginTypes.ts:50-53,138`) where a user
pastes the ABDM facility details for a Care facility. Stored in the plug's
``Facility.extensions["abdm"]` (core facility extensions landed 2026-09-09, a90aa5981).
required to act as an HIP — confirm exact names via MCP `get_operation` on
`m2-hip-link-care-context` and the bridge/HRP registration operations before
building the form.

## Field guide

| Field or action | What it is | How to obtain it | Docs URL |
|---|---|---|---|
| `facility_id` | HFR facility ID for the facility. It starts with `IN` and has 12 characters. | Onboard the facility to HFR in M4. Submit and verify the facility before use. Example: `IN1410000232`. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m4/undocumented/index.md |
| `facility_name` | Official facility name in HFR. Allowed characters: letters, digits, space, `-_.(),/`. The docs list `-_.(),/` but do not say if space is allowed. | Use the exact name from the HFR facility record. The HRP call fails if it differs. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m4/undocumented/index.md |
| `hip_name` | Patient-visible HIP name for bridge linkage. It is 15 characters or fewer. It has no special characters. The docs do not say if space is allowed. | Choose a short name patients know. Keep it unique for every bridge on a facility. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m4/undocumented/index.md |
| `service_id` | Service ID for one registered HIP or HIU service. | `gateway-get-bridge-service-by-id` returns `serviceId`. The docs do not say how a user discovers it manually. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-get-bridge-service-by-id/index.md |
| `hip_id` | HIP identifier sent in `X-HIP-ID`. It is derived from `facility_id`. It is not editable. | The HRP registration page has no HIP ID field. A facility becomes an HIP by `facilityId`. The docs team confirmed on 2026-09-14 that HIP ID equals the HFR facility ID. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m2/endpoints/m2-hip-link-care-context/index.md |
| Bridge ID (not a form field) | Bridge ID used in bridge linkage. It is instance-level. | Open `/admin/abdm/bridge` and refresh the gateway snapshot. See ADR-010. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-list-bridge-services/index.md |
| Bridge URL (not a form field) | HTTPS callback URL for the bridge. 1 per `clientId`, not per facility. | Set `ABDM_CALLBACK_BASE_URL`. Open `/admin/abdm/bridge` or run `manage.py abdm_register_bridge_url`. Run it before the HRP service registration. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/getting-started/sandbox/index.md ("Register one base URL"); https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-update-bridge-url/index.md |
| Register HRP service | HSP Registry call that registers or updates the HIP service under a facility. | Save `facilityId`, `facilityName`, and `hipName`. The plug reads `bridgeId` from `AbdmBridge`. Send `type: HIP` and `active: true`. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md |
| `hrp_registered_at` | CARE timestamp for the last successful HRP service registration. | Click Register HRP service after a save. ABDM docs show ISO UTC timestamps, but do not define this CARE status field. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md |
| `last_error` | Last ABDM error stored from a facility setup call. | Read the error code and message. Fix missing or invalid parameters first. | https://abdm-docs.dev.eka.care/docs/hiecm/v3/reference/error-codes/index.md |

## Known gateway errors

| Observed error | Meaning | User action | Source |
|---|---|---|---|
| `HTTP 200: 2500 Provided facility name is not matched with registered name` | `facilityName` does not match the HFR record exactly. This meaning is not in the docs error tables. The code number collides with documented `ABDM-2500` meanings. | Enter the exact HFR facility name. Then register the HRP service again. | Observed sandbox answer 2026-09-14. Endpoint: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md |

## Consequences
- Temporary code; delete when M4's registry browse/link exists.
- Multi-tenant: mapping is per Care facility, never per instance.
- Amended 2026-09-10 by ADR-009: the form is a plug page at
  `/facility/:facilityId/abdm/setup`. The slot only links to it.
- Amended 2026-09-14 by ADR-010: bridge ID and bridge URL actions are
  instance-level. The facility page keeps only facility and HIP service values.
