"""Pure validation rules for the ABDM facility setup form."""

import re

FACILITY_ID_RE = re.compile(r"^IN[A-Za-z0-9]{10}$")
FACILITY_NAME_RE = re.compile(r"^[A-Za-z0-9 \-_.(),/]+$")
HIP_NAME_RE = re.compile(r"^[A-Za-z0-9 ]{1,15}$")


def validate_facility_id(value: str) -> None:
    if value and not FACILITY_ID_RE.fullmatch(value):
        raise ValueError("HFR facility ID must start with IN and have 12 characters.")


def validate_facility_name(value: str) -> None:
    if value and not FACILITY_NAME_RE.fullmatch(value):
        raise ValueError("Facility name can use only letters, digits, space, and -_.(),/.")


def validate_hip_name(value: str) -> None:
    if value and not HIP_NAME_RE.fullmatch(value):
        raise ValueError("HIP name must be 15 characters or fewer with no special characters.")


def validate_facility_setup(config: dict) -> None:
    validate_facility_id(str(config.get("facility_id") or ""))
    validate_facility_name(str(config.get("facility_name") or ""))
    validate_hip_name(str(config.get("hip_name") or ""))
