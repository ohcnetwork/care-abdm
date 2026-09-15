# Get System of Medicine List

`GET /health/service/facility/master/system-of-medicine`

Lists the systems of medicine a facility can be filtered by.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/facility/master/system-of-medicine \
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
    "id": "M",
    "value": "Modern Medicine(Allopathy)"
  },
  {
    "id": "D",
    "value": "Dentistry"
  },
  "... 7 more of the same shape"
]
```
