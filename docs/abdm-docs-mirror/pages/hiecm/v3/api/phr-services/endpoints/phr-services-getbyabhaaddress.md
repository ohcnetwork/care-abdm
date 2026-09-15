# getByAbhaAddress

`GET /health/service/bookmark/getByAbhaAddress`

Lists the places the signed-in ABHA address has bookmarked.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/bookmark/getByAbhaAddress \
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
    "id": 242,
    "abhaAddress": "<ABHA_ADDRESS>",
    "title": "House_05",
    "address": "<ADDRESS>",
    "latitude": 40.7128,
    "longitude": -74.006,
    "isDeleted": false,
    "createdTime": "2026-05-29T15:36:08.236642",
    "updatedTime": "2026-05-29T15:36:08.236654"
  },
  {
    "id": 244,
    "abhaAddress": "<ABHA_ADDRESS>",
    "title": "House_05",
    "address": "<ADDRESS>",
    "latitude": 40.7128,
    "longitude": -74.006,
    "isDeleted": false,
    "createdTime": "2026-05-29T15:36:43.437327",
    "updatedTime": "2026-05-29T15:36:43.437335"
  },
  "... 1 more of the same shape"
]
```
