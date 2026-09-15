# Public-Health-Lockers-Subscribe

`POST /health-locker/lockers/subscribe`

Subscribes the person to a health locker, so their new records are shared with it automatically.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/health-locker/lockers/subscribe \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "consentAutoApprovalId": "<TXN_ID>"
}
```
