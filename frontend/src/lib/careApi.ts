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

/** The registry record kept at link time (ADR-016), plus who linked it and when. */
export type AbdmRegistrySnapshot = Partial<AbdmHfrFacility> & {
  linked_at?: string;
  linked_by?: string;
};

export type AbdmFacilityConfig = {
  /**
   * Read-only. The service id the gateway issued when the HRP service was registered
   * (e.g. IN1410000232_1). Empty until then; not the HFR facility ID.
   */
  hip_id?: string;
  /** Read-only: set by a registry link (lookup, search or the HFR wizard), never typed. */
  facility_id: string;
  /** Read-only: the registered name, exactly as the registry holds it. */
  facility_name: string;
  hip_name: string;
  /** Scan and Share counter codes; each 1 to 20 letters or digits. */
  counters: string[];
  /** Read-only: the registry record behind `facility_id`. Empty when not linked. */
  hfr?: AbdmRegistrySnapshot;
  /** Read-only, from ABDM_SHARE_QR_URL_TEMPLATE. Placeholders {hip_id} and {context}. */
  share_qr_url_template?: string;
  hrp_registered_at?: string;
  last_error?: string;
};

/** PUT body: the 2 typed fields. */
export type AbdmFacilityConfigUpdate = Pick<
  AbdmFacilityConfig,
  "hip_name" | "counters"
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
  gateway: {
    ok: boolean;
    token_prefix?: string;
    status_code?: number;
    request_id?: string;
  };
  /** Every facility the caller can see (ADR-016), linked to the registry or not. */
  facilities: AbdmAdminFacilityRow[];
};

