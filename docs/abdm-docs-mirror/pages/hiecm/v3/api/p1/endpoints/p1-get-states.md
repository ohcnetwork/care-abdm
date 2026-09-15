# Get States

`GET /global/lgd/state`

Lists every state with its LGD code.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/global/lgd/state \
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
    "stateCode": 35,
    "stateName": "ANDAMAN AND NICOBAR ISLANDS"
  },
  {
    "stateCode": 28,
    "stateName": "ANDHRA PRADESH"
  },
  "... 34 more of the same shape"
]
```
