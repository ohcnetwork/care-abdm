# Get facilities declared by HPR ID

`POST /getFacilityDeclaredByHprId`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/getFacilityDeclaredByHprId \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>",
  "source": "<SOURCE>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hprId` (string)
- `source` (string)

## Responses

- `200`: OK
- `404`: Not Found
