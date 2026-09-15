# HIU On-Fetch (Consent Artefact Fetch Callback)

`POST /api/consent-management/consent/on-fetch`

Callback the gateway sends with a consent artefact the HIU asked to fetch, or the error that stopped it.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consent/on-fetch \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "requestId": "<GENERATED>",
  "timestamp": "<ISO_8601_TIMESTAMP>",
  "consent": {
    "status": "GRANTED",
    "consentDetail": {
      "consentId": "<consent-artefact-id>",
      "createdAt": "<ISO_8601_TIMESTAMP>",
      "patient": {
        "id": "<abha-address>@abdm"
      },
      "careContexts": [],
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT"
      },
      "hip": {
        "id": "<hip-id>"
      },
      "hiu": {
        "id": "<hiu-id>"
      },
      "consentManager": {
        "id": "sbx.abdm.gov.in"
      },
      "hiTypes": [
        "OPConsultation"
      ],
      "permission": {
        "accessMode": "VIEW",
        "dateRange": {
          "from": "2021-01-01T00:00:00.000Z",
          "to": "2023-12-31T23:59:59.999Z"
        },
        "dataEraseAt": "2024-12-31T23:59:59.999Z",
        "frequency": {
          "unit": "HOUR",
          "value": 1,
          "repeats": 0
        }
      }
    },
    "signature": "<signature>"
  },
  "resp": {
    "requestId": "<original-request-id>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `requestId` (string, required)
- `timestamp` (string, required)
- `consent` (object, required)
- `consent.status` (string, required)
- `consent.consentDetail` (object, required)
- `consent.consentDetail.consentId` (string, required)
- `consent.consentDetail.createdAt` (string, required)
- `consent.consentDetail.patient` (object, required)
- `consent.consentDetail.patient.id` (string, required)
- `consent.consentDetail.careContexts` (object[], required)
- `consent.consentDetail.purpose` (object, required)
- `consent.consentDetail.purpose.text` (string, required)
- `consent.consentDetail.purpose.code` (string, required)
- `consent.consentDetail.hip` (object, required)
- `consent.consentDetail.hip.id` (string, required)
- `consent.consentDetail.hiu` (object, required)
- `consent.consentDetail.hiu.id` (string, required)
- `consent.consentDetail.consentManager` (object, required)
- `consent.consentDetail.consentManager.id` (string, required)
- `consent.consentDetail.hiTypes` (string[], required)
- `consent.consentDetail.permission` (object, required)
- `consent.consentDetail.permission.accessMode` (string, required)
- `consent.consentDetail.permission.dateRange` (object, required)
- `consent.consentDetail.permission.dataEraseAt` (string, required)
- `consent.consentDetail.permission.frequency` (object, required)
- `consent.signature` (string, required)
- `resp` (object, required)
- `resp.requestId` (string, required)

## Responses

- `200`: No response body is documented for this request.
