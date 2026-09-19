# Get master data

`GET /v1.5/facility/get-master-data`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-master-data \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `type` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "type": "MEDICINE",
  "data": [
    {
      "code": "H",
      "value": "Homeopathy"
    },
    {
      "code": "UN",
      "value": "Unani"
    },
    "... 1 more of the same shape"
  ]
}
```
