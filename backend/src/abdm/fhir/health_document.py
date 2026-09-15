"""HealthDocumentRecord HI type builder for ABDM NRCES FHIR R4 bundles."""

from __future__ import annotations

from django.utils import timezone

from abdm.fhir import HI_TYPE_PROFILES, BundleError
from abdm.fhir.bundle import (
    CARE_BUNDLE_SYSTEM,
    DOCUMENT_BUNDLE_PROFILE,
    attachment_from_bytes,
    attachment_from_url,
    composition,
    document_reference_resource,
    fhir_datetime,
    new_bundle,
    organization_resource,
    patient_resource,
    practitioner_resource,
    reference,
    section,
)


def _files(encounter):
    from care.emr.models.file_upload import FileUpload

    return FileUpload.objects.filter(
        file_type="encounter",
        associating_id=str(encounter.external_id),
        upload_completed=True,
        is_archived=False,
    )


def has_data(encounter) -> bool:
    return _files(encounter).exists()


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
    """Build a HealthDocumentRecord bundle from completed CARE encounter files."""
    files = list(_files(encounter))
    if not files:
        raise BundleError("Encounter has no health document files")

    from abdm.facility.service import hip_id_for

    timestamp = timezone.now()
    hip_id = hip_id_for(encounter.facility)
    patient = _patient_resource(encounter, timestamp)
    patient_ref = reference(patient, getattr(encounter.patient, "name", "") or "Patient")
    organization = organization_resource(encounter.facility, hip_id=hip_id, timestamp=timestamp)
    org_ref = reference(organization, getattr(encounter.facility, "name", "") or "Organization")
    author = getattr(encounter, "created_by", None)
    practitioner = practitioner_resource(author, timestamp=timestamp) if author else None
    author_ref = reference(practitioner, "Practitioner") if practitioner else org_ref

    documents = [
        document_reference_resource(file_obj, patient_ref=patient_ref, attachment=_attachment(file_obj))
        for file_obj in files
    ]
    comp = composition(
        profile_url=HI_TYPE_PROFILES["HealthDocumentRecord"],
        type_code="419891008",
        type_display="Record artifact",
        subject_ref=patient_ref,
        date_value=min((file_obj.created_date for file_obj in files if file_obj.created_date), default=timestamp),
        author_refs=[author_ref],
        title="Record artifact",
        sections=[
            section(
                title="Health Document",
                entries=[reference(document, "DocumentReference") for document in documents],
            )
        ],
        attester_ref=org_ref,
        timestamp=timestamp,
    )
    resources = [patient, *(list(filter(None, [practitioner]))), organization, *documents]
    return new_bundle(
        DOCUMENT_BUNDLE_PROFILE,
        comp,
        resources,
        hip_system=CARE_BUNDLE_SYSTEM,
        hip_id=str(hip_id),
        timestamp=fhir_datetime(timestamp),
    )


def _attachment(file_obj) -> dict:
    name = getattr(file_obj, "name", "") or getattr(file_obj, "internal_name", "") or "Document"
    content_type = (getattr(file_obj, "meta", None) or {}).get("mime_type")
    try:
        stored_content_type, content = file_obj.files_manager.file_contents(file_obj)
        return attachment_from_bytes(
            name=name,
            content=content,
            content_type=stored_content_type or content_type,
            created=getattr(file_obj, "created_date", None),
        )
    except Exception:
        pass
    try:
        url = file_obj.files_manager.read_signed_url(file_obj)
    except Exception:
        url = f"urn:care:file-upload:{getattr(file_obj, 'external_id', '')}"
    return attachment_from_url(
        name=name,
        url=url,
        content_type=content_type,
        created=getattr(file_obj, "created_date", None),
    )
