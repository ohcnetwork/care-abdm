# Reset password

`POST /password/resetPassword`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/resetPassword \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "9b78fdfb-3ba4-4707-8913-63c7c5e3a743",
  "newPassword": "<BASE64 ENCODED STRING>"
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

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Password has been changed successfully!"
}
```
