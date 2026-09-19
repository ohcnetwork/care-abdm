# HIE-CM p4 build

Scaffolds an ABDM p4 integration one journey at a time. It covers setting up a health locker and listing the lockers and requests on an ABHA address.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

## Journeys

### Locker (`p4-locker`)

**Act: the calls in this journey, in order**

#### 1. Setup health locker for a patient (`p4_post_subscription_requests_v3_setup_locker`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/setup-locker \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'X-LOCKER-ID: <X_LOCKER_ID>'
```

#### 2. Get the subscription requests patients lockers (`p4_get_subscription_requests_v3_patients_lockers`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/patients/lockers \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

#### 3. Get health locker settings of a patient by locker ID (`p4_get_subscription_requests_v3_patients_lockers_lockerid`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/patients/lockers/{lockerId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

#### 4. Get all the consent and subscription requests with given filters (`p4_get_subscription_requests_v3_patients_requests`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/patients/requests \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "consents": {
    "size": 10,
    "limit": 10,
    "offset": 0,
    "requests": [
      {
        "requestId": "e5ec415f-c098-40f6-a0db-faa162fc5295",
        "createdAt": "2021-09-28T12:30:08.573Z",
        "lastUpdated": "2021-09-28T12:30:08.573Z",
        "status": "GRANTED",
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
        "careContexts": [
          {
            "patientReference": "batman@tmh",
            "careContextReference": "Episode1"
          }
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
    ]
  },
  "subscriptions": {
    "limit": 5,
    "size": 0,
    "offset": 5,
    "requests": [
      {
        "id": "1234",
        "requestId": "f29f0e59-8388-4698-9fe6-05db67aeac46",
        "subscriptionId": "f29f0e59-8388-4698-9fe6-05db67aeac46",
        "patient": {
          "id": "<ABHA_ADDRESS>"
        },
        "purpose": {
          "text": "Care Management",
          "code": "CAREMGT",
          "refUri": "https://abc.def.in"
        },
        "hiu": {
          "id": "INDIA_HIU",
          "name": "INDIA HIU",
          "type": "HIU"
        },
        "hips": [
          {
            "id": "INDIA_HIP",
            "name": "INDIA HIP",
            "type": "HIP"
          }
        ],
        "categories": [
          "LINK"
        ],
        "period": {
          "from": "2024-05-09T10:34:00.389Z",
          "to": "2024-05-09T10:34:00.389Z"
        },
        "createdAt": "2024-05-09T10:34:00.389Z",
        "lastUpdated": "2024-05-09T10:34:00.389Z",
        "status": "GRANTED",
        "requestType": "HEALTH_LOCKER"
      }
    ]
  }
}
```

## Where the detail is

- Every operation, with its body fields and responses: /docs/hiecm/v3/api/p4
