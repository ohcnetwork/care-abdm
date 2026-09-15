# Request a patient's health information

`POST /hiecm/data-flow/v3/health-information/request`

Also known as: HIU Health Information Request.
Requests health data from the HIP for a specific consent artefact.

The HIU must:
1. Generate an ECDH key pair before this call
2. Pass the ECDH public key in `keyMaterial.dhPublicKey`
3. Expose a `dataPushUrl` endpoint that can receive encrypted FHIR data from the HIP

The HIP encrypts data using the HIU's public key (ECDH shared secret) and pushes
it to `dataPushUrl`. The HIU decrypts using its private key + HIP's public key
from the push request's `keyMaterial`.

**Supported ECDH curves:** `Curve25519`
**Supported crypto algorithms:** `ECDH`

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiRequest": {
    "consent": {
      "id": "consent-art-uuid-001"
    },
    "dateRange": {
      "from": "2023-01-01T00:00:00.000Z",
      "to": "2024-01-01T00:00:00.000Z"
    },
    "dataPushUrl": "https://your-hiu-server.com/abdm/data/push",
    "keyMaterial": {
      "cryptoAlg": "ECDH",
      "curve": "Curve25519",
      "dhPublicKey": {
        "expiry": "2024-12-31T00:00:00.000Z",
        "parameters": "Curve25519/32byte",
        "keyValue": "base64-encoded-hiu-ecdh-public-key"
      },
      "nonce": "base64-encoded-random-nonce-32bytes"
    }
  }
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

- `hiRequest` (object, required)
- `hiRequest.consent` (object, required)
- `hiRequest.consent.id` (string, required): Consent artefact ID from the granted consent
- `hiRequest.dateRange` (object, required)
- `hiRequest.dateRange.from` (string, required): Must be within the consent's permitted date range
- `hiRequest.dateRange.to` (string, required)
- `hiRequest.dataPushUrl` (string, required): HTTPS endpoint on the HIU server to receive encrypted FHIR data
- `hiRequest.keyMaterial` (object, required)

## Responses

- `202`: Health information request accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 202 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "transactionId": "<TRANSACTION_ID>"
}
```
