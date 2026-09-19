# Login profile verify

`POST /abha/api/v3/phr/app/login/profile/verify`

Flows in the Postman collection:
- P2-Management › P2 -PHR Profile › P2 - Update Email (optional) › Verify OTP - Update Email
- P2-Management › P2 -PHR Profile › P2 - Update Mobile › Verify OTP - Update Mobile
- P2-Management › P2 -PHR Profile › P2 - Update Password › Verify Password - Update Password
- P2-Management › P2 -PHR Profile › P2 - Link ABHA Number › P2 - via ABHA OTP › Verify ABHA OTP - Link-DeLink
- P2-Management › P2 -PHR Profile › P2 - Link ABHA Number › P2 - via Aadhaar OTP › Verify Aadhaar OTP - Link-DeLink

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/profile/verify \
  --header 'X-token: Bearer <JWT TOKEN>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "<BASE64_PHOTO>"
    }
  }
}'
```

## Headers

- `X-token` (string, required)
- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Body

- `scope` (string[])
- `authData` (object)
- `authData.authMethods` (string[])
- `authData.otp` (object)
- `authData.otp.txnId` (string)
- `authData.otp.otpValue` (string)
- `authData.password` (object)
- `authData.password.abhaAddress` (string)
- `authData.password.password` (string)

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "e10ca603-97f5-4cf2-8191-d51ea7db3845",
  "message": "Entered OTP is incorrect. Kindly re-enter valid OTP.",
  "authResult": "failed",
  "users": []
}
```
