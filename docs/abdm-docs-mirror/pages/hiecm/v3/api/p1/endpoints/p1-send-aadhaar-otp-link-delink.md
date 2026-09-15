# Send AADHAAR Otp - Link-DeLink

`POST /login/profile/request/otp`

Sends an Aadhaar OTP to authorise linking or delinking an ABHA number with the signed-in address. `loginId` is the encrypted Aadhaar.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/login/profile/request/otp \
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

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "<TXN_ID>",
  "message": "OTP is sent to Aadhaar registered mobile number ending with *******2425"
}
```
