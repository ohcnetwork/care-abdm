# Verify email OTP

`POST /apis/v1/doctors/verify-email-otp`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/verify-email-otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "hpr_id": "<HPR_ID>",
  "officialEmail": "<ABHA_ADDRESS>.com",
  "emailOtp": 515999
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hpr_token` (string)
- `hpr_id` (string)
- `officialEmail` (string)
- `emailOtp` (integer)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "status": "fail",
  "msg": "Email Verification Failed"
}
```
