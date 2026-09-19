# Fetch HPID sub categories from category

`GET /hpid/get/subCategories`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/hpid/get/subCategories \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `categoryCode` (string)
- `role` (integer)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
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
```
