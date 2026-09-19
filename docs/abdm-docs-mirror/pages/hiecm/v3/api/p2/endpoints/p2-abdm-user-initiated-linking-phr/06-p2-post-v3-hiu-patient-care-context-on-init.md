# Receive the initial linking of care contexts for a patient

`POST /api/v3/hiu/patient/care-context/on-init`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
The on-init API endpoint allows HIUs to receive and process the initial linking of care contexts associated with a patient. When a request is made to this endpoint, it returns a detailed response containing the transaction ID, linking information, authentication details, and any errors that occurred. This ensures that HIUs have the necessary information to manage patient care effectively.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/v3/hiu/patient/care-context/on-init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "f901b782-bfdf-4224-9f8d-da2cadc20c0d",
  "link": {
    "referenceNumber": "d353b782-bfdf-4224-9f8d-da2cadc20c0d",
    "authenticationType": "DIRECT",
    "meta": {
      "communicationMedium": "MOBILE",
      "communicationHint": "OTP",
      "communicationExpiry": "2024-05-01T05:22:34.123Z"
    }
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

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `transactionId` (string, required): UUID from discover request callback to track the entire user link flow
- `link` (object, required)
- `link.referenceNumber` (string, required): The link reference number. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `link.authenticationType` (string, required): The authenticationType. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$" One of: DIRECT, MEDIATED.
- `link.meta` (object, required)
- `link.meta.communicationMedium` (string, required): The communication medium. Allows alpha numeric characters and special characters like"^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$ One of: MOBILE, EMAIL.
- `link.meta.communicationHint` (string, required): The communication hint. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$
- `link.meta.communicationExpiry` (string, required): The communication expiry date. Should be UTC date in ISO format.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message
- `response` (object, required): The request id is from the link/init callback
- `response.requestId` (string, required): The request id that was passed.Allows alpha numeric characters and special characters like "^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
