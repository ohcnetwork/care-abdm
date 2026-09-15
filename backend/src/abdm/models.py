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
        # Scan and Share (SHARE_PATIENT_PROFILE_701): the profile came from the gateway
        # callback, not from an OTP flow. No tokens. Used only for registration prefill.
        PROFILE_SHARE = "profile_share"

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
    # CRT_ABHA_102: the system records the consent the person gave before enrolment.
    # The code and the version are the `consent` block sent to ABDM (abdm/abha/client.py::CONSENT).
    consent_recorded_at = models.DateTimeField(null=True, blank=True)
    consent_code = models.CharField(max_length=64, blank=True, default="")
    consent_version = models.CharField(max_length=16, blank=True, default="")

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

    class ProcessedStatus(models.TextChoices):
        RECEIVED = "received"
        QUEUED = "queued"
        UNHANDLED = "unhandled"
        HANDLED = "handled"
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
    # The header that carried the verified token (the docs do not publish it) and the last reason
    # a verification did not pass. Both are evidence for docs/findings.md E2.
    signature_header = models.CharField(max_length=64, blank=True, default="")
    signature_error = models.CharField(max_length=256, blank=True, default="")
    raw_body = models.TextField(blank=True, default="")
    parsed_json = models.JSONField(default=dict, blank=True)
    response_request_id = models.CharField(max_length=128, blank=True, default="", db_index=True)
    transaction_id = models.CharField(max_length=128, blank=True, default="", db_index=True)
    idempotency_key = models.CharField(max_length=64, unique=True)
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


class AbdmProfileShare(BaseModel):
    """
    One Scan and Share event (m1-receive-patient-share). The gateway posts the profile
    that a person shared at a facility counter. The plug matches the facility by hipId,
    assigns a token number, answers with m1-on-share-acknowledgement, and shows the
    share in the front desk inbox until the desk dismisses it.
    """

    class Status(models.TextChoices):
        RECEIVED = "received"
        ACKNOWLEDGED = "acknowledged"
        ACK_FAILED = "ack_failed"
        REJECTED = "rejected"

    callback = models.ForeignKey(AbdmCallback, null=True, blank=True, on_delete=models.SET_NULL)
    facility = models.ForeignKey("facility.Facility", null=True, blank=True, on_delete=models.SET_NULL)
    hip_id = models.CharField(max_length=128, blank=True, default="", db_index=True)
    context = models.CharField(max_length=64, blank=True, default="")
    hpr_id = models.CharField(max_length=128, blank=True, default="")
    abha_number = models.CharField(max_length=32, blank=True, default="", db_index=True)
    abha_address = models.CharField(max_length=128, blank=True, default="", db_index=True)
    # `profile.patient` as received. kycPhoto is kept here and is not copied to the transaction.
    profile = models.JSONField(default=dict, blank=True)
    patient = models.ForeignKey("emr.Patient", null=True, blank=True, on_delete=models.SET_NULL)
    transaction = models.ForeignKey(AbhaTransaction, null=True, blank=True, on_delete=models.SET_NULL)
    token_number = models.CharField(max_length=32, blank=True, default="")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.RECEIVED, db_index=True)
    error_code = models.CharField(max_length=64, blank=True, default="")
    error_message = models.CharField(max_length=256, blank=True, default="")
    ack_request = models.ForeignKey(AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(db_index=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    dismissed_by = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        indexes = [
            models.Index(fields=["facility", "received_at"]),
            models.Index(fields=["facility", "context", "received_at"]),
        ]

    def __str__(self):
        return f"{self.hip_id}/{self.context}:{self.token_number or self.status}"


# --- M2: HIP linking and sharing -------------------------------------------------------


class AbdmLinkToken(BaseModel):
    """
    The link token that authorises care-context linking for 1 patient at 1 facility.

    Docs: the token is per patient, stored at registration, valid 6 months
    (/concepts/linking). It arrives on the `/v3/hip/token/on-generate-token` callback.
    It is a secret: it never leaves the server and never goes in a Care extension.
    """

    class Status(models.TextChoices):
        REQUESTED = "requested"
        ACTIVE = "active"
        FAILED = "failed"

    patient = models.ForeignKey("emr.Patient", on_delete=models.CASCADE)
    facility = models.ForeignKey("facility.Facility", on_delete=models.CASCADE)
    abha_address = models.CharField(max_length=128, blank=True, default="")
    token = models.TextField(blank=True, default="")
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.REQUESTED, db_index=True)
    request = models.ForeignKey(AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL)
    error_code = models.CharField(max_length=64, blank=True, default="")
    error_message = models.CharField(max_length=512, blank=True, default="")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["patient", "facility"], name="abdm_link_token_patient_facility")]

    @property
    def usable(self) -> bool:
        from django.utils import timezone

        return (
            self.status == self.Status.ACTIVE
            and bool(self.token)
            and (self.expires_at is None or self.expires_at > timezone.now())
        )

    def __str__(self):
        return f"link-token:{self.patient_id}@{self.facility_id}:{self.status}"


