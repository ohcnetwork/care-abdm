"""
Celery tasks. Care autodiscovers `<app>.tasks` (config/celery_app.py:8-18).

`dispatch_callback` routes a verified callback to its handler by operation id
(callbacks/paths.py::CALLBACK_OPERATION_BY_PATH). `sync_encounter` runs the HIP-initiated
link for an Encounter. Both do ABDM I/O, so a Celery worker must run for M2.
"""

import logging
import traceback

from celery import current_app, shared_task
from django.core.cache import cache
from django.utils import timezone

from abdm.callbacks.exceptions import CallbackNotReady
from abdm.models import AbdmCallback

logger = logging.getLogger(__name__)

# ADR-018: the periodic tasks record that the worker is alive. The developer readiness check reads
# it: with no worker, every callback stays `queued` and every link waits for ever, and nothing on
# the desk says why.
WORKER_HEARTBEAT_KEY = "abdm:worker:last_seen"
WORKER_HEARTBEAT_TTL = 24 * 60 * 60
# The traceback kept on a callback row. 20 KB holds every frame of a handler; a runaway repr does
# not grow the row without bound.
TRACEBACK_CHARS = 20_000


def worker_heartbeat() -> None:
    cache.set(WORKER_HEARTBEAT_KEY, timezone.now().isoformat(), timeout=WORKER_HEARTBEAT_TTL)


def _handle_profile_share(callback: AbdmCallback) -> dict:
    from abdm.share.service import handle_profile_share

    share = handle_profile_share(callback)
    return {"share_id": str(share.external_id), "status": share.status, "token_number": share.token_number}


def _lazy(module: str, name: str):
    def handler(callback: AbdmCallback) -> dict:
        import importlib

        return getattr(importlib.import_module(module), name)(callback)

    return handler


# A callback whose handler raises `CallbackNotReady` is run again on this ladder: the row it names
# may still be on its way (the `on-init` / notify race). `on-init` is an immediate gateway answer,
# so ~3.5 minutes is generous; past that the request is not late, it is absent (deleted with the
# database, or raised by another deployment sharing the bridge URL).
NOT_READY_COUNTDOWNS = (15, 30, 60, 120)

# operation_id -> handler(callback) -> dict, run once the retry window is spent. The duty differs
# per operation: the consent notify must be acknowledged or the gateway redelivers for ever; the
# health-information push has nobody to answer, so its hook only drops the ciphertext it held.
CALLBACK_GIVE_UP = {
    "m3-hiu-consent-notify": _lazy("abdm.hiu.service", "abandon_consent_notify"),
    "m3-health-information-transfer": _lazy("abdm.hiu.service", "abandon_transfer"),
}

# operation_id -> handler(callback) -> dict
CALLBACK_HANDLERS = {
    "m1-receive-patient-share": _handle_profile_share,
    "m2-on-generate-token-result": _lazy("abdm.hip.contexts", "handle_generate_token_result"),
    "m2-on-carecontext-result": _lazy("abdm.hip.contexts", "handle_carecontext_result"),
    "m2-on-context-notify-result": _lazy("abdm.hip.contexts", "handle_context_notify_result"),
    "m2-on-sms-notify-result": _lazy("abdm.hip.contexts", "handle_sms_notify_result"),
    "m2-on-discovery-request": _lazy("abdm.hip.discovery", "handle_discover"),
    "m2-on-link-init": _lazy("abdm.hip.discovery", "handle_link_init"),
    "m2-on-link-confirm": _lazy("abdm.hip.discovery", "handle_link_confirm"),
    "m2-consent-hip-notify": _lazy("abdm.hip.consent", "handle_consent_notify"),
    "m2-on-health-information-request": _lazy("abdm.hip.transfer", "handle_health_information_request"),
    # M3 (HIU), ADR-014.
    "m3-on-consent-request-init": _lazy("abdm.hiu.service", "handle_on_init"),
    "m3-on-consent-request-status": _lazy("abdm.hiu.service", "handle_on_status"),
    "m3-hiu-consent-notify": _lazy("abdm.hiu.service", "handle_consent_notify"),
    "m3-on-consent-fetch": _lazy("abdm.hiu.service", "handle_on_fetch"),
    "m3-on-health-information-request": _lazy("abdm.hiu.service", "handle_hi_on_request"),
    "m3-health-information-transfer": _lazy("abdm.hiu.service", "handle_transfer"),
}


