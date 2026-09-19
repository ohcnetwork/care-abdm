# 02 — CARE host contract (what a plug can actually hook into)

Everything here was read from the host checkouts on 2026-09-09. Slot line
numbers were re-read on 2026-09-10.

## Frontend host: `~/ohc.network/care_fe`

### How a remote is loaded
- `src/PluginEngine.tsx:73-79` fetches enabled plugs from the backend
  (`plug_config` API). Each config has `slug` and `meta.url`.
- `src/PluginEngine.tsx:46-55` registers a module-federation remote under the
  slug at `meta.url` and imports `./manifest` from it. **The manifest is the
  entire contract.** A broken import logs to console and renders nothing.
- Local dev: `virtual:care-local-plugins` (`PluginEngine.tsx:26,30`) lets a
  local checkout be served without the backend registering it.
- Host `shared:` list (`vite.config.mts:443-451`): `react`, `react-dom`,
  `react-i18next`, `@tanstack/react-query`, `raviger`, `sonner`, `decimal.js`.
  The plug's federation config must share the same set.
- Globals the plug may consume (`src/index.tsx:19-28`): `window.CARE_API_URL`,
  `window.AuthUserContext`.

### Manifest shape — `src/pluginTypes.ts:202-220`
```
plugin: string
routes?: AppRoutes
extends?: ("DoctorConnectButtons" | "PatientExternalRegistration")[]
navItems? / billingNavItems? / userNavItems? / adminNavItems?: NavigationLink[]
organizationTabs?: PluginOrganizationTab[]
components?: PluginComponentMap        // keyed slots, lazy components
encounterTabs?: Record<string, Lazy<FC<PluginEncounterTabProps>>>
encounterFileTabs?: Record<string, Lazy<FC<FilesTabsProps>>>
devices?: PluginDeviceManifest[]
overrides?: PluginOverride[]
```

### Component slots relevant to ABDM — `src/pluginTypes.ts:131-150`, props at 30-97
| Slot | Props | Where the host renders it | ABDM use |
|---|---|---|---|
| `PatientRegistrationForm` | `{form, facilityId?, patientId?, submitForm?}` | `components/Patient/PatientRegistration.tsx:410-413` | M1: create/verify ABHA during registration, write ABHA address into the patient |
| `PatientDetailsTabDemographyGeneralInfo` | `{facilityId, patientId, patientData}` | `components/Patient/PatientDetailsTab/Demography.tsx:172-176` | Show ABHA number/address, link status, card download |
| `PatientHomeActions` / `PatientHomeQuickActions` | `{patient, facilityId?}` | `components/Patient/PatientProfile.tsx:177-180` | "Link ABHA", "Link care context" actions |
| `PatientSearchActions` | `{facilityId}` | `components/Patient/PatientIndex.tsx:259-262` | "Find patient by ABHA / scan QR" entry point |
| `EncounterActions` / `PatientInfoCardQuickActions` | `{encounter}` | `pages/Encounters/tabs/overview/summary-panel-actions.tab.tsx:93-97`; `pages/Encounters/EncounterShow.tsx:240-244` | M2: link this encounter as a care context |
| `FacilityHomeActions` | `{facility}` | `components/Facility/FacilityHome.tsx:253-256` | M4: facility HFR ID status / bridge callback registration |
| `encounterTabs` | `PluginEncounterTabProps` (`pluginTypes.ts:212-214`) | `pages/Encounters/EncounterShow.tsx:80` | M3: consent requests + fetched records tab |
| `extends: ["PatientExternalRegistration"]` | — | `pluginTypes.ts:199-200`; verify consumer before use | possibly the sanctioned hook for external-identity registration |

Everything else in that table is a hypothesis about *fit*, not about the slot
existing — the slots exist (cited). Which ones we use is decided in ADR-003.

### Reference MFE: `~/ohc.network/care_token_display_fe`
The user's instruction is to copy this and refactor: it has Care UI
(careui.ohc.network) styling working. Layout observed:
`src/manifest.tsx` (plugin, routes, devices, components), `src/index.tsx`,
`src/lib/{careApi,request}.ts`, `src/hooks/use-translation.ts`,
`src/components/common/{plugin-component,trans}.tsx`, `src/components/ui/*`
(shadcn-style; per the CPE house rule these get replaced by Care UI registry
items, fetched from `https://careui.ohc.network/registry/care-ui/<name>/<name>.json`),
`public/locale/en.json`, `scripts/postcss-scope-plugin.ts`, `vite.config.ts`,
Tailwind v4 via `@tailwindcss/vite`.

## Backend host: `~/ohc.network/care`

- Plugs are listed in `plug_config.py` (`plugs = [Plug(name, package_name, version, configs)]`)
  or via `ADDITIONAL_PLUGS` env (JSON, same shape) — `plugs/manager.py:19-27`.
