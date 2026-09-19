# Verify mobile OTP

`POST /v1/registration/aadhaar/verifyMobileOTP`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/registration/aadhaar/verifyMobileOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "otp": "<BASE64 ENCODED STRING>",
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `otp` (string)
- `txnId` (string)

## Responses

- `200`: OK
- `404`: Not Found
