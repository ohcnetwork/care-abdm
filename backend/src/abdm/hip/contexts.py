"""
HIP-initiated linking (M2 journey 1) and the SMS deep link (journey 2).

Flow (/docs/hiecm/v3/milestones/m2, /docs/hiecm/v3/concepts/linking):
  1. The patient has an ABHA address (M1) and the facility has an HFR facility ID (setup page).
  2. `ensure_link_token()` sends m2-generate-link-token (202). The token arrives on
     `/v3/hip/token/on-generate-token`; it is stored per patient and facility for 6 months.
  3. `request_link()` sends m2-hip-link-care-context with `X-Link-Token` (202). The context is
     linked only when `/v3/link/on_carecontext` arrives with `status` (whats-new 2026-09-10).
  4. `notify_context()` sends m2-link-care-context-notify after a link, and again when a linked
     context gains records. `/v3/links/context/on-notify` acknowledges it.
Every ABDM call goes through gateway.outbound.send(), which adds X-HIP-ID for the facility.
"""

import logging

from care.emr.models.encounter import Encounter
from care.emr.models.patient import Patient
from django.utils import timezone

from abdm.care_seams import AbhaAddressIdentifier, AbhaNumberIdentifier
from abdm.facility.service import facility_for_hip_id, get_config, hip_id_for
from abdm.fhir import available_hi_types
from abdm.gateway import outbound
from abdm.gateway.session import utc_timestamp
from abdm.hip import rules
from abdm.models import AbdmCallback, AbdmCareContext, AbdmLinkToken, AbdmOutboundRequest

logger = logging.getLogger(__name__)

GENERATE_TOKEN_URL = "/api/hiecm/v3/token/generate-token"
LINK_URL = "/api/hiecm/hip/v3/link/carecontext"
NOTIFY_URL = "/api/hiecm/hip/v3/link/context/notify"
SMS_URL = "/api/hiecm/hip/v3/link/patient/links/sms/notify2"

# m2-errors: "ABDM-1056 This care contexts has been already linked" -> treat as success.
ALREADY_LINKED_CODES = {"ABDM-1056"}
# m2-errors: "ABDM-1092 Duplicate Link token request". Observed 2026-09-15 with a fresh REQUEST-ID:
# the gateway still holds the earlier request for this ABHA at this HIP open, and its callback
# is the answer. The docs' remedy "New request id" does not apply (findings F6).
DUPLICATE_TOKEN_REQUEST = "ABDM-1092"


class LinkingError(Exception):
    pass


# --- patient and care-context state ------------------------------------------------------


def patient_abha(patient: Patient) -> tuple[str, str]:
    """(abha_address, abha_number) held on the Care patient, or empty strings."""
    return AbhaAddressIdentifier.get(patient) or "", AbhaNumberIdentifier.get(patient) or ""


def encounter_start(encounter: Encounter):
    start = rules.parse_iso((encounter.period or {}).get("start")) if isinstance(encounter.period, dict) else None
    return start or encounter.created_date


def ensure_care_context(encounter: Encounter) -> AbdmCareContext:
    """Create or refresh the care-context row for an Encounter. Display and HI types are recomputed;
    the link status is kept."""
    display = rules.care_context_display(encounter.encounter_class, encounter_start(encounter))
    hi_types = available_hi_types(encounter)
    context, created = AbdmCareContext.objects.get_or_create(
        encounter=encounter,
        defaults={
            "patient": encounter.patient,
            "facility": encounter.facility,
            "reference_number": str(encounter.external_id),
            "display": display,
            "hi_types": hi_types,
        },
    )
    if not created and (context.display != display or context.hi_types != hi_types):
        context.display = display
        context.hi_types = hi_types
        context.save(update_fields=["display", "hi_types", "modified_date"])
    return context


def care_context_payload(context: AbdmCareContext) -> dict:
    return {"referenceNumber": context.reference_number, "display": context.display}


def patient_block_for(patient: Patient, contexts: list[AbdmCareContext]) -> dict:
    hi_types = sorted({t for c in contexts for t in (c.hi_types or [])})
    return rules.patient_block(
        str(patient.external_id), patient.name, [care_context_payload(c) for c in contexts], hi_types
    )


