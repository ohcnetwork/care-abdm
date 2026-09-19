# Receive the patients SMS on notify

`POST /api/v3/patients/sms/on-notify`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This API endpoint is a call back API for /api/hiecm/hip/v3/link/patient/links/sms/notify2 <br><br/> <ol> <li>If the SMS trigger is successful, pass the successful message </li> <li>If the SMS trigger is unsuccessful, pass the error message with the error code and message </li> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/patients/sms/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "SUCCESS"
  },
  "error": {
    "code": "ABDM-1024",
    "message": "Dependent service unavailable"
  },
  "response": {
    "requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Body

- `acknowledgement` (object, required)
- `acknowledgement.status` (string, required) One of: SUCCESS, ERRORED.
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1024 - Dependent service unavailable. May be returned either bare (`ABDM-1024`) or with a trailing ": " separator (`ABDM-1024: `); match on the code itself and tolerate the separator.
- `error.message` (string, required)
- `response` (object, required)
- `response.requestId` (string, required): The requestId that was passed

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
