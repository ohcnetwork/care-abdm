# Receive the health information data request acknowledgement to HIU

`POST /api/v3/hiu/health-information/on-request`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
Callback API for acknowledgment of Health information request of HIU. CM calls this API when it has validated the Health Information request given the consent ID.<br> Either the hiRequest or error would need to be specified. If the health info request was valid, then the hiRequest.transactionId specifies the transaction context against which HIP would send over the data.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hiu/health-information/on-request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiRequest": {
    "transactionId": "18235d89-cb13-479d-ad71-7a57d5f669a8",
    "sessionStatus": "REQUESTED"
  },
  "error": {
    "code": "ABDM-1001",
    "message": "unable to connect database"
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
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `hiRequest` (object, required)
- `hiRequest.transactionId` (string, required): The UUID generated when the health information request was initiated.
- `hiRequest.sessionStatus` (string, required): The status of the health information request that was initiated.
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message
- `response` (object, required)
- `response.requestId` (string, required): The requestId that was passed. Allows alpha numeric character and special characters like ^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized. The request carried no valid credentials, or the access token has expired. Obtain a fresh token from the session API and retry.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
