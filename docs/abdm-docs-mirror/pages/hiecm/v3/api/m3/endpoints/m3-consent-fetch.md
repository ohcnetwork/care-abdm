# Fetch the full consent artefact

`POST /hiecm/consent/v3/fetch`

Also known as: Consent Fetch.
Fetches the full consent artefact for a given consent artefact ID.
Should be called after receiving the `on-notify` callback with status `GRANTED`.

The artefact contains:
- Exact care contexts approved
- HI types permitted
- Date range for data access
- Data erase date
- Digital signature for validation
- HIP and HIU identifiers

Store the artefact securely, it is required for the health information request.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/fetch \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "consentId": "consent-art-uuid-001"
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value. In M3 a single consent can produce several callbacks, so keep the mapping from request id to consent request id rather than relying on ordering.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production.
- `X-HIU-ID` (string, required): Identifier of the health information user the request or callback is intended for. This is per facility, and it is what a callback arriving at your one bridge URL is routed on. The bridge URL and your credentials belong to the integration, not to the facility.

## Body

- `consentId` (string, required): Consent artefact ID (from consentArtefacts array in on-notify or status)

## Responses

- `200`: Consent artefact details.
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Resource not found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "consent": {
    "status": "GRANTED",
    "consentDetail": {
      "consentId": "<CONSENT_ID>",
      "createdAt": "2026-08-24T10:15:30.000Z",
      "purpose": {
        "text": "<TEXT>",
        "code": "<CODE>"
      },
      "patient": {
        "id": "<ID>"
      },
      "careContexts": [
        {
          "patientReference": "<PATIENT_REFERENCE>",
          "careContextReference": "<CARE_CONTEXT_REFERENCE>"
        }
      ],
      "hiTypes": [
        "<HI_TYPES>"
      ],
      "permission": "<PERMISSION>",
      "hiu": {
        "id": "<ID>"
      },
      "hip": {
        "id": "<ID>"
      }
    },
    "signature": "<SIGNATURE>"
  }
}
```
