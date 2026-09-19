# Fetch HPID categories

`GET /hpid/get/categories`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/hpid/get/categories \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `role` (integer)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "code": 1,
    "name": "Doctor",
    "subCategories": [
      {
        "code": "220",
        "name": "Yoga and Naturopathy"
      },
      {
        "code": "1",
        "name": "Modern Medicine"
      },
      "... 1 more of the same shape"
    ]
  },
  {
    "code": 2,
    "name": "Nurse",
    "subCategories": [
      {
        "code": "9",
        "name": "Registered Nurse and Registered Midwife (RN & RM)"
      },
      {
        "code": "10",
        "name": "Registered Lady Health Visitor (RLHV)"
      },
      "... 1 more of the same shape"
    ]
  },
  "... 1 more of the same shape"
]
```
