# Generate mobile OTP 1

`POST /password/recover/byMobile/sendMobileOTP`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/recover/byMobile/sendMobileOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "amol.xxxxxx"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hprId` (string, required)
- `categories` (object)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "7ebad8aa-127b-492f-bd0e-56da716bd39e",
  "msg": "Please enter OTP sent on your mobile number ******2021",
  "otp": 0,
  "mobileNumber": "******2021"
}
```
