# Update-scheduled push notification

`PUT /api/notification/schedule-push-notification`

Changes the delivery time of a scheduled push notification.

```bash
curl --request PUT \
  --url https://phrsbx.abdm.gov.in/api/notification/schedule-push-notification \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "patient_id": "<PATIENT_ID>",
  "id": 42,
  "timestamp_to_push": "2025-08-25 15:00:00",
  "medical_remainder_id": "MED-NEW-001"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `patient_id` (string, required)
- `id` (integer, required)
- `timestamp_to_push` (string, required)
- `medical_remainder_id` (string, required)

## Responses

- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
