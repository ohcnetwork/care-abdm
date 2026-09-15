# Get Care Context Links

`GET /api/care-context-link/care-context-link/fetch`

Lists the care contexts linked to the signed-in person's ABHA address, with the HIP each came from.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/care-context-link/fetch \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "lockerView": "<LOCKER_VIEW>",
    "id": 0,
    "hipId": "<HIP_ID>",
    "hipName": "<HIP_NAME>",
    "patientId": "<PATIENT_ID>",
    "careContext": {
      "patientReference": "<PATIENT_REFERENCE>",
      "careContextReference": "<CARE_CONTEXT_REFERENCE>",
      "hiTypes": [
        "<HI_TYPES>"
      ]
    },
    "dateCreated": "<DATE_CREATED>",
    "dateModified": "<DATE_MODIFIED>",
    "resourceDate": "<RESOURCE_DATE>",
    "dataTransferStatus": "<DATA_TRANSFER_STATUS>",
    "dataReceived": false,
    "bookmarked": false
  }
]
```
