# 3. Verify Auth

`POST /api/registration/abha/verify/auth`

Verifies the OTP for a registration transaction started against an ABHA number. `authData` carries the transaction id and the encrypted OTP.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/registration/abha/verify/auth \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-enroll",
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
