# Verify OTP / Biometric for ABHA Address Login

`POST /phr/web/login/abha/verify`

Complete the ABHA Address login with OTP or biometric.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/phr/web/login/abha/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
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
      "txnId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "otpValue": "{{RSA_encrypted_otp}}"
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
- `authData.bio` (object)
- `authData.bio.txnId` (string)
- `authData.bio.bioType` (string) One of: FMR.
- `authData.bio.pid` (string)
- `authData.face` (object)
- `authData.face.txnId` (string)
- `authData.face.pid` (string)
- `authData.iris` (object)
- `authData.iris.txnId` (string)
- `authData.iris.pid` (string)

## Responses

- `200`: Login successful
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized, missing, invalid, or expired Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "token": "<TOKEN>",
  "refreshToken": "<REFRESH_TOKEN>",
  "expiresIn": 0,
  "refreshExpiresIn": 0,
  "accounts": "<ACCOUNTS>"
}
```
