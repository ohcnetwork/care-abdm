# GET-scheduled push Notifications

`GET /api/notification/schedule-push-notification`

Lists the push notifications scheduled for later delivery, with their processing state.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/notification/schedule-push-notification \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
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
  "id": 682,
  "patient_id": "<PATIENT_ID>",
  "push_notification_data": {
    "body": "Don't forget to take your medicine today.",
    "title": "Medical remainder",
    "params": {
      "medicalRemainderId": "279"
    },
    "target": "MEDICATION_REMINDER",
    "healthId": "<ABHA_ADDRESS>",
    "timestamp": "2026-04-20T09:44:32.878501204Z"
  },
  "date_created": "2026-04-20T15:14:32",
  "timestamp_to_push": "2026-04-21T17:14:00",
  "is_processed": true,
  "processing_started_at": "2026-04-21T17:15:50",
  "processing_pod_id": "aarogya-setu-notification-app-service-7db645d7f9-pzbvz",
  "medical_remainder_id": null
}
```
