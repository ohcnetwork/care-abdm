# on_check

`POST /nhcx/v1/coverageeligibility/on_check`

Callback carrying the payer's answer to a coverage eligibility check.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/nhcx/v1/coverageeligibility/on_check \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "type": "JWEPayload",
  "payload": ""
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `type` (string, required)
- `payload` (string, required)

## Responses

- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
