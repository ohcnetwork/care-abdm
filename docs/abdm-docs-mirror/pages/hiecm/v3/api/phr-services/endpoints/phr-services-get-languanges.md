# Get Languanges

`GET /health/service/doctor/master/languages`

Lists the languages a doctor can be filtered by.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/doctor/master/languages \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": 1,
    "name": "<NAME>",
    "culture": "",
    "status": true
  },
  {
    "id": 2,
    "name": "<NAME>",
    "culture": "",
    "status": true
  },
  "... 27 more of the same shape"
]
```
