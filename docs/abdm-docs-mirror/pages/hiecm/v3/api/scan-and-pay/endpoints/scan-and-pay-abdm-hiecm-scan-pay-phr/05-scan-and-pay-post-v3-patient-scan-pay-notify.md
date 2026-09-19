# Notify patient scan pay

`POST /v3/patient/scan-pay/notify`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This is callback API for the notify API. This API needs to implement by HIU to received the payment status. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>X-HIU-ID [Example: HIU_ID] </li><li>Authorisation will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: Bearer <TOKEN> ]</li><li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li>
</ol> </li> <br/> <li> <b>Request Body</b> <ol type='a'><br/><li>acknowledgement This is a key value which contains the payment status abhaAddress transactionId orderNumber paymentRecipetURL[ Example: { status: [SUCCESS, CANCELED, PENDING, FAIL, REFUND_INITIATED, REFUND_SUCCESS] abhaAddress: <ABHA_ADDRESS> transactionId: uniqueId orderNumber: 76274**** openOrderRequestId: 3876e71 paymentDate: 12314 paymentRecipetURL: URL } ]</li> </ol> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/v3/patient/scan-pay/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "SUCCESS/ CANCELED/ PENDING/ FAIL/ REFUND_INITIATED/ REFUND_SUCCESS",
    "abhaAddress": "<username>@sbx",
    "transactionId": "string",
    "orderNumber": "string",
    "openOrderRequestId": "b767614f-153a-4aa3-946f-1622596f0fab",
    "paymentDate": "2025-01-20T07:47:49.102Z",
    "paymentRecipetLink": "PDF URL LINK of RECIPT"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds.
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `acknowledgement` (object, required): The intention of share API call
- `acknowledgement.status` (string, required): Indicates the outcome of the transaction. Possible values are: <br></br>SUCCESS: The transaction was completed successfully. <br></br>FAIL: The transaction failed. <br></br>CANCELED: The transaction was cancelled. <br></br>PENDING: The transaction in pending.<br></br> REFUND_INITIATED: refund initiated.<br></br>REFUND_SUCCESS: refunded successfully
- `acknowledgement.abhaAddress` (string, required): The abha addresss of the user, formatted as <ABHA_ADDRESS>. This is a unique identifier for the user in the health system.
- `acknowledgement.transactionId` (string, required): A unique identifier for the transaction. This helps in tracking and referencing the specific transaction.
- `acknowledgement.orderNumber` (string, required): A unique identifier for the order associated with the transaction. This helps in tracking and referencing the specific order.
- `acknowledgement.openOrderRequestId` (object, required): This is the response request-id which is generated from the share/openOrder api
- `acknowledgement.paymentDate` (string, required): ISO Timestamp.
- `acknowledgement.paymentRecipetLink` (string, required): This attribute holds the URL link to the payment receipt. It is a string that provides a direct link to a PDF document or other format of the receipt for the transaction.

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