def _fail(context: AbdmCareContext, code: str, message: str, *, status: str | None = None) -> AbdmCareContext:
    context.error_code = code[:64]
    context.error_message = message[:512]
    if status:
        context.status = status
    context.save(update_fields=["error_code", "error_message", "status", "modified_date"])
    return context


# --- link token -------------------------------------------------------------------------


def ensure_link_token(patient: Patient, facility) -> AbdmLinkToken:
    """Return the token row. Sends m2-generate-link-token when no usable token exists and no
    request is in flight. The token itself arrives on the callback."""
    address, number = patient_abha(patient)
    if not address:
        raise LinkingError("The patient has no ABHA address. Link an ABHA first.")
    row, _ = AbdmLinkToken.objects.get_or_create(patient=patient, facility=facility, defaults={"abha_address": address})
    if row.usable:
        return row
    in_flight = (
        row.status == row.Status.REQUESTED
        and row.request_id
        and row.request.sent_at
        and (timezone.now() - row.request.sent_at).total_seconds() < 120
    )
    if in_flight:
        return row
    year = patient.year_of_birth or (patient.date_of_birth.year if patient.date_of_birth else None)
    if not year:
        raise LinkingError("The patient has no year of birth. ABDM needs it for the link token.")
    body = rules.generate_token_body(address, number, patient.name, patient.gender, year)
    request = outbound.send("m2-generate-link-token", GENERATE_TOKEN_URL, body, facility=facility, patient=patient)
    row.abha_address = address
    if request.status == request.Status.SUCCEEDED:
        row.request = request
        row.status = row.Status.REQUESTED
        row.error_code = ""
        row.error_message = ""
    elif request.error_code == DUPLICATE_TOKEN_REQUEST:
        # Keep the earlier request: the callback echoes its REQUEST-ID, not this one.
        row.status = row.Status.REQUESTED
        row.error_code = DUPLICATE_TOKEN_REQUEST
        row.error_message = (
            "The gateway still holds an open link-token request for this patient at this facility. "
            "Waiting for its callback; a new request is refused until then."
        )
    else:
        row.request = request
        row.status = row.Status.FAILED
        row.error_code = request.error_code[:64]
        row.error_message = outbound.failure_detail(request)[:512]
    row.save()
    return row


def handle_generate_token_result(callback: AbdmCallback) -> dict:
    """`/v3/hip/token/on-generate-token`: {abhaAddress, linkToken, error, response.requestId}."""
    row = _token_for_callback(callback)
    body = callback.parsed_json or {}
    error = body.get("error") if isinstance(body.get("error"), dict) else None
    token = str(body.get("linkToken") or "")
    if token and not error:
        row.token = token
        row.expires_at = rules.link_token_expiry(token, timezone.now())
        row.status = row.Status.ACTIVE
        row.error_code = ""
        row.error_message = ""
        row.save()
        linked = link_pending_contexts(row.patient, row.facility)
        return {"link_token": "active", "expires_at": row.expires_at.isoformat(), "links_requested": linked}
    row.status = row.Status.FAILED
    row.error_code = str((error or {}).get("code") or "NO_TOKEN")[:64]
    row.error_message = str((error or {}).get("message") or "The callback carried no linkToken")[:512]
    row.save()
    for context in AbdmCareContext.objects.filter(
        patient=row.patient, facility=row.facility, status=AbdmCareContext.Status.PENDING
    ):
        _fail(context, row.error_code, f"Link token failed: {row.error_message}")
    return {"link_token": "failed", "error": row.error_code}


