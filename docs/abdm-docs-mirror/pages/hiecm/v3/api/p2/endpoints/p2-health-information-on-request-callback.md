# Health Information On-Request Callback

`POST /api/care-context-link/health-information/on-request`

Callback the gateway sends after a health information request: the transaction id for the transfer, or the error that stopped it.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/health-information/on-request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "requestId": "<GENERATED>",
  "timestamp": "2026-06-12T00:00:00.000Z",
  "hiRequest": {
    "transactionId": "txn-001",
    "sessionStatus": "ACKNOWLEDGED"
  },
  "error": null,
  "resp": {
    "requestId": "<REQUEST_ID>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `requestId` (string, required)
- `timestamp` (string, required)
- `hiRequest` (object, required)
- `hiRequest.transactionId` (string, required)
- `hiRequest.sessionStatus` (string, required)
- `error` (null, required)
- `resp` (object, required)
- `resp.requestId` (string, required)

## Responses

- `200`: No response body is documented for this request.
