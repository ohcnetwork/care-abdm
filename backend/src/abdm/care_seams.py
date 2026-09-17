"""
Care core seams used by the ABDM plug (ADR-004).

1. Patient.extensions["abdm"] — PlugExtension (care/emr/extensions/base.py:107),
   registered like the live `patient_demographics` plug does. Non-secret state only.
   The write schema accepts `txn_id`: the registration form hands the plug's enrolment
   transaction to core, and the post_save receiver in abdm/signals.py turns it into
   identifiers + read-only link metadata. Nothing client-supplied becomes an identifier.
2. ABHA number / ABHA address identifiers reuse core's own auto-maintained identifier
   helper `BasePatientIdentifierConfig` (care/emr/signals/patient/base.py) — the same
   machinery core uses for the name identifier. Instance-level (facility=None).
"""

from care.emr.extensions.base import ExtensionResource, PlugExtension
from care.emr.models.patient import PatientIdentifier
from care.emr.registries.extensions.registry import ExtensionRegistry
from care.emr.signals.patient.base import BasePatientIdentifierConfig

EXTENSION_NAME = "abdm"

# Identifier `system` strings. The docs prescribe no URI for ABHA (see findings.md);
# these are plug-chosen and stable — do not rename once patients carry them.
ABHA_NUMBER_SYSTEM = "abdm/abha-number"
ABHA_ADDRESS_SYSTEM = "abdm/abha-address"


class AbdmPatientExtension(PlugExtension):
    extension_name = EXTENSION_NAME
    extension_version = "1.0.0"
    resource_type = ExtensionResource.patient
    # care_fe hides a property from a host slot via x-ui.render_blacklist
    # (care_fe/src/Utils/schema/extensionSchema.ts:472-483). Every field here is
    # server-written; forms never edit them. The plug's own ABHA panel is the display surface.
    FORMS = ["registration", "patient_edit"]
    ALL = [*FORMS, "patient_summary", "appointment_print"]
    write_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ABDM",
        "type": "object",
        "properties": {
            # Consumed once by abdm.signals.link_abha_from_txn and removed.
            "txn_id": {"type": "string", "title": "ABHA enrolment transaction", "x-ui": {"render_blacklist": ALL}},
            "abha_number": {
                "type": "string",
                "title": "ABHA Number",
                "readOnly": True,
                "x-ui": {"render_blacklist": FORMS},
            },
            "abha_address": {
                "type": "string",
                "title": "ABHA Address",
                "readOnly": True,
                "x-ui": {"render_blacklist": FORMS},
            },
            "abha_linked_at": {
                "type": "string",
                "format": "date-time",
                "title": "ABHA linked at",
                "readOnly": True,
                "x-ui": {"render_blacklist": ALL},
            },
            "abha_source": {
                "type": "string",
                "title": "How the ABHA was obtained",
                "enum": [
                    "enrol_aadhaar",
                    "login_mobile",
                    "login_abha_number",
                    "login_abha_address",
                    "login_aadhaar",
                ],
                "readOnly": True,
                "x-ui": {"render_blacklist": ALL},
            },
            "kyc_verified": {
                "type": "boolean",
                "title": "KYC verified",
                "readOnly": True,
                "x-ui": {"render_blacklist": ALL},
            },
        },
        "additionalProperties": False,
    }
    retrieve_schema = {
        **write_schema,
        "properties": {k: v for k, v in write_schema["properties"].items() if k != "txn_id"},
    }


ExtensionRegistry.register(AbdmPatientExtension())


class AbdmFacilityExtension(PlugExtension):
    extension_name = EXTENSION_NAME
    extension_version = "1.0.0"
    resource_type = ExtensionResource.facility
    FORMS = ["facility_create", "facility_update"]
    ALL = [*FORMS, "facility_list", "facility_retrieve"]
    SERVER_OWNED = [*FORMS, "facility_list"]
    write_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ABDM",
        "type": "object",
        "properties": {
            "facility_id": {"type": "string", "title": "HFR facility ID", "default": ""},
            "facility_name": {"type": "string", "title": "Facility name", "default": ""},
            "hip_name": {"type": "string", "title": "HIP name", "default": ""},
            "counters": {
                "type": "array",
                "items": {"type": "string"},
                "title": "Scan and Share counters",
                "default": [],
                "x-ui": {"render_blacklist": SERVER_OWNED},
            },
            # The service id the gateway issued for this facility (facility/service.py). Server-written.
            "hip_id": {
                "type": "string",
                "title": "HIP ID",
                "default": "",
                "readOnly": True,
                "x-ui": {"render_blacklist": SERVER_OWNED},
            },
            "hrp_registered_at": {
                "type": "string",
                "format": "date-time",
                "title": "HRP registered at",
                "readOnly": True,
                "x-ui": {"render_blacklist": SERVER_OWNED},
            },
            "last_error": {
                "type": "string",
                "title": "Last ABDM error",
                "readOnly": True,
                "x-ui": {"render_blacklist": SERVER_OWNED},
            },
        },
        "additionalProperties": False,
    }
    read_schema = write_schema
    retrieve_schema = write_schema


ExtensionRegistry.register(AbdmFacilityExtension())


class _AbhaIdentifier(BasePatientIdentifierConfig):
    RETRIEVE_WITH_YOB = False
    PARTIAL_SEARCH = False
    CACHED_CONFIG = {}

    @classmethod
    def get_value(cls, patient):
        return (patient.extensions or {}).get(EXTENSION_NAME, {}).get(cls.EXTENSION_KEY)

    @classmethod
    def set(cls, patient, value: str) -> None:
        """Write the identifier directly (value is not derivable from Patient fields)."""
        config = cls.get_or_create_system_name_identifier_config(None)
        PatientIdentifier.objects.update_or_create(
            patient=patient, config=config, facility=None, defaults={"value": value}
        )

    @classmethod
    def get(cls, patient) -> str | None:
        config = cls.get_or_create_system_name_identifier_config(None)
        row = PatientIdentifier.objects.filter(patient=patient, config=config).only("value").first()
        return row.value if row else None

    @classmethod
    def find_patient(cls, value: str):
        config = cls.get_or_create_system_name_identifier_config(None)
        row = PatientIdentifier.objects.filter(config=config, value=value).select_related("patient").first()
        return row.patient if row else None


class AbhaNumberIdentifier(_AbhaIdentifier):
    IDENTIFIER_SYSTEM = ABHA_NUMBER_SYSTEM
    DISPLAY = "ABHA Number"
    EXTENSION_KEY = "abha_number"
    CACHED_CONFIG = {}


class AbhaAddressIdentifier(_AbhaIdentifier):
    IDENTIFIER_SYSTEM = ABHA_ADDRESS_SYSTEM
    DISPLAY = "ABHA Address"
    EXTENSION_KEY = "abha_address"
    CACHED_CONFIG = {}
