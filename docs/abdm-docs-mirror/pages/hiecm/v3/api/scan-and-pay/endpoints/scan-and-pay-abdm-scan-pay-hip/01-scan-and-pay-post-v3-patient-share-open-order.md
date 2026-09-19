# Check the status of reports

`POST /v3/patient/share/open-order`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This is an API is called by HIU to check the status of reports. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>Authorisation will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: Bearer <TOKEN> ]</li><li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li> <li>X-HIP-ID [ Example: HIP ID ]</li> </ol> </li> <br/> <li> <b>Request Body</b> <ol type='a'><br/> <li>intent This is a key value pair which contains the purpose [ Example: type: OPEN_PAYMENT_ORDER ]</li> <li>metaData This is a key value pair which contains hipId and counterId[ Example: { hipId: IN3810000008 counterId:12123 } ]</li> <li>profile which contains user details</li> </ol> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/v3/patient/share/open-order \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "intent": "OPEN_PAYMENT_ORDER",
  "metaData": {
    "hipId": "HIP_1",
    "counterId": 1
  },
  "profile": {
    "patient": {
      "abhaNumber": "91-7507-xxxx-xxxx",
      "abhaAddress": "<ABHA_ADDRESS>",
      "name": "name",
      "gender": "M",
      "dayOfBirth": "string",
      "monthOfBirth": "string",
      "yearOfBirth": "string",
      "address": {
        "line": "Address line 1",
        "district": "XXXXXXX",
        "state": "XXXXXX",
        "pincode": "XXXXXX"
      },
      "phoneNumber": "987654xxxx"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds.
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Body

- `intent` (string, required): The intention of share API call
- `metaData` (object, required): A key-value pair carrying the location longitude and latitude.
- `metaData.hipId` (string, required): The service ID of the health information provider
- `metaData.counterId` (number, required): it describes the counterId.
- `profile` (object, required): This should populated only for PAYMENT_SHARE
- `profile.patient` (object, required)
- `profile.patient.abhaNumber` (string, required): The abha number of the patient. Should be only 14 digit
- `profile.patient.abhaAddress` (string, required): The abha address of the patient. Should start with Alphanumeric . and  _  in the middle and must be ending with @abdm or @sbx
- `profile.patient.name` (string, required): The name of the patient. Only alphabets.
- `profile.patient.gender` (string, required): The gender of the patient One of: M, F, O, D.
- `profile.patient.dayOfBirth` (string): The day of birth of the patient. Only allows numeric values between 1 abd 31
- `profile.patient.monthOfBirth` (string): The month of birth of the patient. Only allows numeric values between 1 abd 12
- `profile.patient.yearOfBirth` (string, required): The month of birth of the patient. Only allows numeric values and must be 4 digit ranging between 1900 and 2200
- `profile.patient.address` (object, required)
- `profile.patient.address.line` (string, required): The address line
- `profile.patient.address.district` (string): The district and should only contain alphabets
- `profile.patient.address.state` (string): The state and should only contain alphabets
- `profile.patient.address.pincode` (string): Should be 5 digits and only contain numbers
- `profile.patient.phoneNumber` (string): The mobile number of the patient. Must be 10 digit and contain only 0-9

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
