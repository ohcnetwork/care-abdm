import { HttpMethod, apiRoutes } from "@/lib/request";

// Routes served by the backend plug (care-abdm-sbx/backend/src/abdm/urls.py),
// mounted by Care at /api/abdm/ (care/config/urls.py:111-112).

/** Shape of a relayed ABDM failure (HTTP 502 from abdm/abha/views.py). */
export type AbdmRelayError = {
  abdm_code: string | null;
  message: string;
  request_id: string;
  upstream_status: number;
};

export type AbdmFacilityConfig = {
  /**
   * Read-only. The service id the gateway issued when the HRP service was registered
   * (e.g. IN1410000232_1). Empty until then; not the HFR facility ID.
   */
  hip_id?: string;
  facility_id: string;
  facility_name: string;
  hip_name: string;
  /** Scan and Share counter codes; each 1 to 20 letters or digits. */
  counters: string[];
  /** Read-only, from ABDM_SHARE_QR_URL_TEMPLATE. Placeholders {hip_id} and {context}. */
  share_qr_url_template?: string;
  hrp_registered_at?: string;
  last_error?: string;
};

export type AbdmFacilityConfigUpdate = Omit<
  AbdmFacilityConfig,
  "hip_id" | "share_qr_url_template" | "hrp_registered_at" | "last_error"
>;

/** GET /api/abdm/bridge: the derived callback URL plus the live gateway view (1 bridge per clientId). */
export type AbdmBridgeState = {
  callback_url: string;
  bridge: {
    id: string;
    name: string;
    url: string;
    active: boolean | null;
    blocklisted: boolean | null;
  } | null;
  services: unknown[];
  error: string;
  registration?: { url: string; status_code: number; request_id: string };
};

/** GET /api/abdm/admin/overview (superuser): the bridge state plus the gateway session and the HIP facilities. */
export type AbdmAdminOverview = AbdmBridgeState & {
  gateway: { ok: boolean; token_prefix?: string; status_code?: number; request_id?: string };
  facilities: {
    id: string;
    name: string;
    /** HFR facility ID (e.g. IN1410000232). */
    facility_id: string;
    /** Gateway-issued HIP service id (e.g. IN1410000232_1); empty until the HRP service is registered. */
    hip_id: string;
    facility_name: string;
    hip_name: string;
    counters: string[];
    hrp_registered_at: string | null;
    last_error: string;
    /** The most recent refused ABDM call at this facility (backend errors.py, ADR-012). */
    last_failure: {
      operation_id: string;
      request_id: string;
      sent_at: string;
      http_status: number | null;
      code: string;
      action: string;
      retry: "now" | "after" | "never";
      retryAt: string | null;
      what: string;
      nextStep: string;
      detail: string;
      supportReference: string;
    } | null;
  }[];
};

// --- M2: care contexts, consents, data requests ---

export type AbdmOutboundSummary = {
  requestId: string;
  operationId: string;
  status: "sent" | "succeeded" | "failed";
  httpStatus: number | null;
  errorCode: string;
  sentAt: string | null;
  callbacks: {
    path: string;
    signatureStatus: string;
    processedStatus: string;
    receivedAt: string;
  }[];
};

export type AbdmCareContextStatus =
  | "pending"
  | "link_requested"
  | "linked"
  | "failed";

/** GET /api/abdm/encounters/{encounterId}/care-context */
export type AbdmCareContextState = {
  facilityConfigured: boolean;
  patientAbhaAddress: string;
  patientAbhaNumber: string;
  linkToken: {
    status: "requested" | "active" | "failed";
    expiresAt: string | null;
    errorCode: string;
  } | null;
  careContext: {
    referenceNumber: string;
    display: string;
    hiTypes: string[];
    status: AbdmCareContextStatus;
    linkedVia: "hip" | "user" | "";
    linkedAt: string | null;
    notifiedAt: string | null;
    errorCode: string;
    errorMessage: string;
  } | null;
  /** The 1 thing the desk reads when a share does not go through (backend errors.py, ADR-012). */
  failure: {
    code: string;
    action: string;
    retry: "now" | "after" | "never";
    retryAt: string | null;
    what: string;
    nextStep: string;
    detail: string;
    supportReference: string;
  } | null;
  activity: AbdmOutboundSummary[];
  /** ADR-013: 1 row per shareable record of this Encounter. */
  shareItems: AbdmShareItem[];
  /** The Encounter is completed or discharged: every staged item was queued. */
  encounterClosed: boolean;
};

