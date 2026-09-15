# Init Consent Request

`POST /api/consent-management/consent/request/init`

Raises a consent request as a HIU: names the patient, the purpose, the record types and the period of care wanted.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consent/request/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "consent": {
    "purpose": {
      "text": "Care management",
      "code": "CAREMGT",
      "refUri": "www.abdm.gov.in"
    },
    "patient": {
      "id": "nithishjanithi@sbx"
    },
    "hiu": {
      "id": "IN0002222"
    },
    "hip": {
      "id": "wdwsd"
    },
    "careContexts": null,
    "requester": {
      "name": "<NAME>",
      "identifier": {
        "type": "REGNO1",
        "value": "MH1001",
        "system": "https://www.mciindia.9985"
      }
    },
    "hiTypes": [
      "Prescription"
    ],
    "permission": {
      "accessMode": "VIEW",
      "dateRange": {
        "from": "2023-05-09T08:58:09.738Z",
        "to": "2025-04-12T09:00:00.738Z"
      },
      "dataEraseAt": "2026-09-10T12:26:00.738Z",
      "frequency": {
        "unit": "HOUR",
        "value": 0,
        "repeats": 0
      }
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `consent` (object, required)
- `consent.purpose` (object, required)
- `consent.purpose.text` (string, required)
- `consent.purpose.code` (string, required)
- `consent.purpose.refUri` (string, required)
- `consent.patient` (object, required)
- `consent.patient.id` (string, required)
- `consent.hiu` (object, required)
- `consent.hiu.id` (string, required)
- `consent.hip` (object, required)
- `consent.hip.id` (string, required)
- `consent.careContexts` (null, required)
- `consent.requester` (object, required)
- `consent.requester.name` (string, required)
- `consent.requester.identifier` (object, required)
- `consent.requester.identifier.type` (string, required)
- `consent.requester.identifier.value` (string, required)
- `consent.requester.identifier.system` (string, required)
- `consent.hiTypes` (string[], required)
- `consent.permission` (object, required)
- `consent.permission.accessMode` (string, required)
- `consent.permission.dateRange` (object, required)
- `consent.permission.dateRange.from` (string, required)
- `consent.permission.dateRange.to` (string, required)
- `consent.permission.dataEraseAt` (string, required)
- `consent.permission.frequency` (object, required)
- `consent.permission.frequency.unit` (string, required)
- `consent.permission.frequency.value` (integer, required)
- `consent.permission.frequency.repeats` (integer, required)

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
