# Login PHR verify

`POST /abha/api/v3/phr/app/login/verify`

Flows in the Postman collection:
- P1-Registration-login › P1 - PHR Login › P1 - Login via Mobile Number › Login OTP Verify - Mobile
- P1-Registration-login › P1 - PHR Login › P1 - Login via Email (optional) › Login OTP Verify - Email
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Address - Mobile OTP › Login OTP Verify - ABHAADDRES Mobile
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Number-Aadhaar OTP › Login OTP Verify - AADHAR
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Number-ABHA OTP › Login OTP Verify - ABHA
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Address - Password › Login Verify - Password
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Address - Email OTP › Login OTP Verify - ABHAADDRESS Email
- P1-Registration-login › P1 - PHR Login › P1 - Login via Aadhaar- OTP › new OTP verify- Aadhaar

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

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
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "b81a963d-4b97-48b4-9f9f-acf9f13afab7",
  "message": "OTP verified successfully",
  "authResult": "success",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "VERIFIED"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    },
    "... 1 more of the same shape"
  ],
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": null,
    "refreshExpiresIn": null
  }
}
```
