# {{aarogya-setu-sandbox-url}}api/health/service/doctor/master/system-of-medicine

`GET /health/service/doctor/master/system-of-medicine`

Lists the systems of medicine a doctor can be filtered by.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/doctor/master/system-of-medicine \
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
    "medicalSystem": "Modern Medicine",
    "code": "modern_medicine",
    "position": 1,
    "excludeStates": "[\"1\",\"6\",\"104\",\"17\",\"18\",\"26\",\"32\"]",
    "hprType": "doctor"
  },
  {
    "id": 2,
    "medicalSystem": "Dentistry",
    "code": "dentist",
    "position": 2,
    "excludeStates": "[\"1\",\"17\",\"18\",\"103\",\"32\"]",
    "hprType": "doctor"
  },
  "... 12 more of the same shape"
]
```