- `manager.install()` pip-installs them (`plugs/manager.py:29-34`).
- `config/settings/base.py:142-149`: `PLUGIN_APPS = manager.get_apps()` is
  appended to `INSTALLED_APPS`; `PLUGIN_CONFIGS = manager.get_config()`.
- `config/urls.py:111-112`: for each plug, `path(f"api/{plug}/", include(f"{plug}.urls"))`.
  So a plug named `abdm` gets `/api/abdm/...` for free by shipping `abdm/urls.py`.
  **This is where ABDM callbacks land** (publicly reachable path under the Care API host).
- Plugin settings pattern: copy `care_token_display/src/token_display/settings.py`
  (`PluginSettings` reading `settings.PLUGIN_CONFIGS[plugin]` then env, with
  `required_settings`). ABDM needs at minimum `ABDM_CLIENT_ID`,
  `ABDM_CLIENT_SECRET`, `ABDM_GATEWAY_URL`, `ABDM_HSP_URL`, `ABDM_ABHA_URL`,
  `ABDM_CM_ID`, plus the public callback base URL.
- Registries available in `care/emr/registries/`: `device_type`,
  `care_valueset`, `extensions` (`ExtensionRegistry.register`),
  `system_questionnaire`. Read `extensions/registry.py` before deciding whether
  ABDM identity is an "extension" of Patient.
- `care/emr/models/patient.py:46-47`: `Patient.instance_identifiers` (JSON list)
  and `facility_identifiers` (JSON dict); `PatientIdentifierConfig` at :162.
  Candidate home for the ABHA number/address — decide in ADR-004 after reading
  how `PatientIdentifierConfig` is consumed.
- `apps.py::ready()` does registrations; import Care modules inside `ready()`
  only (`care_token_display/src/token_display/apps.py:15-25`).
- Packaging: `pyproject.toml` with `[tool.uv] package = true`, src layout,
  `dependencies = ["django","celery","djangorestframework","pydantic"]`.
  Celery is available in-process — that is where M2 background work
  (link, data push within the 20-minute window) belongs.

## Phase 3 host facts re-read on 2026-09-10

### Encounter data that M2 can use

| Host fact | Source |
|---|---|
| `Encounter` has `status`, `status_history`, `encounter_class`, `patient`, `period`, `facility`, `discharge_summary_advice`, and `extensions`. | `~/ohc.network/care/care/emr/models/encounter.py:8-37` |
| The API enum has status values `planned`, `in_progress`, `on_hold`, `discharged`, `completed`, `cancelled`, `discontinued`, `entered_in_error`, and `unknown`. | `~/ohc.network/care/care/emr/resources/encounter/constants.py:4-13` |
| The API enum has encounter class values `imp`, `amb`, `obsenc`, `emer`, `vr`, and `hh`. | `~/ohc.network/care/care/emr/resources/encounter/constants.py:28-35` |
| Encounter create validates `patient`, `facility`, and `encounter_class`, then writes a status history row. | `~/ohc.network/care/care/emr/resources/encounter/spec.py:72-97` |

### Shareable CARE records by Encounter

| CARE model | Relationship | ABDM design use | Source |
|---|---|---|---|
| `Observation` | `patient` and `encounter` FK | `WellnessRecord`, `OPConsultation`, `DiagnosticReport` input | `~/ohc.network/care/care/emr/models/observation.py:6-15` |
| `MedicationRequestPrescription` | `encounter` and `patient` FK | Prescription group | `~/ohc.network/care/care/emr/models/medication_request.py:9-18` |
| `MedicationRequest` | `patient` and `encounter` FK | Prescription group | `~/ohc.network/care/care/emr/models/medication_request.py:31-41` |
| `DiagnosticReport` | `patient` and `encounter` FK | Diagnostic report group | `~/ohc.network/care/care/emr/models/diagnostic_report.py:6-20` |
| `Condition` | `patient` and `encounter` FK | OP consult problem list input | `~/ohc.network/care/care/emr/models/condition.py:6-14` |
| `AllergyIntolerance` | `patient` and `encounter` FK | OP consult allergy input | `~/ohc.network/care/care/emr/models/allergy_intolerance.py:6-13` |
| `ServiceRequest` | `patient` and `encounter` FK | Diagnostic order or OP consult input | `~/ohc.network/care/care/emr/models/service_request.py:7-22` |
| `FormSubmission` and `QuestionnaireResponse` | `patient` and `encounter` FK | Form-based clinical input | `~/ohc.network/care/care/emr/models/questionnaire.py:47-72` |
| `FileUpload` | `associating_id`, `file_type`, `file_category` | Simple FHIR bundles for patient, encounter, diagnostic, and service-request files | `~/ohc.network/care/care/emr/models/file_upload.py:13-18`; `~/ohc.network/care/care/emr/resources/file_upload/spec.py:14-29` |
| Discharge summary report | `associating_model=Encounter` | Simple `DischargeSummary` bundle | `~/ohc.network/care/care/emr/reports/report_types.py:12-18` |

