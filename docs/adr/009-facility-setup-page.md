# ADR-009 — The facility setup form is a plug page, not a dialog

Status: Accepted (Rithvik, 2026-09-10)
Date: 2026-09-10

## Context

ADR-007 put the manual facility link form in the `FacilityHomeActions` slot as
a dialog. The host renders that slot inside its "Configurations" dropdown
(`~/ohc.network/care_fe/src/components/Facility/FacilityHome.tsx:253-257`).
Two defects came from this:

1. The slot rendered a status badge and a button side by side. The host
   dropdown is `w-full min-w-48`, so the two elements made the dropdown very
   wide.
2. The dialog did not center itself, and it closed with the dropdown. Every
   portal of this plug mounts into the `PluginComponent` container, because the
   design tokens live on that container
   (`frontend/src/components/common/plugin-component.tsx`). Inside the dropdown
   this container has a transformed ancestor. CSS makes a transformed ancestor
   the containing block of a `position: fixed` element. The dialog therefore
   anchored to the dropdown popup and not to the viewport.

Defect 2 has no fix inside the dropdown. A portal to `document.body` escapes
the transform, but it also escapes the token scope, so the panel renders
without a background.

## Decision

The plug registers its own page and the slot only links to it.

| Item | Value |
|---|---|
| Route | `/facility/:facilityId/abdm/setup` |
| Registered by | `frontend/src/manifest.tsx` `routes` |
| Merged by the host | `~/ohc.network/care_fe/src/Routers/AppRouter.tsx:104-115` |
| Page component | `frontend/src/components/abdm/facility-setup-page.tsx` |
| Slot component | `frontend/src/components/abdm/facility-home-actions.tsx` |

The host merges plug routes first and its own routes last, so a host route wins
a collision. The host claims `/facility/:facilityId/settings*`
(`~/ohc.network/care_fe/src/Routers/routes/FacilityRoutes.tsx:46`). The plug
route must stay outside that prefix.

The slot renders one row only. The row shows the setup label and a small
colored dot for the gateway status.

The page reads the facility name from the host route
`GET /api/v1/facility/{facilityId}/`
(`~/ohc.network/care_fe/src/types/facility/facilityApi.ts:34-38`). This is the
first host API route that the MFE calls.

## Consequences

- The plug now owns a route in the host router. Keep the path outside every
  host prefix, and re-check the host route table before you add another page.
- The MFE must not open a dialog from `FacilityHomeActions`. The same trap
  applies to any future slot that the host renders inside a popup.
- The form is still the ADR-007 workaround. Delete the page and the route when
  M4 gives a browse-and-link flow.
