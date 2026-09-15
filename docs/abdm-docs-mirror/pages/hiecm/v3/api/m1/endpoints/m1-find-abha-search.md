# Find an ABHA for somebody who does not know theirs

`POST /v3/profile/account/abha/search`

Takes an encrypted mobile number, Aadhaar number or biometric result and
sends an OTP to the mobile on record. The response carries a `txnId` and
a message naming the masked mobile the OTP went to, so the person can
confirm it is theirs before waiting for it.

Two shapes are documented for the response: an array, which fits one
mobile number mapping to several accounts, and a single object. The
single-object example carries a URL of `profile/login/request/otp`,
so it likely describes a different endpoint. Expect an array, and
treat the single object as unconfirmed.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'BENEFIT_NAME: healthid api' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search-abha"
  ],
  "mobile": "<MOBILE>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `BENEFIT_NAME` (string): The benefit scheme an enrolment belongs to. Send `healthid api` on the enrol and search calls, and `healthid` on the login OTP and verify calls under Find ABHA. On the enrolment OTP request the header is present but explicitly disabled, so it is not sent there. A login OTP request sent with `healthid api` rather than `healthid` was accepted on the sandbox on 2026-09-11, so the login calls may take either. NHA's files spell this header four different ways and use scheme values beyond healthid. Which spelling each endpoint accepts is not confirmed against the sandbox. The Conventions page for this module lists all four.

## Body

- `scope` (string[], required)
- `mobile` (string, required)

## Responses

- `200`: Two shapes are documented; the array is the more likely of the two.
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized, missing, invalid, or expired Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `404`: Resource not found
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "txnId": "<TXN_ID>",
    "message": "OTP is sent to Mobile number ending with ******0161"
  }
]
```
