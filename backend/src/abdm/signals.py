"""
post_save(Patient): consume extensions.abdm.txn_id → identifiers + link metadata.

Same mechanism core uses for its own auto-maintained identifiers
(care/emr/signals/patient/name_identifier.py:26). Runs inside the request's
transaction, so a failed link rolls the patient create back too — deliberate:
a patient half-linked to an ABHA is worse than a clean retry.
"""

import logging

from care.emr.models.diagnostic_report import DiagnosticReport
from care.emr.models.encounter import Encounter
from care.emr.models.medication_request import MedicationRequestPrescription
from care.emr.models.patient import Patient
from care.emr.models.report.report_upload import ReportUpload
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from abdm.care_seams import EXTENSION_NAME, AbhaAddressIdentifier, AbhaNumberIdentifier
from abdm.models import AbhaTransaction

logger = logging.getLogger(__name__)


class LinkError(Exception):
    pass


def link_patient_to_transaction(patient: Patient, txn: AbhaTransaction, *, save_patient: bool = True) -> None:
    """Single writer for ABHA↔Patient linkage. Used by the signal and by the explicit link API."""
    if not txn.abha_number:
        raise LinkError("Transaction has no ABHA number yet (claim / account selection not completed)")
    if txn.patient_id and txn.patient_id != patient.id:
        raise LinkError("Transaction already linked to another patient")
    other = AbhaNumberIdentifier.find_patient(txn.abha_number)
    if other and other.id != patient.id:
        raise LinkError(f"ABHA {txn.abha_number} is already linked to patient {other.external_id}")

    AbhaNumberIdentifier.set(patient, txn.abha_number)
    if txn.abha_address:
        AbhaAddressIdentifier.set(patient, txn.abha_address)

    now = timezone.now()
    ext = dict((patient.extensions or {}).get(EXTENSION_NAME, {}))
    ext.pop("txn_id", None)
    ext.update(
        {
            "abha_number": txn.abha_number,
            "abha_address": txn.abha_address,
            "abha_linked_at": now.isoformat(),
            "abha_source": txn.kind,
            "kyc_verified": bool(txn.profile.get("kycVerified", txn.kind == AbhaTransaction.Kind.ENROL_AADHAAR)),
        }
    )
    extensions = dict(patient.extensions or {})
    extensions[EXTENSION_NAME] = ext
    patient.extensions = extensions
    # Core reads identifiers from the denormalised Patient.instance_identifiers JSON
    # (care/emr/resources/patient/spec.py:275), rebuilt only by the viewset
    # (care/emr/api/viewsets/patient.py:147,190). Rebuild it here or the UI never sees them.
    patient.build_instance_identifiers()
    if save_patient:
        # .update() keeps us out of core's full save() path and out of this signal's txn branch.
        Patient.objects.filter(pk=patient.pk).update(
            extensions=extensions, instance_identifiers=patient.instance_identifiers
        )

    txn.patient = patient
    txn.linked_at = now
    txn.save(update_fields=["patient", "linked_at", "modified_date"])
    logger.info("abdm: linked ABHA %s to patient %s via %s", txn.abha_number, patient.external_id, txn.txn_id)


@receiver(post_save, sender=Patient)
def link_abha_from_txn(sender, instance: Patient, **kwargs):
    txn_id = ((instance.extensions or {}).get(EXTENSION_NAME) or {}).get("txn_id")
    if not txn_id:
        return
    txn = AbhaTransaction.objects.filter(txn_id=txn_id).first()
    if txn is None:
        # Client sent a txn the server never saw: strip it rather than persist junk; never trust it.
        logger.warning("abdm: unknown txn_id %s on patient %s; dropping", txn_id, instance.external_id)
        ext = dict(instance.extensions)
        ext[EXTENSION_NAME] = {k: v for k, v in ext[EXTENSION_NAME].items() if k != "txn_id"}
        Patient.objects.filter(pk=instance.pk).update(extensions=ext)
        return
    link_patient_to_transaction(instance, txn)


# --- M2 / ADR-013: stage records; link on Encounter close ----------------------------------------

ENCOUNTER_SYNC_FIELDS = {"status", "encounter_class", "period"}


def _queue(task, *args):
    transaction.on_commit(lambda: task.delay(*args))


@receiver(post_save, sender=Encounter)
def sync_encounter_care_context(sender, instance: Encounter, created: bool, update_fields=None, **kwargs):
    """Queue `tasks.sync_encounter` after the Encounter commits: a closing status links every
    staged item; other changes refresh the display name. Saves that touch only cache fields
    (care/emr/models/encounter.py::sync_organization_cache) are skipped."""
    if update_fields is not None and not (set(update_fields) & ENCOUNTER_SYNC_FIELDS):
        return
    from abdm.facility.service import hip_id_for

    if created or not hip_id_for(instance.facility):
        return
    from abdm.tasks import sync_encounter

    _queue(sync_encounter, instance.id)


@receiver(post_save, sender=MedicationRequestPrescription)
def stage_prescription_item(sender, instance: MedicationRequestPrescription, **kwargs):
    from abdm.tasks import stage_record

    _queue(stage_record, "medication_request_prescription", instance.id)


@receiver(post_save, sender=DiagnosticReport)
def stage_diagnostic_report_item(sender, instance: DiagnosticReport, **kwargs):
    from abdm.tasks import stage_record

    _queue(stage_record, "diagnostic_report", instance.id)


@receiver(post_save, sender=ReportUpload)
def stage_discharge_summary_item(sender, instance: ReportUpload, **kwargs):
    if instance.report_type != "discharge_summary":
        return
    from abdm.tasks import stage_record

    _queue(stage_record, "report_upload", instance.id)
