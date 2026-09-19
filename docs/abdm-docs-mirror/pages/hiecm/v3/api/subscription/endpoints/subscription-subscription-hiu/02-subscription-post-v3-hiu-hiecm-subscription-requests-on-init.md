# Receive the HIU subscription requests on init

`POST /api/v3/hiu/hiecm/subscription-requests/on-init`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This API endpoint serves as a callback for the /api/hiecm/subscription-requests/v3/init API. It is used to handle the response from the subscription request initiation process. By invoking this API, the Health Information User (HIU) can receive and process the outcome of the subscription request, ensuring that the system accurately reflects the status and actions taken.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hiu/hiecm/subscription-requests/on-init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "subscriptionRequest": {
    "id": "f29f0e59-8388-4698-9fe6-05db67aeac46"
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
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `subscriptionRequest` (object, required)
- `subscriptionRequest.id` (string): Random generated uniqueid. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `error` (object): Incase of success, error object is optional
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message
- `response` (object, required)
- `response.requestId` (string, required): Request id that was passed. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$

## Responses

- `200`: OK
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
