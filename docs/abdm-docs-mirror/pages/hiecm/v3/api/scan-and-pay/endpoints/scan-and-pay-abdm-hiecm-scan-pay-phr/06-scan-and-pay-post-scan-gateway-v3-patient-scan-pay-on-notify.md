# Notify to HIP so that confirm that the HIU received the payment status

`POST /api/hiecm/scan-gateway/v3/patient/scan-pay/on-notify`

Notify to HIP so that confirm that the HIU received the payment status. This HIU will confirm the we will received the payment bundle(SUCCESS,CANCELED,PENDING,FAIL,REFUND_INITIATED, REFUND_SUCCESS) from HIP. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>AUTHORIZATION will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: Bearer <TOKEN> ]</li> <li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li><li>X-CM-ID consent manager ID[ Example: sbx ]</li> </ol> </li> <br/> <li> <b>Request Body</b> <ol type='a'><br/> <li>acknowledgement This is a key value which contains the payment status abhaAddress transactionId orderNumber paymentRecipetURL[ Example: { status: [SUCCESS, CANCELED, PENDING, FAIL, REFUND_INITIATED, REFUND_SUCCESS] abhaAddress: <ABHA_ADDRESS> transactionId: uniqueId orderNumber: 76274**** openOrderRequestId: 939**800-325d-42c3-****-1******* paymentDate: 2025-01-20T07:47:49.102Z paymentRecipetURL: URL } ]</li> <li>error is optional object in case of any error or Failure then only send error object</li> <li>response which contains the requestId [ Example: requestId: 059fcb69-8ad8-4789-a049-62db16c7b5a0 ]</li> </ol> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/scan-pay/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds.
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

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
