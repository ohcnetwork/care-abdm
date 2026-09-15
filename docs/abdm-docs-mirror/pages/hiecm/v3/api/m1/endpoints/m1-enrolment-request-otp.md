# Send an OTP to begin or continue an enrolment

`POST /v3/enrollment/request/otp`

The first call of most enrolment flows, and the one people reuse without
noticing. What it does depends on `scope` and `loginHint`.

Starting an enrolment: `scope` is `["abha-enrol"]`, `loginHint` is
`aadhaar`, `loginId` is the encrypted Aadhaar number and `otpSystem` is
`aadhaar`. The OTP goes to the mobile registered with Aadhaar.

Verifying a mobile or email afterwards: `scope` gains `mobile-verify` or
`email-verify`, `otpSystem` becomes `abdm`, and you pass the `txnId` from
the enrolment you are continuing.

`loginId` is encrypted, never the raw value. Encrypt it against the ABDM
public key first.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol"
  ],
  "loginHint": "aadhaar",
  "loginId": "_encrypted_12_digit_aadhaar_no_",
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
- `txnId` (string)

## Responses

- `200`: The transaction id to carry into the next step, with a message.
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
