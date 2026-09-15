# Get all notification details

`GET /api/notification/get-notification`

Lists the person's push notifications with their read state and the unread count.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/notification/get-notification \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `403`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": 13192,
    "patientId": "<PATIENT_ID>",
    "pushNotificationData": {
      "healthId": "<ABHA_ADDRESS>",
      "target": "selfUpload",
      "title": "File Processed Successfully",
      "body": "Your record PreviousMedicalprescription-ParveenSharma1.pdf has been processed and is ready for review.",
      "timestamp": "2026-05-27T10:44:29.657Z",
      "params": {}
    },
    "dateCreated": "2026-05-27T10:44:29.660Z",
    "dateModified": "2026-05-27T10:44:29.660Z",
    "isNotificationRead": false,
    "isDeleted": false,
    "unreadCount": 5,
    "totalNotificationCount": 298
  },
  {
    "id": 13172,
    "patientId": "<PATIENT_ID>",
    "pushNotificationData": {
      "healthId": "<ABHA_ADDRESS>",
      "target": "selfUpload",
      "title": "File Processed Successfully",
      "body": "Your record IN0110000034-Consultation_VISIT-18199008-<TXN_ID>.pdf has been processed and is ready for review.",
      "timestamp": "2026-05-27T05:41:50.162Z",
      "params": {}
    },
    "dateCreated": "2026-05-27T05:41:50.165Z",
    "dateModified": "2026-05-27T05:41:50.165Z",
    "isNotificationRead": false,
    "isDeleted": false,
    "unreadCount": 5,
    "totalNotificationCount": 298
  },
  "... 18 more of the same shape"
]
```
