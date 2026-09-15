# Get Relationship Types

`GET /api/family-management/get-relationship-types`

Lists the relationship types an address can be assigned under, each with the id `assign` takes.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/family-management/get-relationship-types \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": 3,
    "typeName": "Self"
  },
  {
    "id": 6,
    "typeName": "Father"
  },
  "... 13 more of the same shape"
]
```
