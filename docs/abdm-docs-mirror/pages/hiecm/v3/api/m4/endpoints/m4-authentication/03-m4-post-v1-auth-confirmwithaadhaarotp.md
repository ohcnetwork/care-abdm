# Verify Aadhaar OTP 1

`POST /api/v1/auth/confirmWithAadhaarOtp`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/api/v1/auth/confirmWithAadhaarOtp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "otp": "308709",
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
