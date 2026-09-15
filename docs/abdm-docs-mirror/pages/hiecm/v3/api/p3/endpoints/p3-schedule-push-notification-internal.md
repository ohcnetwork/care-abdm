# Schedule-push-notification - internal

`POST /api/notification/schedule-push-notification`

Schedules a push notification to a person for a given time, for example a medication reminder.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/notification/schedule-push-notification \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "patient_id": "<PATIENT_ID>",
  "push_notification_data": {
    "healthId": "<ABHA_ADDRESS>",
    "target": "TELECONSULTATION",
    "title": "Doctor Consultation",
    "body": "You have a doctor booking for Dr Nithish at 09.00 am today.",
    "timestamp": "2026-04-15T12:30:45.123Z",
    "params": {
      "orderId": "001"
    }
  },
  "timestamp_to_push": "2026-04-15T18:30:00",
  "medical_remainder_id": "01"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `patient_id` (string, required)
- `push_notification_data` (object, required)
- `push_notification_data.healthId` (string, required)
- `push_notification_data.target` (string, required)
- `push_notification_data.title` (string, required)
- `push_notification_data.body` (string, required)
- `push_notification_data.timestamp` (string, required)
- `push_notification_data.params` (object, required)
- `push_notification_data.params.orderId` (string, required)
- `timestamp_to_push` (string, required)
- `medical_remainder_id` (string, required)

## Responses

- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
