# Save Care Context Link

`POST /api/care-context-link/save`

Records a care context link for a person, with the HIP it came from and whether its data has been transferred.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/save \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hipId": "IN0002222",
  "patientId": "<PATIENT_ID>",
  "careContext": {
    "patientReference": "NITHISH_1999",
    "careContextReference": "Prescription566",
    "hiTypes": [
      "Prescription",
      "WellnessRecord",
      "Invoice",
      "OPConsultation",
      "HealthDocumentRecord"
    ]
  },
  "dataTransferred": true
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `hipId` (string, required)
- `patientId` (string, required)
- `careContext` (object, required)
- `careContext.patientReference` (string, required)
- `careContext.careContextReference` (string, required)
- `careContext.hiTypes` (string[], required)
- `dataTransferred` (boolean, required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "id": 1018,
  "hipId": "IN0002222",
  "patientId": "<PATIENT_ID>",
  "careContext": {
    "patientReference": "NITHISH_1999",
    "careContextReference": "Prescription566",
    "hiTypes": [
      "Prescription",
      "WellnessRecord",
      "... 3 more of the same shape"
    ]
  },
  "dateCreated": "2026-06-13 17:51:19.114",
  "dateModified": "2026-06-13 17:51:19.114",
  "resourceDate": "2026-06-13 17:51:19.114",
  "dataTransferStatus": "NEW",
  "dataReceived": false,
  "bookmarked": false
}
```
