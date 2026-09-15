"""OPConsultation HI type builder for ABDM NRCES FHIR R4 bundles."""

from __future__ import annotations

from django.utils import timezone

from abdm.fhir import HI_TYPE_PROFILES, BundleError
from abdm.fhir.bundle import (
    CARE_BUNDLE_SYSTEM,
    DOCUMENT_BUNDLE_PROFILE,
    allergy_resource,
    codeable,
    composition,
    condition_resource,
    encounter_resource,
    fhir_datetime,
    medication_request_resource,
    meta,
    new_bundle,
    organization_resource,
    patient_resource,
    practitioner_resource,
    reference,
    section,
    snomed,
)

EXCLUDED_MEDICATION_STATUSES = {"cancelled", "entered_in_error", "entered-in-error"}
CHIEF_COMPLAINT_CATEGORIES = {"problem_list_item"}


def _querysets(encounter):
    from care.emr.models.allergy_intolerance import AllergyIntolerance
    from care.emr.models.condition import Condition
    from care.emr.models.medication_request import MedicationRequest
    from care.emr.models.observation import Observation

    return {
        "conditions": Condition.objects.filter(encounter=encounter),
        "allergies": AllergyIntolerance.objects.filter(encounter=encounter),
        "medications": MedicationRequest.objects.filter(encounter=encounter, do_not_perform=False).exclude(
            status__in=EXCLUDED_MEDICATION_STATUSES
        ),
        "observations": Observation.objects.filter(encounter=encounter).exclude(status="entered_in_error"),
    }


def has_data(encounter) -> bool:
    if getattr(encounter, "encounter_class", None) == "amb":
        return True
    return any(qs.exists() for qs in _querysets(encounter).values())


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
    """Build an OPConsultRecord bundle from encounter-linked CARE clinical rows."""
    if not has_data(encounter):
        raise BundleError("Encounter has no OP consultation data")

    from abdm.facility.service import hip_id_for

    timestamp = timezone.now()
    hip_id = hip_id_for(encounter.facility)
    data = _materialize(_querysets(encounter))

    patient = _patient_resource(encounter, timestamp)
    patient_ref = reference(patient, getattr(encounter.patient, "name", "") or "Patient")
    organization = organization_resource(encounter.facility, hip_id=hip_id, timestamp=timestamp)
    org_ref = reference(organization, getattr(encounter.facility, "name", "") or "Organization")
    author = _author(encounter, data["medications"], data["observations"])
    practitioner = practitioner_resource(author, timestamp=timestamp) if author else None
    author_ref = reference(practitioner, "Practitioner") if practitioner else org_ref

    chief_conditions = [
        condition for condition in data["conditions"] if condition.category in CHIEF_COMPLAINT_CATEGORIES
    ]
    history_conditions = [
        condition for condition in data["conditions"] if condition.category not in CHIEF_COMPLAINT_CATEGORIES
    ]
    chief_resources = [condition_resource(condition, patient_ref=patient_ref) for condition in chief_conditions]
    history_resources = [condition_resource(condition, patient_ref=patient_ref) for condition in history_conditions]
    allergy_resources = [
        allergy_resource(allergy, patient_ref=patient_ref, recorder_ref=author_ref) for allergy in data["allergies"]
    ]
    encounter_entry = encounter_resource(
        encounter,
        patient_ref=patient_ref,
        diagnosis_refs=[reference(resource, "Condition") for resource in history_resources],
        timestamp=timestamp,
    )
    encounter_ref = reference(encounter_entry, "Encounter")
    medication_resources = [
        medication_request_resource(
            medication,
            patient_ref=patient_ref,
            requester_ref=reference(practitioner, "Practitioner")
            if medication.requester_id and practitioner
            else author_ref,
            reason_refs=[reference(resource, "Condition") for resource in history_resources[:1]],
        )
        for medication in data["medications"]
    ]
    observation_resources = [
        _observation_resource(observation, patient_ref=patient_ref) for observation in data["observations"]
    ]

    sections = _sections(
        chief_resources, allergy_resources, history_resources, medication_resources, observation_resources
    )
    if not sections:
        sections.append(
            section(
                title="Medical History",
                code=snomed("371529009", "History and physical report"),
                empty_text="No clinical entries recorded",
            )
        )

    comp = composition(
        profile_url=HI_TYPE_PROFILES["OPConsultation"],
        type_code="371530004",
        type_display="Clinical consultation report",
        subject_ref=patient_ref,
        encounter_ref=encounter_ref,
        date_value=(getattr(encounter, "period", {}) or {}).get("start") or timestamp,
        author_refs=[author_ref],
        title="Clinical Consultation report",
        custodian_ref=org_ref,
        attester_ref=org_ref,
        sections=sections,
        timestamp=timestamp,
    )
    resources = [
        patient,
        *(list(filter(None, [practitioner]))),
        organization,
        encounter_entry,
        *chief_resources,
        *allergy_resources,
        *history_resources,
        *medication_resources,
        *observation_resources,
    ]
    return new_bundle(
        DOCUMENT_BUNDLE_PROFILE,
        comp,
        resources,
        hip_system=CARE_BUNDLE_SYSTEM,
        hip_id=str(hip_id),
        timestamp=fhir_datetime(timestamp),
    )


def _materialize(querysets):
    return {key: list(qs) for key, qs in querysets.items()}


def _author(encounter, medications, observations):
    for medication in medications:
        if medication.requester_id:
            return medication.requester
    for observation in observations:
        if observation.data_entered_by_id:
            return observation.data_entered_by
    return getattr(encounter, "created_by", None)


def _sections(chief_resources, allergy_resources, history_resources, medication_resources, observation_resources):
    sections = []
    if chief_resources:
        sections.append(
            section(
                title="Chief complaints",
                code=snomed("422843007", "Chief complaint section"),
                entries=[reference(resource, "Condition") for resource in chief_resources],
            )
        )
    if allergy_resources:
        sections.append(
            section(
                title="Allergies",
                code=snomed("722446000", "Allergy record"),
                entries=[reference(resource, "AllergyIntolerance") for resource in allergy_resources],
            )
        )
    if history_resources:
        sections.append(
            section(
                title="Medical History",
                code=snomed("371529009", "History and physical report"),
                entries=[reference(resource, "Condition") for resource in history_resources],
            )
        )
    if medication_resources:
        sections.append(
            section(
                title="Medications",
                code=snomed("721912009", "Medication summary document"),
                entries=[reference(resource, "MedicationRequest") for resource in medication_resources],
            )
        )
    if observation_resources:
        sections.append(
            section(
                title="Other Observations",
                entries=[reference(resource, "Observation") for resource in observation_resources],
            )
        )
    return sections


def _observation_resource(observation, *, patient_ref):
    resource = {
        "resourceType": "Observation",
        "id": str(getattr(observation, "external_id", "")),
        "meta": meta("Observation"),
        "status": getattr(observation, "status", None) or "final",
        "code": codeable(getattr(observation, "main_code", None), "Observation"),
        "subject": patient_ref,
        "effectiveDateTime": fhir_datetime(getattr(observation, "effective_datetime", None)),
        "valueString": _observation_value(observation),
        "note": [{"text": getattr(observation, "note", None)}],
    }
    return resource


def _observation_value(observation) -> str:
    value = getattr(observation, "value", None)
    if isinstance(value, dict):
        return value.get("value") or value.get("display") or str(value)
    return str(value) if value is not None else ""
