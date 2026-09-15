# Pull Patient Health Information

`POST /api/care-context-link/patient/health-information/pull`

Asks the HIPs given to send the person's records. The data arrives later through the transfer endpoint.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/patient/health-information/pull \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hipIds": [
    "HIP001"
  ],
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `hipIds` (string[], required)
- `abhaAddress` (string, required)

## Responses

- `200`: No response body is documented for this request.
