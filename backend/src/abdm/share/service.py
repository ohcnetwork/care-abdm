"""
Scan and Share (SHARE_PATIENT_PROFILE_701, m1-receive-patient-share + m1-on-share-acknowledgement).

Flow (docs: /docs/hiecm/v3/api/m1/endpoints/m1-receive-patient-share):
  1. The person scans the counter QR code in the PHR app and gives consent.
  2. The gateway posts `POST <bridge_url>/patient-share/v3/share` to this HIP.
  3. The HIP answers 2xx at once (callbacks/views.py) and queues this handler.
  4. This handler matches the facility by `metaData.hipId`, assigns a token number,
     stores the share for the front desk inbox, and sends
     `POST {GATEWAY_URL}/api/hiecm/patient-share/v3/on-share` with SUCCESS or FAILURE.
  5. The PHR app waits about 30 seconds for the acknowledgement and shows the token.

The counter list lives in the facility extension (facility/service.py::get_counters).
"""

import logging

from django.db import transaction
from django.utils import timezone

from abdm.care_seams import AbhaAddressIdentifier, AbhaNumberIdentifier
from abdm.facility import service as facility_service
from abdm.gateway import outbound
from abdm.models import AbdmCallback, AbdmProfileShare, AbhaTransaction
from abdm.share.rules import ack_body, prefill_profile, token_number

logger = logging.getLogger(__name__)

SHARE_CALLBACK_PATH = "/patient-share/v3/share"
SHARE_OPERATION_ID = "m1-receive-patient-share"
ACK_OPERATION_ID = "m1-on-share-acknowledgement"
ACK_URL = "/api/hiecm/patient-share/v3/on-share"


class ShareError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _patient_block(parsed: dict) -> dict:
    profile = parsed.get("profile") or {}
    patient = profile.get("patient") or {}
    return patient if isinstance(patient, dict) else {}


def _next_token_number(facility, context: str, received_at) -> str:
    """Sequential per facility, per counter, per local day. Format `<context>-<nnn>`."""
    day_start = timezone.localtime(received_at).replace(hour=0, minute=0, second=0, microsecond=0)
    count = (
        AbdmProfileShare.objects.select_for_update()
        .filter(facility=facility, context=context, received_at__gte=day_start, token_number__gt="")
        .count()
    )
    return token_number(context, count + 1)


def _find_patient(abha_number: str, abha_address: str):
    patient = None
    if abha_number:
        patient = AbhaNumberIdentifier.find_patient(abha_number)
    if patient is None and abha_address:
        patient = AbhaAddressIdentifier.find_patient(abha_address)
    return patient


def _ack_body(share: AbdmProfileShare, callback: AbdmCallback, *, error: ShareError | None = None) -> dict:
    return ack_body(
        abha_address=share.abha_address,
        context=share.context,
        token=share.token_number,
        request_id=callback.request_id_header,
        error=(error.code, error.message) if error else None,
    )


def _send_ack(share: AbdmProfileShare, callback: AbdmCallback, *, error: ShareError | None = None) -> None:
    body = _ack_body(share, callback, error=error)
    try:
        row = outbound.send(ACK_OPERATION_ID, ACK_URL, body, facility=share.facility, patient=share.patient)
    except Exception as exc:  # network error: the row is already marked FAILED by outbound.send
        logger.warning("abdm on-share failed to send: %s", exc)
        share.status = AbdmProfileShare.Status.ACK_FAILED
        share.error_code = share.error_code or exc.__class__.__name__
        share.error_message = share.error_message or str(exc)[:256]
        share.save(update_fields=["status", "error_code", "error_message", "modified_date"])
        return
    share.ack_request = row
    share.acknowledged_at = timezone.now()
    if row.status == row.Status.SUCCEEDED:
        share.status = AbdmProfileShare.Status.REJECTED if error else AbdmProfileShare.Status.ACKNOWLEDGED
    else:
        share.status = AbdmProfileShare.Status.ACK_FAILED
        share.error_code = share.error_code or row.error_code
        share.error_message = share.error_message or outbound.failure_detail(row)[:256]
    share.save(
        update_fields=["ack_request", "acknowledged_at", "status", "error_code", "error_message", "modified_date"]
    )


