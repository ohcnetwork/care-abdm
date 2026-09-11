# ADR-004 — Data model: use Care's identifiers and extensions; plug tables only for what they cannot hold

Status: Proposed (Rithvik asked for core concepts first; flag what doesn't fit)
Date: 2026-09-09

## What Care core offers (read 2026-09-09)

**Patient identifiers** — `care/emr/models/patient.py:162-176`.
`PatientIdentifierConfig(facility nullable, config JSON)` + `PatientIdentifier(patient, config, value indexed)`.
`config` follows `IdentifierConfig` (`care/emr/resources/patient_identifier/spec.py:34-44`):
`use, system, required, unique, regex, display, retrieve_config, default_value, auto_maintained`.
- `facility=None` ⇒ instance-wide identifier (right for ABHA: one identity across all tenants' facilities).
- `auto_maintained=True` ⇒ users cannot set it through create/update
  (`care/emr/api/viewsets/patient.py:138,171,410`); only code writes it. Core itself
  creates such configs from a signal (`care/emr/signals/patient/base.py:41-60`).
- `retrieve_config` makes the identifier searchable through core's existing
  patient search (`viewsets/patient.py:203-260`) — no plug search UI needed.

**Extensions** — `care/emr/extensions/base.py`, `care/emr/registries/extensions/registry.py`.
`Patient.extensions` (`models/patient.py:52`) and `Encounter.extensions`
(`models/encounter.py:37`) are JSON. A plug registers a `PlugExtension`
subclass (`resource_type`, `extension_name`, JSON `write/read/retrieve_schema`,
`validate`, `serialize_*`) via `ExtensionRegistry.register(obj)`. Write payloads
are validated against the registered schema (`extensions/validator.py:7-19`);
read specs render every registered extension (`validator.py:43-70`);
`GET /api/v1/extensions/` lists them for the frontend (`viewsets/extensions.py`).
`ExtensionResource` enum (`base.py:10-18`): account, encounter, patient,
payment_reconciliation, supply_delivery, supply_delivery_order, product,
resource_request, **facility** (added 2026-09-09 in care commit a90aa5981 [ENG-989], `base.py:19`; `Facility.extensions` at `care/facility/models/facility.py:203`).

## Decision

| ABDM datum | Where | Why |
|---|---|---|
| ABHA number (14-digit) | `PatientIdentifierConfig` instance-level, `system="https://abdm-docs.dev.eka.care/abha-number"`* , `auto_maintained=True`, `unique=True`, Luhn regex | core search/display for free; user can't hand-edit an unverified value |
| ABHA address (`x@sbx`) | second identifier config, same pattern | as above |
| ABHA link status / verified-at / KYC-restricted flag / profile snapshot (name, gender, yob, photo ref) | `Patient.extensions["abdm"]` via a registered `PlugExtension` | non-secret, useful to render in host patient views |
| Care-context state per encounter (linked?, linked_at, request-id, ABDM ref) | `Encounter.extensions["abdm"]` via `PlugExtension` | one care context per OPD visit / IPD admission (docs `/concepts/hip-hiu`) maps 1:1 to Encounter |
| Link token (JWT, 6 months), `X-token`s, gateway token cache | plug table `AbdmPatientToken` / cache | secrets; extensions are rendered to the browser |
| Inbound callbacks (raw body, request-id, sig status) | plug table `AbdmCallback` | operational log, see ADR-006 |
| Consent artefacts, HI requests, transfer jobs | plug tables | lifecycle state machines with many rows per patient |
| Facility ↔ ABDM facility ID (HFR) / HIP flags / bridge state | `Facility.extensions["abdm"]` via `PlugExtension` on `ExtensionResource.facility` | pre-M4 form (ADR-007) writes here too; M4 browse-and-link replaces the input, not the storage |

\* `system` URI is our own naming; the docs do not prescribe an identifier system URI. Finding to record.

## Flags for Care core

1. ~~No extension surface on Facility~~ — RESOLVED 2026-09-09: core added `ExtensionResource.facility` and `Facility.extensions` (a90aa5981). No plug-owned `AbdmFacility` model needed.
2. **`validate_extensions` silently drops unknown keys** (`validator.py:16-18`,
   `# TODO: Once stable, raise error`). If the plug isn't installed, writes to
   `extensions.abdm` vanish without error. Acceptable, but worth knowing.
3. Identifier config creation: core does it in a signal for its own configs;
   the plug will create/ensure its two configs in a data migration (idempotent
   on `system`). No registry exists for "identifier providers" — nothing to flag
   unless we want ABHA to be a first-class identifier type in core later.

## Amendment 2026-09-09 — how the ABHA reaches the Patient

Approved by Rithvik ("go ahead with post_save").

- Registration: the plug sets `extensions.abdm.txn_id` on the host form. Core persists it with the
  Patient; a `post_save(Patient)` receiver (`abdm/signals.py`) resolves the txn to the plug's
  `AbhaTransaction` row (server-recorded at claim/select time), writes the two auto-maintained
  identifiers via core's `BasePatientIdentifierConfig`, rebuilds `instance_identifiers`, and
  replaces `txn_id` with `abha_number/abha_address/abha_linked_at/abha_source/kyc_verified`.
  Nothing client-supplied ever becomes an identifier.
- Existing patient: `POST /api/abdm/patients/<id>/abha/link {txn_id}` → same single writer.
- `AbhaTransaction` (plug table) holds the ABDM X-token so the card can be proxied later without a
  new OTP. Aadhaar and OTP values are never stored.
- Extension fields carry `x-ui.render_blacklist` for all form/summary contexts; the plug's own panel
  (`PatientDetailsTabDemographyGeneralInfo` slot) is the display surface.
