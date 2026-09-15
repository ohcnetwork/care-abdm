# 03 link-confirm

`POST /user-initiated-linking/link/confirm`

Confirms a user-initiated link with the OTP the HIP sent, completing the link of the discovered care contexts.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/user-initiated-linking/link/confirm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "token": 123456,
  "linkRefNumber": "<TXN_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `token` (integer, required)
- `linkRefNumber` (string, required)

## Responses

- `200`: No response body is documented for this request.
