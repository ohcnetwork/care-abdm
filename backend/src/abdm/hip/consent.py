"""
Consent notifications to the HIP (M2 journey 4, step "consent").

The gateway posts the patient's decision to the bridge. The docs name the path 2 ways
(`/v0.5/consents/hip/notify`, `/api/v3/consent/request/hip/notify`); the body is on the M3
page m3-on-consent-request-notify-hip: {status GRANTED|REVOKED|EXPIRED, consentId,
consentDetail{patient.id, careContexts[], hiTypes[], permission{dateRange, dataEraseAt}, hip, hiu,
purpose, ...}, signature, grantAcknowledgement}.
The HIP answers with m2-consent-hip-on-notify {acknowledgement{status OK|ERROR, consentId}, response.requestId}.

Certification (abdm-m2 test.md): HIP_INIT_GRANT_CONSENT_ "consent request seen in HMIS";
HIP_INIT_REVOKE_CONSENT and HIP_INIT_EXPIRE_CONSENT "seen in HMIS". The row keeps the status.
The artefact signature has no published algorithm, so it is stored and not verified.
"""

import logging

from django.utils import timezone

from abdm.care_seams import AbhaAddressIdentifier
from abdm.facility.service import facility_for_hip_id
from abdm.gateway import outbound
from abdm.hip import rules
from abdm.models import AbdmCallback, AbdmConsent

logger = logging.getLogger(__name__)

ON_NOTIFY_URL = "/api/hiecm/consent/v3/request/hip/on-notify"


def handle_consent_notify(callback: AbdmCallback) -> dict:
    data = rules.parse_consent_notification(callback.parsed_json or {})
    if not data["consent_id"]:
        raise ValueError("Consent notification has no consentId")
    hip_id = data["hip_id"] or callback.hip_id_header
    facility = facility_for_hip_id(hip_id)
    patient = AbhaAddressIdentifier.find_patient(data["abha_address"].lower()) if data["abha_address"] else None
    status = data["status"] if data["status"] in AbdmConsent.Status.values else ""
    consent, _ = AbdmConsent.objects.update_or_create(
        consent_id=data["consent_id"],
        defaults={
            "facility": facility,
            "patient": patient,
            "abha_address": data["abha_address"],
            "hiu_id": data["hiu_id"],
            "hiu_name": data["hiu_name"][:256],
            "purpose_code": data["purpose_code"][:32],
            "hi_types": data["hi_types"],
            "care_context_references": data["care_context_references"],
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "data_erase_at": data["data_erase_at"],
            "status": status or AbdmConsent.Status.GRANTED,
            "artefact": data["detail"],
            "signature": data["signature"],
            "callback": callback,
            "notified_at": timezone.now(),
        },
    )
    ok = bool(status)
    request = outbound.send(
        "m2-consent-hip-on-notify",
        ON_NOTIFY_URL,
        rules.consent_ack_body(consent.consent_id, callback.request_id_header, ok=ok),
        facility=facility,
        patient=patient,
    )
    consent.ack_request = request
    consent.save(update_fields=["ack_request", "modified_date"])
    if not ok:
        logger.warning("abdm: consent %s carried unknown status %r", consent.consent_id, data["status"])
    return {
        "consent_id": consent.consent_id,
        "status": consent.status,
        "matched_patient": patient is not None,
        "ack": request.status,
    }


def consent_summary(consent: AbdmConsent) -> dict:
    return {
        "id": str(consent.external_id),
        "consentId": consent.consent_id,
        "status": consent.status,
        "hiuId": consent.hiu_id,
        "hiuName": consent.hiu_name,
        "purposeCode": consent.purpose_code,
        "hiTypes": consent.hi_types,
        "careContextReferences": consent.care_context_references,
        "dateFrom": consent.date_from,
        "dateTo": consent.date_to,
        "dataEraseAt": consent.data_erase_at,
        "notifiedAt": consent.notified_at,
        "facility": str(consent.facility.external_id) if consent.facility_id else None,
    }
