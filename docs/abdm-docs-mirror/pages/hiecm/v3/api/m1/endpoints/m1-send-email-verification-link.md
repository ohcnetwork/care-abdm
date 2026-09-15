# Send Email Verification Link

`POST /profile/account/request/emailVerificationLink`

Send a one-click email verification link. The user clicks it to verify their email, no OTP required.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/profile/account/request/emailVerificationLink \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-Token: <X_TOKEN>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "email-link-verify"
  ],
  "loginHint": "email",
  "loginId": "{{RSA_encrypted_email}}",
  "otpSystem": "abdm, aadhaar"
}'
```

## Authorization

- `Authorization` (bearer token, required): JWT Bearer token from `POST /api/hiecm/gateway/v3/sessions`. Header: `Authorization: Bearer {accessToken}`
- `X-Token` (apiKey, required): Short-lived session token returned in login/verify responses. Required for all `/profile/account/*` operations. Header: `X-Token: {token}`

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `scope` (string[], required)
- `loginHint` (string, required) One of: email.
- `loginId` (string, required): RSA-encrypted email address
- `otpSystem` (string, required): Which identity system the loginId is encrypted for. Example values include `abdm` and `aadhaar`.

## Responses

- `200`: Verification link sent to email
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
  "message": "<MESSAGE>"
}
```
