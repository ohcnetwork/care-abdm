# Get all facility type by ownership and sys of med

`POST /v1.5/facility/fetch-facility-type`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/fetch-facility-type \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "ownershipCode": "G",
  "systemOfMedicineCode": "M"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `ownershipCode` (string, required)
- `systemOfMedicineCode` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "type": "FACILITY-TYPE",
  "data": [
    {
      "code": "9",
      "value": "Blood Bank"
    },
    {
      "code": "74",
      "value": "Imaging Center"
    },
    "... 1 more of the same shape"
  ]
}
```
