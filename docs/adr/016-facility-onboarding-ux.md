# ADR-016 — Facility onboarding UX: 1 registry card, extension-only state, "Add a facility"

Status: Accepted (Rithvik, 2026-09-19: "no manual linking support needed"; "if everything can be part of
facility extensions, well and good"; "we could leverage component overrides and override the
`AddFacilitySheet`")
Date: 2026-09-19
Depends on: ADR-007 (facility setup page), ADR-012 (1 failure shape), ADR-015 (M4: the NHPR from CARE).
Amends: ADR-015 (the `AbdmHfrOnboarding` table is removed; the state moves into the facility extension).

## Context

After M4 the setup page held 2 cards for 1 identity: the ADR-007 "facility identity" card with typed
inputs for the HFR facility ID and the registered name, and the ADR-015 HFR card that finds the same
record in the registry and links it. A typed HFR name was the cause of the 2026-09-14 linkage refusal
("provided facility name is not matched with registered name"). Nothing is in production, so no data
must survive.

Rithvik asked for 4 things (2026-09-19): question-mark help on every M4 field; 1 card instead of 2;
a way to create a Care facility from a registry record, with the Care fields filled from it; and a
step-by-step "add a facility" flow where the person decides Care-only or Care and NHPR.

Facts that shape the design:

| Fact | Source |
|---|---|
| A facility record holds name, ownership, system of medicine, type, address as LGD codes, contacts, timings, 2 photographs, scheme ids, specialities and infrastructure. The registry accepts codes, never display values. | `registries/nhpr/hfr` §What a facility record holds, §Codes, not names |
| The HIP name is the 1 field a patient sees: 15 characters or fewer, no special characters, unique per bridge. | `registries/nhpr/hfr` §Bridge linkage |
| Search by `facilityId` or by name and LGD state answers the registered name, status, type, ownership, address, pincode, state and district names and LGD codes, latitude and longitude. | `m4-search/02` |
| Care creates a facility through `FacilityViewSet.handle_create`: `FacilityCreateSpec` (name, description, `facility_type` as a type **name**, `features`, `pincode`, `address`, `phone_number`, latitude, longitude, `geo_organization`, `is_public`), the `can_create_facility` check, then `Facility.save()` which creates the root `FacilityOrganization` and makes the creator its admin. | `care/emr/api/viewsets/base.py:141-153`, `care/emr/resources/facility/spec.py:100-175`, `care/facility/models/facility.py:241-256` |
| Care government organizations carry `govt_org_type` and `govt_org_children_type` in `metadata`, **no LGD codes**. The host facility form accepts a leaf organization only. | local DB (2 govt rows: Kerala → Ernakulam); `care_fe/src/components/Facility/FacilityForm.tsx:110-114` |
| The host shares only `react`, `react-dom`, `react-i18next`, `@tanstack/react-query`, `raviger`, `sonner`, `decimal.js` with remotes: no `FacilityForm`, no organization picker. | `care_fe/vite.config.mts:445-453` |
| The host wraps the exported components named in `REACT_MFE_REGISTERED_COMPONENTS` with `register()` at build time; a plug replaces 1 by declaring `overrides: [{component, replacement, condition?, priority?}]` in its manifest, which `PluginEngine` registers. The replacement gets the base props and `__base`. `AddFacilitySheet` is `export default function`, a supported form. | `care_fe/plugins/autoRegisterComponents.ts`, `care_fe/docs/care-apps-plugin-overrides.md`, `care_fe/src/PluginEngine.tsx:142-150`, `care_fe/src/pages/Organization/components/AddFacilitySheet.tsx:23` |
| The organization page has a plug tab slot: `organizationTabs: [{name, slug, icon, component: FC<{contextId, navOrganizationId?}>}]`, at `/organization/:id/<slug>`. | `care_fe/src/pages/Organization/components/OrganizationLayout.tsx:71-72,156-157`, `pluginTypes.ts:181-186` |

## Decisions (Rithvik, 2026-09-19)

1. **Nobody types a registry value.** The HFR facility ID and the registered name are set only by a
   registry link: lookup by ID, search by name and state, the HFR wizard's submission, or the "Add a
   facility" wizard. The setup `PUT` accepts `hip_name` and `counters` only. The extension schema marks
   `facility_id` and `facility_name` `readOnly` and blacklists them from the host forms.
2. **No new table.** The registry record snapshot (`extensions["abdm"]["hfr"]`: the 17 search fields
   plus `linked_at`, `linked_by`) and the resumable HFR onboarding (`extensions["abdm"]["hfr_onboarding"]`:
   status, tracking id, the 4 step bodies without photo bytes, last message, errors, who started it, the
   HPR ID used) live on the facility. `AbdmHfrOnboarding` is removed from migration `0004`. Every
   registry call is already in `AbdmOutboundRequest`, so the table added no audit value.
3. **1 card.** The setup page shows 1 "Health Facility Registry" card. Not linked: the finder (lookup,
   search) and the wizard entry. Linked: the registry record read-only, "Link a different record"
   (the finder again), the HIP name (the 1 typed field), the issued HIP ID, "Register as HIP and HIU",
   the bridge status line, the programme OTP. The ADR-007 identity card is gone.
4. **"Add a facility" replaces the host sheet.** The manifest declares
   `overrides: [{component: "AddFacilitySheet", replacement}]`; the replacement is a button that opens
   the wizard at `/organization/:organizationId/abdm/facilities/new`. The deployment must name
   `AddFacilitySheet` in the host build variable `REACT_MFE_REGISTERED_COMPONENTS`, or the host keeps
   its own sheet. No host code changes.
5. **The wizard has 3 ways in**, chosen first: *already in the registry* (find, pick, Care form filled
   from the record, create and link in 1 call); *not in the registry yet* (Care form, create, then the
   5 HFR steps embedded, then the services); *Care only* (Care form, create, done). The Care facility is
   created **first** in the register path, so the resumable state has a home. The URL carries
   `mode`, `facility` and `step`; a refresh resumes.
6. **Geo by name.** The record's state and district names are matched to Care government organizations
   by name (case-insensitive); the person picks the local body and the ward. No LGD codes exist in
   Care to match on (findings N14).
7. **Facility type is a suggestion.** `nhpr.rules.suggest_care_facility_type` maps the record's type text
   and ownership to a Care type name (labs, telemedicine, government sub-types by name, private hospital,
   else "Other"); the person confirms it in the form (findings N13).
8. ~~An ABDM organization tab~~ **Withdrawn the same day** (Rithvik: "we don't need to keep ABDM as
   a tab in the organization tabs"). The readiness overview and the "Add a facility" entry live on the
   ABDM admin dashboard's **Facilities** card (`/admin/abdm`), which now lists every facility, linked or
   not, with counts, a filter, columns Registry / Services / Problem and the setup link. The wizard is an
   app route, `/abdm/facilities/new`, with `?organization=<id>` as optional geo context; the admin
   dashboard opens it by a full page load (findings J7), the organization page override by a client-side
   move. The create, search and prefill routes are organization-less.
9. **Field help on every M4 field.** `NhprField` resolves `abdm_nhpr_help_<label key>_{title,what,how,
   example}` from the locale when present; 125 fields have text written from the NHPR pages.

## Design

**Backend.** `facility/service.py`: `EDITABLE_FIELDS = (hip_name, counters)`; `set_registry_link(facility,
record, user)` (writes id, name, snapshot, a default HIP name, forgets the HIP ID when the id changes);
`get_onboarding` / `save_onboarding`; `is_linked`. `nhpr/facility.py`: the onboarding functions take the
facility and a state dict, save after every call. `nhpr/rules.py`: `care_prefill`,
`suggest_care_facility_type`, `is_government` (pure). `facility/create.py`: `form_options` (Care's
`FACILITY_TYPES` and `FacilityFeature`), `geo_suggestions`, `prefill`, `create_facility` (runs
`FacilityViewSet.handle_create` in-process; Care's pydantic errors come back in Care's own
`{"errors": [{loc, msg}]}` shape; a browser-sent `extensions` is dropped; a registry id already linked
elsewhere is refused before any create), `list_facilities` (Care's own visibility rules).

**Routes.** `GET care/facility-form-options`; `GET hfr/search` (`?facility_id=` or
`?name=&state=&district=&page=`); `GET hfr/prefill?facility_id=`; `POST facilities`
(`{care, registry_id?, hip_name?, organization?}`). All 3 need `can_create_facility`. The facility list
with ABDM state is part of `GET admin/overview` (`facility/create.list_facilities`, Care's visibility).

**Frontend.** `registry-card.tsx` (the merged card; exports `RegistryFinder` and `RegistryRecord`),
`add-facility-wizard.tsx` (route), `care-facility-form.tsx` + `care-facility-draft.ts` (the Care form
and its validation), `geo-organization-picker.tsx` (cascading, from `GET /api/v1/govt/organization/?parent=`),
`add-facility-sheet-override.tsx` (`overrides`; `AddFacilityButton`), the admin dashboard's `FacilitiesCard`
(counts, filter, `ProblemBadge` tooltip, sideways scroll),
`nhpr-field.tsx` + `useNhprHelp` (field help), `hfr-onboarding-wizard.tsx` gains `embedded` and
`onSubmitted`. `hfr-card.tsx` is deleted. `AbdmFacilityConfigUpdate` is `{hip_name, counters}`.

## Consequences

- 0 new tables; migration `0004` now creates 3 tables. A local database that applied the earlier
  `0004` must roll back to `0003` and re-apply (`04-dev-setup.md`).
- The M2 and M3 smokes link through the registry mock instead of a typed `PUT`.
- A registry name with characters outside the ADR-007 typed-name rule is accepted as-is: it is the
  registry's value. `validate_facility_name` stays for typed names only.
- The override needs a host build setting. Until a deployment sets it, the host "Add facility" sheet
  stays on the organization page; the ABDM admin dashboard is the entry in that case.
- Problem text on the admin dashboard is a code badge with a tooltip: ABDM's sentences can run to 100
  characters and used to widen the facility column past the card (Rithvik's screenshot, 2026-09-19).
- The wizard's register path depends on the M4 facts still unconfirmed on the sandbox (ADR-015 N1,
  N7, N8). `03-roadmap.md` Phase 5 lists the proofs.

## Amendments

- 2026-09-21: the finder's name search takes the name, the LGD state and the ownership (Government,
  Private, Public-Private-Partnership). The registry refuses a name search without the state or the
  ownership (HTTP 422 HIS-1070, `findings.md` N16), so the plug refuses it first and Search enables only
  when all 3 are set. A facility linked before this ADR (id and name, no `hfr` record) gets its registry
  record on the first `GET` of the setup page. Decision 3 stands.

