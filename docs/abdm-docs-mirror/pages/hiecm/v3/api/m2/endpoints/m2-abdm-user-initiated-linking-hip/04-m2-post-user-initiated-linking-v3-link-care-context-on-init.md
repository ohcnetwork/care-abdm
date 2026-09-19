# Link care context on init

`POST /api/hiecm/user-initiated-linking/v3/link/care-context/on-init`

Share the response of the /api/hiecm/user-initiated-linking/v3/link/care-context/on-init API. By using this API, the HIP communicates the outcome of the care context linking process, ensuring that the system accurately reflects the status of the operation. This process is essential for maintaining the integrity and synchronization of patient health records, supporting seamless and efficient health information exchange within the healthcare ecosystem.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/user-initiated-linking/v3/link/care-context/on-init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
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

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Body

- `transactionId` (string, required): UUID from discover request callback to track the entire user link flow.
- `link` (object, required)
- `link.referenceNumber` (string, required): The link reference number. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `link.authenticationType` (string, required): The type of authentication.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$" One of: DIRECT, MEDIATED.
- `link.meta` (object, required)
- `link.meta.communicationMedium` (string, required): The communication medium. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$" One of: MOBILE, EMAIL.
- `link.meta.communicationHint` (string, required): The communication hint. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `link.meta.communicationExpiry` (string, required): The communication expiry date. Should be UTC date in ISO format. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `response` (object, required): The request id is from the link/init callback. Allows alpha numeric characters and special characters like "^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
- `response.requestId` (string, required): The request id that was passed

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
