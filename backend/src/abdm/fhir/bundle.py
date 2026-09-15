"""Pure FHIR R4 document-bundle helpers for ABDM NRCES record profiles.

Shapes are taken from https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/fhir,
MCP ``get_fhir_profile`` for DocumentBundle/record profiles, and the MCP NRCES
example bundles fetched for this implementation pass.
"""

from __future__ import annotations

import base64
import mimetypes
import uuid
from collections.abc import Iterable
from datetime import date, datetime, timezone
from decimal import Decimal
from html import escape
from typing import Any

DOCUMENT_BUNDLE_PROFILE = "https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"
PROFILE_BASE = "https://nrces.in/ndhm/fhir/r4/StructureDefinition"
SNOMED = "http://snomed.info/sct"
CONFIDENTIALITY = "http://terminology.hl7.org/CodeSystem/v3-Confidentiality"
CARE_BUNDLE_SYSTEM = "https://care.ohc.network/abdm/bundle"
CARE_COMPOSITION_SYSTEM = "https://care.ohc.network/abdm/composition"
CARE_PATIENT_SYSTEM = "https://care.ohc.network/patient"
CARE_ENCOUNTER_SYSTEM = "https://care.ohc.network/encounter"
CARE_PRACTITIONER_SYSTEM = "https://care.ohc.network/practitioner"


def resource_profile(resource_type: str) -> str:
    return f"{PROFILE_BASE}/{resource_type}"


def ensure_id(resource: dict[str, Any]) -> str:
    resource.setdefault("id", str(uuid.uuid4()))
    return str(resource["id"])


def uuid_ref(resource: dict[str, Any]) -> str:
    """Return the ``urn:uuid`` reference form used by the NRCES examples."""
    return f"urn:uuid:{ensure_id(resource)}"


def reference(resource: dict[str, Any], display: str | None = None) -> dict[str, str]:
    ref = {"reference": uuid_ref(resource)}
    if display:
        ref["display"] = display
    return ref


def fhir_datetime(value: Any | None = None) -> str:
    """Format dates/times for FHIR JSON; naive datetimes are treated as UTC."""
    if value is None:
        value = datetime.now(timezone.utc)
    if isinstance(value, str):
        return value.replace("Z", "+00:00")
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def gender_code(care_gender: str | None) -> str:
    """Map CARE genders to FHIR R4 AdministrativeGender."""
    return {
        "male": "male",
        "female": "female",
        "transgender": "other",
        "non_binary": "other",
        "non-binary": "other",
    }.get(str(care_gender or "").strip().lower(), "unknown")


def _clean(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items() if v not in (None, "", [], {})}
    if isinstance(value, list):
        return [_clean(v) for v in value if v not in (None, "", [], {})]
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return fhir_datetime(value)
    return value


def codeable(coding_dict: dict[str, Any] | None, text: str | None = None) -> dict[str, Any]:
    """Convert CARE Coding-like JSON into FHIR ``CodeableConcept``."""
    coding_dict = coding_dict or {}
    if isinstance(coding_dict.get("coding"), list):
        concept = {"coding": coding_dict["coding"], "text": coding_dict.get("text") or text}
        return _clean(concept)
    coding = {
        "system": coding_dict.get("system"),
        "code": coding_dict.get("code"),
        "display": coding_dict.get("display"),
    }
    concept: dict[str, Any] = {}
    if coding.get("code"):
        concept["coding"] = [_clean(coding)]
    concept["text"] = coding_dict.get("display") or coding_dict.get("text") or text
    return _clean(concept)


def snomed(code: str, display: str) -> dict[str, Any]:
    return {"coding": [{"system": SNOMED, "code": code, "display": display}], "text": display}


