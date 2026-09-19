# HIE-CM m3 build

Scaffolds an ABDM m3 integration one journey at a time. It covers raising a consent request, tracking it, and fetching the records it covers as an HIU.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

## Journeys

### Consent-management-data-flow (`m3-consent-management-data-flow-hiu`)

**Act: the calls in this journey, in order**

#### 1. Initiate the consent request (`m3_post_consent_v3_request_init`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "consent": {
    "purpose": {
      "text": "Care Management",
      "code": "CAREMGT",
      "refUri": "www.abc.com"
    },
    "patient": {
      "id": "<ABHA_ADDRESS>"
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
    "careContexts": [
      {
        "patientReference": "batman@tmh",
        "careContextReference": "Episode1"
      }
    ],
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
  }
}'
```

#### 2. Receive the consent request for patient HIU (`m3_post_v3_hiu_consent_request_on_init`)

Inbound to your bridge at `/api/v3/hiu/consent/request/on-init`. Acknowledge it and continue.

#### 3. Get consent request status (`m3_post_consent_v3_request_status`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "consentRequestId": "5f7a535d-a3fd-416b-b069-c97d021fbacd"
}'
```

#### 4. Receive the consent status request (`m3_post_v3_hiu_consent_request_on_status`)

Inbound to your bridge at `/api/v3/hiu/consent/request/on-status`. Acknowledge it and continue.

#### 5. Notify HIU when consent is APPROVED, DENIED or REVOKED (`m3_post_v3_hiu_consent_request_notify`)

Inbound to your bridge at `/api/v3/hiu/consent/request/notify`. Acknowledge it and continue.

#### 6. Acknowledge the consent notification (`m3_post_consent_v3_request_hiu_on_notify`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/hiu/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": [
    {
      "status": "OK",
      "consentId": "e3c74829-3f82-4f94-959e-e10f57bcd57b"
    }
  ],
  "error": {
    "code": "ABDM-1001",
    "message": "unable to connect database"
  },
  "response": {
    "requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"
  }
}'
```

#### 7. Fetch the consent details (`m3_post_consent_v3_fetch`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/fetch \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "consentId": "5f7a535d-a3fd-416b-b069-c97d021fbacd"
}'
```

#### 8. Receive the provide fetched consent artefact details to HIU (`m3_post_v3_hiu_consent_on_fetch`)

Inbound to your bridge at `/api/v3/hiu/consent/on-fetch`. Acknowledge it and continue.

#### 9. Submit the health information data request from HIU (`m3_post_data_flow_v3_health_information_request`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiRequest": {
    "consent": {
      "id": "18235d89-cb13-479d-ad71-7a57d5f669a8"
    },
    "dateRange": {
      "from": "2022-10-06T15:10:00.587Z",
      "to": "2022-11-06T15:10:00.587Z"
    },
    "dataPushUrl": "https://live.ndhm.gov.in/api-hiu/data/notification",
    "keyMaterial": {
      "cryptoAlg": "ECDH",
      "curve": "curve25519",
      "dhPublicKey": {
        "expiry": "2022-12-28T13:18:20.742Z",
        "parameters": "Ephemeral public key",
        "keyValue": "BFN7KTdOT0jIAExG2A8Jg+01wMPWxptiGqwHRVvtiVEsUq2FR7P2UdqZxJyPJSeR6muai21iQhasNxnhh8I5M+g="
      },
      "nonce": "28236d89-cb13-479d-ad71-7a57d5f669a9"
    }
  }
}'
```

#### 10. Receive the health information data request acknowledgement to HIU (`m3_post_v3_hiu_health_information_on_request`)

Inbound to your bridge at `/api/v3/hiu/health-information/on-request`. Acknowledge it and continue.

#### 11. Submit the notifications corresponding to events during data flow (`m3_post_data_flow_v3_health_information_notify`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "consentId": "18235d89-cb13-479d-ad71-7a57d5f669a8",
    "transactionId": "18235d89-cb13-479d-ad71-7a57d5f669a8",
    "doneAt": "2023-01-24T06:35:44.167Z",
    "notifier": {
      "type": "HIU",
      "id": "100005"
    },
    "statusNotification": {
      "sessionStatus": "RECEIVED",
      "hipId": "IN2810014366",
      "statusResponses": [
        {
          "careContextReference": "10004-20200001768-1",
          "hiStatus": "OK",
          "description": "Data received successfully"
        }
      ]
    }
  }
}'
```

#### 12. Get the current status of the health information request (`m3_get_data_flow_v3_health_information_request_status_tra_550104`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/request/status/{transaction-id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "transactionId": "18235d89-cb13-479d-ad71-7a57d5f669a8",
  "status": "TRANSFERRED"
}
```

## Where the detail is

- Every operation, with its body fields and responses: /docs/hiecm/v3/api/m3
- Error codes: /docs/hiecm/v3/api/m3/errors
