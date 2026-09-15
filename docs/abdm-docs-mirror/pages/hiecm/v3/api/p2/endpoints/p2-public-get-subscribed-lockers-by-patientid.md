# Public -Get-Subscribed-Lockers-By-PatientId

`GET /health-locker/subscription-requests/patients/lockers`

Lists the health lockers a person is subscribed to.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health-locker/subscription-requests/patients/lockers \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": 9720,
    "lockerId": "Harish4_lti",
    "lockerName": "Testing",
    "patientId": "<PATIENT_ID>",
    "dateCreated": "2025-05-22T12:22:28.454Z",
    "dateModified": "2025-06-11T06:13:58.645Z",
    "healthIdNumber": "<ABHA_NUMBER>",
    "isActive": true
  },
  {
    "id": 8726,
    "lockerId": "driefcasehl",
    "lockerName": "DRiefcase Health Locker",
    "patientId": "<PATIENT_ID>",
    "dateCreated": "2025-03-11T12:00:27.982Z",
    "dateModified": "2025-06-11T06:13:47.713Z",
    "healthIdNumber": "<ABHA_NUMBER>",
    "isActive": true
  },
  "... 4 more of the same shape"
]
```
