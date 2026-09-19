# Generate mobile OTP

`POST /v1/forgot/hprId/mobile/generateOtp`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/forgot/hprId/mobile/generateOtp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "mobileNumber": "VPoaDCJBNyGhJiX+sAh9yRq1WXAfRXkgcE31/0U2DMkH/+nvpspAA4GEmkbideZhKsSLYnFA1lHPkBH7PS6Bg4jz0aSdDAoovnYgVftJ/suP4mzhhg1Hrf7zQFPriHiraNlsIzsDeLl3ckGejNiCmXhfhBBw==xxxxxxxxxxxxx"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `mobileNumber` (string)
- `email` (string)
- `type` (string)
- `hpid` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "132dd7dd-ca5a-4ec1-a36c-093c007bf794",
  "msg": "Please enter OTP sent on your mobile number ******2021",
  "mobileNumber": "******2021"
}
```
