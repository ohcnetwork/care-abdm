"""
Staged sharing (ADR-013): which Care records a care context links, and when.

  stage_*()            `post_save` receivers call these. They create or update 1 `AbdmShareItem`
                       per shareable record. Nothing is sent to ABDM.
  queue_items()        the desk (ABDM tab) or the Encounter close marks items `queued`.
  link_queued()        1 link call per care context for every queued item (F7: 1 patient block
                       per HI type). Runs in Celery.
  on_link_result()     the `on_carecontext` callback marks the queued items linked or failed and
                       schedules a retry (ADR-013 D4).
  retry_due_items()    the periodic task re-queues items whose `next_attempt_at` has passed.
"""

import logging
from datetime import timedelta

from care.emr.models.diagnostic_report import DiagnosticReport
from care.emr.models.encounter import Encounter
from care.emr.models.medication_request import MedicationRequestPrescription
from care.emr.models.report.report_upload import ReportUpload
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from abdm import errors
from abdm.facility.service import hip_id_for
from abdm.hip import rules
from abdm.models import AbdmCareContext, AbdmShareItem

logger = logging.getLogger(__name__)

HiType = AbdmShareItem.HiType
Source = AbdmShareItem.Source
Status = AbdmShareItem.Status


def _settings():
    from abdm.settings import plugin_settings

    return (
        timedelta(minutes=int(plugin_settings.LINK_RETRY_INTERVAL_MINUTES or 60)),
        int(plugin_settings.LINK_MAX_RETRIES or 0),
    )


# --- staging --------------------------------------------------------------------------------


def _context_for(encounter: Encounter) -> AbdmCareContext | None:
    if not hip_id_for(encounter.facility):
        return None
    from abdm.hip.contexts import ensure_care_context

    return ensure_care_context(encounter)


def _upsert(
    context: AbdmCareContext, hi_type: str, source: str, source_id: int, label: str, shareable: bool
) -> AbdmShareItem | None:
    """Stage a shareable record; exclude a staged record that stopped being shareable. A linked
    item is never changed: ABDM holds no per-record state and the docs give no unlink call."""
    item = AbdmShareItem.objects.filter(
        care_context=context, hi_type=hi_type, source_model=source, source_id=source_id
    ).first()
    if item is None:
        if not shareable:
            return None
        return AbdmShareItem.objects.create(
            care_context=context, hi_type=hi_type, source_model=source, source_id=source_id, label=label
        )
    if item.status in (Status.LINKED, Status.QUEUED):
        return item
    wanted = Status.STAGED if shareable else Status.EXCLUDED
    # The desk's own exclusion stands while the record is still shareable.
    if item.status == Status.EXCLUDED and shareable and item.last_error_code != "NOT_SHAREABLE":
        return item
    if item.status != wanted or item.label != label:
        item.status = wanted
        item.label = label
        item.last_error_code = "" if shareable else "NOT_SHAREABLE"
        item.save(update_fields=["status", "label", "last_error_code", "modified_date"])
    return item


def stage_op_consultation(encounter: Encounter, context: AbdmCareContext) -> None:
    """1 OPConsultation item per outpatient Encounter, created with its first clinical record."""
    if not rules.op_consultation_applies(encounter.encounter_class):
        return
    from abdm.hip.contexts import encounter_start

    _upsert(
        context,
        HiType.OP_CONSULTATION,
        Source.ENCOUNTER,
        encounter.id,
        rules.item_label(HiType.OP_CONSULTATION, encounter_start(encounter)),
        True,
    )


def stage_prescription(prescription: MedicationRequestPrescription) -> AbdmShareItem | None:
    context = _context_for(prescription.encounter)
    if context is None:
        return None
    shareable = rules.prescription_is_shareable(prescription.status)
    stage_op_consultation(prescription.encounter, context)
    return _upsert(
        context,
        HiType.PRESCRIPTION,
        Source.PRESCRIPTION,
        prescription.id,
        rules.item_label(HiType.PRESCRIPTION, prescription.created_date, prescription.name or ""),
        shareable,
    )


def stage_diagnostic_report(report: DiagnosticReport) -> AbdmShareItem | None:
    context = _context_for(report.encounter)
    if context is None:
        return None
    shareable = rules.diagnostic_report_is_shareable(report.status)
    stage_op_consultation(report.encounter, context)
    code = report.code if isinstance(report.code, dict) else {}
    return _upsert(
        context,
        HiType.DIAGNOSTIC_REPORT,
        Source.DIAGNOSTIC_REPORT,
        report.id,
        rules.item_label(HiType.DIAGNOSTIC_REPORT, report.created_date, str(code.get("display") or "")),
        shareable,
    )


def stage_discharge_summary(upload: ReportUpload) -> AbdmShareItem | None:
    if upload.report_type != rules.DISCHARGE_SUMMARY_REPORT_TYPE:
        return None
    encounter = (
        Encounter.objects.filter(external_id=upload.associating_id).select_related("patient", "facility").first()
    )
    if encounter is None:
        return None
    context = _context_for(encounter)
    if context is None:
        return None
    shareable = rules.discharge_summary_is_shareable(upload.report_type, upload.upload_completed, upload.is_archived)
    return _upsert(
        context,
        HiType.DISCHARGE_SUMMARY,
        Source.REPORT_UPLOAD,
        upload.id,
        rules.item_label(HiType.DISCHARGE_SUMMARY, upload.created_date),
        shareable,
    )


# --- queue and link ----------------------------------------------------------------------


