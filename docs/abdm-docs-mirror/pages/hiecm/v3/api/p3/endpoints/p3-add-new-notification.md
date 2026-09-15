# Add new Notification

`POST /api/notification/new-app-push-notification`

Creates a push notification for a person.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/notification/new-app-push-notification \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '[
  {
    "id": 515459874,
    "patientId": "<PATIENT_ID>",
    "pushNotificationData": {
      "healthId": "<ABHA_ADDRESS>",
      "target": "in.projecteka.jataayu.consent.ui.activity.ConsentDetailsActivity",
      "title": "Dr. ManishTEST_HIU",
      "body": "Wants to access your records\nPurpose : Care Management",
      "timestamp": 1743788382266,
      "params": {
        "consentRequestId": "<TXN_ID>"
      }
    },
    "dateCreated": "2025-04-04T17:39:42.268Z",
    "dateModified": "2025-04-04T17:39:42.270Z",
    "isNotificationRead": false,
    "unreadCount": 3
  }
]'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "id": 13295,
  "patientId": "<PATIENT_ID>",
  "pushNotificationData": {
    "healthId": "<ABHA_ADDRESS>",
    "target": "familyManagementId",
    "title": "Notification",
    "body": "You have a new notification",
    "timestamp": "2026-06-01T08:06:55.128Z",
    "params": {}
  },
  "dateCreated": "2026-06-01T08:06:55.131Z",
  "dateModified": "2026-06-01T08:06:55.131Z",
  "isNotificationRead": false,
  "isDeleted": false
}
```
