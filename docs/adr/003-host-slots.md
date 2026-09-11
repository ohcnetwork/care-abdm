# ADR-003 — Host slots for the MFE

Status: Accepted for M1 slots; Proposed for M2/M3/M4 slots
Date: 2026-09-10

## Context
CARE loads a plug from its module-federation manifest.
The host defines typed component slots in `care_fe`.
Source: `docs/02-care-host-contract.md:14-20`, `~/ohc.network/care_fe/src/pluginTypes.ts:202-214`.

The M1 docs require ABHA creation, ABHA login, profile, card, and QR flows.
Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m1/index.md.

## Decision
Use these host slots for the accepted M1 surface.
The line numbers were re-read on 2026-09-10.

| Slot | Status | Host source | Plug source | Use |
|---|---|---|---|---|
| `FacilityHomeActions` | Accepted as a Phase 0 probe | `~/ohc.network/care_fe/src/pluginTypes.ts:50-52`; `~/ohc.network/care_fe/src/components/Facility/FacilityHome.tsx:253-256` | `frontend/src/manifest.tsx:14-16`; `frontend/src/components/abdm/facility-home-actions.tsx:1-27` | Show gateway status. ADR-007 will replace this with a facility link form. |
| `PatientRegistrationForm` | Accepted | `~/ohc.network/care_fe/src/pluginTypes.ts:55-60`; `~/ohc.network/care_fe/src/components/Patient/PatientRegistration.tsx:410-413` | `frontend/src/manifest.tsx:17-19`; `frontend/src/components/abdm/patient-registration-form.tsx:16-86` | Start or receive an ABHA transaction. Set `extensions.abdm.txn_id`. |
| `PatientDetailsTabDemographyGeneralInfo` | Accepted | `~/ohc.network/care_fe/src/pluginTypes.ts:62-70`; `~/ohc.network/care_fe/src/components/Patient/PatientDetailsTab/Demography.tsx:172-176` | `frontend/src/manifest.tsx:20-22`; `frontend/src/components/abdm/patient-abha-panel.tsx:1-321` | Show ABHA state, card, and link action. |
| `PatientHomeActions` | Accepted | `~/ohc.network/care_fe/src/pluginTypes.ts:30-34`; `~/ohc.network/care_fe/src/components/Patient/PatientProfile.tsx:177-180` | `frontend/src/manifest.tsx:23-25`; `frontend/src/components/abdm/patient-home-actions.tsx:1-48` | Show a compact ABHA chip. |
| `PatientSearchActions` | Accepted | `~/ohc.network/care_fe/src/pluginTypes.ts:73-76`; `~/ohc.network/care_fe/src/components/Patient/PatientIndex.tsx:259-262` | `frontend/src/manifest.tsx:26-28`; `frontend/src/components/abdm/patient-search-actions.tsx:13-40` | Find by ABHA after ABDM OTP verification. |

Keep these slots planned but unused.

| Surface | Status | Host source | Planned use |
|---|---|---|---|
| `EncounterActions` | Proposed | `~/ohc.network/care_fe/src/pluginTypes.ts:36-39`; `~/ohc.network/care_fe/src/pages/Encounters/tabs/overview/summary-panel-actions.tab.tsx:93-97` | M2 link a Care encounter as a care context. |
| `PatientInfoCardQuickActions` | Proposed | `~/ohc.network/care_fe/src/pluginTypes.ts:41-48`; `~/ohc.network/care_fe/src/pages/Encounters/EncounterShow.tsx:240-244` | M2 quick action for the selected encounter. |
| `encounterTabs` | Proposed | `~/ohc.network/care_fe/src/pluginTypes.ts:212-214`; `~/ohc.network/care_fe/src/pages/Encounters/EncounterShow.tsx:80` | M3 consent and record transfer log. |
| `extends: PatientExternalRegistration` | Proposed, unverified consumer | `~/ohc.network/care_fe/src/pluginTypes.ts:199-200` | Possible future external identity flow. |

Hide host-form extension fields with `x-ui.render_blacklist`.
Use the plug panel as the display surface.
Code: `backend/src/abdm/care_seams.py:30-80`.

Do not use core `?identifier=` search for Find by ABHA.
Verify ABHA with ABDM before CARE lookup.
Source: `docs/findings.md:85-87`.
Code: `frontend/src/components/abdm/patient-search-actions.tsx:18-25`.

## Consequences
- M1 needs no host change beyond existing slots.
- M2 can start with encounter action slots after ADR-007.
- `PatientExternalRegistration` stays unused until the consumer is verified.

## Amendment — 2026-09-10: no QR code in the staff panel
The ABHA QR code (`GET /v3/profile/account/qrCode`) is a patient-held credential. The patient
shows it at a facility (`m1-profile-get-qr-code`). A staff panel already shows the ABHA number
and the ABHA address, so a QR preview adds no value for staff. The QR preview is removed from
the panel and from the plug API. The staff-side use of a QR is a scan in `PatientSearchActions`.
