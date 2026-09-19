# Receive the consent status request

`POST /api/v3/hiu/consent/request/on-status`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This API endpoint is used to provide the result of a previously submitted consent request. The status of the request can be one of the following: REQUESTED, DENIED, or EXPIRED. By invoking this API, the Health Information User (HIU) receives the outcome of their consent request, ensuring that they are informed about the current status. This functionality is essential for maintaining transparency and enabling HIUs to take appropriate actions based on the consent status. The API supports secure and compliant health information exchange, facilitating efficient consent management within the healthcare ecosystem.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hiu/consent/request/on-status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "consentRequest": {
    "id": "e5ec415f-c098-40f6-a0db-faa162fc5295",
    "status": "REQUESTED"
  },
  "error": {
    "code": "ABDM-1001",
    "message": "unable to connect database"
  },
  "response": {
    "requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"
  },
  "resp": null
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `consentRequest` (object, required)
- `consentRequest.id` (string, required): The consent request id from a consent. Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\-@,. ":/]{0,255}$"
- `consentRequest.status` (string, required) One of: REQUESTED, DENIED, EXPIRED, REVOKED.
- `error` (object, required): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message
- `response` (object, required)
- `response.requestId` (string, required): The requestId that was passed.Allows alpha numeric character and special characters like ^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}
- `resp` (string, required)

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
