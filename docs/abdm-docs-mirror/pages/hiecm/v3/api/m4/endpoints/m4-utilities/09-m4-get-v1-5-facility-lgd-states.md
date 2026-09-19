# Get all states by LGD

`GET /v1.5/facility/lgd/states`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/lgd/states \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "code": "35",
    "name": "Andaman And Nicobar Islands",
    "districts": [
      {
        "code": "603",
        "name": "Nicobars"
      },
      {
        "code": "632",
        "name": "North And Middle Andaman"
      },
      "... 1 more of the same shape"
    ]
  },
  {
    "code": "28",
    "name": "Andhra Pradesh",
    "districts": [
      {
        "code": "745",
        "name": "<NAME>"
      },
      {
        "code": "744",
        "name": "Anakapalli"
      },
      "... 1 more of the same shape"
    ]
  },
  "... 1 more of the same shape"
]
```
