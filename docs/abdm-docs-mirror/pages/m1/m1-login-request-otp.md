# Send a login OTP

`POST /v3/profile/login/request/otp`

Starts a login. `loginHint` selects what the person is identifying
themselves with: `mobile`, `aadhaar` or `abha-number`. As everywhere in
M1, `loginId` is encrypted rather than raw.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'BENEFIT_NAME: healthid api' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "<ENCRYPTED_MOBILE_NUMBER>",
  "otpSystem": "abdm"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `BENEFIT_NAME` (string): The benefit scheme an enrolment belongs to. Send `healthid api` on the enrol and search calls, and `healthid` on the login OTP and verify calls under Find ABHA. On the enrolment OTP request the header is present but explicitly disabled, so it is not sent there. NHA's files spell this header four different ways and use scheme values beyond healthid. Which spelling each endpoint accepts is not confirmed against the sandbox. The Conventions page for this module lists all four.

## Body

- `scope` (string[], required)
- `loginHint` (string, required)
- `loginId` (string, required)
- `otpSystem` (string, required)
- `txnId` (string)

## Responses

- `200`: The transaction id to carry into the next step, with a message.
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The error returned, with its code and message.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `404`: Resource not found
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Example 200 response:

```json
{
  "txnId": "<TXN_ID>",
  "message": "Transaction Id generated Successfully"
}
```