export type AbdmShareItemStatus =
  | "staged"
  | "queued"
  | "linked"
  | "failed"
  | "excluded";

export type AbdmShareItem = {
  id: string;
  hiType: string;
  sourceModel:
    | "encounter"
    | "medication_request_prescription"
    | "diagnostic_report"
    | "report_upload";
  sourceId: number;
  label: string;
  status: AbdmShareItemStatus;
  attempts: number;
  nextAttemptAt: string | null;
  linkedAt: string | null;
  requestId: string;
  failure: AbdmCareContextState["failure"];
};

export type AbdmConsentSummary = {
  id: string;
  consentId: string;
  status: "GRANTED" | "REVOKED" | "EXPIRED";
  hiuId: string;
  hiuName: string;
  purposeCode: string;
  hiTypes: string[];
  careContextReferences: string[];
  dateFrom: string | null;
  dateTo: string | null;
  dataEraseAt: string | null;
  notifiedAt: string | null;
  facility: string | null;
};

export type AbdmDataRequestSummary = {
  id: string;
  transactionId: string;
  consentId: string;
  status: "received" | "acknowledged" | "transferred" | "failed";
  receivedAt: string;
  deadlineAt: string;
  pushedAt: string | null;
  entries: {
    careContextReference: string;
    hiType: string;
    hiStatus: "OK" | "ERRORED";
    description: string;
  }[];
  errorCode: string;
  errorMessage: string;
};

export type FacilityBridgeActionResponse = {
  config: AbdmFacilityConfig;
  gateway: {
    status_code: number;
    request_id: string;
    response: Record<string, unknown>;
  };
};

export type AbdmCallbackSummary = {
  id: string;
  path: string;
  operation_id: string;
  request_id_header: string;
  response_request_id: string;
  transaction_id: string;
  signature_status: "missing" | "ok" | "failed";
  /** The header that carried the verified token, once a real callback has been verified. */
  signature_header: string;
  /** Why the last verification did not pass; empty on success. */
  signature_error: string;
  processed_status: "received" | "queued" | "unhandled" | "handled" | "failed";
  received_at: string;
};

/** One Scan and Share event (GET facilities/{id}/abdm/profile-shares). */
export type AbdmProfileShare = {
  id: string;
  status: "received" | "acknowledged" | "ack_failed" | "rejected";
  context: string;
  tokenNumber: string;
  abhaNumber: string;
  abhaAddress: string;
  profile: {
    name?: string;
    gender?: string;
    dob?: string;
    mobile?: string;
    address?: {
      line?: string;
      district?: string;
      state?: string;
      pinCode?: string;
    };
  };
  hasPhoto: boolean;
  patient: string | null;
  patientName: string | null;
  txnId: string | null;
  errorCode: string;
  errorMessage: string;
  receivedAt: string;
  acknowledgedAt: string | null;
  dismissedAt: string | null;
  kycPhoto?: string;
};

export type AbdmCallbackDetail = AbdmCallbackSummary & {
  headers: Record<string, string>;
  raw_body: string;
  parsed_json: Record<string, unknown>;
};

export type AbhaProfile = {
  ABHANumber?: string;
  firstName?: string;
  middleName?: string;
  lastName?: string;
  name?: string;
  dob?: string; // observed formats unknown; parsed defensively
  gender?: "M" | "F" | "O" | string;
  mobile?: string;
  phrAddress?: string[];
  preferredAbhaAddress?: string;
  abhaStatus?: string;
  [k: string]: unknown;
};

