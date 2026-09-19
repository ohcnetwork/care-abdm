# Request profile OTP

`POST /abha/api/v3/phr/app/login/profile/request/otp`

Flows in the Postman collection:
- P2-Management › P2 -PHR Profile › P2 - Update Email (optional) › Send OTP - Update Email
- P2-Management › P2 -PHR Profile › P2 - Update Mobile › Send OTP - Update Mobile
- P2-Management › P2 -PHR Profile › P2 - Link ABHA Number › P2 - via ABHA OTP › Send ABHA OTP - Link-DeLink
- P2-Management › P2 -PHR Profile › P2 - Link ABHA Number › P2 - via Aadhaar OTP › Send Aadhaar OTP - Link-DeLink

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/profile/request/otp \
  --header 'X-token: Bearer <JWT TOKEN>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-profile",
    "mobile-verify"
  ],
  "loginHint": "mobile-number",
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

## Headers

- `X-token` (string, required)
- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Body

- `scope` (string[])
- `loginHint` (string)
- `loginId` (string)
- `otpSystem` (string)

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
  "txnId": "d01cebdf-95f5-480c-8289-6f3b218e7248",
  "message": "OTP is sent to Mobile number ending with ******2425"
}
```
