# Submit the notifications corresponding to events during data flow

`POST /api/hiecm/data-flow/v3/health-information/notify`

HIU and HIP during data transfer. </br></br> HIP on the transfer of data would send sessionStatus - one of [TRANSFERRED, FAILED]</br> HIP would also send hiStatus for each careContextReference - on of [DELIVERED, ERRORED]</br> HIU on receipt of data would send sessionStatus - one of [RECEIVED, FAILED]. For example, FAILED when data was not sent or if invalid data was sent</br> HIU would also send hiStatus for each careContextReference - one of [OK, ERRORED]

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "consentId": "18235d89-cb13-479d-ad71-7a57d5f669a8",
    "transactionId": "18235d89-cb13-479d-ad71-7a57d5f669a8",
    "doneAt": "2023-01-24T06:35:44.167Z",
    "notifier": {
      "type": "HIU",
      "id": "100005"
    },
    "statusNotification": {
      "sessionStatus": "RECEIVED",
      "hipId": "IN2810014366",
      "statusResponses": [
        {
          "careContextReference": "10004-20200001768-1",
          "hiStatus": "OK",
          "description": "Data received successfully"
        }
      ]
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Body

- `notification` (object, required)
- `notification.consentId` (string, required): The consent artefact id with which health information was requested.Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `notification.transactionId` (string, required): The UUID generated when the health information request was initiated.Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `notification.doneAt` (string, required): The date at which the transaction was initiated. Should be a UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `notification.notifier` (object, required)
- `notification.notifier.type` (string, required): The Service ID.Allows alpha numeric characters and special characters like  "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$" One of: HIU, HIP.
- `notification.notifier.id` (string, required): The service ID of the notifier. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `notification.statusNotification` (object, required)
- `notification.statusNotification.sessionStatus` (string, required): The status of the health information request that was initiated. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `notification.statusNotification.hipId` (string, required): The service ID of the health information provider. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `notification.statusNotification.statusResponses` (object[], required)
- `notification.statusNotification.statusResponses.careContextReference` (string, required): The care context reference number.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `notification.statusNotification.statusResponses.hiStatus` (string, required): The status of the health information transfer. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `notification.statusNotification.statusResponses.description` (string, required): The brief description of the status. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Access Denied
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
