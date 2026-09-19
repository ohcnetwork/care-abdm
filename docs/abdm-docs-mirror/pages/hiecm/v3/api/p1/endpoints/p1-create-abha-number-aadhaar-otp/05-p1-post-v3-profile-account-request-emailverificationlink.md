# Submit the email verification link

`POST /abha/api/v3/profile/account/request/emailVerificationLink`

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/emailVerificationLink \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-token: Bearer <JWT TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "email-link-verify"
  ],
  "loginHint": "email",
  "loginId": "{{encrypted email}}",
  "otpSystem": "abdm"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.
- `X-token` (string, required)

## Body

- `scope` (string[])
- `loginHint` (string)
- `loginId` (string)
- `otpSystem` (string)

## Responses

- `default`: No response was saved in the Postman collection and no documented definition exists.
