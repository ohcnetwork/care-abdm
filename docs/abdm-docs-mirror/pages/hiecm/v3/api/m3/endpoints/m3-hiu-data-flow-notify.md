# Notify the gateway that data was received

`POST /hiecm/data-flow/v3/health-information/notify`

Also known as: HIU Data Flow Notification.
After receiving all FHIR health data at the `dataPushUrl`, the HIU calls this endpoint
to notify the ABDM Gateway that the data transfer session is complete.

The `statusNotification.sessionStatus` should be:
- `RECEIVED`, All data received successfully
- `FAILED`, Data receipt failed (with details in `statusResponses`)

The `notifier.type` must be `HIU` (contrast with M2 where the HIP sends the same
endpoint with `notifier.type: HIP`, and the value it sends is `TRANSFERRED` rather
than `RECEIVED`; the two milestones report the same event with different values
because they are the two ends of the same transfer).

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "consentId": "consent-art-uuid-001",
    "transactionId": "txn-uuid-data-001",
    "doneAt": "2024-01-15T10:30:00.000Z",
    "notifier": {
      "type": "HIU",
      "id": "HIU_SERVICE_ID"
    },
    "statusNotification": {
      "sessionStatus": "RECEIVED",
      "hipId": "HIP_SERVICE_ID",
      "statusResponses": [
        {
          "careContextReference": "VISIT-2024-001",
          "hiStatus": "OK",
          "description": "Data received and decrypted successfully"
        },
        {
          "careContextReference": "LAB-2024-001",
          "hiStatus": "OK",
          "description": "Data received and decrypted successfully"
        }
      ]
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value. In M3 a single consent can produce several callbacks, so keep the mapping from request id to consent request id rather than relying on ordering.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production.

## Body

- `notification` (object, required)
- `notification.consentId` (string, required)
- `notification.transactionId` (string, required)
- `notification.doneAt` (string, required)
- `notification.notifier` (object, required)
- `notification.notifier.type` (string, required): Must be "HIU" for M3 (vs "HIP" for M2) One of: HIP, HIU.
- `notification.notifier.id` (string, required)
- `notification.statusNotification` (object, required)
- `notification.statusNotification.sessionStatus` (string, required): HIU-side value, this is the M3 half of the exchange. RECEIVED on success, not TRANSFERRED, which is what the HIP sends on the M2 side of the same event. One of: RECEIVED, FAILED.
- `notification.statusNotification.hipId` (string, required)
- `notification.statusNotification.statusResponses` (object[], required)
- `notification.statusNotification.statusResponses.careContextReference` (string)
- `notification.statusNotification.statusResponses.hiStatus` (string) One of: OK, ERRORED.
- `notification.statusNotification.statusResponses.description` (string)

## Responses

- `202`: Notification accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
