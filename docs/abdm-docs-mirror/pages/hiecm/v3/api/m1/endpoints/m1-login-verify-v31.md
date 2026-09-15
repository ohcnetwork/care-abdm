# Verify a login OTP, v3.1

`POST /v3.1/profile/login/verify`

The v3.1 counterpart of the login verification, on the `/abha/api/v3.1`
base path.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3.1/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify",
    "aadhaar-otp-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `scope` (string[], required)
- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `authData.otp` (object)
- `authData.otp.txnId` (string, required)
- `authData.otp.otpValue` (string, required)
- `authData.face_login` (object)
- `authData.face_login.aadhaar` (string, required)
- `authData.face_login.faceAuthPid` (string)
- `authData.face_login.txnId` (string)
- `authData.bio_login` (object)
- `authData.bio_login.aadhaar` (string, required)
- `authData.bio_login.fingerPrintAuthPid` (string, required)
- `authData.iris_login` (object)
- `authData.iris_login.aadhaar` (string, required)
- `authData.iris_login.irisAuthPid` (string, required)

## Responses

- `200`: Whether the login verified, with the user token and its expiry.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "<TXN_ID>",
  "authResult": "success",
  "message": "FACE verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<REFRESHTOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": [
    {
      "ABHANumber": "<ABHA_NUMBER>",
      "preferredAbhaAddress": "<ABHA_ADDRESS>",
      "name": "<NAME>",
      "status": "ACTIVE",
      "profilePhoto": "<BASE64_PHOTO>"
    }
  ]
}
```