@shared_task(name="abdm.tasks.dispatch_callback", bind=True, max_retries=len(NOT_READY_COUNTDOWNS))
def dispatch_callback(self, callback_id: int):
    callback = AbdmCallback.objects.get(id=callback_id)
    handler = CALLBACK_HANDLERS.get(callback.operation_id)
    result = {"callback_id": callback_id, "operation_id": callback.operation_id}
    worker_heartbeat()
    if handler is None:
        callback.processed_status = AbdmCallback.ProcessedStatus.UNHANDLED
        callback.processed_at = timezone.now()
        callback.save(update_fields=["processed_status", "processed_at", "modified_date"])
        return result
    try:
        result.update(handler(callback))
    except CallbackNotReady as exc:
        return _wait_for_row(self, callback, result, exc)
    except Exception:
        logger.exception("abdm callback %s (%s) failed", callback_id, callback.operation_id)
        callback.processed_status = AbdmCallback.ProcessedStatus.FAILED
        callback.processing_error = traceback.format_exc()[-TRACEBACK_CHARS:]
        callback.processed_at = timezone.now()
        callback.save(update_fields=["processed_status", "processing_error", "processed_at", "modified_date"])
        raise
    callback.processed_status = AbdmCallback.ProcessedStatus.HANDLED
    callback.processing_error = ""
    callback.processed_at = timezone.now()
    callback.save(update_fields=["processed_status", "processing_error", "processed_at", "modified_date"])
    return result


def _wait_for_row(task, callback: AbdmCallback, result: dict, exc: "CallbackNotReady") -> dict:
    """The handler asked to be run again once the row it names exists (see
    `callbacks/exceptions.CallbackNotReady`). Retries left: sleep and repeat, leaving the callback
    `queued` — this is not a failure and must not read as one on the developer page. Retries spent:
    hand the callback to the operation's give-up hook (which acknowledges it to ABDM) and mark it
    `unhandled`, because nothing on our side broke."""
    attempt = task.request.retries
    if attempt < len(NOT_READY_COUNTDOWNS):
        countdown = NOT_READY_COUNTDOWNS[attempt]
        logger.info(
            "abdm callback %s (%s) is not ready (%s); retrying in %s s",
            callback.id,
            callback.operation_id,
            exc,
            countdown,
        )
        callback.processed_status = AbdmCallback.ProcessedStatus.QUEUED
        callback.processing_error = f"Waiting for the row it names: {exc}"[:TRACEBACK_CHARS]
        callback.save(update_fields=["processed_status", "processing_error", "modified_date"])
        raise task.retry(countdown=countdown, exc=exc)
    logger.warning("abdm callback %s (%s) gave up waiting: %s", callback.id, callback.operation_id, exc)
    give_up = CALLBACK_GIVE_UP.get(callback.operation_id)
    if give_up is not None:
        try:
            result.update(give_up(callback))
        except Exception:
            logger.exception("abdm callback %s: the give-up hook failed", callback.id)
    callback.processed_status = AbdmCallback.ProcessedStatus.UNHANDLED
    callback.processing_error = str(exc)[:TRACEBACK_CHARS]
    callback.processed_at = timezone.now()
    callback.save(update_fields=["processed_status", "processing_error", "processed_at", "modified_date"])
    result["not_ready"] = str(exc)
    return result


@shared_task(
    name="abdm.tasks.sync_encounter",
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=30,
)
def sync_encounter(self, encounter_id: int):
    """Link the Encounter. ADR-012 D5: repeat only a failure that a repeat can cure. A refusal is
    not repeated, because ABDM gives the same answer and a second link-token request inside the
    refusal window earns ABDM-1092."""
    from care.emr.models.encounter import Encounter

    from abdm import errors
    from abdm.hip.contexts import sync_encounter as run
    from abdm.models import AbdmCareContext

    encounter = Encounter.objects.filter(id=encounter_id).select_related("patient", "facility").first()
    if encounter is None:
        return {"encounter_id": encounter_id, "skipped": "missing"}
    context = run(encounter)
    if context is None:
        return {"encounter_id": encounter_id, "skipped": "facility not configured"}
    result = {"encounter_id": encounter_id, "status": context.status, "error": context.error_code}
    if context.status == AbdmCareContext.Status.FAILED and context.error_code:
        failure = errors.classify(code=context.error_code, message=context.error_message)
        if failure.retry_now and self.request.retries < 3:
            result["retry"] = failure.action
            raise self.retry(countdown=30 * (2**self.request.retries))
    return result


