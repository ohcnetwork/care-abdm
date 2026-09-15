# App Notification Token

`GET /api/notification/request/app-notification-token`

Returns the device token registered for push notifications to the signed-in person.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/notification/request/app-notification-token \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "id": 48,
  "healthId": "<ABHA_ADDRESS>",
  "appToken": "<APPTOKEN>",
  "dateCreated": "2025-08-11 18:20:41.039",
  "dateModified": "2026-05-27 16:12:16.215",
  "osType": "android"
}
```
