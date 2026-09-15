# Acknowledge a consent notification, as the HIP

`POST /hiecm/consent/v3/request/hip/on-notify`

Also known as: Consent HIP On-Notify.
**Async Callback:** After ABDM Gateway sends a consent grant notification to the HIP bridge URL
(`{bridgeUrl}/v0.5/consents/hip/notify`), the HIP calls this Gateway endpoint to
acknowledge receipt of the consent artefact.

The consent notification contains the full consent details including care contexts,
HI types, date range, and digital signature for validation.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/hip/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "OK",
    "consentId": "consent-art-uuid-001"
  },
  "response": {
    "requestId": "req-uuid-from-hip-notify"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Body

- `acknowledgement` (object, required)
- `acknowledgement.status` (string, required) One of: OK, ERROR.
- `acknowledgement.consentId` (string, required): The consent artefact ID being acknowledged
- `response` (object, required): Echo of the requestId from the original Gateway-to-HIP request
- `response.requestId` (string, required): requestId received in the original Gateway request to HIP bridge

## Responses

- `202`: Consent acknowledgement accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
