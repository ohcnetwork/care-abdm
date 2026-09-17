import hashlib
import json
from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from abdm.callbacks.paths import operation_for_path
from abdm.models import AbdmCallback, AbdmOutboundRequest


@dataclass
class CallbackReceipt:
    callback: AbdmCallback
    duplicate: bool


def _header_value(headers: dict[str, str], name: str) -> str:
    for key, value in headers.items():
        if key.lower() == name.lower():
            return value
    return ""


def parse_json(raw_body: bytes) -> dict:
    if not raw_body:
        return {}
    try:
        data = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _body_value(parsed: dict, path: tuple[str, ...]) -> str:
    current = parsed
    for part in path:
        if not isinstance(current, dict):
            return ""
        current = current.get(part)
    return str(current or "")


def _idempotency_key(path: str, request_id: str, response_request_id: str, transaction_id: str, raw_body: bytes) -> str:
    h = hashlib.sha256()
    for value in (path, request_id, response_request_id, transaction_id):
        h.update(value.encode("utf-8"))
        h.update(b"\0")
    h.update(raw_body)
    return h.hexdigest()


def create_callback(request, path: str) -> CallbackReceipt:
    raw_body = request.body
    headers = {k: v for k, v in request.headers.items()}
    parsed = parse_json(raw_body)
    request_id = _header_value(headers, "REQUEST-ID")
    response_request_id = _body_value(parsed, ("response", "requestId"))
    transaction_id = _body_value(parsed, ("transactionId",))
    key = _idempotency_key(path, request_id, response_request_id, transaction_id, raw_body)
    operation_id = operation_for_path(path)
    outbound = None
    if response_request_id:
        outbound = AbdmOutboundRequest.objects.filter(request_id=response_request_id).first()
    try:
        with transaction.atomic():
            callback = AbdmCallback.objects.create(
                path=path,
                operation_id=operation_id,
                request_id_header=request_id,
                timestamp_header=_header_value(headers, "TIMESTAMP"),
                hip_id_header=_header_value(headers, "X-HIP-ID"),
                headers_json=headers,
                raw_body=raw_body.decode("utf-8", errors="replace"),
                parsed_json=parsed,
                response_request_id=response_request_id,
                transaction_id=transaction_id,
                idempotency_key=key,
                outbound_request=outbound,
                received_at=timezone.now(),
            )
    except IntegrityError:
        return CallbackReceipt(AbdmCallback.objects.get(idempotency_key=key), True)
    return CallbackReceipt(callback, False)
