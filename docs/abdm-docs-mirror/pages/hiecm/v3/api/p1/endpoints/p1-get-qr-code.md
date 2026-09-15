# Get QR Code

`GET /profile/phr/qr-code`

Returns the QR code that encodes the person's ABHA address, for scanning at a facility.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/profile/phr/qr-code \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
