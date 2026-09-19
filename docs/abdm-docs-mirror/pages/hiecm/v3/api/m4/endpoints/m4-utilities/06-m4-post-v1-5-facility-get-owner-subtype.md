# Get all sub types by owner ship type and sub type

`POST /v1.5/facility/get-owner-subtype`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-owner-subtype \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "ownershipCode": "P",
  "ownerSubtypeCode": "NP"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `ownershipCode` (string, required)
- `ownerSubtypeCode` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "type": "CENTRAL-GOVERNMENT",
  "data": [
    {
      "code": "MOHF",
      "value": "Mo Health and Family Welfare"
    },
    {
      "code": "MOR",
      "value": "Mo Railways"
    },
    "... 1 more of the same shape"
  ]
}
```
