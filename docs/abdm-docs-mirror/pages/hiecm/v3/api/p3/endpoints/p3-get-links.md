# Get Links

`POST /api/consent-management/link/get-links`

Lists the person's linked care contexts at the HIPs given, for choosing what to grant in a consent.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/link/get-links \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "patientId": "<PATIENT_ID>",
  "hipIds": [
    "<hip-id-1>",
    "<hip-id-2>"
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `patientId` (string, required)
- `hipIds` (string[], required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "patient": {
      "id": "nithishjanithi@sbx",
      "links": [
        {
          "hip": {
            "id": "DigiLocker_NEGD",
            "name": "<NAME>",
            "type": "HIP"
          },
          "referenceNumber": "nithishjanithi@sbx",
          "display": "Health Document",
          "careContexts": [
            {
              "referenceNumber": "25ac532f-178d-5885-9bcb-b82052f345eb_20260604192056317009",
              "display": "DigiLocker_2026-06-04-19:20:57",
              "hiTypes": [
                "OPConsultation"
              ]
            }
          ],
          "dateCreated": "2026-06-04T13:50:57.157Z"
        },
        {
          "hip": {
            "id": "DigiLocker_NEGD",
            "name": "<NAME>",
            "type": "HIP"
          },
          "referenceNumber": "nithishjanithi@sbx",
          "display": "Health Document",
          "careContexts": [
            {
              "referenceNumber": "25ac532f-178d-5885-9bcb-b82052f345eb_20260604191949954362",
              "display": "DigiLocker_2026-06-04-19:19:51",
              "hiTypes": [
                "OPConsultation"
              ]
            }
          ],
          "dateCreated": "2026-06-04T13:49:51.549Z"
        },
        "... 3 more of the same shape"
      ]
    }
  }
]
```
