# Get all master types

`GET /v1.5/facility/get-master-types`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-master-types \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "masterTypes": [
    {
      "type": "MEDICINE",
      "desc": "System Of Medicine"
    },
    {
      "type": "OWNER",
      "desc": "Ownership Of Facility"
    },
    "... 1 more of the same shape"
  ]
}
```