def _token_for_callback(callback: AbdmCallback) -> AbdmLinkToken:
    outbound_row = callback.outbound_request
    if outbound_row is None and callback.response_request_id:
        outbound_row = AbdmOutboundRequest.objects.filter(request_id=callback.response_request_id).first()
    row = AbdmLinkToken.objects.filter(request=outbound_row).first() if outbound_row else None
    if row is None:
        # Fall back to the ABHA address in the body: the gateway may echo an earlier request id, and
        # the row may have moved on (failed on ABDM-1092, or re-requested) since that request.
        address = str((callback.parsed_json or {}).get("abhaAddress") or "").lower()
        rows = AbdmLinkToken.objects.filter(abha_address__iexact=address)
        facility = facility_for_hip_id(callback.hip_id_header)
        if facility is not None:
            rows = rows.filter(facility=facility)
        row = rows.order_by("-modified_date").first()
    if row is None:
        raise LinkingError(f"No link-token request matches callback {callback.external_id}")
    return row


# --- linking ----------------------------------------------------------------------------


def sync_encounter(encounter: Encounter) -> AbdmCareContext | None:
    """The one entry point for an Encounter: create the context, then link it or notify about new
    records. Returns None when the facility is not set up for ABDM."""
    if not hip_id_for(encounter.facility):
        return None
    address, _ = patient_abha(encounter.patient)
    previous = AbdmCareContext.objects.filter(encounter=encounter).values_list("hi_types", flat=True).first()
    context = ensure_care_context(encounter)
    if not address:
        return _fail(context, "NO_ABHA", "The patient has no ABHA address. Link an ABHA first.")
    if not context.hi_types:
        return _fail(context, "NO_RECORDS", "The encounter has no shareable records yet.")
    if context.status == context.Status.LINKED:
        if previous is not None and set(previous) != set(context.hi_types):
            return notify_context(context)
        return context
    if context.status == context.Status.LINK_REQUESTED:
        return context
    return request_link(context)


def request_link(context: AbdmCareContext) -> AbdmCareContext:
    try:
        token = ensure_link_token(context.patient, context.facility)
    except LinkingError as exc:
        return _fail(context, "NO_LINK_TOKEN", str(exc))
    if token.status == token.Status.FAILED:
        return _fail(context, token.error_code or "LINK_TOKEN_FAILED", token.error_message or "Link token failed")
    if not token.usable:
        # Token requested; handle_generate_token_result() continues from here.
        context.status = context.Status.PENDING
        context.error_code = token.error_code if token.error_code == DUPLICATE_TOKEN_REQUEST else ""
        context.error_message = token.error_message or "Waiting for the link token"
        context.save(update_fields=["status", "error_code", "error_message", "modified_date"])
        return context
    address, number = patient_abha(context.patient)
    body = rules.link_body(address, number, patient_block_for(context.patient, [context]))
    request = outbound.send(
        "m2-hip-link-care-context",
        LINK_URL,
        body,
        facility=context.facility,
        patient=context.patient,
        encounter=context.encounter,
        extra_headers={"X-Link-Token": token.token},
    )
    context.link_request = request
    if request.status == request.Status.SUCCEEDED:
        context.status = context.Status.LINK_REQUESTED
        context.error_code = ""
        context.error_message = ""
    else:
        context.status = context.Status.FAILED
        context.error_code = request.error_code[:64]
        context.error_message = outbound.failure_detail(request)[:512]
        if request.error_code in {"ABDM-1026", "ABDM-1038", "ABDM-1063"}:
            # Invalid or mismatched link token: drop it so the next attempt regenerates it.
            AbdmLinkToken.objects.filter(pk=token.pk).update(status=AbdmLinkToken.Status.FAILED, token="")
    context.save()
    return context


def link_pending_contexts(patient: Patient, facility) -> int:
    count = 0
    for context in AbdmCareContext.objects.filter(
        patient=patient, facility=facility, status=AbdmCareContext.Status.PENDING
    ):
        if context.hi_types and request_link(context).status == AbdmCareContext.Status.LINK_REQUESTED:
            count += 1
    return count


def _context_for_callback(callback: AbdmCallback, field: str) -> AbdmCareContext:
    outbound_row = callback.outbound_request
    if outbound_row is None and callback.response_request_id:
        outbound_row = AbdmOutboundRequest.objects.filter(request_id=callback.response_request_id).first()
    context = AbdmCareContext.objects.filter(**{field: outbound_row}).first() if outbound_row else None
    if context is None:
        raise LinkingError(f"No {field} matches callback {callback.external_id}")
    return context


