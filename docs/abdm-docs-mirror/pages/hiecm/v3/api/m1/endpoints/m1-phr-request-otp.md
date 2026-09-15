# Send OTP for ABHA Address Login

`POST /phr/web/login/abha/request/otp`

Send OTP to login via ABHA Address.

| scope | loginHint | Method |
|-------|-----------|--------|
| `["abha-address-login","mobile-verify"]` | `abha-address` | Mobile OTP |
| `["abha-address-login","aadhaar-verify"]` | `abha-address` | Aadhaar OTP |
| `["abha-login","aadhaar-bio-verify"]` | `abha-address` | Fingerprint |
| `["abha-login","aadhaar-face-verify"]` | `abha-address` | Face |
| `["abha-login","aadhaar-iris-verify"]` | `abha-address` | Iris |

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/phr/web/login/abha/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "mobile-verify"
  ],
  "loginHint": "abha-address",
  "loginId": "{{RSA_encrypted_abha_address}}",
  "otpSystem": "abdm, aadhaar"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `scope` (string[], required)
- `loginHint` (string, required) One of: abha-address.
- `loginId` (string, required): RSA-encrypted ABHA Address
- `otpSystem` (string, required): Which identity system the loginId is encrypted for. Example values include `abdm` and `aadhaar`.

## Responses

- `200`: OTP sent
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
  "txnId": "<TXN_ID>",
  "message": "<MESSAGE>"
}
```
