# Notify the gateway that a data transfer finished

`POST /hiecm/data-flow/v3/health-information/notify`

Also known as: HIP Data Flow Notification.
After successfully pushing all encrypted FHIR health data to the HIU's `dataPushUrl`,
the HIP calls this endpoint to notify the ABDM Gateway that the data transfer session
is complete. The Gateway relays this status to the HIU.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "consentId": "consent-art-uuid-001",
    "transactionId": "txn-uuid-data-001",
    "doneAt": "2024-01-15T10:30:00.000Z",
    "notifier": {
      "type": "HIP",
      "id": "HIP_SERVICE_ID"
    },
    "statusNotification": {
      "sessionStatus": "TRANSFERRED",
      "hipId": "HIP_SERVICE_ID",
      "statusResponses": [
        {
          "careContextReference": "VISIT-2024-001",
          "hiStatus": "OK",
          "description": "Successfully transferred"
        }
      ]
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Body

- `notification` (object, required)
- `notification.consentId` (string, required)
- `notification.transactionId` (string, required)
- `notification.doneAt` (string, required)
- `notification.notifier` (object, required)
- `notification.notifier.type` (string) One of: HIP, HIU.
- `notification.notifier.id` (string)
- `notification.statusNotification` (object, required)
- `notification.statusNotification.sessionStatus` (string) One of: TRANSFERRED, FAILED.
- `notification.statusNotification.hipId` (string)
- `notification.statusNotification.statusResponses` (object[])
- `notification.statusNotification.statusResponses.careContextReference` (string)
- `notification.statusNotification.statusResponses.hiStatus` (string) One of: OK, ERRORED.
- `notification.statusNotification.statusResponses.description` (string)

## Responses

- `202`: Notification accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
