"""DischargeSummary HI type builder for ABDM NRCES FHIR R4 bundles.

Care's discharge summary is a generated PDF (`ReportUpload`, `report_type="discharge_summary"`,
`care/emr/reports/report_types.py:12-18`), so the bundle is the profile's `DocumentReference`
section slice (MCP `get_fhir_profile DischargeSummary`: required `Composition.encounter`,
sections ChiefComplaints … DocumentReference, all 0..1; example type SNOMED `373942005`
"Discharge summary"). Structured sections can be added later from the same Encounter data the
OPConsultRecord builder reads.
"""

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
    encounter_resource,
    fhir_datetime,
    new_bundle,
    organization_resource,
    patient_resource,
    practitioner_resource,
    reference,
    section,
    snomed,
)

DISCHARGE_SUMMARY_CODE = ("373942005", "Discharge summary")


def _reports(encounter, source_ids=None):
    from care.emr.models.report.report_upload import ReportUpload

    rows = ReportUpload.objects.filter(
        report_type="discharge_summary",
        associating_id=str(encounter.external_id),
        upload_completed=True,
        is_archived=False,
    )
    if source_ids is not None:
        rows = rows.filter(id__in=source_ids)
    return rows.order_by("-created_date")


def has_data(encounter) -> bool:
    return _reports(encounter).exists()


def _patient_resource(encounter, timestamp):
    from abdm.care_seams import AbhaAddressIdentifier, AbhaNumberIdentifier

    patient = encounter.patient
    return patient_resource(
        patient,
        timestamp=timestamp,
        abha_number=AbhaNumberIdentifier.get(patient),
        abha_address=AbhaAddressIdentifier.get(patient),
    )


def build(encounter, source_ids=None) -> dict:
    """Build a DischargeSummaryRecord bundle around the generated discharge summary PDF(s)."""
    reports = list(_reports(encounter, source_ids))
    if not reports:
        raise BundleError("Encounter has no completed discharge summary report")

    from abdm.facility.service import hip_id_for

    timestamp = timezone.now()
    hip_id = hip_id_for(encounter.facility)
    patient = _patient_resource(encounter, timestamp)
    patient_ref = reference(patient, getattr(encounter.patient, "name", "") or "Patient")
    organization = organization_resource(encounter.facility, hip_id=hip_id, timestamp=timestamp)
    org_ref = reference(organization, getattr(encounter.facility, "name", "") or "Organization")
    author = getattr(reports[0], "created_by", None) or getattr(encounter, "created_by", None)
    practitioner = practitioner_resource(author, timestamp=timestamp) if author else None
    author_ref = reference(practitioner, "Practitioner") if practitioner else org_ref
    encounter_entry = encounter_resource(encounter, patient_ref=patient_ref, timestamp=timestamp)
    encounter_ref = reference(encounter_entry, "Encounter")

    documents = []
    for report in reports:
        document = document_reference_resource(report, patient_ref=patient_ref, attachment=_attachment(report))
        document["type"] = {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": DISCHARGE_SUMMARY_CODE[0],
                    "display": DISCHARGE_SUMMARY_CODE[1],
                }
            ],
            "text": DISCHARGE_SUMMARY_CODE[1],
        }
        documents.append(document)
    comp = composition(
        profile_url=HI_TYPE_PROFILES["DischargeSummary"],
        type_code=DISCHARGE_SUMMARY_CODE[0],
        type_display=DISCHARGE_SUMMARY_CODE[1],
        subject_ref=patient_ref,
        encounter_ref=encounter_ref,
        custodian_ref=org_ref,
        date_value=max((report.created_date for report in reports if report.created_date), default=timestamp),
        author_refs=[author_ref],
        title="Discharge Summary",
        sections=[
            section(
                title="Document Reference",
                code=snomed(*DISCHARGE_SUMMARY_CODE),
                entries=[reference(document, "Discharge Summary") for document in documents],
            )
        ],
        attester_ref=org_ref,
        timestamp=timestamp,
    )
    resources = [patient, *(list(filter(None, [practitioner]))), organization, encounter_entry, *documents]
    return new_bundle(
        DOCUMENT_BUNDLE_PROFILE,
        comp,
        resources,
        hip_system=CARE_BUNDLE_SYSTEM,
        hip_id=str(hip_id),
        timestamp=fhir_datetime(timestamp),
    )


def _attachment(file_obj) -> dict:
    name = getattr(file_obj, "name", "") or "Discharge summary"
    content_type = (getattr(file_obj, "meta", None) or {}).get("mime_type") or "application/pdf"
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
        url = f"urn:care:report-upload:{getattr(file_obj, 'external_id', '')}"
    return attachment_from_url(
        name=name,
        url=url,
        content_type=content_type,
        created=getattr(file_obj, "created_date", None),
    )
