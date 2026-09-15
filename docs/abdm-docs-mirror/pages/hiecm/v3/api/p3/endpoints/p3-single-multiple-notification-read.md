# Single/Multiple Notification read

`POST /api/notification/app-push-notification/all`

Marks one or more push notifications as read.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/notification/app-push-notification/all \
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
[
  {
    "stateCode": 0,
    "stateName": "<STATE_NAME>",
    "id": 0,
    "patientId": "<PATIENT_ID>",
    "pushNotificationData": {
      "healthId": "<HEALTH_ID>",
      "title": "<TITLE>",
      "body": "<BODY>",
      "timestamp": "<TIMESTAMP>",
      "params": {
        "orderId": "<ORDER_ID>"
      },
      "target": "<TARGET>"
    },
    "dateCreated": "<DATE_CREATED>",
    "dateModified": "<DATE_MODIFIED>",
    "isNotificationRead": false,
    "isDeleted": false
  }
]
```
