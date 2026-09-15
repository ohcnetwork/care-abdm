# 4. Create Custom PHR Address

`POST /api/registration/abha/custom/phr/create`

Creates an ABHA address of the person's own choosing, once the registration transaction has been verified.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/registration/abha/custom/phr/create \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `txnId` (string, required)
- `abhaAddress` (string, required)

## Responses

- `200`: No response body is documented for this request.
