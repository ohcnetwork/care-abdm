# Search auth methods ABHAAddress

`POST /abha/api/v3/phr/app/login/search`

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/search \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

## Headers

- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Body

- `abhaAddress` (string)

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "healthIdNumber": "<ABHA_NUMBER>",
  "abhaAddress": "<ABHA_ADDRESS>",
  "authMethods": [
    "MOBILE_OTP",
    "PASSWORD",
    "... 1 more of the same shape"
  ],
  "blockedAuthMethods": [],
  "status": "ACTIVE",
  "message": null
}
```
