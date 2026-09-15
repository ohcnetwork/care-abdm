import hashlib
import json
from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from abdm.models import AbdmCallback, AbdmOutboundRequest

CALLBACK_OPERATION_BY_PATH = {
    # M1 Scan and Share (SHARE_PATIENT_PROFILE_701). Handled by abdm/share/service.py.
    "/patient-share/v3/share": "m1-receive-patient-share",
    "/v3/hip/token/on-generate-token": "m2-on-generate-token-result",
    "/v3/link/on_carecontext": "m2-on-carecontext-result",
    "/v3/links/context/on-notify": "m2-on-context-notify-result",
    "/v3/patients/sms/on-notify": "m2-on-sms-notify-result",
    "/api/v3/hip/patient/care-context/discover": "m2-on-discovery-request",
    "/v0.5/care-contexts/discover": "m2-on-discovery-request",
    "/api/v3/hip/link/care-context/init": "m2-on-link-init",
    "/v0.5/links/link/init": "m2-on-link-init",
    "/api/v3/hip/link/care-context/confirm": "m2-on-link-confirm",
    "/v0.5/links/link/confirm": "m2-on-link-confirm",
    # The HIP consent notification. 2 paths in the docs: the M2 on-notify page names
    # `/v0.5/consents/hip/notify`; the M3 page m3-on-consent-request-notify-hip names
    # `/api/v3/consent/request/hip/notify`. Handled by abdm/hip/consent.py.
    "/v0.5/consents/hip/notify": "m2-consent-hip-notify",
    "/api/v3/consent/request/hip/notify": "m2-consent-hip-notify",
    "/api/v3/hip/health-information/request": "m2-on-health-information-request",
    "/v0.5/health-information/hip/request": "m2-on-health-information-request",
}


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
    operation_id = CALLBACK_OPERATION_BY_PATH.get(path, "")
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
