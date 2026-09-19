# Check the status of reports

`POST /api/hiecm/scan-gateway/v3/patient/scan-pay/order-status`

Check the status of reports. If the notification is not get from HIP then this API will help to check the status on HIU side. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>Authorisation will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: Bearer <TOKEN> ]</li><li>X-AUTH-TOKEN JWT Authentication token which was issued by ABDM after successful validation of user[ Example: Bearer <TOKEN> ]</li><li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li> <li>X-CM-ID consent manager ID[ Example: sbx ]</li> <li>X-HIU-ID [ EXample: HIU_ID]</li></ol> </li> <br/> <li> <b>Request Body</b> <ol type='a'><br/> <li> queryStatus which contains the orderNumber and requestId[ Example: { orderNumber: 39413413 abhaAddress: <ABHA_ADDRESS> openOrderRequestId: 059fcb69-8ad8-***-a049-62db16c7b5a0 } ] </li> </ol> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/scan-pay/order-status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "queryStatus": {
    "orderNumber": "string",
    "abhaAddress": "<ABHA_ADDRESS>",
    "openOrderRequestId": "0d8bd16b-117c-4d07-9916-109fe3a9ab88"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds.
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `queryStatus` (object, required): The queryStatus is used to check the status of a specific order and its associated patient-share request.
- `queryStatus.orderNumber` (string, required): A unique identifier for the order. This helps in tracking and referencing the specific order associated with the query.
- `queryStatus.abhaAddress` (string, required): abha address of the user/patient.
- `queryStatus.openOrderRequestId` (string, required): The request id is generated from the /share/Open Order Request id

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
- `429`: Too Many Requests
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
