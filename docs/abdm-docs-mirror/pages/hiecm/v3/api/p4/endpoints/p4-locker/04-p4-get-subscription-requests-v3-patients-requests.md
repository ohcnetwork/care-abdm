# Get all the consent and subscription requests with given filters

`GET /api/hiecm/subscription-requests/v3/patients/requests`

Retrieve all consent and subscription requests based on specified filters. By invoking this API, users can obtain a comprehensive list of requests that match the given criteria, including details about their status, scope, and any associated conditions. This functionality is essential for managing and tracking consent and subscription requests efficiently, ensuring that users have access to accurate and up-to-date information.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/patients/requests \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for tracking the end-to-end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds, and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Query parameters

- `consentLimit` (string, required): The consent limit - to limit records being fetched
- `consentOffset` (string, required): The consent offset - to skip the records before fetching the first record
- `subscriptionLimit` (string, required): The subscription limit - to limit records being fetched
- `subscriptionOffset` (string, required): The subscription offset - to skip the records before fetching the first record
- `status` (string, required): The status of the subscription and consent

## Responses

- `200`: OK
- `400`: Bad Request
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
- `404`: server cannot find the requested resource
- `500`: Internal Server Error
- `503`: Internal Server Error -> It is just one example, for every api the path will be changed.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

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
