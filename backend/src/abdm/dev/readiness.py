"""
The readiness check of the developer explorer (ADR-018): what is missing, named, before a flow runs.

abdm-m2 design.md, "What the integrator needs on screen": "A readiness check that names what is
missing", and 2 configuration failures told apart: a missing facility id "cannot be sent" (a blocker,
refuse locally); a missing callback URL "sends and is accepted, and the answer has nowhere to go" (a
warning, send anyway). abdm-m3 design.md adds: "A capability that is going to fail should fail in
the readiness check, where an integrator is already looking for problems".

Every check answers `{id, status, what, next_step, detail?}` with status `ok`, `warning` or
`blocker`. No check returns a token or a secret; the gateway check reports that a token is cached
and when it expires, never the token. Live calls made here: the bridge read (1, cached bridge id).
"""

from datetime import datetime, timedelta

from django.core.cache import cache
from django.utils import timezone

from abdm.facility import service as facility_service
from abdm.gateway import bridge, certs, session
from abdm.models import AbdmCallback, AbdmOutboundRequest
from abdm.nhpr.client import CERT_CACHE_KEY as NHPR_CERT_CACHE_KEY
from abdm.settings import plugin_settings
from abdm.tasks import WORKER_HEARTBEAT_KEY

# The worker heartbeat comes from the 5-minute periodic task; 3 missed beats is silence.
WORKER_SILENCE = timedelta(minutes=15)
ENV_NAMES = (
    "CLIENT_ID",
    "CLIENT_SECRET",
    "GATEWAY_URL",
    "HSP_URL",
    "ABHA_URL",
    "CM_ID",
    "CALLBACK_BASE_URL",
)


def _check(check_id: str, status: str, what: str, next_step: str = "", **extra) -> dict:
    return {"id": check_id, "status": status, "what": what, "nextStep": next_step, **extra}


def _env() -> dict:
    missing = [name for name in ENV_NAMES if not getattr(plugin_settings, name)]
    present = {name: bool(getattr(plugin_settings, name)) for name in ENV_NAMES}
    if missing:
        return _check(
            "env",
            "blocker",
            f"{len(missing)} setting(s) are empty: {', '.join('ABDM_' + m for m in missing)}.",
            "Set them in the Care environment (`.env`, prefix ABDM_), then restart Care and the worker.",
            values=present,
        )
    return _check("env", "ok", f"All {len(ENV_NAMES)} ABDM_* settings are set.", values=present)


def _gateway_session() -> dict:
    ttl = None
    try:
        ttl = cache.ttl(session.CACHE_KEY) if hasattr(cache, "ttl") else None
    except Exception:  # noqa: BLE001
        ttl = None
    if cache.get(session.CACHE_KEY):
        detail = (
            f"A gateway session token is cached; it expires in {ttl} s."
            if ttl
            else "A gateway session token is cached."
        )
        return _check("gateway_session", "ok", detail)
    last = AbdmOutboundRequest.objects.filter(operation_id="gateway-sessions-create").order_by("-sent_at").first()
    if last is not None and last.status == AbdmOutboundRequest.Status.FAILED:
        return _check(
            "gateway_session",
            "blocker",
            f"The last session call was refused: HTTP {last.http_status} ({last.error_code}).",
            "Check ABDM_CLIENT_ID and ABDM_CLIENT_SECRET on the sandbox portal, then try again.",
            requestId=last.request_id,
        )
    return _check(
        "gateway_session",
        "warning",
        "No gateway session token is cached right now.",
        "The next call creates one. Open the gateway status probe to force it.",
    )


def _bridge() -> tuple[dict, dict]:
    """The bridge check and the live state it read (reused by the services check)."""
    state = bridge.bridge_state()
    if state["error"]:
        return (
            _check(
                "bridge_url",
                "warning" if not state["callback_url"] else "blocker",
                state["error"],
                "Set ABDM_CALLBACK_BASE_URL to the public https URL of this Care, then register the bridge URL.",
            ),
            state,
        )
    live = (state.get("bridge") or {}).get("url") or ""
    if not live:
        return (
            _check(
                "bridge_url",
                "warning",
                "The gateway holds no bridge URL for this client. Every call is accepted, and no callback can arrive.",
                "Register the bridge URL from /admin/abdm or `manage.py abdm_register_bridge_url`.",
                expected=state["callback_url"],
            ),
            state,
        )
    if live.rstrip("/") != state["callback_url"].rstrip("/"):
        return (
            _check(
                "bridge_url",
                "warning",
                f"The gateway posts callbacks to {live}, this deployment listens at {state['callback_url']}.",
                "Register the bridge URL again from /admin/abdm.",
                expected=state["callback_url"],
                live=live,
            ),
            state,
        )
    return _check("bridge_url", "ok", f"Callbacks arrive at {live}.", live=live), state


