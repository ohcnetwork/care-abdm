"""
Discovery and user-initiated linking (M2 journey 3).

Inbound callbacks on the bridge (paths conflict in the docs; the receiver accepts every variant):
  discover  {transactionId, patient{id, verifiedIdentifiers[], unverifiedIdentifiers[], name, gender, yearOfBirth}}
  init      {transactionId, abhaAddress, patient[{referenceNumber, display, careContexts[], hiType, count}]}
  confirm   {confirmation{token, linkRefNumber}}
Answers the HIP sends to the gateway (each 202):
  m2-on-discover-care-contexts, m2-receive-link-init (on-init), m2-receive-link-confirm (on-confirm)

Matching (ADR-008 decision 3): verified ABHA address or ABHA number only. No demographic match.
The OTP for link confirm is the HIP's own. The docs do not say how it is made or delivered
(docs/findings.md); this plug sends it with Care's SMS backend and keeps only a hash.
"""

import logging
import uuid

from care.emr.models.encounter import Encounter
from care.emr.models.patient import Patient
from django.conf import settings
from django.utils import timezone

from abdm.care_seams import AbhaAddressIdentifier, AbhaNumberIdentifier
from abdm.facility.service import facility_for_hip_id, get_config
from abdm.gateway import outbound
from abdm.gateway.session import utc_timestamp
from abdm.hip import rules
from abdm.hip.contexts import care_context_payload, ensure_care_context, schedule_notify
from abdm.models import AbdmCallback, AbdmCareContext, AbdmLinkSession

logger = logging.getLogger(__name__)

ON_DISCOVER_URL = "/api/hiecm/user-initiated-linking/v3/patient/care-context/on-discover"
ON_INIT_URL = "/api/hiecm/user-initiated-linking/v3/link/care-context/on-init"
ON_CONFIRM_URL = "/api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm"
# Care core uses a fixed OTP outside production (care/emr/api/otp_viewsets/login.py). Same rule here.
FIXED_OTP_OUTSIDE_PRODUCTION = "123456"


def facility_for_callback(callback: AbdmCallback):
    """The facility the gateway named in X-HIP-ID (HFR facility ID or the gateway service id)."""
    return facility_for_hip_id(callback.hip_id_header)


def find_patient(abha_address: str, abha_number: str) -> Patient | None:
    patient = AbhaAddressIdentifier.find_patient(abha_address.lower()) if abha_address else None
    if patient is None and abha_number:
        patient = AbhaNumberIdentifier.find_patient(abha_number)
    return patient


def contexts_for(patient: Patient, facility) -> list[AbdmCareContext]:
    """Every Encounter of the patient at this facility as a care context, newest first."""
    encounters = Encounter.objects.filter(patient=patient, facility=facility).order_by("-created_date")
    return [ensure_care_context(e) for e in encounters]


# --- discovery ---------------------------------------------------------------------------


def handle_discover(callback: AbdmCallback) -> dict:
    body = callback.parsed_json or {}
    transaction_id = str(body.get("transactionId") or "")
    patient_block = body.get("patient") if isinstance(body.get("patient"), dict) else {}
    address, number = rules.abha_candidates(patient_block)
    facility = facility_for_callback(callback)
    patient = find_patient(address, number) if facility else None
    patients: list[dict] = []
    contexts = [c for c in contexts_for(patient, facility) if c.hi_types] if patient else []
    if contexts:
        hi_types = sorted({t for c in contexts for t in c.hi_types})
        patients.append(
            rules.patient_block(
                str(patient.external_id), patient.name, [care_context_payload(c) for c in contexts], hi_types
            )
        )
    session, _ = AbdmLinkSession.objects.update_or_create(
        transaction_id=transaction_id,
        defaults={
            "facility": facility,
            "patient": patient,
            "abha_address": address or (patient and AbhaAddressIdentifier.get(patient)) or "",
            "status": AbdmLinkSession.Status.DISCOVERED,
        },
    )
    # The docs do not say how to answer when nothing matches: an empty `patient` list is sent.
    request = outbound.send(
        "m2-on-discover-care-contexts",
        ON_DISCOVER_URL,
        rules.on_discover_body(transaction_id, patients, callback.request_id_header),
        facility=facility,
        patient=patient,
    )
    return {
        "transaction_id": transaction_id,
        "matched": patient is not None,
        "care_contexts": sum(len(p["careContexts"]) for p in patients),
        "request_id": request.request_id,
        "sent": request.status,
        "session": str(session.external_id),
    }


# --- link init: send the OTP ---------------------------------------------------------------


def _send_otp(patient: Patient, hip_name: str, otp: str) -> None:
    from care.utils import sms

    text = f"{otp} is the OTP to link your health records at {hip_name}. It is valid for 10 minutes."
    try:
        sms.send_text_message(content=text, recipients=patient.phone_number, fail_silently=not settings.IS_PRODUCTION)
    except Exception:  # noqa: BLE001 - the link must still answer the gateway
        logger.exception("abdm: link OTP SMS failed for patient %s", patient.external_id)