def meta(resource_type: str, timestamp: Any | None = None, *, version: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {"profile": [resource_profile(resource_type)]}
    if version:
        result["versionId"] = "1"
        result["lastUpdated"] = fhir_datetime(timestamp)
    return result


def patient_resource(
    patient: Any,
    *,
    timestamp: Any | None = None,
    abha_number: str | None = None,
    abha_address: str | None = None,
) -> dict[str, Any]:
    identifiers: list[dict[str, Any]] = [
        {"system": CARE_PATIENT_SYSTEM, "value": str(getattr(patient, "external_id", ""))}
    ]
    if abha_number:
        identifiers.append({"type": {"text": "ABHA Number"}, "system": "abdm/abha-number", "value": abha_number})
    if abha_address:
        identifiers.append({"type": {"text": "ABHA Address"}, "system": "abdm/abha-address", "value": abha_address})
    resource = {
        "resourceType": "Patient",
        "id": str(uuid.uuid4()),
        "meta": meta("Patient", timestamp, version=True),
        "identifier": identifiers,
        "name": [{"text": getattr(patient, "name", "") or "Unknown"}],
        "telecom": [{"system": "phone", "value": getattr(patient, "phone_number", ""), "use": "home"}],
        "gender": gender_code(getattr(patient, "gender", None)),
        "birthDate": getattr(patient, "date_of_birth", None),
        "address": [
            {
                "text": getattr(patient, "address", ""),
                "postalCode": str(getattr(patient, "pincode", "") or ""),
            }
        ],
    }
    return _clean(resource)


def organization_resource(facility: Any, *, hip_id: str, timestamp: Any | None = None) -> dict[str, Any]:
    resource = {
        "resourceType": "Organization",
        "id": str(uuid.uuid4()),
        "meta": meta("Organization", timestamp),
        "identifier": [
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "PRN",
                            "display": "Provider number",
                        }
                    ]
                },
                "system": "https://facility.ndhm.gov.in",
                "value": hip_id or str(getattr(facility, "external_id", "")),
            }
        ],
        "name": getattr(facility, "name", "") or "CARE facility",
        "telecom": [{"system": "phone", "value": getattr(facility, "phone_number", ""), "use": "work"}],
        "address": [
            {
                "text": getattr(facility, "address", ""),
                "postalCode": str(getattr(facility, "pincode", "") or ""),
            }
        ],
    }
    return _clean(resource)


def practitioner_resource(user: Any, *, timestamp: Any | None = None) -> dict[str, Any]:
    name = " ".join(filter(None, [getattr(user, "first_name", ""), getattr(user, "last_name", "")])).strip()
    name = name or getattr(user, "username", "") or "CARE practitioner"
    resource = {
        "resourceType": "Practitioner",
        "id": str(uuid.uuid4()),
        "meta": meta("Practitioner", timestamp, version=True),
        "identifier": [
            {
                "system": CARE_PRACTITIONER_SYSTEM,
                "value": str(getattr(user, "external_id", "")),
            }
        ],
        "name": [{"text": name}],
    }
    return _clean(resource)


def encounter_resource(
    encounter: Any,
    *,
    patient_ref: dict[str, str],
    diagnosis_refs: Iterable[dict[str, str]] = (),
    timestamp: Any | None = None,
) -> dict[str, Any]:
    period = getattr(encounter, "period", {}) or {}
    diagnosis = [
        {
            "condition": ref,
            "use": {"coding": [{"system": SNOMED, "code": "39154008", "display": "Clinical diagnosis"}]},
        }
        for ref in diagnosis_refs
    ]
    resource = {
        "resourceType": "Encounter",
        "id": str(uuid.uuid4()),
        "meta": meta("Encounter", timestamp),
        "identifier": [{"system": CARE_ENCOUNTER_SYSTEM, "value": str(getattr(encounter, "external_id", ""))}],
        "status": _encounter_status(getattr(encounter, "status", None)),
        "class": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": _encounter_class(getattr(encounter, "encounter_class", None)),
            "display": "ambulatory",
        },
        "subject": patient_ref,
        "period": {"start": period.get("start"), "end": period.get("end")},
        "diagnosis": diagnosis,
    }
    return _clean(resource)


def _encounter_status(status: str | None) -> str:
    if status in {"completed", "discharged"}:
        return "finished"
    if status in {"cancelled", "entered_in_error", "unknown"}:
        return str(status).replace("_", "-")
    return "in-progress" if status == "in_progress" else "unknown"


def _encounter_class(encounter_class: str | None) -> str:
    return {
        "amb": "AMB",
        "imp": "IMP",
        "emer": "EMER",
        "obsenc": "OBSENC",
        "vr": "VR",
        "hh": "HH",
    }.get(str(encounter_class or "").lower(), "AMB")


def medication_request_resource(
    medication_request: Any,
    *,
    patient_ref: dict[str, str],
    requester_ref: dict[str, str] | None,
    reason_refs: Iterable[dict[str, str]] = (),
) -> dict[str, Any]:
    resource = {
        "resourceType": "MedicationRequest",
        "id": str(uuid.uuid4()),
        "meta": meta("MedicationRequest"),
        "status": _medication_status(getattr(medication_request, "status", None)),
        "intent": _medication_intent(getattr(medication_request, "intent", None)),
        "medicationCodeableConcept": codeable(getattr(medication_request, "medication", None), "Medication"),
        "subject": patient_ref,
        "authoredOn": fhir_datetime(getattr(medication_request, "authored_on", None)),
        "requester": requester_ref,
        "reasonReference": list(reason_refs),
        "dosageInstruction": [_dosage(d) for d in (getattr(medication_request, "dosage_instruction", None) or [])],
        "note": [{"text": getattr(medication_request, "note", None)}],
    }
    return _clean(resource)


