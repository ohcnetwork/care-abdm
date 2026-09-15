"""
FHIR R4 document bundles for the ABDM HI types this plug can serve.

Contract (used by abdm/hip/contexts.py and abdm/hip/transfer.py):
  HI_TYPE_PROFILES           hiType -> NRCES profile URL (MCP list_fhir_profiles, 2026-09-15)
  available_hi_types(enc)    the HI types that have data for this Encounter, in HI_TYPE_PROFILES order
  build_bundle(enc, hi_type) a `Bundle` of type `document` as a dict; raises BundleError when
                             the Encounter has no data for that type

Rules every bundle keeps (/docs/hiecm/v3/concepts/fhir, MCP get_fhir_profile DocumentBundle):
  Bundle.type = document; Bundle.meta.versionId, Bundle.meta.lastUpdated, Bundle.meta.profile
  = DocumentBundle URL; Bundle.identifier.system + value; Bundle.timestamp; the first entry is
  the Composition whose meta.profile is the record profile; every entry.fullUrl is `urn:uuid:<id>`
  and every reference points at one of them (the NRCES IG examples use this form).

Record types after this pass (ADR-011): DiagnosticReport, DischargeSummary, WellnessRecord,
ImmunizationRecord, Invoice. Add a builder module and register it in BUILDERS.
"""

HI_TYPE_PROFILES = {
    "OPConsultation": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord",
    "Prescription": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord",
    "HealthDocumentRecord": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/HealthDocumentRecord",
}


class BundleError(Exception):
    """The Encounter has no data for the requested HI type, or a required field is missing."""


def _builders() -> dict:
    # Imported lazily: the builder modules import Care models.
    from abdm.fhir import health_document, op_consult, prescription

    return {
        "OPConsultation": op_consult,
        "Prescription": prescription,
        "HealthDocumentRecord": health_document,
    }


def available_hi_types(encounter) -> list[str]:
    builders = _builders()
    return [hi_type for hi_type in HI_TYPE_PROFILES if builders[hi_type].has_data(encounter)]


def build_bundle(encounter, hi_type: str) -> dict:
    builders = _builders()
    if hi_type not in builders:
        raise BundleError(f"No bundle builder for HI type {hi_type}")
    return builders[hi_type].build(encounter)
