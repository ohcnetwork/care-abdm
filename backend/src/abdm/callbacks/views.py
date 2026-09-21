import logging

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.callbacks.receiver import create_callback
from abdm.callbacks.signature import (
    CallbackSignatureError,
    redact_headers,
    seconds_late,
    verify_callback_signature,
)
from abdm.models import AbdmCallback
from abdm.tasks import dispatch_callback

logger = logging.getLogger(__name__)


class GenericCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, path=""):
        """Store first, verify second, never raise: Care runs every request in a transaction
        (ATOMIC_REQUESTS), so an exception here would roll the stored callback back and leave no
        evidence of what the gateway sent."""
        receipt = create_callback(request, f"/{path}")
        callback = receipt.callback
        if receipt.duplicate:
            if callback.signature_status == AbdmCallback.SignatureStatus.OK:
                return Response({}, status=202)
            return Response({"errors": "Callback signature verification failed."}, status=401)
        try:
            claims, header_name = verify_callback_signature(callback.headers_json)
        except CallbackSignatureError as exc:
            return self._refuse(callback, str(exc), status=401)
        except Exception as exc:  # noqa: BLE001 - our side failed (JWKS fetch); keep the row, ask for a retry
            logger.exception("abdm callback %s: verification could not run", callback.external_id)
            return self._refuse(callback, f"Verification unavailable: {exc}", status=503)
        late = seconds_late(claims)
        callback.signature_status = AbdmCallback.SignatureStatus.OK
        callback.signature_header = header_name[:64]
        # Not an error: evidence that ABDM repeated a late delivery (ADR-012 D4).
        callback.signature_error = f"Accepted {late} s after the token expired." if late else ""
        callback.processed_status = AbdmCallback.ProcessedStatus.QUEUED
        callback.save(
            update_fields=[
                "signature_status",
                "signature_header",
                "signature_error",
                "processed_status",
                "modified_date",
            ]
        )
        dispatch_callback.delay(callback.id)
        return Response({}, status=202)

    @staticmethod
    def _refuse(callback: AbdmCallback, reason: str, *, status: int) -> Response:
        callback.signature_status = AbdmCallback.SignatureStatus.FAILED
        callback.signature_error = reason[:256]
        callback.processed_status = AbdmCallback.ProcessedStatus.FAILED
        callback.save(update_fields=["signature_status", "signature_error", "processed_status", "modified_date"])
        return Response({"errors": "Callback signature verification failed."}, status=status)


def _callback_summary(callback: AbdmCallback) -> dict:
    return {
        "id": str(callback.external_id),
        "path": callback.path,
        "operation_id": callback.operation_id,
        "request_id_header": callback.request_id_header,
        "response_request_id": callback.response_request_id,
        "transaction_id": callback.transaction_id,
        "signature_status": callback.signature_status,
        "signature_header": callback.signature_header,
        "signature_error": callback.signature_error,
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
                # Names and lengths only: the signed token is a credential, and this panel is a browser.
                "headers": redact_headers(callback.headers_json),
                "raw_body": callback.raw_body,
                "parsed_json": callback.parsed_json,
            }
        )
        return Response(data)