class AbdmCareContext(BaseModel):
    """
    1 Care Encounter as 1 ABDM care context (docs: 1 per OPD visit or IPD admission).

    `reference_number` is the Encounter external_id. `display` carries no clinical detail.
    The context is linked only when the `/v3/link/on_carecontext` callback says so, or
    when the patient confirms a user-initiated link (whats-new 2026-09-10).
    """

    class Status(models.TextChoices):
        PENDING = "pending"  # waiting for ABHA, facility setup, or a link token
        LINK_REQUESTED = "link_requested"  # m2-hip-link-care-context accepted (202); awaiting callback
        LINKED = "linked"
        FAILED = "failed"

    class LinkedVia(models.TextChoices):
        HIP = "hip"
        USER = "user"

    encounter = models.OneToOneField("emr.Encounter", on_delete=models.CASCADE, related_name="abdm_care_context")
    patient = models.ForeignKey("emr.Patient", on_delete=models.CASCADE)
    facility = models.ForeignKey("facility.Facility", on_delete=models.CASCADE)
    reference_number = models.CharField(max_length=64, db_index=True)
    display = models.CharField(max_length=256)
    hi_types = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    linked_via = models.CharField(max_length=8, choices=LinkedVia.choices, blank=True, default="")
    linked_at = models.DateTimeField(null=True, blank=True)
    link_request = models.ForeignKey(
        AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    notify_request = models.ForeignKey(
        AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    notified_at = models.DateTimeField(null=True, blank=True)
    error_code = models.CharField(max_length=64, blank=True, default="")
    error_message = models.CharField(max_length=512, blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["facility", "reference_number"], name="abdm_care_context_reference")
        ]
        indexes = [models.Index(fields=["patient", "status"]), models.Index(fields=["facility", "status"])]

    def __str__(self):
        return f"{self.reference_number}:{self.status}"


class AbdmLinkSession(BaseModel):
    """
    1 user-initiated link flow: discover -> init (OTP) -> confirm. Keyed by the gateway
    `transactionId`. The OTP is stored as a hash and expires with `otp_expires_at`.
    """

    class Status(models.TextChoices):
        DISCOVERED = "discovered"
        OTP_SENT = "otp_sent"
        CONFIRMED = "confirmed"
        FAILED = "failed"

    transaction_id = models.CharField(max_length=128, unique=True)
    facility = models.ForeignKey("facility.Facility", null=True, blank=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey("emr.Patient", null=True, blank=True, on_delete=models.SET_NULL)
    abha_address = models.CharField(max_length=128, blank=True, default="")
    # Care-context reference numbers the PHR app asked to link (from the init callback).
    care_context_references = models.JSONField(default=list, blank=True)
    link_reference_number = models.CharField(max_length=64, blank=True, default="", db_index=True)
    otp_hash = models.CharField(max_length=128, blank=True, default="")
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DISCOVERED, db_index=True)
    error_code = models.CharField(max_length=64, blank=True, default="")
    error_message = models.CharField(max_length=512, blank=True, default="")

    def __str__(self):
        return f"link-session:{self.transaction_id}:{self.status}"


class AbdmConsent(BaseModel):
    """
    A consent artefact as the gateway notifies it to this HIP (GRANTED, REVOKED, EXPIRED).
    Body shape: /docs/hiecm/v3/api/m3/endpoints/m3-on-consent-request-notify-hip.
    """

    class Status(models.TextChoices):
        GRANTED = "GRANTED"
        REVOKED = "REVOKED"
        EXPIRED = "EXPIRED"

    consent_id = models.CharField(max_length=128, unique=True)
    facility = models.ForeignKey("facility.Facility", null=True, blank=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey("emr.Patient", null=True, blank=True, on_delete=models.SET_NULL)
    abha_address = models.CharField(max_length=128, blank=True, default="", db_index=True)
    hiu_id = models.CharField(max_length=128, blank=True, default="")
    hiu_name = models.CharField(max_length=256, blank=True, default="")
    purpose_code = models.CharField(max_length=32, blank=True, default="")
    hi_types = models.JSONField(default=list, blank=True)
    care_context_references = models.JSONField(default=list, blank=True)
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    data_erase_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, db_index=True)
    artefact = models.JSONField(default=dict, blank=True)
    signature = models.TextField(blank=True, default="")
    callback = models.ForeignKey(AbdmCallback, null=True, blank=True, on_delete=models.SET_NULL)
    ack_request = models.ForeignKey(AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL)
    notified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"consent:{self.consent_id}:{self.status}"


class AbdmDataRequest(BaseModel):
    """
    1 health-information request under a consent: ack, build, encrypt, push, notify.
    The docs give 20 minutes from the request to the data push (/concepts/data-flow).
    """

    class Status(models.TextChoices):
        RECEIVED = "received"
        ACKNOWLEDGED = "acknowledged"
        TRANSFERRED = "transferred"
        FAILED = "failed"

    transaction_id = models.CharField(max_length=128, unique=True)
    consent = models.ForeignKey(AbdmConsent, null=True, blank=True, on_delete=models.SET_NULL)
    consent_artefact_id = models.CharField(max_length=128, blank=True, default="", db_index=True)
    facility = models.ForeignKey("facility.Facility", null=True, blank=True, on_delete=models.SET_NULL)
    data_push_url = models.URLField(max_length=1024, blank=True, default="")
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    key_material = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.RECEIVED, db_index=True)
    received_at = models.DateTimeField()
    deadline_at = models.DateTimeField(db_index=True)
    callback = models.ForeignKey(AbdmCallback, null=True, blank=True, on_delete=models.SET_NULL)
    ack_request = models.ForeignKey(
        AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    push_request = models.ForeignKey(
        AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    notify_request = models.ForeignKey(
        AbdmOutboundRequest, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    # 1 entry per (care context, HI type): {careContextReference, hiType, hiStatus, description, checksum}
    entries = models.JSONField(default=list, blank=True)
    pushed_at = models.DateTimeField(null=True, blank=True)
    error_code = models.CharField(max_length=64, blank=True, default="")
    error_message = models.CharField(max_length=512, blank=True, default="")

    def __str__(self):
        return f"data-request:{self.transaction_id}:{self.status}"
