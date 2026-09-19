# Answer the subscription request notification

`POST /api/hiecm/subscription-requests/v3/hiu/on-notify`

Be invoked by the Health Information User (HIU) to respond to notifications received from the /subscription-requests/hiu/notify API. By using this API, the HIU can acknowledge and process the subscription request notifications, ensuring that the system accurately reflects the status and actions taken. This functionality is essential for maintaining the integrity and synchronization of subscription requests, supporting efficient and transparent health information exchange within the healthcare ecosystem.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/hiu/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "OK",
    "subscriptionRequestId": "f29f0e59-8388-4698-9fe6-05db67aeac46"
  },
  "error": {
    "code": "ABDM-1001",
    "message": "No data found"
  },
  "response": {
    "requestId": "f29f0e59-8388-4698-9fe6-05db67aeac46"
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

- `acknowledgement` (object, required)
- `acknowledgement.status` (string, required): The status of the subscription request. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$":
- `acknowledgement.subscriptionRequestId` (string, required): The subscription request id. This should be from the subscription request. Allows alphanumeric characters and  special characters like "^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}$"
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message
- `response` (object, required)
- `response.requestId` (string): Request id that was passed.  Allows alphanumeric characters and special characters like "^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
