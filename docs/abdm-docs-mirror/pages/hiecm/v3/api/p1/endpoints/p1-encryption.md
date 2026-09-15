# ENCRYPTION

`POST /abha/api/v3/phr/app/enrollment/encrypt`

Encrypts a value with the ABDM public key so it can be sent in the fields that only accept ciphertext, such as `loginId` and OTP values.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/encrypt \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "data": "<ABHA_NUMBER>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `data` (string, required)

## Responses

- `200`: No response body is documented for this request.
