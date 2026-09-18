"""
FHIR R4 document bundles for the ABDM HI types this plug can serve.

Contract (used by abdm/hip/sharing.py and abdm/hip/transfer.py):
  HI_TYPE_PROFILES                     hiType -> NRCES profile URL (MCP list_fhir_profiles, 2026-09-15)
  available_hi_types(enc)              the HI types that have data for this Encounter (a check that a
                                       bundle can be built; ADR-013 moved the sharing decision to the
                                       staged items)
  build_bundle(enc, hi_type, source_ids=None)
                                       a `Bundle` of type `document` as a dict. `source_ids` limits
                                       the records to the linked share items of that type (ADR-013):
                                       prescription ids, diagnostic report ids, report upload ids.
                                       None = every shareable record. Raises BundleError when there
                                       is no data.

Rules every bundle keeps (/docs/hiecm/v3/concepts/fhir, MCP get_fhir_profile DocumentBundle):
  Bundle.type = document; Bundle.meta.versionId, Bundle.meta.lastUpdated, Bundle.meta.profile
  = DocumentBundle URL; Bundle.identifier.system + value; Bundle.timestamp; the first entry is
  the Composition whose meta.profile is the record profile; every entry.fullUrl is `urn:uuid:<id>`
  and every reference points at one of them (the NRCES IG examples use this form).

Record types after this pass: DiagnosticReport (structured), WellnessRecord, ImmunizationRecord,
Invoice. HealthDocumentRecord was removed on 2026-09-18 (Rithvik). Add a builder module and
register it in `_builders()`.
"""

HI_TYPE_PROFILES = {
    "OPConsultation": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord",
    "Prescription": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord",
    "DischargeSummary": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/DischargeSummaryRecord",
}


class BundleError(Exception):
    """The Encounter has no data for the requested HI type, or a required field is missing."""


def _builders() -> dict:
    # Imported lazily: the builder modules import Care models.
    from abdm.fhir import discharge_summary, op_consult, prescription

    return {
        "OPConsultation": op_consult,
        "Prescription": prescription,
        "DischargeSummary": discharge_summary,
    }


def available_hi_types(encounter) -> list[str]:
    builders = _builders()
    return [hi_type for hi_type in HI_TYPE_PROFILES if builders[hi_type].has_data(encounter)]


def build_bundle(encounter, hi_type: str, source_ids: list[int] | None = None) -> dict:
    builders = _builders()
    if hi_type not in builders:
        raise BundleError(f"No bundle builder for HI type {hi_type}")
    return builders[hi_type].build(encounter, source_ids=source_ids)
