# Get categories

`GET /teleconsulting/getCategories`

Lists the teleconsultation categories available to search in.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/teleconsulting/getCategories \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "categoryId": 2,
    "descriptor": "Consultation"
  },
  {
    "categoryId": 3,
    "descriptor": "Consultation"
  },
  "... 782 more of the same shape"
]
```
