# IsKycVerified

`POST /login/phr/isKycVerified`

Reports whether the ABHA address given has completed KYC verification.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/login/phr/isKycVerified \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `abhaAddress` (string, required)

## Responses

- `200`: No response body is documented for this request.
