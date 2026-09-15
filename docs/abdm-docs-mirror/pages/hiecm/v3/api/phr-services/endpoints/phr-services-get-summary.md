# get/summary

`GET /health/service/bookmark/summary`

Lists the person's bookmarked places in summary form: title, address and coordinates.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/bookmark/summary \
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
    "title": "Home",
    "address": "<ADDRESS>",
    "latitude": 18.511805,
    "longitude": 73.735285
  },
  {
    "title": "office 2",
    "address": "<ADDRESS>",
    "latitude": 18.593371,
    "longitude": 73.73306
  },
  "... 2 more of the same shape"
]
```
