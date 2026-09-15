# call-back on-discovery

`POST /user-initiated-linking/link/on-discover`

Callback the gateway sends with the care contexts discovered at the HIP, or the error that stopped discovery.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/user-initiated-linking/link/on-discover \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "<TXN_ID>",
  "error": {
    "code": "ABDM-1010",
    "message": "Patient not found"
  },
  "response": {
    "requestId": "<TXN_ID>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `transactionId` (string, required)
- `error` (object, required)
- `error.code` (string, required)
- `error.message` (string, required)
- `response` (object, required)
- `response.requestId` (string, required)

## Responses

- `200`: No response body is documented for this request.
