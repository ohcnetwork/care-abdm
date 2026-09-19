# Receive the patient on-share

`POST /v3/patient/on-share/open-order`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This is a callback API for patient on-share. This API needs to implement by HIU for receive all the open order. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>Authorisation will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: Bearer <TOKEN> ]</li><li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li><li>X-HIU-ID [Example: HIU_ID]
</ol></li><br/><li> <b>Request Body</b> <ol type='a'><br/> <li>intent This is a key value pair which contains the purpose [ Example: type: OPEN_PAYMENT_ORDER ]</li> <li>ABHA Address of the user/patient.</li> <li>error is optional object in case of any error or Failure then only send error object</li> <li>Procedures which contains the list of open order</li><li>response which contains the requestId [ Example: resquestId: 059fcb69-8ad8-4789-a049-62db16c7b5a0 ]</li> </ol> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/v3/patient/on-share/open-order \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "intent": "OPEN_PAYMENT_ORDER",
  "abhaAddress": "<ABHA_ADDRESS>",
  "patientUid": "string5",
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
    },
    {
      "category": "Miscellaneous/Other",
      "services": [
        {
          "name": "Miscellaneous",
          "serviceId": "service-12348",
          "description": "Albumin 24 hrs Urine",
          "amount": 629.12
        }
      ]
    }
  ],
  "response": {
    "requestId": "6c3d4e5c-09d1-4ecc-817b-a0c82d130c53"
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
- `abhaAddress` (string, required): The abha address of the patient. Should start with Alphanumeric . and _ in the middle and must be ending with @abdm or @sbx
- `patientUid` (string, required)
- `procedures` (object[], required)
- `procedures.category` (string, required): The category of the procedure
- `procedures.services` (object[], required)
- `procedures.services.serviceId` (string): Unique identifier for the service
- `procedures.services.name` (string, required): Name of the service
- `procedures.services.description` (string): Description of the service
- `procedures.services.amount` (number, required): Amount for the service
- `response` (object): This is the response request-id which is generated from the share API
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
