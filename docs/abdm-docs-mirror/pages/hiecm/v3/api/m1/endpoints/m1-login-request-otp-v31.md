# Send a login OTP, v3.1

`POST /v3.1/profile/login/request/otp`

The v3.1 variant of the login OTP request. It sits on a different base
path from the rest of M1, `/abha/api/v3.1` rather than `/abha/api/v3`,
which is why the version appears in the path here.

Use v3 by default. v3.1 is used for Aadhaar OTP and biometric login.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3.1/profile/login/request/otp \
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
  "loginHint": "aadhaar",
  "loginId": "<ENCRYPTED_AADHAAR_NUMBER>",
  "otpSystem": "aadhaar"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `scope` (string[], required)
- `loginHint` (string, required)
- `loginId` (string, required)
- `otpSystem` (string, required)

## Responses

- `200`: The specification does not describe this body. Send the call with Try it to see what comes back.
