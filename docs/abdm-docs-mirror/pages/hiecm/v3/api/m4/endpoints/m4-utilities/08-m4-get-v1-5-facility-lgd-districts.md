# Get all district by state ID

`GET /v1.5/facility/lgd/districts`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/lgd/districts \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `stateCode` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "code": "1",
    "name": "Anantnag"
  },
  {
    "code": "623",
    "name": "Bandipora"
  },
  "... 1 more of the same shape"
]
```