def handle_carecontext_result(callback: AbdmCallback) -> dict:
    """`/v3/link/on_carecontext`: {abhaAddress, status, error{code,message}, response.requestId}.
    `status` is free text on the docs page, so success = no error block."""
    context = _context_for_callback(callback, "link_request")
    body = callback.parsed_json or {}
    error = body.get("error") if isinstance(body.get("error"), dict) else None
    code = str((error or {}).get("code") or "")
    if error and code not in ALREADY_LINKED_CODES:
        _fail(context, code or "LINK_FAILED", str(error.get("message") or "Link failed"), status=context.Status.FAILED)
        return {"care_context": context.reference_number, "status": "failed", "error": code}
    context.status = context.Status.LINKED
    context.linked_via = context.LinkedVia.HIP
    context.linked_at = timezone.now()
    context.error_code = ""
    context.error_message = ""
    context.save()
    notify_context(context)
    return {"care_context": context.reference_number, "status": "linked", "gateway_status": body.get("status")}


def notify_context(context: AbdmCareContext) -> AbdmCareContext:
    address, _ = patient_abha(context.patient)
    config = get_config(context.facility)
    body = rules.notify_body(
        address,
        context.reference_number,
        context.hi_types,
        utc_timestamp(),
        config["hip_id"],
        config.get("hip_name") or config.get("facility_name") or context.facility.name,
    )
    request = outbound.send(
        "m2-link-care-context-notify",
        NOTIFY_URL,
        body,
        facility=context.facility,
        patient=context.patient,
        encounter=context.encounter,
    )
    context.notify_request = request
    if request.status != request.Status.SUCCEEDED:
        context.error_code = request.error_code[:64]
        context.error_message = f"Notify failed: {outbound.failure_detail(request)}"[:512]
    context.save(update_fields=["notify_request", "error_code", "error_message", "modified_date"])
    return context


def handle_context_notify_result(callback: AbdmCallback) -> dict:
    """`/v3/links/context/on-notify`: {acknowledgement.status SUCCESS|ERRORED, error, response.requestId}."""
    context = _context_for_callback(callback, "notify_request")
    body = callback.parsed_json or {}
    ack = body.get("acknowledgement") if isinstance(body.get("acknowledgement"), dict) else {}
    error = body.get("error") if isinstance(body.get("error"), dict) else None
    if str(ack.get("status") or "").upper() == "SUCCESS" and not error:
        context.notified_at = timezone.now()
        context.save(update_fields=["notified_at", "modified_date"])
        return {"care_context": context.reference_number, "notify": "success"}
    code = str((error or {}).get("code") or ack.get("status") or "NOTIFY_ERRORED")
    _fail(context, code, str((error or {}).get("message") or "Notify errored"))
    return {"care_context": context.reference_number, "notify": "errored", "error": code}


# --- SMS deep link (journey 2) ------------------------------------------------------------


def send_sms_deep_link(patient: Patient, facility) -> AbdmOutboundRequest:
    """m2-sms-deep-link-notify: ask ABDM to SMS the patient a link to the ABHA app. For a patient
    with a mobile number but no ABHA address."""
    if not patient.phone_number:
        raise LinkingError("The patient has no mobile number.")
    config = get_config(facility)
    if not config["hip_id"]:
        raise LinkingError("This facility has no HFR facility ID. Complete the ABDM setup first.")
    request_id = outbound.new_request_id()
    body = rules.sms_body(
        request_id,
        utc_timestamp(),
        patient.phone_number,
        config["hip_id"],
        config.get("hip_name") or config.get("facility_name") or facility.name,
    )
    return outbound.send(
        "m2-sms-deep-link-notify", SMS_URL, body, facility=facility, patient=patient, request_id=request_id
    )


def handle_sms_notify_result(callback: AbdmCallback) -> dict:
    """`/v3/patients/sms/on-notify`: the outbound row keeps the outcome; nothing else to update."""
    body = callback.parsed_json or {}
    ack = body.get("acknowledgement") if isinstance(body.get("acknowledgement"), dict) else {}
    return {"sms": str(ack.get("status") or "unknown"), "error": body.get("error")}
