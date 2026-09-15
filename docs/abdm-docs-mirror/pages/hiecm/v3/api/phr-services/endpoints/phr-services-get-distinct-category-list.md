# Get Distinct Category List

`GET /health/service/facility/categories/distinct`

Lists the distinct facility categories, with the care settings each offers.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/facility/categories/distinct \
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
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": {
      "sno": 9,
      "systemmedicine": "M"
    },
    "facilityType": "G",
    "facilityTypeNdhm": "Blood Bank",
    "opd": "No",
    "ipd": "No",
    "dayCare": "No",
    "other": "No",
    "activeYN": "Y",
    "createdBy": "1358478",
    "createdDate": "2020-07-23T13:55:32.623+00:00",
    "lastUpdatedUser": "",
    "lastUpdatedDate": null,
    "linkToForm": "SubmitForm                                                                                          ",
    "facilityCode": "NHRR_08                                                                                             ",
    "facilityCodeUfid": "blb",
    "facilityOrder": 8
  },
  {
    "id": {
      "sno": 44,
      "systemmedicine": "M"
    },
    "facilityType": "P",
    "facilityTypeNdhm": "Blood Bank",
    "opd": "No",
    "ipd": "No",
    "dayCare": "No",
    "other": "No",
    "activeYN": "Y",
    "createdBy": "1358478",
    "createdDate": "2020-07-23T13:55:32.623+00:00",
    "lastUpdatedUser": "",
    "lastUpdatedDate": null,
    "linkToForm": "SubmitForm                                                                                          ",
    "facilityCode": "NHRR_08                                                                                             ",
    "facilityCodeUfid": "blb",
    "facilityOrder": 43
  }
]
```
