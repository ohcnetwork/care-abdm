# Verify User, verify user

`POST /abha/api/v3/phr/app/login/verify/user`

Flows in the Postman collection:
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-ABHA OTP › Verify User
- P1-Registration-login › P1 - PHR Login › P1 - Login via Mobile Number › Verify - User
- P1-Registration-login › P1 - PHR Login › P1 - Login via Email (optional) › Verify - User
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Number-Aadhaar OTP › Verify - User
- P1-Registration-login › P1 - PHR Login › P1 - Login via ABHA Number-ABHA OTP › Verify - User
- P1-Registration-login › P1 - PHR Login › P1 - Login via Aadhaar- OTP › Verify - User

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'T-token: Bearer <JWT TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "txnId": "48bc0a00-1127-459c-b040-8147f4ccc11a"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for each request.
- `T-token` (string, required)
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Body

- `abhaAddress` (string)
- `txnId` (string)

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "token": "<JWT TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<JWT TOKEN>",
  "refreshExpiresIn": 1296000
}
```
