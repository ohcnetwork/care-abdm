from celery import shared_task

from abdm.models import AbdmCallback


@shared_task(name="abdm.tasks.dispatch_callback")
def dispatch_callback(callback_id: int):
    callback = AbdmCallback.objects.get(id=callback_id)
    callback.processed_status = AbdmCallback.ProcessedStatus.UNHANDLED
    callback.save(update_fields=["processed_status", "modified_date"])
    return {"callback_id": callback_id, "operation_id": callback.operation_id}
