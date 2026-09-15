# Get District with stateCode

`GET /global/lgd/district`

Lists the districts of a state with their LGD codes.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/global/lgd/district \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `403`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "districtCode": 610,
    "districtName": "ARIYALUR"
  },
  {
    "districtCode": 730,
    "districtName": "CHENGALPATTU"
  },
  "... 36 more of the same shape"
]
```
