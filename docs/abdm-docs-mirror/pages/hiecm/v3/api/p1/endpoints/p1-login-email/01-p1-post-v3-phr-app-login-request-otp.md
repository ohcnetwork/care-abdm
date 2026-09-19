# Login request OTP

`POST /abha/api/v3/phr/app/login/request/otp`

Flows in the Postman collection:
- P1-Registration-login › P1 - PHR Login › P1 - Login via Mobile Number › OTP Request - Mobile
- P1-Registration-login › P1 - PHR Login › P1 - Login via Email (optional) › OTP Request - Email
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Address - Mobile OTP › OTP Request - ABHAADDRES Mobile
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Number-Aadhaar OTP › OTP Request - AADHAR OTP
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Number-ABHA OTP › OTP Request - ABHA OTP
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Address - Email OTP › OTP Request - ABHAADDRES Email
- P1-Registration-login › P1 - PHR Login › P1 - Login via Aadhaar- OTP › new OTP Request- Aadhaar

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "email-verify"
  ],
  "loginHint": "email",
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

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
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "b81a963d-4b97-48b4-9f9f-acf9f13afab7",
  "message": "OTP is sent to Mobile number ending with ******2425"
}
```