No model named `Immunization` or `Procedure` was found under `care/emr/models/` on this pass. Treat those as mapping gaps until Rithvik selects a source.

### Celery pattern

| Host fact | Source |
|---|---|
| Care creates a Celery app named `care`, loads settings with the `CELERY_` namespace, sets timezone, and autodiscovers tasks. | `~/ohc.network/care/config/celery_app.py:8-18` |
| Care uses `@shared_task` for tasks. | `~/ohc.network/care/care/emr/tasks/cleanup_incomplete_file_uploads.py:14-20` |
| Care uses `autoretry_for`, `retry_kwargs`, and `expires` for report jobs. | `~/ohc.network/care/care/emr/tasks/report_generation.py:12-14` |
| Care registers periodic tasks with `current_app.on_after_finalize` and `sender.add_periodic_task`. | `~/ohc.network/care/care/emr/tasks/__init__.py:12-31` |

### Facility extension and rendering facts

| Host fact | Source |
|---|---|
| `ExtensionResource` includes `facility`. | `~/ohc.network/care/care/emr/extensions/base.py:10-19` |
| `Facility` has an `extensions` JSON field. | `~/ohc.network/care/care/facility/models/facility.py:199-203` |
| `FacilityBareMinimumSpec` sets `___extension_resource_type__ = ExtensionResource.facility`. | `~/ohc.network/care/care/emr/resources/facility/spec.py:36-41` |
| `FacilityCreateSpec` validates extensions. | `~/ohc.network/care/care/emr/resources/facility/spec.py:131-135` |
| `FacilityReadSpec` renders list extensions, and `FacilityRetrieveSpec` renders retrieve extensions. | `~/ohc.network/care/care/emr/resources/facility/spec.py:176-201` |
| The frontend drops extension fields when `x-ui.render_blacklist` contains the context. | `~/ohc.network/care_fe/src/Utils/schema/extensionSchema.ts:472-483` |
| care_fe has no facility-settings plug slot on this pass. `FacilityHomeActions` is the only facility-level component slot. | `~/ohc.network/care_fe/src/pluginTypes.ts:50-53,131-150`; `~/ohc.network/care_fe/src/components/Facility/FacilityHome.tsx:253-257` |

### Plug routes (read 2026-09-10)

| Host fact | Source |
|---|---|
| The host merges plug routes into its router, then its own routes. A host route wins a collision. | `~/ohc.network/care_fe/src/Routers/AppRouter.tsx:104-115` |
| A route value is a function that takes the path parameters and returns a node. | `~/ohc.network/care_fe/src/Routers/AppRouter.tsx:60-73` |
| The host claims `/facility/:facilityId/settings*`, so a plug page must stay outside that prefix. | `~/ohc.network/care_fe/src/Routers/routes/FacilityRoutes.tsx:46` |
| The host wraps a slot component in `Suspense` and an error boundary, but not a route node. A lazy page must add its own boundary. | `~/ohc.network/care_fe/src/PluginEngine.tsx:200-215`; `~/ohc.network/care_fe/src/Routers/AppRouter.tsx:117` |
| The host renders `FacilityHomeActions` inside the "Configurations" dropdown popup. The popup is a transformed ancestor, so a `position: fixed` panel in that subtree anchors to the popup and not to the viewport. | `~/ohc.network/care_fe/src/components/Facility/FacilityHome.tsx:236-257` |
| `GET /api/v1/facility/{facilityId}/` returns the facility. The setup page reads the name from it. | `~/ohc.network/care_fe/src/types/facility/facilityApi.ts:34-38` |

### Errors from a plug signal (read 2026-09-19)

| Host fact | Source |
|---|---|
| A plug's `post_save` receiver runs inside Care's patient viewset. An exception the host handler does not know becomes HTTP 500, and the desk reads "Something went wrong". | `~/ohc.network/care/care/emr/api/viewsets/base.py:26-56`; `~/ohc.network/care_fe/src/Utils/request/errorHandler.ts:65` |
| The host passes a DRF `ValidationError` whose `detail` is a dict that holds `errors` through unchanged, as HTTP 400. A plug refusal must use that shape. | `~/ohc.network/care/care/emr/api/viewsets/base.py:44-47` |
| care_fe shows a string `errors` value in a toast. A list of `{type, msg}` objects gives 1 toast for each entry. | `~/ohc.network/care_fe/src/Utils/request/errorHandler.ts:104-127,143-158` |
| `perform_create` wraps the model save in `transaction.atomic()`, so an exception from a receiver rolls the patient create back. The host handler itself calls no `set_rollback`. | `~/ohc.network/care/care/emr/api/viewsets/base.py:95-98` |

