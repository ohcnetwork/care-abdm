# Submit the retrieval health ID by Aadhaar

`POST /v1/forgot/hprId/aadhaar`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/forgot/hprId/aadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "otp": "<BASE64 ENCODED STRING>",
  "txnId": "4c115e27-a602-4320-b4cd-ee658539e2f0"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `txnId` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "hprId": "<EMAIL>",
  "hprIdNumber": "71-1********-0212",
  "token": "<JWT TOKEN>"
}
```
