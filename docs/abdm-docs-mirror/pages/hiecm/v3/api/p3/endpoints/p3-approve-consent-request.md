# Approve Consent Request

`POST /api/consent-management/consent-requests/{consentRequestId}/approve`

Approves a consent request. `consents` names the HIPs and care contexts the person is granting, and the artefact ids come back.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consent-requests/{consentRequestId}/approve \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "consents": [
    {
      "hiTypes": [
        "OPConsultation"
      ],
      "hip": {
        "id": "wdwsd"
      },
      "careContexts": [
        {
          "patientReference": "nithishjanithi@sbx",
          "careContextReference": "25ac532f-178d-5885-9bcb-b82052f345eb_20260428112424637418"
        }
      ],
      "permission": {
        "accessMode": "VIEW",
        "dateRange": {
          "from": "2023-05-09T08:58:09.738Z",
          "to": "2025-04-12T09:00:00.738Z"
        },
        "dataEraseAt": "2026-09-12T13:26:00.738Z",
        "frequency": {
          "unit": "HOUR",
          "value": 0,
          "repeats": 0
        }
      }
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `consentRequestId` (string, required): Passed as a path segment.

## Body

- `consents` (object[], required)
- `consents.hiTypes` (string[], required)
- `consents.hip` (object, required)
- `consents.hip.id` (string, required)
- `consents.careContexts` (object[], required)
- `consents.careContexts.patientReference` (string, required)
- `consents.careContexts.careContextReference` (string, required)
- `consents.permission` (object, required)
- `consents.permission.accessMode` (string, required)
- `consents.permission.dateRange` (object, required)
- `consents.permission.dateRange.from` (string, required)
- `consents.permission.dateRange.to` (string, required)
- `consents.permission.dataEraseAt` (string, required)
- `consents.permission.frequency` (object, required)
- `consents.permission.frequency.unit` (string, required)
- `consents.permission.frequency.value` (integer, required)
- `consents.permission.frequency.repeats` (integer, required)

## Responses

- `200`: Example values, scrubbed.
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "<MESSAGE>",
  "consentIds": [
    {
      "id": "<ID>"
    }
  ],
  "error": {
    "code": "<CODE>",
    "message": "<MESSAGE>"
  }
}
```
