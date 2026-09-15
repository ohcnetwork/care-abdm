# Get categories by id

`GET /teleconsulting/getCategories/1`

Returns one teleconsultation category by its id.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/teleconsulting/getCategories/1 \
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
    "categoryId": 1,
    "descriptor": "Consultation"
  }
]
```
