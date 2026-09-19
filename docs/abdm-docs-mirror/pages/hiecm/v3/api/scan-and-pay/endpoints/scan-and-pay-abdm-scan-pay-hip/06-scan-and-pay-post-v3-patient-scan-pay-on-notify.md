# Receive the patient scan pay on notify

`POST /v3/patient/scan-pay/on-notify`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This is an callback API for on-notify API need to implement by HIP to received the confirmation of notification. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>Authorisation will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: Bearer <TOKEN> ]</li> <li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li><li>X-HIP-ID [ Example: HIP ID ]</li> </ol> </li> <br/> <li> <b>Request Body</b> <ol type='a'><br/> <li>acknowledgement This is a key value which contains the payment status abhaAddress transactionId orderNumber paymentRecipetURL[ Example: { status: [SUCCESS, CANCELED, PENDING, FAIL, REFUND_INITIATED, REFUND_SUCCESS] abhaAddress: <ABHA_ADDRESS> transactionId: uniqueId orderNumber: 76274**** paymentRecipetURL: URL } ]</li> <li>error is optional object in case of any error or Failure then only send error object</li> <li>response which contains the requestId [ Example: requestId: 059fcb69-8ad8-4789-a049-62db16c7b5a0 ]</li> </ol> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/v3/patient/scan-pay/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds.
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
- `401`: Unauthorized. The request carried no valid credentials, or the access token has expired. Obtain a fresh token from the session API and retry.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/scan-and-pay/errors
