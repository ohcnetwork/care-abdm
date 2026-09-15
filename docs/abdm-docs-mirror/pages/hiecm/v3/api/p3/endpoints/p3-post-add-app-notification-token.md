# Post - add App Notification Token

`POST /notification/app-notification-token`

Registers a device token for push notifications, with the operating system it belongs to.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/notification/app-notification-token \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "healthId": "<ABHA_ADDRESS>",
  "appToken": "<APPTOKEN>",
  "osType": "android"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `healthId` (string, required)
- `appToken` (string, required)
- `osType` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "stateCode": 35,
    "stateName": "ANDAMAN AND NICOBAR ISLANDS"
  },
  {
    "stateCode": 28,
    "stateName": "ANDHRA PRADESH"
  },
  "... 34 more of the same shape"
]
```
