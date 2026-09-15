# Public-Health-Lockers-Unsubscribe

`POST /api/health-locker/lockers/unsubscribe`

Ends the person's subscription to a health locker, so it stops receiving their new records.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/health-locker/lockers/unsubscribe \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `403`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "patientId": "<PATIENT_ID>",
  "lockerId": "Priyanka_Health_Locker",
  "isActive": false
}
```