export type AbdmAdminFacilityRow = {
  id: string;
  name: string;
  /** Care's facility type name. */
  facility_type: string;
  /** HFR facility ID (e.g. IN1410000232); empty when not linked. */
  facility_id: string;
  /** Gateway-issued HIP service id (e.g. IN1410000232_1); empty until the HRP service is registered. */
  hip_id: string;
  facility_name: string;
  /** The registry's own status of the linked record (Verified, Submitted, ...). */
  registry_status: string;
  hip_name: string;
  counters: string[];
  hrp_registered_at: string | null;
  onboarding_status: AbdmHfrOnboardingStatus | "";
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
  "pending" | "link_requested" | "linked" | "failed";

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
  "staged" | "queued" | "linked" | "failed" | "excluded";

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

// --- M3 (HIU, ADR-014): consent requests this facility raised and the records it received ---

export type AbdmFailureBlock = AbdmCareContextState["failure"];

export type AbdmConsentRequestStatus =
  "REQUESTED" | "GRANTED" | "DENIED" | "EXPIRED" | "REVOKED" | "failed";

export type AbdmFetchStatus =
  "requested" | "acknowledged" | "received" | "partial" | "failed";

/** 1 decrypted bundle another facility pushed. `bundle` is only on the detail route. */
export type AbdmFetchedRecord = {
  id: string;
  careContextReference: string;
  hiType: string;
  title: string;
  authoredAt: string | null;
  hipId: string;
  hipName: string;
  checksumOk: boolean;
  resourceCount: number;
  receivedAt: string;
  eraseAt: string | null;
  erasedAt: string | null;
  available: boolean;
};

export type AbdmFetchedRecordDetail = AbdmFetchedRecord & {
  bundle: Record<string, unknown> | null;
};

/** 1 health-information request under an artefact (20-minute window). */
export type AbdmFetchRequest = {
  id: string;
  transactionId: string;
  status: AbdmFetchStatus;
  requestedAt: string;
  deadlineAt: string;
  acknowledgedAt: string | null;
  receivedAt: string | null;
  pages: string;
  entries: {
    careContextReference: string;
    hiStatus: "OK" | "ERRORED";
    description: string;
  }[];
  requestId: string;
  failure: AbdmFailureBlock;
};

/** 1 consent artefact the HIE-CM created for a request of ours. */
export type AbdmConsentArtefact = {
  id: string;
  artefactId: string;
  status: "GRANTED" | "DENIED" | "EXPIRED" | "REVOKED";
  live: boolean;
  hipId: string;
  hipName: string;
  hiTypes: string[];
  careContextReferences: string[];
  dateFrom: string | null;
  dateTo: string | null;
  dataEraseAt: string | null;
  fetchedAt: string | null;
  failure: AbdmFailureBlock;
  fetches: AbdmFetchRequest[];
  records: AbdmFetchedRecord[];
};

/** 1 consent request (the ask). The artefacts are the permission. */
export type AbdmConsentRequest = {
  id: string;
  consentRequestId: string;
  status: AbdmConsentRequestStatus;
  open: boolean;
  purposeCode: string;
  purposeText: string;
  hiTypes: string[];
  dateFrom: string;
  dateTo: string;
  dataEraseAt: string;
  hipId: string;
  hipName: string;
  requestedBy: string;
  requestedAt: string;
  statusCheckedAt: string | null;
  decidedAt: string | null;
  reason: string;
  requestId: string;
  failure: AbdmFailureBlock;
  artefacts: AbdmConsentArtefact[];
};

/** GET /api/abdm/patients/{patientId}/abha/consent-requests?facility= */
export type AbdmHiuState = {
  facilityConfigured: boolean;
  callbackUrlSet: boolean;
  patientAbhaAddress: string;
  purposes: { code: string; text: string }[];
  hiTypes: string[];
  defaults: {
    purposeCode: string;
    hiTypes: string[];
    dateFrom: string;
    dateTo: string;
    dataEraseAt: string;
  };
  requests: AbdmConsentRequest[];
  /** Set on the POST answer: the id of the request just created. */
  created?: string;
};

export type AbdmConsentRequestCreate = {
  facility_id: string;
  purpose_code?: string;
  hi_types?: string[];
  date_from?: string;
  date_to?: string;
  data_erase_at?: string;
  hip_id?: string;
  hip_name?: string;
};

export type AbdmProvider = { id: string; name: string; isHip: boolean };

// --- M4 (NHPR, ADR-015): HFR lookup/link/onboarding for a facility; the caller's own HPR ID ---

export type AbdmMasterRow = {
  code: string;
  name: string;
  children?: AbdmMasterRow[];
};

/** 1 registry facility (m4-search/02). */
export type AbdmHfrFacility = {
  facilityId: string;
  facilityName: string;
  facilityStatus: string;
  facilityType: string;
  facilityTypeCode: string;
  ownership: string;
  ownershipCode: string;
  systemOfMedicine: string;
  address: string;
  pincode: string;
  stateName: string;
  stateLGDCode: string;
  districtName: string;
  districtLGDCode: string;
  subDistrictName: string;
  latitude: string;
  longitude: string;
};

export type AbdmHfrSearchResult = {
  facilities: AbdmHfrFacility[];
  message: string;
  total: number;
  pages: number;
};

export type AbdmHfrOnboardingStatus =
  | "draft"
  | "basic_saved"
  | "additional_saved"
  | "detailed_saved"
  | "submitted"
  | "failed";

export type AbdmHfrOnboarding = {
  status: AbdmHfrOnboardingStatus;
  nextStep: AbdmHfrStep;
  trackingId: string;
  facilityId: string;
  dedupResults: Record<string, unknown>[];
  basic: Record<string, unknown>;
  additional: Record<string, unknown>;
  detailed: Record<string, unknown>;
  submit: Record<string, unknown>;
  lastMessage: string;
  submittedAt: string | null;
  createdAt: string;
  startedBy: string;
  hprId: string;
  failure: AbdmFailureBlock;
};

// --- "Add a facility" (ADR-016): organization-level create + registry search ----------------------

/** GET care/facility-form-options: Care's own choice lists. */
export type AbdmFacilityFormOptions = {
  facilityTypes: { id: number; name: string }[];
  features: { id: number; name: string }[];
};

/** A Care government organization as `OrganizationReadSpec` serialises it. */
export type CareGovtOrganizationParent = {
  id?: string;
  name?: string;
  org_type?: string;
  level_cache?: number;
  metadata?: Record<string, unknown>;
  parent?: CareGovtOrganizationParent | Record<string, never>;
};

export type CareGovtOrganization = {
  id: string;
  name: string;
  org_type: string;
  level_cache: number;
  has_children: boolean;
  parent?: CareGovtOrganizationParent | Record<string, never>;
  metadata?: Record<string, unknown>;
};

/** GET organizations/{id}/hfr/prefill?facility_id= */
export type AbdmFacilityPrefill = {
  registry: AbdmHfrFacility;
  care: {
    name: string;
    address: string;
    pincode: number | null;
    latitude: number | null;
    longitude: number | null;
    facility_type: string;
    state_name: string;
    district_name: string;
  };
  geo: {
    state: CareGovtOrganization | null;
    district: CareGovtOrganization | null;
  };
  hipName: string;
  alreadyLinked: { id: string; name: string } | null;
};

/** The Care facility form, as `FacilityCreateSpec` takes it. */
export type CareFacilityCreate = {
  name: string;
  description: string;
  facility_type: string;
  features: number[];
  pincode: number;
  address: string;
  phone_number: string;
  latitude?: number;
  longitude?: number;
  geo_organization: string;
  is_public: boolean;
};

export type AbdmCreateFacilityRequest = {
  care: CareFacilityCreate;
  registry_id?: string;
  hip_name?: string;
  /** Optional context: the default `geo_organization` when the form sent none. */
  organization?: string;
};

export type AbdmCreateFacilityResponse = {
  facility: { id: string; name: string } & Record<string, unknown>;
  abdm: AbdmFacilityConfig;
  registry: AbdmHfrFacility | null;
};

/** GET/POST facilities/{id}/abdm/hfr/onboarding */
export type AbdmHfrState = {
  config: AbdmFacilityConfig;
  onboarding: AbdmHfrOnboarding | null;
  hprSession: {
    hprId: string;
    active: boolean;
    expiresAt: string | null;
    role: number | null;
  };
  prefill: {
    facilityName: string;
    address: string;
    pincode: string;
    phone: string;
    latitude: string;
    longitude: string;
  };
  errors?: string;
  code?: string;
};

export type AbdmHfrStep =
  "dedup" | "basic" | "additional" | "detailed" | "submit";

export type AbdmHpidStatus =
  | "link_created"
  | "aadhaar_verified"
  | "account_exists"
  | "mobile_verified"
  | "created"
  | "failed";

export type AbdmHpidTransaction = {
  id: string;
  status: AbdmHpidStatus;
  aadhaarUrl: string;
  linkExpiresAt: string | null;
  details: Record<string, string>;
  mobileMasked: string;
  mobileVerified: boolean;
  otpSentAt: string | null;
  suggestions: string[];
  existing: Record<string, unknown>;
  hprId: string;
  hprIdNumber: string;
  failure: AbdmFailureBlock;
};

/** GET users/me/abdm/hpr */
export type AbdmHprState = {
  profile: {
    hprId: string;
    hprIdNumber: string;
    name: string;
    categoryCode: string;
    subCategoryCode: string;
    role: number | null;
    source: "login" | "created";
    account: Record<string, unknown>;
    registeredAt: string | null;
    verifiedAt: string | null;
    professional: Record<string, unknown>;
  } | null;
  session: { active: boolean; expiresAt: string | null; method: string };
  pendingLogin: {
    id: string;
    hprId: string;
    mobileMasked: string;
    attempts: number;
  } | null;
  transaction: AbdmHpidTransaction | null;
  loginMethods: string[];
  roles: { code: number; name: string }[];
  careUser: { username: string; name: string; councilRegistration: string };
  errors?: string;
  code?: string;
};

export type AbdmHprPublicRecord = {
  hpr_id_number: string;
  hpr_id: string;
  name: string;
  auth_methods: string[];
  category_id: string;
  sub_category_id: string;
};

export type AbdmHpidFinishBody = {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  middle_name?: string;
  last_name?: string;
  category_code: number | string;
  sub_category_code: number | string;
  state_code: string;
  district_code: string;
  role: number;
};

export type AbdmDocumentSlot = {
  group: string;
  type: string;
  id: number;
  hasData: boolean;
  system: string;
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
  // --- M3 (HIU): consent requests, fetched records, provider search ---
  consentRequests: {
    path: "/api/abdm/patients/{patientId}/abha/consent-requests",
    method: HttpMethod.GET,
    TResponse: {} as AbdmHiuState,
  },
  createConsentRequest: {
    path: "/api/abdm/patients/{patientId}/abha/consent-requests",
    method: HttpMethod.POST,
    TRequest: {} as AbdmConsentRequestCreate,
    TResponse: {} as AbdmHiuState,
  },
  consentRequestAction: {
    path: "/api/abdm/patients/{patientId}/abha/consent-requests/{requestId}/{action}",
    method: HttpMethod.POST,
    TRequest: {} as Record<string, never>,
    TResponse: {} as AbdmHiuState,
  },
  fetchedRecord: {
    path: "/api/abdm/patients/{patientId}/abha/records/{recordId}",
    method: HttpMethod.GET,
    TResponse: {} as AbdmFetchedRecordDetail,
  },
  providers: {
    path: "/api/abdm/providers",
    method: HttpMethod.GET,
    TResponse: {} as { results: AbdmProvider[] },
  },
  // --- M4 facility side: HFR lookup, search, link, onboarding, facility OTP ---
  hfrLookup: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hfr/lookup",
    method: HttpMethod.GET,
    TResponse: {} as AbdmHfrFacility,
  },
  hfrSearch: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hfr/search",
    method: HttpMethod.GET,
    TResponse: {} as AbdmHfrSearchResult,
  },
  hfrLink: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hfr/link",
    method: HttpMethod.POST,
    TRequest: {} as { facility_id: string },
    TResponse: {} as { config: AbdmFacilityConfig; registry: AbdmHfrFacility },
  },
  hfrOnboarding: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hfr/onboarding",
    method: HttpMethod.GET,
    TResponse: {} as AbdmHfrState,
  },
  // --- "Add a facility" (ADR-016) ---
  facilityFormOptions: {
    path: "/api/abdm/care/facility-form-options",
    method: HttpMethod.GET,
    TResponse: {} as AbdmFacilityFormOptions,
  },
  createFacility: {
    path: "/api/abdm/facilities",
    method: HttpMethod.POST,
    TRequest: {} as AbdmCreateFacilityRequest,
    TResponse: {} as AbdmCreateFacilityResponse,
  },
  hfrSearchForCreate: {
    path: "/api/abdm/hfr/search",
    method: HttpMethod.GET,
    TResponse: {} as AbdmHfrSearchResult,
  },
  hfrPrefill: {
    path: "/api/abdm/hfr/prefill",
    method: HttpMethod.GET,
    TResponse: {} as AbdmFacilityPrefill,
  },
  /** Care's public government organization list (care/emr/api/viewsets/organization.py). */
  govtOrganizations: {
    path: "/api/v1/govt/organization/",
    method: HttpMethod.GET,
    TResponse: {} as { results: CareGovtOrganization[]; count: number },
  },
  govtOrganization: {
    path: "/api/v1/govt/organization/{organizationId}/",
    method: HttpMethod.GET,
    TResponse: {} as CareGovtOrganization,
  },
  hfrOnboardingStep: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hfr/onboarding",
    method: HttpMethod.POST,
    TRequest: {} as { step: AbdmHfrStep; payload: Record<string, unknown> },
    TResponse: {} as AbdmHfrState,
  },
  hfrOtp: {
    path: "/api/abdm/facilities/{facilityId}/abdm/hfr/otp",
    method: HttpMethod.POST,
    TRequest: {} as {
      action: "send" | "validate";
      facility_id: string;
      transaction_id?: string;
      otp?: string;
      source?: string;
      source_id?: string;
    },
    TResponse: {} as {
      transactionId?: string;
      message: string;
      status: string;
    },
  },
  // --- M4 user side: the caller's own HPR ID ---
  hprState: {
    path: "/api/abdm/users/me/abdm/hpr",
    method: HttpMethod.GET,
    TResponse: {} as AbdmHprState,
  },
  hprVerifyId: {
    path: "/api/abdm/users/me/abdm/hpr/verify-id",
    method: HttpMethod.GET,
    TResponse: {} as AbdmHprPublicRecord,
  },
  hprLogin: {
    path: "/api/abdm/users/me/abdm/hpr/login",
    method: HttpMethod.POST,
    TRequest: {} as {
      method: "password" | "aadhaar_otp";
      hpr_id: string;
      password?: string;
    },
    TResponse: {} as AbdmHprState,
  },
  hprLoginVerify: {
    path: "/api/abdm/users/me/abdm/hpr/login/verify",
    method: HttpMethod.POST,
    TRequest: {} as { login_id: string; otp: string },
    TResponse: {} as AbdmHprState,
  },
  hprSessionAction: {
    path: "/api/abdm/users/me/abdm/hpr/session/{action}",
    method: HttpMethod.POST,
    TRequest: {} as Record<string, never>,
    TResponse: {} as AbdmHprState,
  },
  hpidCreate: {
    path: "/api/abdm/users/me/abdm/hpr/create/{action}",
    method: HttpMethod.POST,
    TRequest: {} as Partial<AbdmHpidFinishBody> & {
      mobile?: string;
      otp?: string;
    },
    TResponse: {} as AbdmHprState,
  },
  hprRegister: {
    path: "/api/abdm/users/me/abdm/hpr/register",
    method: HttpMethod.POST,
    TRequest: {} as { practitioner: Record<string, unknown> },
    TResponse: {} as AbdmHprState,
  },
  hprRegisterUpdate: {
    path: "/api/abdm/users/me/abdm/hpr/register/update",
    method: HttpMethod.POST,
    TRequest: {} as { practitioner: Record<string, unknown> },
    TResponse: {} as AbdmHprState,
  },
  hprDocuments: {
    path: "/api/abdm/users/me/abdm/hpr/documents",
    method: HttpMethod.GET,
    TResponse: {} as { slots: AbdmDocumentSlot[] },
  },
  hprUploadDocuments: {
    path: "/api/abdm/users/me/abdm/hpr/documents",
    method: HttpMethod.POST,
    TRequest: {} as {
      documents: {
        document_id: number;
        document_type: string;
        fileType: string;
        data: string;
      }[];
    },
    TResponse: {} as Record<string, { status: string; msg: string } | null>,
  },
  hprProfessionalInfo: {
    path: "/api/abdm/users/me/abdm/hpr/professional-info",
    method: HttpMethod.GET,
    TResponse: {} as Record<string, unknown>,
  },
  nhprMasters: {
    path: "/api/abdm/nhpr/masters/{kind}",
    method: HttpMethod.GET,
    TResponse: {} as { results: AbdmMasterRow[] },
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