### Admin routes and nav (read 2026-09-14; used by `/admin/abdm`)

| Host fact | Source |
|---|---|
| The manifest type accepts `adminNavItems?: NavigationLink[]`. | `~/ohc.network/care_fe/src/pluginTypes.ts:220-227` |
| `NavigationLink` has `name`, `url`, optional `icon`, optional `section`, and optional children. | `~/ohc.network/care_fe/src/components/ui/sidebar/nav-main.tsx:62-72` |
| The admin sidebar appends each plug `adminNavItems` entry after the core admin links. | `~/ohc.network/care_fe/src/components/ui/sidebar/admin-nav.tsx:17-105` |
| The app treats any `/admin` path as an admin page and shows the admin sidebar. | `~/ohc.network/care_fe/src/Routers/AppRouter.tsx:132-138` |
| Plug routes merge into the app route table before the host routes. A plug can own `/admin/...` when no host route collides. | `~/ohc.network/care_fe/src/Routers/AppRouter.tsx:121-132` |
| The frontend permission context treats `user.is_superuser` as `isSuperAdmin`. | `~/ohc.network/care_fe/src/Routers/AppRouter.tsx:169-177` |

### Phase 3 frontend slots

| Need | Slot | Mount source |
|---|---|---|
| Link an Encounter as a care context. Props `{encounter, className}`; the host passes an outline-button class. Used by `encounter-actions.tsx`. | `EncounterActions` | `~/ohc.network/care_fe/src/pluginTypes.ts:36-39`; `~/ohc.network/care_fe/src/pages/Encounters/tabs/overview/summary-panel-actions.tab.tsx:93-101`; `~/ohc.network/care_fe/src/components/Encounter/EncounterCommandDialog.tsx:519-529` |
| Add a primary quick action near the patient card. | `PatientInfoCardQuickActions` | `~/ohc.network/care_fe/src/pluginTypes.ts:41-44`; `~/ohc.network/care_fe/src/pages/Encounters/EncounterShow.tsx:238-248` |
| Show link state at the top of the Encounter overview. Props `{encounter, patientId, encounterId}`. Used by `encounter-overview-top.tsx`. | `EncounterOverviewTop` | `~/ohc.network/care_fe/src/pluginTypes.ts:103-107`; `~/ohc.network/care_fe/src/pages/Encounters/tabs/overview.tsx:54-60` |
| Show a consent and transfer log. | `encounterTabs` | `~/ohc.network/care_fe/src/pluginTypes.ts:212-215`; `~/ohc.network/care_fe/src/pages/Encounters/EncounterShow.tsx:80` |
| Show the ADR-007 facility link form. | `FacilityHomeActions` | `~/ohc.network/care_fe/src/pluginTypes.ts:50-53`; `~/ohc.network/care_fe/src/components/Facility/FacilityHome.tsx:253-257` |

### M3 host facts (read 2026-09-19; ADR-014)

| Host fact | Source |
|---|---|
| `User.doctor_medical_council_registration` (CharField 255, nullable) is the clinician's council registration. The consent `requester.identifier` sends it when set. | `~/ohc.network/care/care/users/models.py:158-163` |
| `can_view_clinical_data(user, patient)` is the patient-level gate for clinical data; a superuser passes. Every HIU route uses it. | `~/ohc.network/care/care/security/authorization/patient.py:94-101` |
| The encounter tab receives `{encounter: EncounterRead, patient: PatientRead}`; `encounter.facility.id` and `patient.id` feed the HIU card. | `~/ohc.network/care_fe/src/pages/Encounters/EncounterShow.tsx:49-52` |
| care_fe has no patient-level tab slot; the Demography slot and the encounter tabs are the 2 patient surfaces. | `~/ohc.network/care_fe/src/pluginTypes.ts:157,231-233` |

### Callback ingress and auth

| Host fact | Source |
|---|---|
| Care mounts plug URLs at `api/{plug}/`, so the `abdm` plug owns `/api/abdm/...`. | `~/ohc.network/care/config/urls.py:111-112` |
| DRF defaults include `CustomJWTAuthentication`, `CustomBasicAuthentication`, `SessionAuthentication`, and `TokenAuthentication`. | `~/ohc.network/care/config/settings/base.py:366-375` |
| DRF defaults require `IsAuthenticated` and `CareAuthentication`. | `~/ohc.network/care/config/settings/base.py:376-379` |

Therefore, gateway callback views must set `AllowAny` and must run ABDM signature checks inside the plug.
