"""Prescription HI type builder for ABDM NRCES FHIR R4 bundles."""

from __future__ import annotations

from django.utils import timezone

from abdm.fhir import HI_TYPE_PROFILES, BundleError
from abdm.fhir.bundle import (
    CARE_BUNDLE_SYSTEM,
    DOCUMENT_BUNDLE_PROFILE,
    composition,
    condition_resource,
    fhir_datetime,
    medication_request_resource,
    new_bundle,
    organization_resource,
    patient_resource,
    practitioner_resource,
    reference,
    section,
    snomed,
)

EXCLUDED_STATUSES = {"cancelled", "entered_in_error", "entered-in-error"}


def _medication_requests(encounter):
    from care.emr.models.medication_request import MedicationRequest

    return MedicationRequest.objects.filter(encounter=encounter, do_not_perform=False).exclude(
        status__in=EXCLUDED_STATUSES
    )


def has_data(encounter) -> bool:
    return _medication_requests(encounter).exists()


def _first_author(encounter, requests):
    for request in requests:
        if request.requester_id:
            return request.requester
        if request.prescription_id and request.prescription.prescribed_by_id:
            return request.prescription.prescribed_by
    return getattr(encounter, "created_by", None)


def _patient_resource(encounter, timestamp):
    from abdm.care_seams import AbhaAddressIdentifier, AbhaNumberIdentifier

    patient = encounter.patient
    return patient_resource(
        patient,
        timestamp=timestamp,
        abha_number=AbhaNumberIdentifier.get(patient),
        abha_address=AbhaAddressIdentifier.get(patient),
    )


def build(encounter) -> dict:
    """Build a PrescriptionRecord bundle from CARE MedicationRequest rows."""
    requests = list(_medication_requests(encounter).select_related("requester", "prescription__prescribed_by"))
    if not requests:
        raise BundleError("Encounter has no prescription data")

    from abdm.facility.service import hip_id_for

    timestamp = timezone.now()
    hip_id = hip_id_for(encounter.facility)
    patient = _patient_resource(encounter, timestamp)
    patient_ref = reference(patient, getattr(encounter.patient, "name", "") or "Patient")
    organization = organization_resource(encounter.facility, hip_id=hip_id, timestamp=timestamp)
    org_ref = reference(organization, getattr(encounter.facility, "name", "") or "Organization")

    author = _first_author(encounter, requests)
    practitioner = practitioner_resource(author, timestamp=timestamp) if author else None
    author_ref = reference(practitioner, "Practitioner") if practitioner else org_ref

    diagnosis_resources, diagnosis_refs = _diagnosis_resources(encounter, patient_ref)
    medication_resources = [
        medication_request_resource(
            request, patient_ref=patient_ref, requester_ref=author_ref, reason_refs=diagnosis_refs[:1]
        )
        for request in requests
    ]
    medication_refs = [reference(resource, "MedicationRequest") for resource in medication_resources]
    date_value = min((request.authored_on for request in requests if request.authored_on), default=timestamp)
    comp = composition(
        profile_url=HI_TYPE_PROFILES["Prescription"],
        type_code="440545006",
        type_display="Prescription record",
        subject_ref=patient_ref,
        date_value=date_value,
        author_refs=[author_ref],
        title="Prescription record",
        sections=[
            section(
                title="Prescription record",
                code=snomed("440545006", "Prescription record"),
                entries=medication_refs,
            )
        ],
        attester_ref=org_ref,
        timestamp=timestamp,
    )
    resources = [
        patient,
        *(list(filter(None, [practitioner]))),
        organization,
        *medication_resources,
        *diagnosis_resources,
    ]
    return new_bundle(
        DOCUMENT_BUNDLE_PROFILE,
        comp,
        resources,
        hip_system=CARE_BUNDLE_SYSTEM,
        hip_id=str(hip_id),
        timestamp=fhir_datetime(timestamp),
    )


def _diagnosis_resources(encounter, patient_ref):
    from care.emr.models.condition import Condition

    conditions = list(Condition.objects.filter(encounter=encounter, category="encounter_diagnosis")[:1])
    resources = [condition_resource(condition, patient_ref=patient_ref) for condition in conditions]
    refs = [reference(resource, "Condition") for resource in resources]
    return resources, refs