def handle_link_init(callback: AbdmCallback) -> dict:
    body = callback.parsed_json or {}
    transaction_id = str(body.get("transactionId") or "")
    address = str(body.get("abhaAddress") or "").lower()
    requested = [
        str(cc.get("referenceNumber") or cc) if isinstance(cc, (dict, str)) else ""
        for block in (body.get("patient") or [])
        if isinstance(block, dict)
        for cc in (block.get("careContexts") or [])
    ]
    facility = facility_for_callback(callback)
    session = AbdmLinkSession.objects.filter(transaction_id=transaction_id).first()
    patient = session.patient if session and session.patient_id else find_patient(address, "")
    if session is None:
        session = AbdmLinkSession(transaction_id=transaction_id, facility=facility, patient=patient)
    session.abha_address = address or session.abha_address
    session.care_context_references = [r for r in requested if r]
    session.facility = session.facility or facility
    if patient is None:
        session.status = session.Status.FAILED
        session.error_code = "HIP_PATIENT_NOT_FOUND"
        session.error_message = "No Care patient carries this ABHA address"
        session.save()
        request = outbound.send(
            "m2-receive-link-init",
            ON_INIT_URL,
            rules.on_init_body(transaction_id, "", "", utc_timestamp(), callback.request_id_header)
            | {"error": {"code": session.error_code, "message": session.error_message}},
            facility=facility,
        )
        return {"transaction_id": transaction_id, "matched": False, "sent": request.status}
    otp = rules.new_otp() if settings.IS_PRODUCTION else FIXED_OTP_OUTSIDE_PRODUCTION
    session.link_reference_number = str(uuid.uuid4())
    session.otp_hash = rules.otp_hash(otp, session.link_reference_number)
    session.otp_expires_at = timezone.now() + rules.OTP_VALIDITY
    session.otp_attempts = 0
    session.status = session.Status.OTP_SENT
    session.error_code = ""
    session.error_message = ""
    session.save()
    config = get_config(session.facility) if session.facility else {}
    _send_otp(patient, config.get("hip_name") or (session.facility.name if session.facility else "your hospital"), otp)
    if not settings.IS_PRODUCTION:
        logger.info("abdm: link OTP for session %s is the fixed non-production value", session.external_id)
    request = outbound.send(
        "m2-receive-link-init",
        ON_INIT_URL,
        rules.on_init_body(
            transaction_id,
            session.link_reference_number,
            rules.mask_mobile(patient.phone_number),
            session.otp_expires_at.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            callback.request_id_header,
        ),
        facility=session.facility,
        patient=patient,
    )
    return {
        "transaction_id": transaction_id,
        "matched": True,
        "link_reference": session.link_reference_number,
        "sent": request.status,
    }


# --- link confirm: check the OTP, link the contexts ---------------------------------------


def handle_link_confirm(callback: AbdmCallback) -> dict:
    body = callback.parsed_json or {}
    confirmation = body.get("confirmation") if isinstance(body.get("confirmation"), dict) else {}
    link_ref = str(confirmation.get("linkRefNumber") or "")
    token = str(confirmation.get("token") or "")
    session = AbdmLinkSession.objects.filter(link_reference_number=link_ref).first() if link_ref else None
    facility = session.facility if session else facility_for_callback(callback)
    error: tuple[str, str] | None = None
    patients: list[dict] = []
    linked: list[AbdmCareContext] = []
    if session is None or session.status != session.Status.OTP_SENT:
        error = ("HIP_UNKNOWN_LINK_REFERENCE", "No open link request matches this reference number")
    elif session.otp_expires_at and session.otp_expires_at < timezone.now():
        error = ("HIP_OTP_EXPIRED", "The OTP has expired. Start the link again.")
    elif session.otp_attempts >= rules.OTP_MAX_ATTEMPTS:
        error = ("HIP_OTP_ATTEMPTS", "Too many wrong OTPs. Start the link again.")
    elif not rules.otp_matches(token, session.link_reference_number, session.otp_hash):
        session.otp_attempts += 1
        session.save(update_fields=["otp_attempts", "modified_date"])
        error = ("HIP_OTP_INVALID", "The OTP is wrong")
    else:
        linked = list(
            AbdmCareContext.objects.filter(
                patient=session.patient, facility=session.facility, reference_number__in=session.care_context_references
            )
        ) or [c for c in contexts_for(session.patient, session.facility) if c.hi_types]
        now = timezone.now()
        for context in linked:
            context.status = context.Status.LINKED
            context.linked_via = context.LinkedVia.USER
            context.linked_at = now
            context.error_code = ""
            context.error_message = ""
            context.save()
        hi_types = sorted({t for c in linked for t in (c.hi_types or [])})
        patients.append(
            rules.patient_block(
                str(session.patient.external_id),
                session.patient.name,
                [care_context_payload(c) for c in linked],
                hi_types,
            )
        )
        session.status = session.Status.CONFIRMED
        session.otp_hash = ""
        session.save(update_fields=["status", "otp_hash", "modified_date"])
    if error and session is not None and error[0] != "HIP_OTP_INVALID":
        session.status = session.Status.FAILED
        session.error_code, session.error_message = error
        session.save(update_fields=["status", "error_code", "error_message", "modified_date"])
    request = outbound.send(
        "m2-receive-link-confirm",
        ON_CONFIRM_URL,
        rules.on_confirm_body(patients, callback.request_id_header, error),
        facility=facility,
        patient=session.patient if session else None,
    )
    for context in linked:
        schedule_notify(context)
    return {"link_reference": link_ref, "confirmed": error is None, "error": error and error[0], "sent": request.status}
