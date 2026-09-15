# on_submit

`POST /nhcx/v1/search/on_submit`

Callback carrying the payer's answer to a policy search.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/nhcx/v1/search/on_submit \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "type": "<TYPE>",
  "payload": "<PAYLOAD>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `type` (string, required)
- `payload` (string, required)

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
