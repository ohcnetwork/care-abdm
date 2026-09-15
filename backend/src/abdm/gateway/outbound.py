import logging
from typing import Any

import requests
from django.utils import timezone

from abdm.facility.service import hip_id_for
from abdm.gateway.session import gateway_headers, get_access_token, new_request_id  # noqa: F401
from abdm.models import AbdmOutboundRequest
from abdm.settings import plugin_settings

logger = logging.getLogger(__name__)


def _json_or_text(response):
    try:
        return response.json() if response.text else {}
    except ValueError:
        return {"text": response.text}


def response_errors(payload: Any) -> list[dict]:
    """
    Return the `{"error": {...}}` envelopes inside a response body.

    ABDM answers some calls with HTTP 200 and an error envelope in the body.
    Observed 2026-09-14 on `gateway-register-bridge-services`:
        HTTP 200 [{"error": {"code": "2500", "message": "Provided facility name
        is not matched with registered name"}}]
    A body like that is a failure, so `send()` uses this test to reject a 2xx
    response. The test stays strict on purpose: only this envelope marks a 2xx
    response as failed, so a normal success body never fails by accident.
    """
    if isinstance(payload, dict):
        error = payload.get("error")
        return [error] if isinstance(error, dict) and error else []
    if isinstance(payload, list):
        return [error for item in payload for error in response_errors(item)]
    return []


def _error_lines(payload: Any) -> list[str]:
    """
    Read every error message out of a response body, in any shape ABDM uses.

    Three shapes are observed against the sandbox:
      1. `{"error": {"code", "message"}}`, also inside a list.
      2. `{"code": "HIS-400", "message": "...", "details": [{"code", "message",
         "attribute": {"key", "value"}}]}` from the HSP Registry.
      3. `{"text": "Please make a valid request."}` when the host answers
         plain text (`_json_or_text` wraps it).
    """
    if isinstance(payload, list):
        return [line for item in payload for line in _error_lines(item)]
    if not isinstance(payload, dict):
        return []
    error = payload.get("error")
    if isinstance(error, dict) and error:
        return _error_lines(error)
    lines = []
    code = str(payload.get("code", "") or "")
    message = str(payload.get("message", "") or "")
    attribute = payload.get("attribute")
    key = attribute.get("key", "") if isinstance(attribute, dict) else ""
    line = " ".join(part for part in (code, message) if part)
    if line and key:
        line = f"{line} ({key})"
    if line:
        lines.append(line)
    for detail in payload.get("details") or []:
        lines.extend(_error_lines(detail))
    text = str(payload.get("text", "") or "").strip()
    if text and not lines:
        lines.append(text)
    return lines


def _error_code(payload: Any) -> str:
    """The most specific ABDM error code in a response body, or an empty string."""
    if isinstance(payload, list):
        for item in payload:
            code = _error_code(item)
            if code:
                return code
        return ""
    if not isinstance(payload, dict):
        return ""
    error = payload.get("error")
    if isinstance(error, dict) and error:
        return str(error.get("code", "") or "")
    return str(payload.get("code", "") or "")


def failure_detail(row: AbdmOutboundRequest) -> str:
    """One human-readable line for an outbound row that did not succeed."""
    lines = _error_lines(row.response_json)
    detail = " | ".join(dict.fromkeys(lines))
    head = f"HTTP {row.http_status}"
    if detail:
        head = f"{head}: {detail}"
    return f"{head} (REQUEST-ID {row.request_id})"


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
    request_id: str | None = None,
) -> AbdmOutboundRequest:
    """Send 1 call to ABDM (or to an HIU data-push URL) and record it as an AbdmOutboundRequest.

    `request_id` lets a caller reuse the REQUEST-ID it already put in the body (SMS deep link)."""
    headers = gateway_headers(get_access_token())
    if request_id:
        headers["REQUEST-ID"] = request_id
    hip_id = hip_id_for(facility)
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
    errors = response_errors(response_json)
    row.http_status = response.status_code
    row.response_json = response_json
    row.completed_at = timezone.now()
    if 200 <= response.status_code < 300 and not errors:
        row.status = AbdmOutboundRequest.Status.SUCCEEDED
    else:
        row.status = AbdmOutboundRequest.Status.FAILED
        row.error_code = _error_code(response_json)[:128] or f"HTTP_{response.status_code}"
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