/**
 * enrol/byAadhaar 200 body is UNDOCUMENTED in the docs (m1-enrolment-by-aadhaar:
 * "Send the call with Try it"). Fields below are the docs' hints only; the
 * component treats everything as optional and the raw body is logged server-side.
 * `tokens` is stripped server-side (abdm/abha/service.py) and never reaches the browser.
 */
export type EnrolByAadhaarResponse = {
  txnId?: string;
  message?: string;
  isNew?: boolean;
  ABHAProfile?: AbhaProfile;
  [k: string]: unknown;
};

/** Accounts returned by login/verify (m1-login-verify), minus profilePhoto. */
export type AbhaAccount = {
  ABHANumber: string;
  preferredAbhaAddress?: string;
  name?: string;
  gender?: string;
  dob?: string;
  status?: string;
  kycVerified?: boolean;
  [k: string]: unknown;
};

/** GET /api/abdm/patients/<id>/abha */
export type AbhaSource =
  | "enrol_aadhaar"
  | "login_mobile"
  | "login_abha_number"
  | "login_abha_address"
  | "login_aadhaar";

export type PatientAbhaStatus = {
  linked: boolean;
  abha_number: string | null;
  abha_address: string | null;
  abha_linked_at: string | null;
  abha_source: AbhaSource | null;
  kyc_verified: boolean | null;
  profile: Partial<
    Pick<
      AbhaProfile,
      | "name"
      | "firstName"
      | "lastName"
      | "gender"
      | "dob"
      | "mobile"
      | "status"
      | "abhaStatus"
    >
  > | null;
  /** True when a user session exists or can be refreshed server-side (R-token). */
  card_available: boolean;
};

/**
 * What the person identifies with when logging in to an existing ABHA
 * (m1-login-request-otp `loginHint`; abha-address goes via the phr variant).
 * `otp_system`: where the OTP is delivered — `abdm` = mobile registered with ABHA,
 * `aadhaar` = mobile registered with Aadhaar. The `mobile` hint only supports `abdm`.
 * The `aadhaar` hint only supports `aadhaar`.
 */
export type LoginHint = "mobile" | "abha-number" | "abha-address" | "aadhaar";
export type OtpSystem = "abdm" | "aadhaar";
export type LoginOtpRequest = {
  hint: LoginHint;
  login_id: string;
  otp_system?: OtpSystem;
};

/**
 * GET /v3/profile/account as stored by the plug (tokens/photo stripped). Field
 * names per m1-profile-get-account; everything optional because the docs only
 * show an example, not a schema.
 */
export type AbhaAccountProfile = AbhaProfile & {
  dayOfBirth?: string;
  monthOfBirth?: string;
  yearOfBirth?: string;
  address?: string;
  districtName?: string;
  stateName?: string;
  pinCode?: string;
  kycVerified?: boolean;
  emailVerified?: boolean;
  email?: string;
};

/** A Care patient that already carries this ABHA (abdm/abha/service.py existing_patient_for). */
export type ExistingPatient = {
  id: string;
  name: string;
  phone_number: string;
  date_of_birth: string | null;
  year_of_birth: number | null;
  gender: string;
};

/** Login finished: the plug holds the X-token; `profile` is the account read-back. */
export type LoginCompleted = {
  txnId: string;
  authResult: "success";
  completed: true;
  ABHANumber: string;
  preferredAbhaAddress: string;
  name?: string;
  profile: AbhaAccountProfile;
  existingPatient: ExistingPatient | null;
};

/** Mobile login: several ABHAs share this number; caller must pick one. */
export type LoginNeedsAccount = {
  txnId: string;
  authResult: string;
  message?: string;
  completed: false;
  accounts: AbhaAccount[];
};

export type LoginVerifyResponse = LoginCompleted | LoginNeedsAccount;

/** GET /api/abdm/abha/transactions/<txnId> */
export type AbhaTransactionSummary = {
  txnId: string;
  kind: AbhaSource;
  ABHANumber: string;
  preferredAbhaAddress: string;
  isNew: boolean | null;
  profile: AbhaAccountProfile;
  /** external_id of the Care patient this txn was linked to, if any */
  patient: string | null;
  linkedAt: string | null;
  sessionAvailable: boolean;
  existingPatient: ExistingPatient | null;
};

