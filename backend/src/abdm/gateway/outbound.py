import logging
from typing import Any

import requests
from django.utils import timezone

from abdm.gateway.session import gateway_headers, get_access_token
from abdm.models import AbdmOutboundRequest
from abdm.settings import plugin_settings

logger = logging.getLogger(__name__)


def _json_or_text(response):
    try:
        return response.json() if response.text else {}
    except ValueError:
        return {"text": response.text}


def _hip_id(facility) -> str:
    if facility is None:
        return ""
    ext = (facility.extensions or {}).get("abdm") or {}
    source = ext.get("x_hip_id_source") or "hip_id"
    return ext.get(source) or ext.get("hip_id") or ""


def send(
    operation_id: str,
    url: str,
    body: dict | None,
    *,
    method: str = "POST",
    facility=None,
    patient=None,
    encounter=None,
    extra_headers: dict[str, str] | None = None,
) -> AbdmOutboundRequest:
    headers = gateway_headers(get_access_token())
    hip_id = _hip_id(facility)
    if hip_id:
        headers["X-HIP-ID"] = hip_id
    if extra_headers:
        headers.update(extra_headers)
    full_url = url if url.startswith(("http://", "https://")) else f"{plugin_settings.GATEWAY_URL}{url}"
    request_json: dict[str, Any] = {"url": full_url, "method": method.upper(), "body": body or {}}
    row = AbdmOutboundRequest.objects.create(
        request_id=headers["REQUEST-ID"],
        operation_id=operation_id,
        facility=facility,
        patient=patient,
        encounter=encounter,
        status=AbdmOutboundRequest.Status.SENT,
        request_json=request_json,
        sent_at=timezone.now(),
    )
    try:
        response = requests.request(
            method,
            full_url,
            headers=headers,
            json=body if method.upper() not in {"GET", "DELETE"} else None,
            timeout=plugin_settings.REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        row.status = AbdmOutboundRequest.Status.FAILED
        row.error_code = exc.__class__.__name__
        row.response_json = {"message": str(exc)}
        row.completed_at = timezone.now()
        row.save(update_fields=["status", "error_code", "response_json", "completed_at", "modified_date"])
        raise
    response_json = _json_or_text(response)
    row.http_status = response.status_code
    row.response_json = response_json
    row.completed_at = timezone.now()
    if 200 <= response.status_code < 300:
        row.status = AbdmOutboundRequest.Status.SUCCEEDED
    else:
        row.status = AbdmOutboundRequest.Status.FAILED
        error = response_json.get("error") if isinstance(response_json, dict) else None
        row.error_code = error.get("code", "") if isinstance(error, dict) else f"HTTP_{response.status_code}"
    row.save(
        update_fields=[
            "http_status",
            "response_json",
            "completed_at",
            "status",
            "error_code",
            "modified_date",
        ]
    )
    logger.info("abdm %s -> HTTP %s (REQUEST-ID %s)", operation_id, response.status_code, row.request_id)
    return row
