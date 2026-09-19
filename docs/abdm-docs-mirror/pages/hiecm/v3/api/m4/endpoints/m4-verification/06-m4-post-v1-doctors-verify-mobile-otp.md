# Verify mobile OTP

`POST /apis/v1/doctors/verify-mobile-otp`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/verify-mobile-otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "txnId": "dd392164-0f4a-4894-8d64-1fce027ee033",
  "otp": "<BASE64 ENCODED STRING>"
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
