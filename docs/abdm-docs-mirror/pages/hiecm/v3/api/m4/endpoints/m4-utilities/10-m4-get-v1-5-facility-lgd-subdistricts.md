# Get all sub district by district code

`GET /v1.5/facility/lgd/subdistricts`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/lgd/subdistricts \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `districtCode` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "code": "6752",
    "name": "Assar"
  },
  {
    "code": "65",
    "name": "Bhaderwah"
  },
  "... 1 more of the same shape"
]
```