def queue_items(items, *, reset_attempts: bool = False) -> int:
    """Mark staged or failed items `queued`. Returns how many changed."""
    count = 0
    for item in items:
        if item.status not in (Status.STAGED, Status.FAILED, Status.EXCLUDED):
            continue
        item.status = Status.QUEUED
        item.next_attempt_at = None
        if reset_attempts:
            item.attempts = 0
        item.last_error_code = ""
        item.last_error_message = ""
        item.save(
            update_fields=[
                "status",
                "next_attempt_at",
                "attempts",
                "last_error_code",
                "last_error_message",
                "modified_date",
            ]
        )
        count += 1
    return count


def queue_all_staged(context: AbdmCareContext) -> int:
    """The Encounter closed: every staged item goes (ADR-013 D2)."""
    return queue_items(context.share_items.filter(status=Status.STAGED))


def schedule_link(context: AbdmCareContext) -> None:
    from abdm.tasks import link_care_context

    transaction.on_commit(lambda: link_care_context.delay(context.id))


def hi_types_to_link(context: AbdmCareContext) -> list[str]:
    """Every linked and queued type, so the call is right whether ABDM adds or replaces types
    (ADR-013 §Open)."""
    return sorted(
        set(context.share_items.filter(status__in=[Status.QUEUED, Status.LINKED]).values_list("hi_type", flat=True))
    )


def link_queued(context: AbdmCareContext) -> AbdmCareContext:
    """1 link call for the queued items of this context. `request_link` sends every type from
    `hi_types_to_link()`; the queued items then wait for the callback."""
    from abdm.hip.contexts import request_link

    queued = list(context.share_items.filter(status=Status.QUEUED))
    if not queued:
        return context
    context = request_link(context)
    if context.status == AbdmCareContext.Status.LINK_REQUESTED:
        AbdmShareItem.objects.filter(pk__in=[i.pk for i in queued]).update(
            link_request=context.link_request, attempts=F("attempts") + 1, modified_date=timezone.now()
        )
        return context
    if context.status == AbdmCareContext.Status.PENDING:
        # The link token is on its way; handle_generate_token_result() links the pending contexts.
        return context
    _record_failure(queued, context.error_code, context.error_message)
    if context.share_items.filter(status=Status.LINKED).exists():
        # ABDM already holds this care context; only the new items failed. Keep the context linked
        # so discovery and data requests still serve what was shared.
        context.status = AbdmCareContext.Status.LINKED
        context.save(update_fields=["status", "modified_date"])
    return context


def _record_failure(items: list[AbdmShareItem], code: str, message: str) -> None:
    interval, max_retries = _settings()
    now = timezone.now()
    for item in items:
        item.attempts += 1
        when = rules.next_attempt(now, item.attempts, interval, max_retries)
        item.last_error_code = (code or "LINK_FAILED")[:64]
        item.last_error_message = (message or "")[:512]
        if when is None:
            item.status = Status.FAILED
            item.next_attempt_at = None
        else:
            item.status = Status.QUEUED
            item.next_attempt_at = when
        item.save(
            update_fields=[
                "attempts",
                "status",
                "next_attempt_at",
                "last_error_code",
                "last_error_message",
                "modified_date",
            ]
        )


def on_link_result(context: AbdmCareContext, *, ok: bool, code: str = "", message: str = "") -> None:
    """The `on_carecontext` callback for `context.link_request` arrived."""
    items = list(context.share_items.filter(status=Status.QUEUED, link_request=context.link_request))
    if not items:
        return
    if ok:
        now = timezone.now()
        for item in items:
            item.status = Status.LINKED
            item.linked_at = now
            item.next_attempt_at = None
            item.last_error_code = ""
            item.last_error_message = ""
            item.save(
                update_fields=[
                    "status",
                    "linked_at",
                    "next_attempt_at",
                    "last_error_code",
                    "last_error_message",
                    "modified_date",
                ]
            )
        return
    _record_failure(items, code, message)


def refresh_hi_types(context: AbdmCareContext) -> list[str]:
    """`AbdmCareContext.hi_types` = the distinct types of the linked items (ADR-013 D1)."""
    types = sorted(set(context.share_items.filter(status=Status.LINKED).values_list("hi_type", flat=True)))
    if types != (context.hi_types or []):
        context.hi_types = types
        context.save(update_fields=["hi_types", "modified_date"])
    return types


def retry_due_items(now=None) -> int:
    """Re-run the link for every context that has a queued item whose wait has passed."""
    now = now or timezone.now()
    due = AbdmShareItem.objects.filter(status=Status.QUEUED, next_attempt_at__lte=now)
    context_ids = set(due.values_list("care_context_id", flat=True))
    for context_id in context_ids:
        AbdmShareItem.objects.filter(care_context_id=context_id, status=Status.QUEUED, next_attempt_at__lte=now).update(
            next_attempt_at=None
        )
        from abdm.tasks import link_care_context

        link_care_context.delay(context_id)
    return len(context_ids)


def failure_for(item: AbdmShareItem) -> dict | None:
    if not item.last_error_code:
        return None
    return errors.classify(code=item.last_error_code, message=item.last_error_message).as_dict()


def item_summary(item: AbdmShareItem) -> dict:
    return {
        "id": str(item.external_id),
        "hiType": item.hi_type,
        "sourceModel": item.source_model,
        "sourceId": item.source_id,
        "label": item.label,
        "status": item.status,
        "attempts": item.attempts,
        "nextAttemptAt": item.next_attempt_at,
        "linkedAt": item.linked_at,
        "requestId": item.link_request.request_id if item.link_request_id else "",
        "failure": failure_for(item),
    }
