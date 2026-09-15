# Get All Linked Care Contexts

`GET /api/care-context-link/link/patient/links`

Lists every care context linked to the signed-in person, grouped by HIP.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/link/patient/links \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "patient": {
    "id": "nithishjanithi1@sbx",
    "links": [
      {
        "hip": {
          "id": "IN0002222",
          "name": "<NAME>",
          "type": "HIP"
        },
        "referenceNumber": "nithishjanithi1@sbx",
        "display": "Blood Test",
        "hiType": "OPConsultation",
        "careContexts": [
          {
            "referenceNumber": "Blood test1-28May",
            "display": "Blood Test"
          }
        ],
        "dateCreated": "2026-01-22T09:09:37.817Z",
        "new": false
      },
      {
        "hip": {
          "id": "DigiLocker_NEGD",
          "name": "<NAME>",
          "type": "HIP"
        },
        "referenceNumber": "nithishjanithi1@sbx",
        "display": "Health Document",
        "hiType": "DiagnosticReport",
        "careContexts": [
          {
            "referenceNumber": "25ac532f-178d-5885-9bcb-b82052f345eb_20260612153648199758",
            "display": "DigiLocker_2026-06-12-15:36:51"
          }
        ],
        "dateCreated": "2026-06-12T10:06:51.884Z",
        "new": false
      },
      "... 1 more of the same shape"
    ]
  }
}
```
