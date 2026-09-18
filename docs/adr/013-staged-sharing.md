# ADR-013 — Staged sharing: what a care context links, and when

Status: Accepted (Rithvik, 2026-09-18)
Date: 2026-09-18
Amends: ADR-011 §3 and §4 (the Encounter `post_save` link and the `hi_types` snapshot).
Keeps: 1 Encounter = 1 care context; the reference number = `Encounter.external_id`; the link
call and its callbacks (F7, F8, F9); ADR-012 error handling.

## Context

Until now the plug linked a care context as soon as the Encounter existed, with every HI type that
had data at that moment (`available_hi_types`). A prescription written after the link was not
announced until the Encounter status changed or the desk pressed the button. The desk could not
see which records ABDM knew about and which it did not.

Rithvik's decisions (2026-09-18):

1. Nothing is linked when a clinician writes a record. The record is **staged**.
2. The desk sees the staged and the linked records in an **ABDM tab** on the Encounter and can
   select staged records and link them.
3. When the Encounter is **completed or discharged**, every staged record is linked.
4. Retries: hourly, up to 3 times; both values configurable.
5. Mapping: `OPConsultation` only for `encounter_class == "amb"`, staged at the first clinical
   record; `Prescription` = `MedicationRequestPrescription` with `status != draft`;
   `DiagnosticReport` = `DiagnosticReport` with `status == final`; `DischargeSummary` =
   `ReportUpload(report_type="discharge_summary")` once uploaded; **no** `HealthDocumentRecord`.

ABDM facts that shape the design (all measured on the sandbox, `findings.md`):

| Fact | Finding |
|---|---|
| The link call carries 1 `patient` block per HI type; 1 call can carry several types; ABDM sends 1 `on_carecontext` callback for the call. | E11, F7 |
| A care context that ABDM already holds answers `ABDM-1056 already linked` on a second link; the plug treats it as success. A later link for the **same** reference with a **new** HI type is how a context gains a type. Whether ABDM keeps or replaces the earlier types is not measured yet. | F4, this ADR §Open |
| A repeat token request inside 7 minutes earns `ABDM-1092`; the plug never sends inside the window. | F6, ADR-012 D3 |
| The notify must wait for ABDM to index the link. | F9 |

Care facts:

| Fact | Source |
|---|---|
| `MedicationRequestPrescription.status` ∈ active, on_hold, ended, stopped, completed, cancelled, entered_in_error, draft. | `care/emr/resources/medication/request_prescription/spec.py:18-26` |
| `DiagnosticReport.status` ∈ registered, partial, preliminary, final; FK `encounter`, `service_request`. | `care/emr/resources/diagnostic_report/spec.py:22-27`, `care/emr/models/diagnostic_report.py` |
| The discharge summary is a generated PDF: `ReportUpload(report_type="discharge_summary", associating_id=str(encounter.external_id), upload_completed=True)`, stored in S3 `BucketType.REPORT`, made by `care/emr/tasks/report_generation.py`. | `care/emr/models/report/report_upload.py`, `care/emr/reports/report_types.py:12-18` |
| Encounter statuses: planned, in_progress, on_hold, discharged, completed, cancelled, discontinued, entered_in_error, unknown. | `care/emr/resources/encounter/constants.py:4-13` |
| Care's action engine fires only after a questionnaire submission and on appointment viewsets (contexts `Appointment`, `Patient`, `EncounterQuestionnaire`, `PatientQuestionnaire`). No Encounter, prescription or report context exists. | `care/action_evaluator/context_engine/contexts/core.py`, `care/emr/api/viewsets/questionnaire/questionnaire.py:364-380`, `action_base.py` |

## Decision

### D1 — One row per shareable record: `AbdmShareItem`

| Field | Meaning |
|---|---|
| `care_context` FK | the Encounter's context (created on the first staged item) |
| `hi_type` | `OPConsultation`, `Prescription`, `DiagnosticReport`, `DischargeSummary` |
| `source_model`, `source_id` | the Care record (`encounter`, `medication_request_prescription`, `diagnostic_report`, `report_upload`) and its pk; unique together with `care_context` and `hi_type` |
| `label` | what the desk reads: "Prescription 18 Sep 2026 10:42" |
| `status` | `staged` → `queued` → `linked`; `failed` after the last retry; `excluded` when the desk removes it |
| `attempts`, `next_attempt_at`, `last_error_code`, `last_error_message` | retry state |
| `link_request` FK, `linked_at` | the accepted link call and the callback time |

