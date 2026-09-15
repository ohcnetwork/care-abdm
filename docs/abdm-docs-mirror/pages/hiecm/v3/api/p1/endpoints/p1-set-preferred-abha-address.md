# Set the preferred ABHA address

`POST /profile/phr/set-preferred/abha-address`

Marks one of the person's ABHA addresses as the preferred one, against a verified transaction.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/profile/phr/set-preferred/abha-address \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "<TRANSACTION_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `transactionId` (string, required)

## Responses

- `200`: No response body is documented for this request.
