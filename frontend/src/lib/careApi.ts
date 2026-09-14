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
  hip_id: string;
  bridge_id: string;
  service_id: string;
  facility_id: string;
  facility_name: string;
  hip_name: string;
  x_hip_id_source: "hip_id" | "bridge_id" | "service_id";
  bridge_url: string;
  bridge_url_registered_at?: string;
  hrp_registered_at?: string;
  last_error?: string;
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
  processed_status: "received" | "queued" | "unhandled" | "failed";
  received_at: string;
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
  // --- M2 step 1: facility and bridge proof ---
  facilityAbdm: {
    path: "/api/abdm/facilities/{facilityId}/abdm",
    method: HttpMethod.GET,
    TResponse: {} as AbdmFacilityConfig,
  },
  updateFacilityAbdm: {
    path: "/api/abdm/facilities/{facilityId}/abdm",
    method: HttpMethod.PUT,
    TRequest: {} as AbdmFacilityConfig,
    TResponse: {} as AbdmFacilityConfig,
  },
  registerBridgeUrl: {
    path: "/api/abdm/facilities/{facilityId}/abdm/bridge-url",
    method: HttpMethod.POST,
    TRequest: {} as { url?: string | null },
    TResponse: {} as FacilityBridgeActionResponse,
  },
  registerHrpService: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hrp-services",
    method: HttpMethod.POST,
    TRequest: {} as Record<string, never>,
    TResponse: {} as FacilityBridgeActionResponse,
  },
  facilityBridgeServices: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hrp-services",
    method: HttpMethod.GET,
    TResponse: {} as {
      status_code: number;
      request_id: string;
      response: Record<string, unknown>;
    },
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
  // --- M1 Journey 1: ABHA creation by Aadhaar OTP ---
  requestAadhaarOtp: {
    path: "/api/abdm/abha/enrol/aadhaar/request-otp",
    method: HttpMethod.POST,
    TRequest: {} as { aadhaar_number: string },
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
