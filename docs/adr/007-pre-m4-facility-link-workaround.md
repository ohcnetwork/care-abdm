# ADR-007 — Pre-M4 workaround: manual facility ↔ ABDM facility linking

Status: Accepted (Rithvik, 2026-09-09)
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

## Consequences
- Temporary code; delete when M4's registry browse/link exists.
- Multi-tenant: mapping is per Care facility, never per instance.
- Amended 2026-09-10 by ADR-009: the form is a plug page at
  `/facility/:facilityId/abdm/setup`. The slot only links to it.