@shared_task(name="abdm.tasks.stage_record")
def stage_record(source_model: str, source_id: int):
    """A clinical record was saved: stage it for sharing (ADR-013 D2). Nothing is sent to ABDM."""
    from care.emr.models.diagnostic_report import DiagnosticReport
    from care.emr.models.medication_request import MedicationRequestPrescription
    from care.emr.models.report.report_upload import ReportUpload

    from abdm.hip import sharing

    loaders = {
        "medication_request_prescription": (MedicationRequestPrescription, sharing.stage_prescription),
        "diagnostic_report": (DiagnosticReport, sharing.stage_diagnostic_report),
        "report_upload": (ReportUpload, sharing.stage_discharge_summary),
    }
    model, stage = loaders[source_model]
    record = model.objects.filter(id=source_id).first()
    if record is None:
        return {"source": source_model, "id": source_id, "skipped": "missing"}
    item = stage(record)
    return {"source": source_model, "id": source_id, "item": item.status if item else None}


@shared_task(
    name="abdm.tasks.link_care_context", bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 2}
)
def link_care_context(self, context_id: int):
    """Send 1 link call for the queued share items of a care context (desk action, Encounter
    close, or retry). A refusal is not repeated here: ADR-013 D4 schedules the next attempt."""
    from abdm.hip.contexts import link_context
    from abdm.models import AbdmCareContext

    context = AbdmCareContext.objects.filter(id=context_id).select_related("patient", "facility", "encounter").first()
    if context is None:
        return {"context_id": context_id, "skipped": "missing"}
    context = link_context(context)
    return {"context_id": context_id, "status": context.status, "error": context.error_code}


@shared_task(name="abdm.tasks.retry_share_items")
def retry_share_items():
    """Periodic (Celery beat, every 5 minutes): re-run the link for contexts whose queued items
    are due (ADR-013 D4)."""
    from abdm.hip import sharing

    worker_heartbeat()
    return {"contexts": sharing.retry_due_items()}


@shared_task(name="abdm.tasks.notify_care_context", bind=True, max_retries=5)
def notify_care_context(self, context_id: int):
    """Tell ABDM that a care context is linked, after the link is indexed.

    ABDM refuses a notify that arrives before it indexes the link (finding F8), so the caller
    delays this task and a refusal is repeated with a longer wait. The care context is already
    linked at this point, so a repeat is safe: it only asks ABDM to tell the patient's app again.
    """
    from abdm.hip.contexts import notify_context
    from abdm.models import AbdmCareContext

    context = AbdmCareContext.objects.filter(id=context_id).select_related("patient", "facility").first()
    if context is None:
        return {"context_id": context_id, "skipped": "missing"}
    context = notify_context(context)
    request = context.notify_request
    if request is not None and request.status == request.Status.FAILED and self.request.retries < 5:
        raise self.retry(countdown=30 * (2**self.request.retries))
    return {"context_id": context_id, "http_status": request.http_status if request else None}


@shared_task(name="abdm.tasks.hiu_housekeeping")
def hiu_housekeeping():
    """Periodic (Celery beat, every 15 minutes), ADR-014: a health-information request with no push
    inside the 20-minute window is failed and the gateway told; a fetched bundle past the consent
    `dataEraseAt` is erased."""
    from abdm.hiu.service import housekeeping

    worker_heartbeat()
    return housekeeping()


@current_app.on_after_finalize.connect
def register_periodic_tasks(sender, **kwargs):
    """Care registers periodic tasks this way (care/emr/tasks/__init__.py:12-31)."""
    sender.add_periodic_task(5 * 60, retry_share_items.s(), name="abdm retry share items")
    sender.add_periodic_task(15 * 60, hiu_housekeeping.s(), name="abdm hiu housekeeping")
