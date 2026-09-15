# Fetch Health Information Status

`POST /api/care-context-link/patient/health-information/status`

Returns the transfer status for the transaction ids given.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/patient/health-information/status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionIds": [
    "txn-001",
    "txn-002"
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `transactionIds` (string[], required)

## Responses

- `200`: No response body is documented for this request.
