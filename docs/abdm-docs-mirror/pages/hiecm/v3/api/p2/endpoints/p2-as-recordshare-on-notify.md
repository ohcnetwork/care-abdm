# AS - RecordShare on-notify

`POST /scan-share/record-share/on-notify`

Callback the gateway sends to notify the PHR that a record share has been acted on.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/scan-share/record-share/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "transactionId": "<TXN_ID>",
    "doneAt": "2026-06-24T06:35:44.167Z",
    "statusNotification": {
      "sessionStatus": "TRANSFERRED",
      "statusResponses": [
        {
          "careContextReference": "74538",
          "hiStatus": "DELIVERED",
          "description": "Data received successfully"
        }
      ]
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `notification` (object, required)
- `notification.transactionId` (string, required)
- `notification.doneAt` (string, required)
- `notification.statusNotification` (object, required)
- `notification.statusNotification.sessionStatus` (string, required)
- `notification.statusNotification.statusResponses` (object[], required)
- `notification.statusNotification.statusResponses.careContextReference` (string, required)
- `notification.statusNotification.statusResponses.hiStatus` (string, required)
- `notification.statusNotification.statusResponses.description` (string, required)

## Responses

- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
