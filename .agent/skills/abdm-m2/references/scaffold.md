# HIE-CM m2 build

Scaffolds an ABDM m2 integration one journey at a time. It covers care contexts, HIP initiated linking, discovery, and pushing encrypted records to a requester.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

## Journeys

### Hip-initiated-linking (`m2-abdm-hip-initiated-linking-hip`)

**Act: the calls in this journey, in order**

#### 1. Perform HIP initiated linking (`m2_post_hip_v3_link_carecontext`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/hip/v3/link/carecontext \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'X-LINK-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": 12345678901234,
  "abhaAddress": "<ABHA_ADDRESS>",
  "patient": [
    {
      "referenceNumber": "TMH-PUID-001",
      "display": "String",
      "careContexts": [
        {
          "referenceNumber": "TMH-PUID-001",
          "display": "display 1"
        }
      ],
      "hiTypes": "DiagnosticReport",
      "count": 1
    }
  ]
}'
```

#### 2. Link on carecontext (`m2_post_v3_link_on_carecontext`)

Inbound to your bridge at `/api/v3/link/on_carecontext`. Acknowledge it and continue.

#### 3. Notify a change to a linked care context (`m2_post_hip_v3_link_context_notify`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/hip/v3/link/context/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "patient": {
      "id": "<ABHA_ADDRESS>"
    },
    "careContext": {
      "patientReference": "<ABHA_ADDRESS>",
      "careContextReference": "b009a970-8b04-4779-abd1-b50f113245bf"
    },
    "hiTypes": [
      "DiagnosticReport"
    ],
    "date": "2024-05-09T10:34:00.387Z",
    "hip": {
      "id": "ABDM_HIP"
    }
  }
}'
```

#### 4. Receive the links context on notify (`m2_post_v3_links_context_on_notify`)

Inbound to your bridge at `/api/v3/links/context/on-notify`. Acknowledge it and continue.

#### 5. Send SMS notification to patient that a care context is linked (`m2_post_hip_v3_link_patient_links_sms_notify2`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/hip/v3/link/patient/links/sms/notify2 \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "phoneNo": "986543***",
    "hip": {
      "id": "ABDM_HIP",
      "name": "ABC Hospital"
    }
  }
}'
```

#### 6. Receive the patients SMS on notify (`m2_post_v3_patients_sms_on_notify`)

Inbound to your bridge at `/api/v3/patients/sms/on-notify`. Acknowledge it and continue.

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### User-initiated-linking (`m2-abdm-user-initiated-linking-hip`)

**Act: the calls in this journey, in order**

#### 1. Discover care contexts associated with a patient (`m2_post_v3_hip_patient_care_context_discover`)

Inbound to your bridge at `/api/v3/hip/patient/care-context/discover`. Acknowledge it and continue.

#### 2. Answer the care context discovery (`m2_post_user_initiated_linking_v3_patient_care_context_on_8c9340`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/user-initiated-linking/v3/patient/care-context/on-discover \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "f901b782-bfdf-4224-9f8d-da2cadc20c0d",
  "patient": [
    {
      "referenceNumber": "<ABHA_ADDRESS>",
      "display": "12345",
      "careContexts": [
        {
          "referenceNumber": "abc123",
          "display": "12345"
        }
      ],
      "hiType": "Prescription",
      "count": 1
    }
  ],
  "matchedBy": [
    "MR"
  ],
  "error": {
    "code": "ABDM-9999",
    "message": "Unknown exception"
  },
  "response": {
    "requestId": "f29f0e59-8388-4698-9fe6-05db67aeac46"
  }
}'
```

#### 3. Initiate the linking of care contexts for a patient (`m2_post_v3_hip_link_care_context_init`)

Inbound to your bridge at `/api/v3/hip/link/care-context/init`. Acknowledge it and continue.

#### 4. Link care context on init (`m2_post_user_initiated_linking_v3_link_care_context_on_init`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/user-initiated-linking/v3/link/care-context/on-init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "f901b782-bfdf-4224-9f8d-da2cadc20c0d",
  "link": {
    "referenceNumber": "d353b782-bfdf-4224-9f8d-da2cadc20c0d",
    "authenticationType": "DIRECT",
    "meta": {
      "communicationMedium": "MOBILE",
      "communicationHint": "OTP",
      "communicationExpiry": "2024-05-01T05:22:34.123Z"
    }
  },
  "error": {
    "code": "ABDM-1001",
    "message": "No data found"
  },
  "response": {
    "requestId": "f29f0e59-8388-4698-9fe6-05db67aeac46"
  }
}'
```

#### 5. Confirm the linking of care contexts for a patient (`m2_post_v3_hip_link_care_context_confirm`)

Inbound to your bridge at `/api/v3/hip/link/care-context/confirm`. Acknowledge it and continue.

#### 6. Link care context on confirm (`m2_post_user_initiated_linking_v3_link_care_context_on_confirm`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "patient": [
    {
      "referenceNumber": "<ABHA_ADDRESS>",
      "display": "12345",
      "careContexts": [
        {
          "referenceNumber": "abc123",
          "display": "12345"
        }
      ],
      "hiType": "Prescription",
      "count": 1
    }
  ],
  "error": {
    "code": "ABDM-1001",
    "message": "No data found"
  },
  "response": {
    "requestId": "f29f0e59-8388-4698-9fe6-05db67aeac46"
  }
}'
```

