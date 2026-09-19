# Get facilities created by HPR ID

`POST /getFacilityCreatedByHprId`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/getFacilityCreatedByHprId \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>",
  "source": "<SOURCE>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `page` (integer)
- `size` (integer)

## Body

- `hprId` (string)
- `source` (string)

## Responses

- `200`: OK
- `404`: Not Found
