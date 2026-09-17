# Link or unlink a benefit record from an ABHA

`POST /v3/profile/benefit/linkAndDelink`

One call does both directions. The success response names the
scheme and confirms the link in a human readable `status` string rather
than a code, so match on the HTTP status and the scheme, not on that
text.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/linkAndDelink \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'BENEFIT_NAME: healthid api' \
  --header 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "link"
  ],
  "loginHint": "abha-number",
  "loginId": "<RSA_ENCRYPTED_ABHA_NUMBER>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `BENEFIT_NAME` (string): The benefit scheme an enrolment belongs to. Send `healthid api` on the enrol and search calls, and `healthid` on the login OTP and verify calls under Find ABHA. On the enrolment OTP request the header is present but explicitly disabled, so it is not sent there. A login OTP request sent with `healthid api` rather than `healthid` was accepted on the sandbox on 2026-09-11, so the login calls may take either. NHA's files spell this header four different ways and use scheme values beyond healthid. Which spelling each endpoint accepts is not confirmed against the sandbox. The Conventions page for this module lists all four.
- `X-token` (string): The user scoped token returned when a person logs in or verifies an OTP. Profile calls act on one account, so they need this in addition to the gateway token. Required on the calls that read or change a specific person's account. Send the bare token. Unlike the Authorization header this one carries no `Bearer ` prefix, and adding one is refused as `ABDM-1094` with the message `X-token expired`. That message names the wrong thing: a token rejected one second after it was issued has not expired, it was malformed. Check the prefix before the lifetime.

## Body

- `scope` (string[], required): The direction. Send `["de-link"]` to de-link and `["link"]` to link. Note the hyphen in `de-link`.
- `loginHint` (string): How the account is identified when the call is not made with an X-token: the recorded variants send `abha-number` or `xmlUid`. Absent on the X-token variant.
- `loginId` (string): The identifier named by `loginHint`, RSA encrypted against the ABDM public key, never raw. Present only alongside `loginHint`.

## Responses

- `200`: The benefit link status for the ABHA.
- `400`: The error returned, with its code and message.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The error returned, with its code and message.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "benefitName": "healthid api",
  "healthId": "<ABHA_ADDRESS>",
  "status": "Benefit record has been linked successfully"
}
```
