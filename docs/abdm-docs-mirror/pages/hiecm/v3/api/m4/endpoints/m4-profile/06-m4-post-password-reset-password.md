# Reset password and session

`POST /password/reset/password`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/reset/password \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "newPassword": "<NEW_PASSWORD>",
  "otp": "<OTP>",
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `newPassword` (string): Encrypted new Password.
- `otp` (string): Encrypted OTP.
- `txnId` (string, required)

## Responses

- `200`: OK
- `404`: Not Found
