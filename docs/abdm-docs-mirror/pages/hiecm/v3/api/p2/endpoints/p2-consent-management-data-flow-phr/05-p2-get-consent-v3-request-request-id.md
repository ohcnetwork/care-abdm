# Get the consent request details by REQUEST-ID

`GET /api/hiecm/consent/v3/request/{request-id}`

Retrieve the details of a consent request using the REQUEST-ID. By invoking this API, users can obtain comprehensive information about a specific consent request, including its status, scope, and any associated conditions. This functionality is essential for ensuring that users have access to accurate and up-to-date consent information, supporting secure and compliant health information exchange. The API facilitates efficient management and verification of consent requests, enhancing the overall integrity of the consent management process.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/api/hiecm/consent/v3/request/{request-id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Path parameters

- `request-id` (string, required): The consent request id

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "requestId": "e5ec415f-c098-40f6-a0db-faa162fc5295",
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
  "status": "GRANTED",
  "createdAt": "2021-09-28T12:30:08.573Z",
  "lastUpdated": "2021-09-28T12:30:08.573Z",
  "hiType": [
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
```
