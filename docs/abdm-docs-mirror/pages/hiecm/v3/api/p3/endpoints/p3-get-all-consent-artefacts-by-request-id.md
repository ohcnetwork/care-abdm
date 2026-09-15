# Get All Consent Artefacts by Request ID

`GET /api/consent-management/consent-requests/{consentRequestId}/consent-artefacts`

Lists the consent artefacts created when a request was approved, one per HIP.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consent-requests/{consentRequestId}/consent-artefacts \
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
[
  {
    "status": "REVOKED",
    "consentDetail": {
      "schemaVersion": "v3",
      "consentId": "<TXN_ID>",
      "createdAt": "2026-06-05T05:49:30.893Z",
      "lastUpdated": "2026-06-05T05:59:33.037Z",
      "patient": {
        "id": "nithishjanithi@sbx"
      },
      "careContexts": [
        {
          "patientReference": "nithishjanithi@sbx",
          "careContextReference": "25ac532f-178d-5885-9bcb-b82052f345eb_20260428112424637418"
        }
      ],
      "purpose": {
        "text": "Care management",
        "code": "CAREMGT",
        "refUri": "www.abdm.gov.in"
      },
      "hip": {
        "id": "wdwsd"
      },
      "hiu": {
        "id": "IN0002222"
      },
      "consentManager": {
        "id": "sbx"
      },
      "requester": {
        "name": "<NAME>",
        "identifier": {
          "value": "MH1001",
          "type": "REGNO1",
          "system": "https://www.mciindia.9985"
        }
      },
      "hiTypes": [
        "OPConsultation"
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
    },
    "signature": "tY9rOuZomDEo3ihjgjiOl92dgQ1wjzBQa4ogJYlLl7BZFAO3IiR6k8p9qcd30eYgBc1xyPEPied6nDrdPwT6oD2mAso/ny6Ykcto3uU/1nViYH7K/H9/XVEoo4hyOPKb62aGUqMn69QpWNhPM9HTnhtj3CXOjB6TA2eFkHYYbaniX02W/6ALtuPb0OsUchlImVbjj1EBlCK4Xs8GrtAnneU2esnMWR7N0ra9bnyR6zF5Bi2ng/pDLTIeKC3wfVKg4AGUC6obC7FCRrykAUlpgWMM4wBbiV7Y1oLPcJ4VFL7DSUdtilGbW53ez0Av4cKlVizRxZ9gWvw2kWQBa2iL/w=="
  }
]
```