def _medication_status(status: str | None) -> str:
    value = str(status or "active").replace("_", "-")
    return (
        value
        if value in {"active", "on-hold", "cancelled", "completed", "entered-in-error", "stopped", "draft", "unknown"}
        else "unknown"
    )


def _medication_intent(intent: str | None) -> str:
    value = str(intent or "order").replace("_", "-")
    return (
        value
        if value
        in {"proposal", "plan", "order", "original-order", "reflex-order", "filler-order", "instance-order", "option"}
        else "order"
    )


def _dosage(dosage: dict[str, Any]) -> dict[str, Any]:
    dose_and_rate = dosage.get("dose_and_rate") or {}
    dose_quantity = _quantity(dose_and_rate.get("dose_quantity"))
    result = {
        "sequence": dosage.get("sequence"),
        "text": dosage.get("text"),
        "additionalInstruction": [codeable(x) for x in (dosage.get("additional_instruction") or [])],
        "patientInstruction": dosage.get("patient_instruction"),
        "timing": _timing(dosage.get("timing")),
        "route": codeable(dosage.get("route")),
        "method": codeable(dosage.get("method")),
        "doseAndRate": [{"type": {"text": dose_and_rate.get("type")}, "doseQuantity": dose_quantity}],
    }
    return _clean(result)


def _timing(timing: dict[str, Any] | None) -> dict[str, Any]:
    if not timing:
        return {}
    repeat = timing.get("repeat") or {}
    return _clean(
        {
            "repeat": {
                "frequency": repeat.get("frequency"),
                "period": repeat.get("period"),
                "periodUnit": repeat.get("period_unit") or repeat.get("periodUnit"),
                "boundsDuration": _quantity(repeat.get("bounds_duration")),
            },
            "code": codeable(timing.get("code")),
        }
    )


def _quantity(quantity: dict[str, Any] | None) -> dict[str, Any]:
    if not quantity:
        return {}
    unit = quantity.get("unit") if isinstance(quantity.get("unit"), dict) else {}
    return _clean(
        {
            "value": quantity.get("value"),
            "unit": unit.get("display") or unit.get("code") or quantity.get("unit"),
            "system": unit.get("system"),
            "code": unit.get("code"),
        }
    )


def condition_resource(condition: Any, *, patient_ref: dict[str, str]) -> dict[str, Any]:
    resource = {
        "resourceType": "Condition",
        "id": str(uuid.uuid4()),
        "meta": meta("Condition"),
        "clinicalStatus": _status_codeable(
            "http://terminology.hl7.org/CodeSystem/condition-clinical",
            getattr(condition, "clinical_status", None) or "active",
        ),
        "verificationStatus": _status_codeable(
            "http://terminology.hl7.org/CodeSystem/condition-ver-status",
            getattr(condition, "verification_status", None),
        ),
        "category": [
            codeable({"code": getattr(condition, "category", None), "display": getattr(condition, "category", None)})
        ],
        "severity": codeable(
            {"code": getattr(condition, "severity", None), "display": getattr(condition, "severity", None)}
        ),
        "code": codeable(getattr(condition, "code", None), "Condition"),
        "subject": patient_ref,
        "onsetString": (getattr(condition, "onset", None) or {}).get("onset_string"),
        "onsetDateTime": (getattr(condition, "onset", None) or {}).get("onset_datetime"),
        "recordedDate": fhir_datetime(getattr(condition, "recorded_date", None))
        if getattr(condition, "recorded_date", None)
        else None,
        "note": [{"text": getattr(condition, "note", None)}],
    }
    return _clean(resource)


def allergy_resource(
    allergy: Any,
    *,
    patient_ref: dict[str, str],
    recorder_ref: dict[str, str] | None = None,
) -> dict[str, Any]:
    resource = {
        "resourceType": "AllergyIntolerance",
        "id": str(uuid.uuid4()),
        "meta": meta("AllergyIntolerance"),
        "clinicalStatus": _status_codeable(
            "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
            getattr(allergy, "clinical_status", None) or "active",
        ),
        "verificationStatus": _status_codeable(
            "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
            getattr(allergy, "verification_status", None) or "confirmed",
        ),
        "type": getattr(allergy, "allergy_intolerance_type", None),
        "category": [getattr(allergy, "category", None)],
        "criticality": getattr(allergy, "criticality", None),
        "code": codeable(getattr(allergy, "code", None), "Allergy"),
        "patient": patient_ref,
        "onsetString": (getattr(allergy, "onset", None) or {}).get("onset_string"),
        "recordedDate": fhir_datetime(getattr(allergy, "recorded_date", None))
        if getattr(allergy, "recorded_date", None)
        else None,
        "recorder": recorder_ref,
        "note": [{"text": getattr(allergy, "note", None)}],
    }
    return _clean(resource)


