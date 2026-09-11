"""
Plug-owned tables (ADR-004: secrets and transaction state never go in extensions).
"""

from care.utils.models.base import BaseModel
from django.db import models


class AbhaTransaction(BaseModel):
    """
    One ABHA service transaction (enrolment or login), keyed by ABDM's txnId.

    Written server-side as each step completes; read by the post_save receiver when a
    Patient arrives carrying extensions.abdm.txn_id, and by the explicit link endpoint.
    Holds the ABDM user token (X-token) so card/profile reads can be proxied later
    without asking the person for another OTP. Aadhaar and OTP values are never stored.
    """

    class Kind(models.TextChoices):
        ENROL_AADHAAR = "enrol_aadhaar"
        LOGIN_MOBILE = "login_mobile"
        # Login to an existing ABHA by another identifier (m1-login-request-otp
        # `loginHint` ∈ {abha-number, aadhaar}; m1-phr-request-otp for abha-address).
        LOGIN_ABHA_NUMBER = "login_abha_number"
        LOGIN_ABHA_ADDRESS = "login_abha_address"
        LOGIN_AADHAAR = "login_aadhaar"

    LOGIN_KINDS = (Kind.LOGIN_MOBILE, Kind.LOGIN_ABHA_NUMBER, Kind.LOGIN_ABHA_ADDRESS, Kind.LOGIN_AADHAAR)

    txn_id = models.CharField(max_length=128, unique=True, db_index=True)
    kind = models.CharField(max_length=32, choices=Kind.choices)
    abha_number = models.CharField(max_length=32, blank=True, default="", db_index=True)
    abha_address = models.CharField(max_length=128, blank=True, default="")
    profile = models.JSONField(default=dict, blank=True)  # ABHAProfile / account as returned
    is_new = models.BooleanField(null=True)
    x_token = models.TextField(blank=True, default="")
    x_token_expires_at = models.DateTimeField(null=True, blank=True)
    refresh_token = models.TextField(blank=True, default="")
    refresh_token_expires_at = models.DateTimeField(null=True, blank=True)
    # Set when consumed. A txn links exactly one patient.
    patient = models.ForeignKey("emr.Patient", null=True, blank=True, on_delete=models.SET_NULL)
    linked_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.kind}:{self.txn_id}"

    @property
    def x_token_valid(self) -> bool:
        from django.utils import timezone

        return bool(self.x_token) and (self.x_token_expires_at is None or self.x_token_expires_at > timezone.now())

    @property
    def refresh_token_valid(self) -> bool:
        from django.utils import timezone

        return bool(self.refresh_token) and (
            self.refresh_token_expires_at is None or self.refresh_token_expires_at > timezone.now()
        )

    @property
    def session_available(self) -> bool:
        """Can a profile call (card/account) be served, possibly after a refresh?"""
        return self.x_token_valid or self.refresh_token_valid


class AbdmOutboundRequest(BaseModel):
    class Status(models.TextChoices):
        SENT = "sent"
        SUCCEEDED = "succeeded"
        FAILED = "failed"

    request_id = models.CharField(max_length=64, unique=True, db_index=True)
    operation_id = models.CharField(max_length=128, db_index=True)
    facility = models.ForeignKey("facility.Facility", null=True, blank=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey("emr.Patient", null=True, blank=True, on_delete=models.SET_NULL)
    encounter = models.ForeignKey("emr.Encounter", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.SENT, db_index=True)
    request_json = models.JSONField(default=dict, blank=True)
    http_status = models.PositiveIntegerField(null=True, blank=True)
    response_json = models.JSONField(default=dict, blank=True)
    error_code = models.CharField(max_length=128, blank=True, default="")
    sent_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["operation_id", "status"]),
            models.Index(fields=["facility", "status"]),
            models.Index(fields=["patient", "status"]),
            models.Index(fields=["encounter", "status"]),
        ]

    def __str__(self):
        return f"{self.operation_id}:{self.request_id}"


class AbdmCallback(BaseModel):
    class SignatureStatus(models.TextChoices):
        MISSING = "missing"
        OK = "ok"
        FAILED = "failed"

    class ShapeStatus(models.TextChoices):
        UNVALIDATED = "unvalidated"
        OK = "ok"
        MISMATCH = "mismatch"

    class ProcessedStatus(models.TextChoices):
        RECEIVED = "received"
        QUEUED = "queued"
        UNHANDLED = "unhandled"
        FAILED = "failed"

    path = models.CharField(max_length=256)
    operation_id = models.CharField(max_length=128, blank=True, default="")
    request_id_header = models.CharField(max_length=128, blank=True, default="")
    timestamp_header = models.CharField(max_length=64, blank=True, default="")
    hip_id_header = models.CharField(max_length=128, blank=True, default="")
    headers_json = models.JSONField(default=dict, blank=True)
    signature_status = models.CharField(
        max_length=16, choices=SignatureStatus.choices, default=SignatureStatus.MISSING, db_index=True
    )
    raw_body = models.TextField(blank=True, default="")
    parsed_json = models.JSONField(default=dict, blank=True)
    response_request_id = models.CharField(max_length=128, blank=True, default="", db_index=True)
    transaction_id = models.CharField(max_length=128, blank=True, default="", db_index=True)
    idempotency_key = models.CharField(max_length=64, unique=True)
    shape_status = models.CharField(max_length=16, choices=ShapeStatus.choices, default=ShapeStatus.UNVALIDATED)
    processed_status = models.CharField(
        max_length=16, choices=ProcessedStatus.choices, default=ProcessedStatus.RECEIVED, db_index=True
    )
    outbound_request = models.ForeignKey(AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL)
    received_at = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["path", "received_at"]),
            models.Index(fields=["response_request_id"]),
            models.Index(fields=["transaction_id"]),
            models.Index(fields=["signature_status"]),
        ]

    def __str__(self):
        return f"{self.operation_id or self.path}:{self.signature_status}"
