# Generate mobile OTP 2

`POST /apis/v1/doctors/generate-mobile-otp`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/generate-mobile-otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "officialMobile": "<BASE64 ENCODED STRING>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hpr_token` (string, required)
- `officialMobile` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "status": "success",
  "txnId": "3a9e7f08-39ea-42fc-b3bc-b81a3cc68ab5"
}
```
