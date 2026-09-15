# PHR - Get Care Context Links

`GET /api/care-context-link/phr/fetch`

Lists the care contexts linked to the signed-in person's ABHA address, with the HIP each came from.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/phr/fetch \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "lockerView": "PHR",
    "id": 496112,
    "hipId": "DigiLocker_NEGD",
    "hipName": "DigiLocker_NEGD",
    "patientId": "<PATIENT_ID>",
    "careContext": {
      "patientReference": "nithishjanithi@sbx",
      "careContextReference": "25ac532f-178d-5885-9bcb-b82052f345eb_20260604192056317009",
      "hiTypes": [
        "OPConsultation"
      ]
    },
    "dateCreated": "2026-06-04 19:03:46.346",
    "dateModified": "2026-06-12 15:32:34.231",
    "resourceDate": "2026-06-04 19:00:00.000",
    "dataTransferStatus": "RECEIVED",
    "dataReceived": true,
    "bookmarked": false
  },
  {
    "lockerView": "PHR",
    "id": 481118,
    "hipId": "DigiLocker_NEGD",
    "hipName": "DigiLocker_NEGD",
    "patientId": "<PATIENT_ID>",
    "careContext": {
      "patientReference": "nithishjanithi@sbx",
      "careContextReference": "25ac532f-178d-5885-9bcb-b82052f345eb_20260523161917547707",
      "hiTypes": [
        "OPConsultation"
      ]
    },
    "dateCreated": "2026-05-23 16:06:14.614",
    "dateModified": "2026-05-23 16:19:23.922",
    "resourceDate": "2026-05-23 16:06:14.614",
    "dataTransferStatus": "RECEIVED",
    "dataReceived": true,
    "bookmarked": false
  },
  "... 8 more of the same shape"
]
```
