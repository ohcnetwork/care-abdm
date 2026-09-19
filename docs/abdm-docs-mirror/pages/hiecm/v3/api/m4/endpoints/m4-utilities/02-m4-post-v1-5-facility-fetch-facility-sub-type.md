# Get all facility sub type by facility type

`POST /v1.5/facility/fetch-facility-Sub-type`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/fetch-facility-Sub-type \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityTypeCode": "2"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `facilityTypeCode` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "type": "FACILITY-SUB-TYPE",
  "data": [
    {
      "code": "29",
      "value": "Any Other"
    },
    {
      "code": "1",
      "value": "Block Primary Health Centre"
    },
    "... 1 more of the same shape"
  ]
}
```
