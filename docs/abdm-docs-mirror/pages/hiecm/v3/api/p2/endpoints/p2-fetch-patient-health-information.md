# Fetch Patient Health Information

`POST /api/care-context-link/patient/health-information/fetch`

Fetches the health information received for the request ids given, with paging.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/patient/health-information/fetch \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "requestIds": [
    "req-001",
    "req-002"
  ],
  "limit": 10,
  "offset": 0
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `requestIds` (string[], required)
- `limit` (integer, required)
- `offset` (integer, required)

## Responses

- `200`: No response body is documented for this request.
