# Verify mobile OTP 1

`POST /password/recover/byMobile/verifyMobileOTP`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/recover/byMobile/verifyMobileOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "7ebad8aa-127b-492f-bd0e-56da716bd39e",
  "otp": "<BASE64 ENCODED STRING>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `oldPassword` (string)
- `newPassword` (string)
- `txnId` (string)
- `hprID` (string)
- `otp` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "verified": true,
  "txnId": "7ebad8aa-127b-492f-bd0e-56da716bd39e"
}
```
