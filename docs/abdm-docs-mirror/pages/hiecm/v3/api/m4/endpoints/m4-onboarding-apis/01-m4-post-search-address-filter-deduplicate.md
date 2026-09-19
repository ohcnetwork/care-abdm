# Get filtered address post

`POST /search/address/filter/deduplicate`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/search/address/filter/deduplicate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "Jethana",
  "address": "<ADDRESS>",
  "district": "511",
  "subDistrict": "5271",
  "village": "",
  "geolocation": "",
  "facilityId": "69765"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `name` (string)
- `address` (string)
- `district` (string)
- `subDistrict` (string)
- `village` (string)
- `geolocation` (string)
- `facilityId` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
"array"
```
