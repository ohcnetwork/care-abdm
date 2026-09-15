# 1. Request OTP for an ABHA registration

`POST /api/registration/abha/request/otp`

Starts ABHA address registration for a person who already holds an ABHA number, by sending an OTP. `loginId` is the encrypted ABHA number or Aadhaar.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/registration/abha/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "B8Vk8rrl0chMaDK5vGV3hae0/2epXDJZujwD7Rfo8Uwx==",
  "otpSystem": "<OTPSYSTEM>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `scope` (string[], required)
- `loginHint` (string, required)
- `loginId` (string, required)
- `otpSystem` (string, required)

## Responses

- `200`: No response body is documented for this request.
