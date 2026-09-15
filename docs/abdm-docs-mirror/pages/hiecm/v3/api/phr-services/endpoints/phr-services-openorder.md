# OPENORDER

`POST /scan-pay/open-order`

Opens a scan and pay order after the person scans a facility's payment counter QR code.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/scan-pay/open-order \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
