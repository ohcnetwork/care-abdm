import unittest
from datetime import date, datetime, timezone
from types import SimpleNamespace

from abdm.fhir.bundle import (
    CARE_BUNDLE_SYSTEM,
    DOCUMENT_BUNDLE_PROFILE,
    codeable,
    composition,
    fhir_datetime,
    gender_code,
    new_bundle,
    organization_resource,
    patient_resource,
    reference,
    section,
    snomed,
    uuid_ref,
)


class FhirBundleHelperTests(unittest.TestCase):
    def test_gender_mapping_uses_fhir_administrative_gender(self):
        self.assertEqual(gender_code("male"), "male")
        self.assertEqual(gender_code("female"), "female")
        self.assertEqual(gender_code("transgender"), "other")
        self.assertEqual(gender_code("non_binary"), "other")
        self.assertEqual(gender_code(""), "unknown")

    def test_datetime_formatting_keeps_timezone_and_dates(self):
        dt = datetime(2026, 9, 15, 6, 30, tzinfo=timezone.utc)
        self.assertEqual(fhir_datetime(dt), "2026-09-15T06:30:00+00:00")
        self.assertEqual(fhir_datetime(date(2026, 9, 15)), "2026-09-15")

    def test_codeable_maps_care_coding_json(self):
        self.assertEqual(
            codeable({"system": "http://snomed.info/sct", "code": "123", "display": "Example"}),
            {
                "coding": [{"system": "http://snomed.info/sct", "code": "123", "display": "Example"}],
                "text": "Example",
            },
        )

    def test_patient_resource_wires_care_and_abha_identifiers(self):
        patient = SimpleNamespace(
            external_id="patient-1",
            name="Test Patient",
            phone_number="+919999999999",
            gender="male",
            date_of_birth=date(1990, 1, 2),
            address="Test address",
            pincode=682001,
        )
        resource = patient_resource(patient, abha_number="12-3456-7890-1234", abha_address="test@sbx")
        identifiers = resource["identifier"]
        self.assertIn({"system": "https://care.ohc.network/patient", "value": "patient-1"}, identifiers)
        self.assertIn(
            {"type": {"text": "ABHA Number"}, "system": "abdm/abha-number", "value": "12-3456-7890-1234"},
            identifiers,
        )
        self.assertEqual(resource["gender"], "male")
        self.assertEqual(resource["birthDate"], "1990-01-02")

    def test_uuid_reference_is_stable_for_resource(self):
        resource = {"resourceType": "Patient", "id": "abc"}
        self.assertEqual(uuid_ref(resource), "urn:uuid:abc")
        self.assertEqual(reference(resource, "Patient"), {"reference": "urn:uuid:abc", "display": "Patient"})

    def test_new_bundle_creates_document_skeleton_with_composition_first(self):
        patient = {"resourceType": "Patient", "id": "patient-id"}
        comp = {"resourceType": "Composition", "id": "comp-id"}
        bundle = new_bundle(DOCUMENT_BUNDLE_PROFILE, comp, [patient], hip_system=CARE_BUNDLE_SYSTEM, hip_id="HIP1")
        self.assertEqual(bundle["resourceType"], "Bundle")
        self.assertEqual(bundle["type"], "document")
        self.assertEqual(bundle["meta"]["profile"], [DOCUMENT_BUNDLE_PROFILE])
        self.assertEqual(bundle["identifier"]["system"], CARE_BUNDLE_SYSTEM)
        self.assertEqual(bundle["entry"][0]["resource"], comp)
        self.assertEqual(bundle["entry"][0]["fullUrl"], "urn:uuid:comp-id")
        self.assertEqual(bundle["entry"][1]["fullUrl"], "urn:uuid:patient-id")

    def test_composition_wires_subject_author_encounter_custodian_and_attester(self):
        facility = SimpleNamespace(external_id="facility-1", name="Facility", phone_number="", address="", pincode=None)
        org = organization_resource(facility, hip_id="HIP1")
        org_ref = reference(org, "Organization")
        comp = composition(
            profile_url="https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord",
            type_code="371530004",
            type_display="Clinical consultation report",
            subject_ref={"reference": "urn:uuid:patient", "display": "Patient"},
            encounter_ref={"reference": "urn:uuid:encounter", "display": "Encounter"},
            date_value="2026-09-15T10:00:00+05:30",
            author_refs=[org_ref],
            title="Clinical Consultation report",
            custodian_ref=org_ref,
            attester_ref=org_ref,
            sections=[section(title="Medical History", code=snomed("371529009", "History and physical report"))],
        )
        self.assertEqual(comp["status"], "final")
        self.assertEqual(comp["subject"]["reference"], "urn:uuid:patient")
        self.assertEqual(comp["encounter"]["reference"], "urn:uuid:encounter")
        self.assertEqual(comp["custodian"], org_ref)
        self.assertEqual(comp["attester"][0]["party"], org_ref)


if __name__ == "__main__":
    unittest.main()
