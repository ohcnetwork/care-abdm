# 1. Request OTP for a PHR registration

`POST /api/registration/phr/request/otp`

Starts ABHA address registration for a person with no ABHA number, by sending an OTP to their mobile. `loginId` is the encrypted mobile number.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/registration/phr/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-enroll",
    "mobile-verify"
  ],
  "loginHint": "mobile-number",
  "loginId": "xHu0gDObXVpar+WN4yvTqpIswFtJmdbufWPlqp==",
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
