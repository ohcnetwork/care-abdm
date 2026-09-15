# subscribe

`POST /nhcx/v1/notification/subscribe`

Subscribes the PHR to National Health Claims Exchange notifications. Confirmation arrives at `on_subscribe`.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/nhcx/v1/notification/subscribe \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