def _status_codeable(system: str, code: str | None) -> dict[str, Any]:
    if not code:
        return {}
    display = str(code).replace("_", " ").replace("-", " ").title()
    return {"coding": [{"system": system, "code": str(code).replace("_", "-"), "display": display}]}


def document_reference_resource(
    file_obj: Any,
    *,
    patient_ref: dict[str, str],
    attachment: dict[str, Any],
) -> dict[str, Any]:
    resource = {
        "resourceType": "DocumentReference",
        "id": str(uuid.uuid4()),
        "meta": meta("DocumentReference"),
        "status": "current",
        "docStatus": "final",
        "type": {"text": getattr(file_obj, "file_category", None) or "Health Document"},
        "subject": patient_ref,
        "date": fhir_datetime(getattr(file_obj, "created_date", None)),
        "content": [{"attachment": attachment}],
    }
    return _clean(resource)


def attachment_from_bytes(
    *,
    name: str,
    content: bytes,
    content_type: str | None,
    created: Any | None = None,
) -> dict[str, Any]:
    guessed_type = content_type or mimetypes.guess_type(name)[0] or "application/octet-stream"
    return _clean(
        {
            "contentType": guessed_type,
            "language": "en-IN",
            "data": base64.b64encode(content).decode("ascii"),
            "title": name,
            "creation": fhir_datetime(created),
        }
    )


def attachment_from_url(*, name: str, url: str, content_type: str | None, created: Any | None = None) -> dict[str, Any]:
    return _clean(
        {
            "contentType": content_type or mimetypes.guess_type(name)[0] or "application/octet-stream",
            "language": "en-IN",
            "url": url,
            "title": name,
            "creation": fhir_datetime(created),
        }
    )


def composition(
    *,
    profile_url: str,
    type_code: str,
    type_display: str,
    subject_ref: dict[str, str],
    date_value: Any,
    author_refs: list[dict[str, str]],
    title: str,
    sections: list[dict[str, Any]],
    encounter_ref: dict[str, str] | None = None,
    custodian_ref: dict[str, str] | None = None,
    attester_ref: dict[str, str] | None = None,
    timestamp: Any | None = None,
) -> dict[str, Any]:
    resource = {
        "resourceType": "Composition",
        "id": str(uuid.uuid4()),
        "meta": {"versionId": "1", "lastUpdated": fhir_datetime(timestamp), "profile": [profile_url]},
        "language": "en-IN",
        "text": generated_text(title),
        "identifier": {
            # ABDM docs require system+value but do not prescribe a URI; keep this stable for CARE traceability.
            "system": CARE_COMPOSITION_SYSTEM,
            "value": str(uuid.uuid4()),
        },
        "status": "final",
        "type": snomed(type_code, type_display),
        "subject": subject_ref,
        "encounter": encounter_ref,
        "date": fhir_datetime(date_value),
        "author": author_refs,
        "title": title,
        "custodian": custodian_ref,
        "attester": [{"mode": "official", "party": attester_ref}] if attester_ref else None,
        "section": sections,
    }
    return _clean(resource)


def section(
    *,
    title: str,
    code: dict[str, Any] | None = None,
    entries: Iterable[dict[str, str]] = (),
    empty_text: str | None = None,
) -> dict[str, Any]:
    result = {"title": title, "code": code, "entry": list(entries)}
    if empty_text and not result["entry"]:
        result["text"] = generated_text(empty_text)
    return _clean(result)


def generated_text(text: str) -> dict[str, str]:
    return {"status": "generated", "div": f'<div xmlns="http://www.w3.org/1999/xhtml">{escape(text)}</div>'}


def new_bundle(
    profile_url: str,
    composition_resource: dict[str, Any],
    resources: list[dict[str, Any]],
    *,
    hip_system: str,
    hip_id: str,
    timestamp: Any | None = None,
) -> dict[str, Any]:
    """Build the DocumentBundle envelope required by MCP ``get_fhir_profile DocumentBundle``."""
    issued_at = fhir_datetime(timestamp)
    entries = [composition_resource, *resources]
    return {
        "resourceType": "Bundle",
        "id": str(uuid.uuid4()),
        "meta": {
            "versionId": "1",
            "lastUpdated": issued_at,
            "profile": [profile_url or DOCUMENT_BUNDLE_PROFILE],
            "security": [{"system": CONFIDENTIALITY, "code": "V", "display": "very restricted"}],
        },
        "identifier": {
            # ABDM docs/examples require a traceable system+value but do not assign CARE a system URI.
            "system": hip_system or CARE_BUNDLE_SYSTEM,
            "value": str(uuid.uuid4()),
        },
        "type": "document",
        "timestamp": issued_at,
        "entry": [{"fullUrl": uuid_ref(resource), "resource": resource} for resource in entries],
    }
