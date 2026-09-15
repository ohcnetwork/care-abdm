# Update mobile verify OTP

`POST /abha/api/v3/phr/app/login/profile/abha/verify`

Verifies the OTP sent for a mobile number update on an ABHA address. `authData` carries the transaction id and the encrypted OTP.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/abha/api/v3/phr/app/login/profile/abha/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `scope` (string[], required)
- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `authData.otp` (object, required)
- `authData.otp.txnId` (string, required)
- `authData.otp.otpValue` (string, required)

## Responses

- `200`: No response body is documented for this request.
