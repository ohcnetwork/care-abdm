import json
from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from abdm.callbacks.identity import body_value, idempotency_key, identity
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
    return body_value(parsed, path)


def create_callback(request, path: str) -> CallbackReceipt:
    raw_body = request.body
    headers = {k: v for k, v in request.headers.items()}
    parsed = parse_json(raw_body)
    request_id = _header_value(headers, "REQUEST-ID")
    response_request_id = _body_value(parsed, ("response", "requestId"))
    transaction_id = _body_value(parsed, ("transactionId",))
    operation_id = operation_for_path(path)
    key = idempotency_key(
        path, request_id, response_request_id, transaction_id, raw_body, identity(operation_id, parsed)
    )
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
