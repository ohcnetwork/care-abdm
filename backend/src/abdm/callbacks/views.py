from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.callbacks.receiver import create_callback
from abdm.callbacks.signature import CallbackSignatureError, verify_callback_signature
from abdm.models import AbdmCallback
from abdm.tasks import dispatch_callback


class GenericCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, path=""):
        receipt = create_callback(request, f"/{path}")
        callback = receipt.callback
        if receipt.duplicate:
            if callback.signature_status == AbdmCallback.SignatureStatus.OK:
                return Response({}, status=202)
            return Response({"errors": "Callback signature verification failed."}, status=401)
        try:
            verify_callback_signature(callback.headers_json)
        except CallbackSignatureError:
            callback.signature_status = AbdmCallback.SignatureStatus.FAILED
            callback.processed_status = AbdmCallback.ProcessedStatus.FAILED
            callback.save(update_fields=["signature_status", "processed_status", "modified_date"])
            return Response({"errors": "Callback signature verification failed."}, status=401)
        callback.signature_status = AbdmCallback.SignatureStatus.OK
        callback.processed_status = AbdmCallback.ProcessedStatus.QUEUED
        callback.save(update_fields=["signature_status", "processed_status", "modified_date"])
        dispatch_callback.delay(callback.id)
        return Response({}, status=202)


def _callback_summary(callback: AbdmCallback) -> dict:
    return {
        "id": str(callback.external_id),
        "path": callback.path,
        "operation_id": callback.operation_id,
        "request_id_header": callback.request_id_header,
        "response_request_id": callback.response_request_id,
        "transaction_id": callback.transaction_id,
        "signature_status": callback.signature_status,
        "processed_status": callback.processed_status,
        "received_at": callback.received_at,
    }


class CallbackList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({"errors": "Only a superuser can read ABDM callbacks."}, status=403)
        limit = min(max(int(request.query_params.get("limit", 20)), 1), 100)
        rows = AbdmCallback.objects.order_by("-received_at")[:limit]
        return Response({"results": [_callback_summary(row) for row in rows]})


class CallbackDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, callback_id):
        if not request.user.is_superuser:
            return Response({"errors": "Only a superuser can read ABDM callback headers."}, status=403)
        callback = get_object_or_404(AbdmCallback, external_id=callback_id)
        data = _callback_summary(callback)
        data.update(
            {
                "headers": callback.headers_json,
                "raw_body": callback.raw_body,
                "parsed_json": callback.parsed_json,
            }
        )
        return Response(data)
