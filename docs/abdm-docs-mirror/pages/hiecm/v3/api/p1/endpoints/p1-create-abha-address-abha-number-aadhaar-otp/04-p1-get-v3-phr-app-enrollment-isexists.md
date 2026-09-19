# Check whether the ABHA address exists

`GET /abha/api/v3/phr/app/enrollment/isExists`

Flows in the Postman collection:
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via Mobile › isExists API
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-ABHA OTP › isExists API Copy
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-Aadhaar OTP › isExists API

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/isExists \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

## Headers

- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Query parameters

- `abhaAddress` (string)

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
false
```