def _facilities(state: dict) -> dict:
    from care.facility.models import Facility

    services = state.get("services") or []
    rows = []
    for facility in Facility.objects.order_by("name"):
        config = facility_service.get_config(facility)
        if not config["facility_id"]:
            continue
        hip_id = facility_service.sync_hip_id(facility, services) if services else config["hip_id"]
        rows.append(
            {
                "id": str(facility.external_id),
                "name": facility.name,
                "facilityId": config["facility_id"],
                "hipId": hip_id,
            }
        )
    linked = len(rows)
    without_service = [r for r in rows if not r["hipId"]]
    if linked == 0:
        return _check(
            "facilities",
            "blocker",
            "No Care facility is linked to a registry record. No M2 or M3 call can name a facility.",
            "Open a facility's ABDM setup page and link its Health Facility Registry record.",
            facilities=rows,
        )
    if without_service:
        names = ", ".join(r["name"] for r in without_service)
        return _check(
            "facilities",
            "blocker",
            f"{len(without_service)} linked facility(ies) have no HIP service on the bridge: {names}.",
            "Press 'Register as HIP and HIU' on the setup page. A call sent with the bare HFR id gets no callback.",
            facilities=rows,
        )
    return _check("facilities", "ok", f"{linked} facility(ies) linked, each with a HIP service.", facilities=rows)


def _jwks() -> dict:
    if cache.get(certs.CACHE_KEY):
        return _check("gateway_jwks", "ok", "The gateway JWKS is cached: callback signatures can be verified.")
    return _check(
        "gateway_jwks",
        "warning",
        "The gateway JWKS is not cached. The first callback fetches it (1 call with the session token).",
    )


def _nhpr_certificate() -> dict:
    if cache.get(NHPR_CERT_CACHE_KEY):
        return _check("nhpr_certificate", "ok", "The NHPR public key is cached: M4 fields can be encrypted.")
    return _check(
        "nhpr_certificate",
        "warning",
        "The NHPR public key is not cached. The first M4 encryption fetches it.",
    )


def _worker(now: datetime) -> dict:
    seen = cache.get(WORKER_HEARTBEAT_KEY)
    if not seen:
        return _check(
            "worker",
            "blocker",
            "No Celery worker heartbeat has been seen. Callbacks stay queued and no link runs.",
            "Start the worker: `cd ~/ohc.network/care && ./scripts/celery-dev.sh` (beat runs in it).",
        )
    try:
        seen_at = datetime.fromisoformat(seen)
    except ValueError:
        seen_at = None
    if seen_at is None:
        return _check("worker", "warning", "The worker heartbeat could not be read.", lastSeen=seen)
    age = now - seen_at
    if age > WORKER_SILENCE:
        return _check(
            "worker",
            "blocker",
            f"The Celery worker was last seen {int(age.total_seconds() // 60)} min ago. Callbacks stay queued.",
            "Restart the worker. After a code change under backend/, it needs a restart or `kill -HUP`.",
            lastSeen=seen,
        )
    return _check("worker", "ok", f"The Celery worker was seen {int(age.total_seconds())} s ago.", lastSeen=seen)


def _traffic(now: datetime) -> dict:
    last_out = AbdmOutboundRequest.objects.order_by("-sent_at").values_list("sent_at", flat=True).first()
    last_in = AbdmCallback.objects.order_by("-received_at").values_list("received_at", flat=True).first()
    queued = AbdmCallback.objects.filter(
        processed_status__in=[AbdmCallback.ProcessedStatus.RECEIVED, AbdmCallback.ProcessedStatus.QUEUED]
    ).count()
    detail = {
        "lastOutboundAt": last_out,
        "lastCallbackAt": last_in,
        "callbacksQueued": queued,
        "outboundTotal": AbdmOutboundRequest.objects.count(),
        "callbackTotal": AbdmCallback.objects.count(),
    }
    if queued and last_in and now - last_in > timedelta(minutes=5):
        return _check(
            "traffic",
            "warning",
            f"{queued} callback(s) wait for a handler. The worker may be down or behind.",
            "Check the worker check above.",
            **detail,
        )
    if last_in is None:
        return _check(
            "traffic",
            "warning",
            "No callback has ever arrived. Until 1 does, the callback path is unproven.",
            "Send a link-token request from an Encounter of an ABHA patient; the callback lands in ~2 s.",
            **detail,
        )
    return _check("traffic", "ok", f"Last callback {last_in.isoformat()}.", **detail)


def readiness() -> dict:
    now = timezone.now()
    bridge_check, state = _bridge()
    checks = [
        _env(),
        _gateway_session(),
        bridge_check,
        _facilities(state),
        _jwks(),
        _nhpr_certificate(),
        _worker(now),
        _traffic(now),
    ]
    worst = "ok"
    for check in checks:
        if check["status"] == "blocker":
            worst = "blocker"
            break
        if check["status"] == "warning":
            worst = "warning"
    return {
        "status": worst,
        "checkedAt": now,
        "checks": checks,
        "hosts": {
            "gateway": plugin_settings.GATEWAY_URL,
            "abha": plugin_settings.ABHA_URL,
            "hsp": plugin_settings.HSP_URL,
            "cmId": plugin_settings.CM_ID,
            "callbackBase": plugin_settings.CALLBACK_BASE_URL,
        },
    }
