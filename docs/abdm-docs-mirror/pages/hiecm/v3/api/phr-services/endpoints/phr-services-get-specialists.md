# Get Specialists

`GET /api/hem/getSpecialists`

Lists the specialities available for filtering a facility search.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/hem/getSpecialists \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "specialityid": "100001",
    "specialitycode": "BM",
    "specialityname": "Burns Management",
    "displayorder": "1",
    "status": "Active"
  },
  {
    "specialityid": "100002",
    "specialitycode": "MC",
    "specialityname": "Cardiology",
    "displayorder": "2",
    "status": "Active"
  },
  "... 132 more of the same shape"
]
```
