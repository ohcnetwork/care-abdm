# Get Specialists Category List

`GET /health/service/facility/categories/specialities`

Lists the specialities available for filtering a facility search.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/facility/categories/specialities \
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
    "id": {
      "id": "S6",
      "systemMedicine": "M"
    },
    "name": "<NAME>",
    "activeYN": "Y",
    "arrangeOrder": null,
    "createdBy": "1593093",
    "createdDate": "2020-07-24T18:30:00.000+00:00",
    "lastUpdatedBy": null,
    "lastUpdatedDate": null,
    "specialityOrder": 19,
    "searchKeywords": "<SEARCHKEYWORDS>"
  },
  {
    "id": {
      "id": "S11",
      "systemMedicine": "M"
    },
    "name": "<NAME>",
    "activeYN": "Y",
    "arrangeOrder": null,
    "createdBy": "1593093",
    "createdDate": "2020-07-24T18:30:00.000+00:00",
    "lastUpdatedBy": null,
    "lastUpdatedDate": null,
    "specialityOrder": 20,
    "searchKeywords": "<SEARCHKEYWORDS>"
  },
  "... 40 more of the same shape"
]
```
