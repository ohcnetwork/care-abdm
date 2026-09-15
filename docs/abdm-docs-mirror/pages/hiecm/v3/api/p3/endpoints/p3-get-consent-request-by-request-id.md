# Get Consent Request by Request ID

`GET /api/consent-management/consent-requests/{consentRequestId}`

Returns one consent request: who is asking, for what purpose, which record types, and its current status.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consent-requests/{consentRequestId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `consentRequestId` (string, required): Passed as a path segment.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "requestId": "<TXN_ID>",
  "createdAt": "2026-04-28T05:54:26.374Z",
  "lastUpdated": "2026-04-28T05:54:26.449Z",
  "status": "GRANTED",
  "purpose": {
    "text": "Care Management",
    "code": "CAREMGT",
    "refUri": "www.abdm.gov.in"
  },
  "patient": {
    "id": "nithishjanithi@sbx"
  },
  "hip": {
    "id": "DigiLocker_NEGD"
  },
  "hiu": {
    "id": "DigiLocker_NEGD"
  },
  "requester": {
    "name": "<NAME>",
    "identifier": {
      "value": "SELF",
      "type": "SELF",
      "system": "nithishjanithi@sbx"
    }
  },
  "hiTypes": [
    "DiagnosticReport"
  ],
  "careContexts": [
    {
      "patientReference": "nithishjanithi@sbx",
      "careContextReference": "25ac532f-178d-5885-9bcb-b82052f345eb_20260428112424637418"
    }
  ],
  "permission": {
    "accessMode": "VIEW",
    "dateRange": {
      "from": "2026-04-27T09:54:25.533Z",
      "to": "2026-04-28T05:54:25.533Z"
    },
    "dataEraseAt": "2036-04-28T11:24:25.533Z",
    "frequency": {
      "unit": "YEAR",
      "value": 1,
      "repeats": 1
    }
  }
}
```
