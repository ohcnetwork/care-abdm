# Search benefit records for a person

`POST /v3/profile/benefit/search`

Searches by encrypted XML UID or by ABHA number, depending on
`loginHint`. Returns an array, one entry per benefit scheme, each with
the scheme name, its identifier and a status.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'BENEFIT_NAME: healthid api' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search"
  ],
  "loginHint": "xmlUid",
  "loginId": "<ENCRYPTED_XML_UID>"
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
- `loginHint` (string, required)
- `loginId` (string, required)

## Responses

- `200`: The response.
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
    "stateCode": null,
    "benefitName": "COVIN",
    "benefitId": "<BENEFIT_ID>",
    "abhaNumber": "<ABHA_NUMBER>",
    "status": 0
  }
]
```
