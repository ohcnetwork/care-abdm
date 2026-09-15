# nhcx-onsubscribe

`POST /nhcx/v1/hcx/notification/on_subscribe`

Callback confirming a subscription to National Health Claims Exchange notifications.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/nhcx/v1/hcx/notification/on_subscribe \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "payload": "<SUPABASE_SERVICE_ROLE_API_KEY_1A5M>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `payload` (string, required)

## Responses

- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
