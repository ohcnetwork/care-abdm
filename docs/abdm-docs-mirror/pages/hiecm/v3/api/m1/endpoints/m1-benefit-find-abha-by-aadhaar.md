# Find an ABHA number from an Aadhaar number

`GET /v3/profile/benefit/search/abhaByAadhaar`

A benefit scheme lookup, not a general search. The Aadhaar value is
encrypted.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/search/abhaByAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'BENEFIT_NAME: healthid api' \
  --header 'aadhaarNumber: <RSA_ENCRYPTED_AADHAAR_NUMBER>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `BENEFIT_NAME` (string): The benefit scheme an enrolment belongs to. Send `healthid api` on the enrol and search calls, and `healthid` on the login OTP and verify calls under Find ABHA. On the enrolment OTP request the header is present but explicitly disabled, so it is not sent there. A login OTP request sent with `healthid api` rather than `healthid` was accepted on the sandbox on 2026-09-11, so the login calls may take either. NHA's files spell this header four different ways and use scheme values beyond healthid. Which spelling each endpoint accepts is not confirmed against the sandbox. The Conventions page for this module lists all four.
- `aadhaarNumber` (string, required): The person's Aadhaar number, RSA encrypted against the ABDM public key and sent as a header rather than in a body. The recorded value is an encrypted blob, never the raw number: encrypt it the same way as an enrolment `loginId`. See the input encryption concept atom for the padding rules.

## Responses

- `200`: The specification does not describe this body. Send the call with Try it to see what comes back.
