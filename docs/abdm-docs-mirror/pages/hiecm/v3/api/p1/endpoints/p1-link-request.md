# Link Request

`POST /profile/phr/link`

Links an ABHA number to the signed-in ABHA address, against a verified transaction.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/profile/phr/link \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "action": "<ACTION>",
  "transactionId": "<TRANSACTION_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `action` (string, required)
- `transactionId` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "<MESSAGE>",
  "authResult": "<AUTH_RESULT>"
}
```