def handle_profile_share(callback: AbdmCallback) -> AbdmProfileShare:
    """Process one m1-receive-patient-share callback. Always sends an acknowledgement."""
    existing = AbdmProfileShare.objects.filter(callback=callback).first()
    if existing is not None:
        return existing
    parsed = callback.parsed_json or {}
    meta = parsed.get("metaData") or {}
    patient_block = _patient_block(parsed)
    hip_id = str(meta.get("hipId") or "")
    context = str(meta.get("context") or "")
    share = AbdmProfileShare(
        callback=callback,
        hip_id=hip_id,
        context=context,
        hpr_id=str(meta.get("hprId") or ""),
        abha_number=str(patient_block.get("abhaNumber") or ""),
        abha_address=str(patient_block.get("abhaAddress") or ""),
        profile=patient_block,
        received_at=callback.received_at or timezone.now(),
    )
    error: ShareError | None = None
    try:
        if parsed.get("intent") != "PROFILE_SHARE":
            raise ShareError("HIP_UNSUPPORTED_INTENT", "Only PROFILE_SHARE is supported")
        facility = facility_service.facility_for_hip_id(hip_id)
        if facility is None:
            raise ShareError(
                "HIP_UNKNOWN",
                f"No facility is configured for HIP ID {hip_id}. It must equal the HFR facility ID.",
            )
        share.facility = facility
        counters = facility_service.get_counters(facility)
        if counters and context.lower() not in {c.lower() for c in counters}:
            raise ShareError("HIP_UNKNOWN_COUNTER", f"Counter {context} is not configured at this facility")
        if not share.abha_address and not share.abha_number:
            raise ShareError("HIP_INVALID_PROFILE", "The shared profile has no ABHA address or ABHA number")
        with transaction.atomic():
            share.token_number = _next_token_number(facility, context, share.received_at)
            share.patient = _find_patient(share.abha_number, share.abha_address)
            share.transaction = AbhaTransaction.objects.create(
                txn_id=f"share:{callback.external_id}",
                kind=AbhaTransaction.Kind.PROFILE_SHARE,
                abha_number=share.abha_number,
                abha_address=share.abha_address,
                profile=prefill_profile(patient_block, timezone.now().isoformat()),
                is_new=False,
            )
            share.save()
    except ShareError as exc:
        error = exc
        share.status = AbdmProfileShare.Status.REJECTED
        share.error_code = exc.code
        share.error_message = exc.message[:256]
        share.save()
    _send_ack(share, callback, error=error)
    return share


def share_summary(share: AbdmProfileShare) -> dict:
    """What the front desk may see. kycPhoto is not sent to the browser list."""
    profile = {k: v for k, v in (share.profile or {}).items() if k != "kycPhoto"}
    return {
        "id": str(share.external_id),
        "status": share.status,
        "context": share.context,
        "tokenNumber": share.token_number,
        "abhaNumber": share.abha_number,
        "abhaAddress": share.abha_address,
        "profile": profile,
        "hasPhoto": bool((share.profile or {}).get("kycPhoto")),
        "patient": str(share.patient.external_id) if share.patient_id else None,
        "patientName": share.patient.name if share.patient_id else None,
        "txnId": share.transaction.txn_id if share.transaction_id else None,
        "errorCode": share.error_code,
        "errorMessage": share.error_message,
        "receivedAt": share.received_at,
        "acknowledgedAt": share.acknowledged_at,
        "dismissedAt": share.dismissed_at,
    }


def inbox(facility, *, include_dismissed: bool = False, limit: int = 50):
    since = timezone.now() - timezone.timedelta(hours=24)
    rows = AbdmProfileShare.objects.filter(facility=facility, received_at__gte=since)
    if not include_dismissed:
        rows = rows.filter(dismissed_at__isnull=True)
    return rows.select_related("patient", "transaction").order_by("-received_at")[:limit]


def dismiss(share: AbdmProfileShare, user) -> AbdmProfileShare:
    if share.dismissed_at is None:
        share.dismissed_at = timezone.now()
        share.dismissed_by = user
        share.save(update_fields=["dismissed_at", "dismissed_by", "modified_date"])
    return share
