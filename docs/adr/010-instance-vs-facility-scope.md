# ADR-010 — Instance and facility scope for ABDM setup

Status: Accepted (Rithvik, 2026-09-14)
Note: ADR-011 (2026-09-15) removed the `AbdmBridge` table and the admin page. The scope split stands; the bridge id is read live from the gateway.
Date: 2026-09-14

## Context

One CARE instance can hold many facilities.
The ABDM facility setup page mixed bridge values with facility values.
The docs split those values across two levels.

Instance values belong to one `clientId` and one bridge.
Facility values belong to one HFR facility or one HIP service.
Patient values belong to one patient.

## Classification

| Value | Scope | Reason | Store today | Store after this ADR |
|---|---|---|---|---|
| `clientId` and `clientSecret` | instance | The sandbox issues them together. The session call uses them to get the token for later calls. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/getting-started/sandbox/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-sessions-create/index.md | `settings.py` | `settings.py` |
| Gateway session token | instance | The gateway session token comes from `clientId` and `clientSecret`. It is the bearer token for later gateway calls. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/gateway/index.md | Redis cache | Redis cache |
| `X-CM-ID` | instance | It selects the consent manager for the gateway host. Sandbox uses `sbx`. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/gateway/index.md | `settings.py` | `settings.py` |
| Bridge URL | instance | The sandbox page says to register one base URL. The bridge URL update body has only `url`. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/getting-started/sandbox/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-update-bridge-url/index.md | `settings.py`; command | `settings.py`; admin action records result in `AbdmBridge` |
| Bridge ID | instance | The services list returns `bridge.id` for the authenticated bridge. HRP linkage uses `bridgeId`. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-list-bridge-services/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md | `Facility.extensions["abdm"].bridge_id` | `AbdmBridge.bridge_id` |
| Bridge name | instance | The services list returns `bridge.name` beside `bridge.id`. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-list-bridge-services/index.md | Not stored | `AbdmBridge.bridge_name` |
| Registered bridge URL from gateway | instance | The services list returns `bridge.url`. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-list-bridge-services/index.md | Not stored | `AbdmBridge.registered_url` |
| Bridge services list | instance | The list endpoint returns all HIP or HIU services under the authenticated bridge. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-list-bridge-services/index.md | Facility page read | `AbdmBridge.services_snapshot` |
| `serviceId` | facility | The get-by-service endpoint returns the registered HIP or HIU service. This identifies one service under the bridge. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-get-bridge-service-by-id/index.md | `Facility.extensions["abdm"].service_id` | `Facility.extensions["abdm"].service_id` |
| HFR `facilityId` | facility | M4 issues a facility ID. Bridge linkage requires it. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m4/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m4/undocumented/index.md | `Facility.extensions["abdm"].facility_id` | Same |
| `facilityName` | facility | Bridge linkage requires the HFR facility name. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m4/undocumented/index.md | `Facility.extensions["abdm"].facility_name` | Same |
| `HRP.hipName` | facility | Bridge linkage requires the patient visible HIP name for one facility link. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m4/index.md | `Facility.extensions["abdm"].hip_name` | Same |
| `HRP.type` | facility | Bridge linkage marks one facility link as `HIP` or `HIU`. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m4/undocumented/index.md | Constant `HIP` in code | Constant `HIP` in code |
| `HRP.active` | facility | Bridge linkage marks one facility link as active or not. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m4/undocumented/index.md | Constant `true` in code | Constant `true` in code |
| `X-HIP-ID` | facility | M2 calls require the identifier of the Health Information Provider. The HRP register page has no HIP ID field. It makes a facility an HIP by `facilityId`. The docs team confirmed on 2026-09-14 that HIP ID equals HFR facility ID. The docs do not yet say this in words. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-register-bridge-services/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m2/endpoints/m2-hip-link-care-context/index.md | `Facility.extensions["abdm"].hip_id` | Derived from `Facility.extensions["abdm"].facility_id` |
| `notification.hip.id` | facility | Notify and SMS calls send HIP ID inside the body. Use the same derived value as `X-HIP-ID`. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m2/endpoints/m2-link-care-context-notify/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m2/endpoints/m2-sms-deep-link-notify/index.md | `Facility.extensions["abdm"].hip_id` | Derived from `Facility.extensions["abdm"].facility_id` |
| RSA public certificate | instance | One M1 certificate encrypts sensitive fields before transmission. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/m1/endpoints/m1-get-public-certificate/index.md | Cache in code path | Cache in code path |
| Gateway JWKS | instance | The JWKS verifies gateway callback signatures. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-get-gateway-certs/index.md | Cache in code path | Cache in code path |
| Link token | patient | The linking page says it ties one facility to one patient ABHA address. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/linking/index.md | Planned plug table | Planned plug table keyed by patient and facility |
| Care contexts | patient | A care context points to one patient's records at a facility. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/hip-hiu/index.md and https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/linking/index.md | Planned encounter state | Planned encounter state |
| Scan and Share counters | facility | The QR code contains a HIP ID and a facility defined context. Counter names must not be the facility ID, HIP ID, or HIP name. Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m3/index.md | `Facility.extensions["abdm"].counters` | Same |

## Decision

Environment-backed instance secrets and config stay in `settings.py`.
This includes `ABDM_CLIENT_ID`, `ABDM_CLIENT_SECRET`, `ABDM_GATEWAY_URL`,
`ABDM_ABHA_URL`, `ABDM_HSP_URL`, `ABDM_CM_ID`, and `ABDM_CALLBACK_BASE_URL`.
They do not go in the database.

Gateway-learned bridge state goes in a plug singleton table, `AbdmBridge`.
It stores the bridge ID, bridge name, registered URL, status flags, services
snapshot, last refresh time, last registration time, last result, and last error.
The table is small and auditable.
It avoids a gateway read on each admin page load.
The admin can refresh it on demand.

Facility values stay in `Facility.extensions["abdm"]`.
These are `facility_id`, `facility_name`, `hip_name`, `service_id`,
`hrp_registered_at`, `last_error`, and `counters`.
`hip_id` is a read-only derived value.
The plug returns it from the setup API for display.
It equals `facility_id`.
Do not accept it from the client.
The docs team confirmed this on 2026-09-14.

## Consequences

- The bridge setup moves to `/admin/abdm/bridge`.
- The facility setup page no longer asks for a bridge ID.
- HRP service registration reads the bridge ID from `AbdmBridge`.
- HRP service registration fails with a clear error if the bridge is not ready.
- A migration moves one old facility `bridge_id` into `AbdmBridge`.
- If old facilities disagree on bridge ID, the migration stores no ID and records an error.

## What moved

- Bridge ID moved from the facility extension to `AbdmBridge`.
- Bridge URL action moved from a management command only to the admin page too.
- Gateway services moved from the facility page to the admin page.
- Last bridge registration time and result moved to `AbdmBridge`.
