# Request artefact by REQUEST-ID

`GET /api/hiecm/consent/v3/artefact/request/{request-id}`

Fetch all consent artefact details associated with a specific consent REQUEST-ID. By invoking this API, users can retrieve comprehensive information about all consent artefacts linked to the given REQUEST-ID, including their status, scope, and any associated conditions. This functionality is essential for ensuring that users have access to accurate and up-to-date consent artefact information, supporting secure and compliant health information exchange. The API facilitates efficient management and verification of consent artefacts, enhancing the overall integrity of the consent management process.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/api/hiecm/consent/v3/artefact/request/{request-id} \
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

- `request-id` (string, required): Consent request id

## Responses

- `200`: Ok
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
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
[
  {
    "status": "GRANTED",
    "consentDetail": {
      "consentId": "e5ec415f-c098-40f6-a0db-faa162fc5295",
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
      "createdAt": "2021-09-28T12:30:08.573Z",
      "lastUpdated": "2021-09-28T12:30:08.573Z",
      "schemaVersion": "v3",
      "consentManager": {
        "id": "abdm"
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
    "signature": "Signature of CM as defined in W3C standards; Base64 encoded"
  }
]
```
