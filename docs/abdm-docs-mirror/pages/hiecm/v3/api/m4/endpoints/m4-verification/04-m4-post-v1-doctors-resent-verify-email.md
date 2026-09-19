# Resend verification email

`POST /apis/v1/doctors/resent-verify-email`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/resent-verify-email \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "emailAddress": "<ABHA_ADDRESS>.com",
  "otp_type": ""
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `emailAddress` (string)
- `otp_type` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "emailAddress": "<ABHA_ADDRESS>.com",
  "otp_type": ""
}
```
