# Verify doctor verification OTP

`POST /v1/verifyDoctorVerificationOtp`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/verifyDoctorVerificationOtp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "otp": "<OTP>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `txnId` (string)
- `otp` (string)

## Responses

- `200`: OK
- `404`: Not Found
