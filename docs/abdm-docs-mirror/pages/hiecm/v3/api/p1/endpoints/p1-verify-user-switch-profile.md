# Verify User Switch Profile

`POST /profile/phr/verify/switch-profile/user`

Completes a profile switch: selects the ABHA address to continue as and returns its session tokens.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/profile/phr/verify/switch-profile/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "txnId": "<TXN_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `abhaAddress` (string, required)
- `txnId` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "token": "<TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<REFRESHTOKEN>",
  "refreshExpiresIn": 1296000
}
```