`AbdmCareContext.hi_types` is **derived**: the distinct `hi_type` of the context's `linked` items.
It is what discovery advertises and what a health-information request may serve.

### D2 — Stage on `post_save`, never link there

| Signal | Rule | Item |
|---|---|---|
| `MedicationRequestPrescription` | `status != draft` and not `entered_in_error`/`cancelled`; only `MedicationRequest` rows that belong to a prescription count | 1 per prescription |
| `DiagnosticReport` | `status == final` | 1 per report |
| `ReportUpload` | `report_type == "discharge_summary"` and `upload_completed` and not archived | 1 per upload |
| any of the above | `encounter.encounter_class == "amb"` | 1 `OPConsultation` item for the Encounter, created with the first clinical record |
| `Encounter` | `status` becomes `completed` or `discharged` | every `staged` item → `queued`, then 1 link call |

A staged record that is later cancelled, entered in error, drafted again or archived is marked
`excluded` if it was not linked yet. A linked record stays linked: ABDM holds no per-record state
and the docs give no unlink call.

The Encounter `post_save` no longer links on create or on other status changes. The facility must
have a HIP ID and the patient an ABHA address; otherwise the item stays `staged` and the tab says
why.

### D3 — The desk links what it selects

`POST /api/abdm/encounters/<id>/share-items/link` with `{"items": [ids]}` (or `{"all": true}`)
marks the items `queued` and runs the link in Celery. The link call carries every queued type of
the context in 1 call (F7). Its `on_carecontext` callback marks the items `linked`, recomputes
`hi_types`, and schedules the notify (F9). `POST .../share-items/<id>/exclude` marks a staged
item `excluded`; `.../include` brings it back.

### D4 — Retries: hourly, 3 times, configurable

`ABDM_LINK_RETRY_INTERVAL_MINUTES` (default 60) and `ABDM_LINK_MAX_RETRIES` (default 3). A link
call that fails (a refusal, a 5xx, no callback within ADR-012's deadline) sets
`next_attempt_at = now + interval` on its queued items and adds 1 to `attempts`. The periodic task
`abdm.tasks.retry_share_items` (every 5 minutes, Celery beat) re-queues items whose
`next_attempt_at` has passed and `attempts < max`. After the last attempt the item is `failed`
with the ADR-012 failure block; the desk can select it again, which resets the count.

The retry never sends a token request inside the 7-minute window (ADR-012 D3) and treats
`ABDM-1056` as success (F4).

### D5 — The ABDM tab

`encounterTabs["abdm"]` (host slot `pluginTypes.ts:212-215`). One page: the care-context header
(display, reference, link state, notify state), the items table (label, HI type, status, attempts,
next attempt, error, checkbox), the actions "Link selected" and "Exclude"/"Include", and the
gateway activity list. The `EncounterActions` button opens this tab instead of its own dialog;
`EncounterOverviewTop` keeps the 1-line status.

### D6 — Care's actions are not the seam

The action engine evaluates rules only after a questionnaire submission and on appointment
viewsets; a plug can register an instruction, but there is no Encounter, prescription or report
context where it would fire. Staging therefore uses `post_save` signals, like the M1 identifier
link. A later `abdm_stage` instruction for form-based OP consults is possible and separate.

## Open (to measure on the sandbox)

- Whether a second link for the same care context reference with a new HI type **adds** the type
  at ABDM or answers `ABDM-1056` and keeps the old set. If it keeps the old set, the plug must send
  every linked type again in each link call. Until measured, the plug sends all linked + queued
  types of the context in every link call, which is correct in both cases.

## Consequences

- `available_hi_types()` is no longer the trigger; it stays as the FHIR-time check that a bundle
  can be built. The FHIR builders for `Prescription` and `DischargeSummary` build from the staged
  record set of the context, not from every record on the Encounter.
- Migration 0003 adds `AbdmShareItem`; existing `AbdmCareContext.hi_types` values are kept as
  linked items with `source_model="encounter"` so the sandbox history stays readable.
- `HealthDocumentRecord` code is removed (Rithvik, 2026-09-18).
