# Get all specialities by system of medicine code

`POST /v1.5/facility/get-specialities`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-specialities \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "systemOfMedicineCode": "D"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `systemOfMedicineCode` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "type": "SPECIALITIES",
  "data": [
    {
      "code": "D-S44",
      "value": "OralMedicine and Radiology"
    },
    {
      "code": "D-S46",
      "value": "Oral& Maxillofacial Surgery"
    },
    "... 1 more of the same shape"
  ]
}
```
