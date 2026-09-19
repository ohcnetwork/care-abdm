# Receive the patient on selection

`POST /v3/patient/on-selection`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This is callback API for the on-selection API. This API needs to implement by HIU to received all the select open order payment requests. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>X-HIU-ID [Example: HIU_ID] </li><li>Authorisation will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: Bearer <TOKEN> ]</li> <li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li></ol> </li> <br/> <li> <b>Request Body</b> <ol type='a'><br/> <li>intent This is a key value pair which contains the purpose [ Example: type: PAYMENT_ORDER ]</li> <li>openOrderRequestId from the share open order requestId [ Example: 059fcb69-****-4789-a049-62db16c7b5a0 ]</li> <li>ABHA address of the user</li> <li>error is optional object in case of any error or Failure then only send error object</li> <li>Procedures which contains the list of open order</li> <li>Payment bundle: which contains payment details.</li><li>response which contains the requestId [ Example: requestId: 059fcb69-8ad8-4789-a049-62db16c7b5a0 ]</li></ol> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/v3/patient/on-selection \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "intent": "PAYMENT_ORDER",
  "openOrderRequestId": "b767614f-153a-4aa3-946f-1622596f0fab",
  "abhaAddress": "<ABHA_ADDRESS>",
  "procedures": [
    {
      "category": "OPD consultation",
      "services": [
        {
          "name": "consultation",
          "serviceId": "service-12345",
          "description": "Albumin 24 hrs Urine",
          "amount": 629.12
        }
      ]
    },
    {
      "category": "Laboratory and Diagnostics",
      "services": [
        {
          "name": "Diagnostics",
          "serviceId": "service-12346",
          "description": "Albumin 24 hrs Urine",
          "amount": 629.12
        }
      ]
    },
    {
      "category": "Pharmacy",
      "services": [
        {
          "name": "Pharmacy",
          "serviceId": "service-12347",
          "description": "Albumin 24 hrs Urine",
          "amount": 629.12
        }
      ]
    }
  ],
  "paymentBundle": {
    "paymentMode": "GATEWAY",
    "paymentUrl": "string",
    "orderNumber": "string",
    "amount": "1250.55",
    "merchantId": "123465",
    "description": "Testing"
  },
  "response": {
    "requestId": "b767614f-153a-4aa3-946f-1622596f0fab"
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

- `intent` (string, required): The intention of share API call
- `openOrderRequestId` (object, required): This is the response request-id which is generated from the share api
- `abhaAddress` (string, required)
- `procedures` (object[], required)
- `procedures.category` (string, required): The category of the procedure
- `procedures.services` (object[], required)
- `procedures.services.serviceId` (string): Unique identifier for the service
- `procedures.services.name` (string, required): Name of the service
- `procedures.services.description` (string): Description of the service
- `procedures.services.amount` (number, required): Amount for the service
- `paymentBundle` (object, required): This should be populated for payments
- `paymentBundle.paymentMode` (string, required): Specifies the mode of payment. For example, “GATEWAY” indicates that the payment is processed through a payment gateway
- `paymentBundle.paymentUrl` (string, required): A URL provided by the payment gateway for processing the payment. This is typically a link where the user can complete the payment transaction.
- `paymentBundle.orderNumber` (string, required): A unique identifier for the order associated with the payment. This helps in tracking and referencing the specific transaction.
- `paymentBundle.amount` (string, required): The total amount to be paid. This is usually a numeric value representing the cost of the transaction.
- `paymentBundle.merchantId` (string, required): A unique identifier for the merchant receiving the payment. This ID is used to identify the merchant in the payment system.
- `paymentBundle.description` (string, required): A brief description of the payment or the transaction. This can include details about what the payment is for or any other relevant information.
- `response` (object, required): This is the response request-id which is generated from the share api
- `response.requestId` (string, required)

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
