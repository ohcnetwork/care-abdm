# Acknowledge a health information data request

`POST /hiecm/data-flow/v3/health-information/hip/on-request`

Also known as: HIP Health Information Response.
**Async Callback:** After ABDM Gateway sends a health information request to the HIP bridge URL
(`{bridgeUrl}/v0.5/health-information/hip/request`), the HIP calls this Gateway endpoint to
acknowledge receipt and indicate it will begin processing (ACKNOWLEDGED).

After this, the HIP prepares and encrypts FHIR records, then pushes them to the HIU's `dataPushUrl`.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/hip/on-request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiRequest": {
    "transactionId": "txn-uuid-data-001",
    "sessionStatus": "ACKNOWLEDGED"
  },
  "response": {
    "requestId": "req-uuid-from-hi-request"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Body

- `hiRequest` (object, required)
- `hiRequest.transactionId` (string, required): Transaction ID from the original data request
- `hiRequest.sessionStatus` (string, required) One of: ACKNOWLEDGED, ERRORED.
- `response` (object, required): Echo of the requestId from the original Gateway-to-HIP request
- `response.requestId` (string, required): requestId received in the original Gateway request to HIP bridge

## Responses

- `202`: Health information request acknowledgement accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
