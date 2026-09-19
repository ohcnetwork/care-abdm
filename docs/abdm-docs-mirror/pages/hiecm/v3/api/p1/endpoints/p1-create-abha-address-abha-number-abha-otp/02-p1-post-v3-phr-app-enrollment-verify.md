# Verify the enrolment OTP

`POST /abha/api/v3/phr/app/enrollment/verify`

Flows in the Postman collection:
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via Mobile › OTP Verify - Mobile
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-ABHA OTP › OTP Verify - ABHA OTP
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-Aadhaar OTP › OTP Verify - AADHAR OTP

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/verify \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
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

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "1cba575d-02cd-40be-90e6-1e2edca88a88",
  "message": "OTP Verified Successfully",
  "authResult": "success",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "XX-XXXX-XXXX-1234",
      "status": "ACTIVE",
      "kycStatus": "VERIFIED"
    }
  ],
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<JWT TOKEN>",
    "refreshExpiresIn": 1296000
  }
}
```
