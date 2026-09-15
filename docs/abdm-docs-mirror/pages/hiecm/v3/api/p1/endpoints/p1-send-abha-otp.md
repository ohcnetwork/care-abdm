# Send ABHA OTP

`POST /profile/phr/request/otp`

Sends an OTP to the contact registered on the signed-in ABHA address, to authorise a profile change. `loginId` is encrypted.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/profile/phr/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "<SCOPE>"
  ],
  "loginHint": "<LOGIN_HINT>",
  "loginId": "<LOGIN_ID>",
  "otpSystem": "<OTP_SYSTEM>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `scope` (string[], required)
- `loginHint` (string, required)
- `loginId` (string, required)
- `otpSystem` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "<TXN_ID>",
  "message": "<MESSAGE>"
}
```
