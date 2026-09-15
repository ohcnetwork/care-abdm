# AS - RecordShare

`POST /scan-share/record-share/share`

Shares selected records with a facility after scanning its counter QR code.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/scan-share/record-share/share \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
