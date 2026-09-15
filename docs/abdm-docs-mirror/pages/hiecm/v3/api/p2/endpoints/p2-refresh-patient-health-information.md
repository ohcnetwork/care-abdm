# Refresh Patient Health Information

`POST /api/care-context-link/patient/health-information/refresh`

Asks the HIPs given to send any records added since the last transfer.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/patient/health-information/refresh \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hipIds": [
    "HIP001",
    "HIP002"
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `hipIds` (string[], required)

## Responses

- `200`: No response body is documented for this request.
