"""
An exchange is 1 unit of work: the call, the wait, and the callback that answers it (abdm-m2
design.md, "The unit of work is an exchange, not a call"). Pure: no Django import.

The 5 outcomes the docs hold apart, and the words for each:

| state            | means                                                                       |
|------------------|-----------------------------------------------------------------------------|
| sent             | in the air: no HTTP answer yet                                              |
| accepted_waiting | 202 (or 200), the answer comes on a callback, nothing back yet              |
| answered         | the answer arrived: the HTTP body (synchronous) or the callback (asynchronous) |
| refused          | a synchronous refusal (4xx, 5xx, an error envelope, the host unreachable)   |
| no_answer        | accepted, then silence past the plug's window (`errors.CALLBACK_DEADLINE`)  |

"No timeout is published for any of these, so the honest words for the fifth outcome are that
nothing arrived in the window you chose." The window is the plug's, 10 minutes.

Kinds of outbound call, by operation id:
  call  the answer comes on a callback (EXPECTS_CALLBACK);
  ack   our answer to a request the gateway made of us; its body carries `response.requestId`,
        the REQUEST-ID of the inbound callback it answers, which is how the 2 are joined;
  push  our encrypted bundles to an HIU's data push URL (M2) — synchronous;
  sync  everything else: gateway, M1, M4, the providers list.
"""

from datetime import datetime, timedelta

# Operation ids whose answer is a callback (the gateway posts it to the bridge URL).
EXPECTS_CALLBACK = frozenset(
    {
        "m2-generate-link-token",  # -> /v3/hip/token/on-generate-token
        "m2-hip-link-care-context",  # -> /v3/link/on_carecontext
        "m2-link-care-context-notify",  # -> /v3/links/context/on-notify
        "m2-sms-deep-link-notify",  # -> /v3/patients/sms/on-notify
        "m3-consent-request-init",  # -> /v3/hiu/consent/request/on-init
        "m3-consent-request-status",  # -> /v3/hiu/consent/request/on-status
        "m3-consent-fetch",  # -> /v3/hiu/consent/on-fetch
        "m3-health-information-request",  # -> /v3/hiu/health-information/on-request, then the push
    }
)

# Our answers to inbound requests. `body.response.requestId` names the inbound REQUEST-ID.
ACKS = frozenset(
    {
        "m1-on-share-acknowledgement",
        "m2-on-discover-care-contexts",
        "m2-receive-link-init",
        "m2-receive-link-confirm",
        "m2-consent-hip-on-notify",
        "m2-hip-health-information-on-request",
        "m2-hip-data-flow-notify",
        "m3-consent-notify-ack",
        "m3-health-information-notify",
    }
)

PUSHES = frozenset({"m2-data-push"})

STATES = ("sent", "accepted_waiting", "answered", "refused", "no_answer")
KINDS = ("call", "ack", "push", "sync")
MODULES = ("gateway", "m1", "m2", "m3", "m4", "probe", "other")


def module_of(operation_id: str) -> str:
    prefix = (operation_id or "").split("-", 1)[0].lower()
    return prefix if prefix in MODULES else "other"


def kind_of(operation_id: str) -> str:
    if operation_id in EXPECTS_CALLBACK:
        return "call"
    if operation_id in ACKS:
        return "ack"
    if operation_id in PUSHES:
        return "push"
    return "sync"


def state_of(
    *,
    operation_id: str,
    status: str,
    http_status: int | None,
    sent_at: datetime | None,
    callbacks_received: int,
    now: datetime,
    window: timedelta,
) -> str:
    """1 of STATES for an outbound row (`AbdmOutboundRequest.status` is sent/succeeded/failed)."""
    if status == "sent" and http_status is None:
        return "sent"
    if status == "failed":
        return "refused"
    if kind_of(operation_id) != "call":
        return "answered"
    if callbacks_received > 0:
        return "answered"
    if sent_at is not None and now - sent_at > window:
        return "no_answer"
    return "accepted_waiting"


def reason_of(*, status: str, http_status: int | None, error_code: str) -> str:
    """Why a row is `refused`: the host was unreachable, or ABDM refused with this code."""
    if status != "failed":
        return ""
    if http_status is None:
        return f"unreachable: {error_code}" if error_code else "unreachable"
    return error_code or f"HTTP {http_status}"


def http_ms(sent_at: datetime | None, completed_at: datetime | None) -> int | None:
    if sent_at is None or completed_at is None:
        return None
    return max(0, round((completed_at - sent_at).total_seconds() * 1000))


def callback_seconds(sent_at: datetime | None, received_at: datetime | None) -> float | None:
    if sent_at is None or received_at is None:
        return None
    return max(0.0, round((received_at - sent_at).total_seconds(), 1))


def path_of(url: str) -> str:
    """The path of a URL without the host: what a reader compares with a docs page."""
    if "://" not in (url or ""):
        return url or ""
    rest = url.split("://", 1)[1]
    return "/" + rest.split("/", 1)[1] if "/" in rest else "/"


def summarize_error(response_json) -> str:
    """The first message in an ABDM answer, in any of the 3 envelopes, for a list row."""
    if isinstance(response_json, list):
        for item in response_json:
            text = summarize_error(item)
            if text:
                return text
        return ""
    if not isinstance(response_json, dict):
        return ""
    error = response_json.get("error")
    if isinstance(error, dict):
        return " ".join(str(error.get(k) or "") for k in ("code", "message") if error.get(k)).strip()
    details = response_json.get("details")
    if isinstance(details, list):
        for detail in details:
            if isinstance(detail, dict) and detail.get("message"):
                return " ".join(str(detail.get(k) or "") for k in ("code", "message") if detail.get(k)).strip()
    if response_json.get("message"):
        return " ".join(str(response_json.get(k) or "") for k in ("code", "message") if response_json.get(k)).strip()
    text = response_json.get("text")
    return str(text)[:200] if isinstance(text, str) else ""