const routes = apiRoutes({
  /**
   * Host route, not a plug route. The setup page gets only `facilityId` from
   * the URL, so it reads the facility name from Care to show a page header.
   * Source: care_fe/src/types/facility/facilityApi.ts:34-38.
   */
  hostFacility: {
    path: "/api/v1/facility/{facilityId}/",
    method: HttpMethod.GET,
    TResponse: {} as { id: string; name?: string },
  },
  gatewayStatus: {
    path: "/api/abdm/gateway/status",
    method: HttpMethod.GET,
    TResponse: {} as {
      ok: boolean;
      token_prefix?: string;
      status_code?: number;
      request_id?: string;
    },
  },
  // --- instance bridge (1 per clientId) and facility setup ---
  bridge: {
    path: "/api/abdm/bridge",
    method: HttpMethod.GET,
    TResponse: {} as AbdmBridgeState,
  },
  bridgeRegisterUrl: {
    path: "/api/abdm/bridge/register-url",
    method: HttpMethod.POST,
    TRequest: {} as Record<string, never>,
    TResponse: {} as AbdmBridgeState,
  },
  adminOverview: {
    path: "/api/abdm/admin/overview",
    method: HttpMethod.GET,
    TResponse: {} as AbdmAdminOverview,
  },
  facilityAbdm: {
    path: "/api/abdm/facilities/{facilityId}/abdm",
    method: HttpMethod.GET,
    TResponse: {} as AbdmFacilityConfig,
  },
  updateFacilityAbdm: {
    path: "/api/abdm/facilities/{facilityId}/abdm",
    method: HttpMethod.PUT,
    TRequest: {} as AbdmFacilityConfigUpdate,
    TResponse: {} as AbdmFacilityConfig,
  },
  registerHrpService: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hrp-services",
    method: HttpMethod.POST,
    TRequest: {} as Record<string, never>,
    TResponse: {} as FacilityBridgeActionResponse,
  },
  // --- M1 Scan and Share: front desk inbox ---
  profileShares: {
    path: "/api/abdm/facilities/{facilityId}/abdm/profile-shares",
    method: HttpMethod.GET,
    TResponse: {} as { results: AbdmProfileShare[] },
  },
  profileShare: {
    path: "/api/abdm/facilities/{facilityId}/abdm/profile-shares/{shareId}",
    method: HttpMethod.GET,
    TResponse: {} as AbdmProfileShare,
  },
  dismissProfileShare: {
    path: "/api/abdm/facilities/{facilityId}/abdm/profile-shares/{shareId}/dismiss",
    method: HttpMethod.POST,
    TRequest: {} as Record<string, never>,
    TResponse: {} as AbdmProfileShare,
  },
  // --- M2 step 2: callback probe ---
  callbacks: {
    path: "/api/abdm/callbacks",
    method: HttpMethod.GET,
    TResponse: {} as { results: AbdmCallbackSummary[] },
  },
  callback: {
    path: "/api/abdm/callbacks/{callbackId}",
    method: HttpMethod.GET,
    TResponse: {} as AbdmCallbackDetail,
  },
  // --- M2: encounter care context, SMS deep link, consents ---
  encounterCareContext: {
    path: "/api/abdm/encounters/{encounterId}/care-context",
    method: HttpMethod.GET,
    TResponse: {} as AbdmCareContextState,
  },
  encounterCareContextLink: {
    path: "/api/abdm/encounters/{encounterId}/care-context/link",
    method: HttpMethod.POST,
    TRequest: {} as { items?: string[]; all?: boolean },
    TResponse: {} as AbdmCareContextState,
  },
  shareItemAction: {
    path: "/api/abdm/encounters/{encounterId}/share-items/{itemId}/{action}",
    method: HttpMethod.POST,
    TRequest: {} as Record<string, never>,
    TResponse: {} as AbdmCareContextState,
  },
  patientSmsLink: {
    path: "/api/abdm/patients/{patientId}/abha/sms-link",
    method: HttpMethod.POST,
    TRequest: {} as { facility_id: string },
    TResponse: {} as AbdmOutboundSummary,
  },
  patientConsents: {
    path: "/api/abdm/patients/{patientId}/abha/consents",
    method: HttpMethod.GET,
    TResponse: {} as {
      consents: AbdmConsentSummary[];
      dataRequests: AbdmDataRequestSummary[];
    },
  },
  // --- M1 Journey 1: ABHA creation by Aadhaar OTP ---
  requestAadhaarOtp: {
    path: "/api/abdm/abha/enrol/aadhaar/request-otp",
    method: HttpMethod.POST,
    TRequest: {} as { aadhaar_number: string; consent: boolean },
    TResponse: {} as { txnId: string; message: string },
  },
  enrolByAadhaar: {
    path: "/api/abdm/abha/enrol/aadhaar/verify",
    method: HttpMethod.POST,
    TRequest: {} as { txn_id: string; otp: string; mobile: string },
    TResponse: {} as EnrolByAadhaarResponse,
  },
  requestMobileOtp: {
    path: "/api/abdm/abha/enrol/mobile/request-otp",
    method: HttpMethod.POST,
    TRequest: {} as { txn_id: string; mobile: string },
    TResponse: {} as { txnId: string; message: string },
  },
  verifyMobileOtp: {
    path: "/api/abdm/abha/enrol/mobile/verify",
    method: HttpMethod.POST,
    TRequest: {} as { txn_id: string; otp: string },
    TResponse: {} as {
      txnId: string;
      authResult: string;
      message: string;
      accounts?: unknown[];
    },
  },
  addressSuggestions: {
    path: "/api/abdm/abha/enrol/address/suggestions",
    method: HttpMethod.POST,
    TRequest: {} as { txn_id: string },
    TResponse: {} as { txnId: string; abhaAddressList: string[] },
  },
  claimAbhaAddress: {
    path: "/api/abdm/abha/enrol/address/claim",
    method: HttpMethod.POST,
    TRequest: {} as { txn_id: string; abha_address: string },
    TResponse: {} as { healthIdNumber: string; preferredAbhaAddress?: string },
  },
  // --- M1: login to an existing ABHA (mobile / ABHA number / ABHA address / Aadhaar) ---
  loginRequestOtp: {
    path: "/api/abdm/abha/login/request-otp",
    method: HttpMethod.POST,
    TRequest: {} as LoginOtpRequest,
    TResponse: {} as { txnId: string; message: string },
  },
  loginVerifyOtp: {
    path: "/api/abdm/abha/login/verify",
    method: HttpMethod.POST,
    TRequest: {} as { txn_id: string; otp: string },
    TResponse: {} as LoginVerifyResponse,
  },
  loginSelectAccount: {
    path: "/api/abdm/abha/login/select-account",
    method: HttpMethod.POST,
    TRequest: {} as { txn_id: string; abha_number: string },
    TResponse: {} as LoginCompleted,
  },
  transaction: {
    path: "/api/abdm/abha/transactions/{txnId}",
    method: HttpMethod.GET,
    TResponse: {} as AbhaTransactionSummary,
  },
  // --- Patient-scoped ---
  patientAbha: {
    path: "/api/abdm/patients/{patientId}/abha",
    method: HttpMethod.GET,
    TResponse: {} as PatientAbhaStatus,
  },
  patientAbhaLink: {
    path: "/api/abdm/patients/{patientId}/abha/link",
    method: HttpMethod.POST,
    TRequest: {} as { txn_id: string },
    TResponse: {} as PatientAbhaStatus,
  },
});

export default routes;

/** The card endpoint is fetched via <img src>; not part of the JSON route table. */
export const patientAbhaCardUrl = (patientId: string) =>
  `/api/abdm/patients/${patientId}/abha/card`;