**Exit condition (Observe until this is true)**

A 202 response. The specification gives no body for it, so read what comes back.

### Link-token (`m2-abdm-link-token-hip`)

**Act: the calls in this journey, in order**

#### 1. Generate link token to link the health records (`m2_post_v3_token_generate_token`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/v3/token/generate-token \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": 12345678901234,
  "abhaAddress": "<ABHA_ADDRESS>",
  "name": "first_name + middle_name + last_name",
  "gender": "M",
  "yearOfBirth": 9999
}'
```

#### 2. Receive the HIP token on generate token (`m2_post_v3_hip_token_on_generate_token`)

Inbound to your bridge at `/api/v3/hip/token/on-generate-token`. Acknowledge it and continue.

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Patient-share (`m2-abdm-patient-share-hip`)

**Act: the calls in this journey, in order**

#### 1. Share HIP patient (`m2_post_v3_hip_patient_share`)

Inbound to your bridge at `/api/v3/hip/patient/share`. Acknowledge it and continue.

#### 2. Answer the patient share request (`m2_post_patient_share_v3_on_share`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/patient-share/v3/on-share \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

**Exit condition (Observe until this is true)**

A 202 response. The specification gives no body for it, so read what comes back.

### Consent-management-data-flow (`m2-consent-management-data-flow-hip`)

**Act: the calls in this journey, in order**

#### 1. Receive the consent decision (`m2_post_v3_consent_request_hip_notify`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/consent/request/hip/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "status": "GRANTED",
    "consentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "consentDetail": {
      "schemaVersion": "v3",
      "consentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "createdAt": "2024-05-01T05:10:20.123Z",
      "patient": {
        "id": "<ABHA_ADDRESS>"
      },
      "careContexts": [
        {
          "patientReference": "batman@tmh",
          "careContextReference": "Episode1"
        }
      ],
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "www.abc.com"
      },
      "hip": {
        "id": "cowin_hip_01",
        "name": "Cowin",
        "type": "HIP"
      },
      "hiu": {
        "id": "cowin_hiu_01",
        "name": "Cowin",
        "type": "HIU"
      },
      "consentManager": {
        "id": "abdm"
      },
      "requester": {
        "name": "<ABHA_ADDRESS>",
        "identifier": {
          "value": "REG1",
          "type": "MH1001",
          "system": "https://www.sample.com"
        }
      },
      "hiTypes": [
        "Prescription"
      ],
      "permission": {
        "accessMode": "VIEW",
        "dateRange": {
          "from": "2021-09-28T12:30:08.573Z",
          "to": "2021-09-28T12:30:08.573Z"
        },
        "dataEraseAt": "2021-09-28T12:30:08.573Z",
        "frequency": {
          "unit": "HOUR",
          "value": 1,
          "repeats": 0
        }
      }
    },
    "signature": "e8nY601CYDsC0FKoDjSp+7GeQ2s2R8oZncLCz5ce+pEuDOr5bZV0aaHjwJg4b9S9V+twjt4hbojx3fl7egrt8+0c+lfPTi5/bBUAQXCABTfFmtFU7jn65HlTt8kgkiONx26ZBhJ0wX3xjYI72PPtzYIiT5Q08YtDoILA62KceioV7lwuKssw7wC4ECbBAvRuXT121TmtrPhf+0myJATSnaajS06S6OthrKfZLNTUFf3pFiJzqouSTrjNblOX6DT2+JuO3rom1Szz/03c0HQG+wWASv+PO3J6uRs0UI4JvKmM/4tP+Z+/HPKM15K5U5K+4pqf6czKrbIDpkT/kP8bGg==",
    "grantAcknowledgement": false
  }
}'
```

#### 2. Acknowledge the consent notification (`m2_post_consent_v3_request_hip_on_notify`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/hip/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "OK",
    "consentId": "e3c74829-3f82-4f94-959e-e10f57bcd57b"
  },
  "error": {
    "code": "ABDM-1001",
    "message": "unable to connect database"
  },
  "response": {
    "requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"
  }
}'
```

#### 3. Receive the health information data request to HIP (`m2_post_v3_hip_health_information_request`)

Inbound to your bridge at `/api/v3/hip/health-information/request`. Acknowledge it and continue.

#### 4. Submit the health information data request acknowledgement from HIP (`m2_post_data_flow_v3_health_information_hip_on_request`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/hip/on-request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

#### 5. Receive the transferred health information (`m2_post_health_information_transfer`)

Inbound to your bridge at `/health-information/transfer`. Acknowledge it and continue.

**Exit condition (Observe until this is true)**

A 202 response. The specification gives no body for it, so read what comes back.

## Where the detail is

- Every operation, with its body fields and responses: /docs/hiecm/v3/api/m2
- Error codes: /docs/hiecm/v3/api/m2/errors
