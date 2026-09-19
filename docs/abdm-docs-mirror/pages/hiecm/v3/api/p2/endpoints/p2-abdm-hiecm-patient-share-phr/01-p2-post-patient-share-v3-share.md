# Share patient share

`POST /api/hiecm/patient-share/v3/share`

This is an API will be invoked from the <b>PHR-HIU</b> to share the user/patient profile with HMIS/LIMS. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>Authorisation will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: <TOKEN> ]</li> <li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li> <li>X-AUTH-TOKEN JWT Authentication token which was issued by ABDM after successful validation of username and password[ Example: <TOKEN> ]</li> <li>X-CM-ID consent manager ID[ Example: sbx ]</li> <li>X-HIU-ID HIU ID[ Example: HIU ]</li> </ol> </li> <br/> <li> <b>Request Body</b> <ol type='a'><br/> <li>intent This is a key value pair which contains the purpose [ Example: {purpose: PROFILE_SHARE } ]</li> <li>metaData This is a key value pair which contains the location longitude and latitude[ Example: {HIP_ID: ABDM_HIP, context: 123, lat: 20.5937 long: 78.9629} ]</li> <li>profile which contains user details.</li> </ol> </ol>

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/hiecm/patient-share/v3/share \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: HIU_ID' \
  --header 'X-AUTH-TOKEN: Bearer <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "intent": "PROFILE_SHARE",
  "metaData": {
    "hipId": "HIP_1",
    "context": "6",
    "hprId": "<EMAIL>",
    "latitude": 20.5937,
    "longitude": 78.9629
  },
  "profile": {
    "patient": {
      "abhaNumber": "<ABHA_NUMBER>",
      "abhaAddress": "<ABHA_ADDRESS>",
      "name": "<NAME>",
      "gender": "M",
      "dayOfBirth": "<DOB>",
      "monthOfBirth": "<DOB>",
      "yearOfBirth": "9999",
      "address": {
        "line": "Address line 1",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "pincode": "<PINCODE>"
      },
      "phoneNumber": "<MOBILE_NUMBER>"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Body

- `intent` (string, required): The intention of share API call One of: PROFILE_SHARE, RECORD_SHARE, PAYMENT_SHARE.
- `metaData` (object, required): A key-value pair carrying the location longitude and latitude.
- `metaData.hipId` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 @//_//-]*[A-Z a-z 0-9]
- `metaData.context` (string, required): This is a counter Id. Allows alpha numeric character and special characters like ^(?:[a-zA-Z0-9 ]|[a-zA-Z0-9 ][a-zA-Z0-9.\\-_ ]*[a-zA-Z0-9 ]){1,250}$
- `metaData.hprId` (string): Healthcare Professionals Registry id. Allows alpha numeric character and special characters like [a-zA-Z0-9][a-zA-Z0-9_.]+[a-zA-Z0-9]@(dr.abdm|hpr.abdm)$|^[1-9][0-9]{13}$
- `metaData.latitude` (number, required): The latitude of the location.Allows alpha numeric character and special characters like ^[0-9-.]+$
- `metaData.longitude` (number, required): The longitude of the location.Allows alpha numeric character and special characters like ^[0-9-.]+$
- `profile` (object, required): This should populated only for PROFILE_SHARE
- `profile.patient` (object, required)
- `profile.patient.abhaNumber` (string): The abha number of the patient. Should be only 14 digit. Allows alpha numeric character and special characters like ^(\\d+-?){13}\\d$
- `profile.patient.abhaAddress` (string, required): The abha address of the patient. Should start with Alphanumeric . and  _  in the middle and must be ending with @abdm or @sbx and Allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.\-!]+[a-zA-Z0-9]@(abdm|sbx)$
- `profile.patient.name` (string, required): The name of the patient. Allows alpha numeric character and special characters like ^[a-zA-Z0-9.-_,]+(([',. -][a-zA-Z0-9. ])?[a-zA-Z0-9. ]*)*$
- `profile.patient.gender` (string, required): The gender of the patient One of: M, F, O, D, T, U.
- `profile.patient.dayOfBirth` (string): The day of birth of the patient. Only allows numeric values between 1 abd 31 and ^(?!\\s*$)(0?[1-9]|[12][0-9]|3[01])$
- `profile.patient.monthOfBirth` (string): The month of birth of the patient. Only allows numeric values between 1 abd 12 and ^(?!\\s*$)(0?[1-9]|[1][0-2])$
- `profile.patient.yearOfBirth` (string, required): The month of birth of the patient. Only allows numeric values and must be 4 digit ranging between 1900 and 2200 and ^(?!\\s*$)(19|20|21|22)\\d{2}$
- `profile.patient.address` (object, required)
- `profile.patient.address.line` (string, required): The address line
- `profile.patient.address.district` (string): The district and should only contain alphabets
- `profile.patient.address.state` (string): The state and should only contain alphabets like [A-Z a-z]+[A-Z a-z //' ']*$
- `profile.patient.address.pincode` (string): Should be 5 digits and only contain numbers
- `profile.patient.phoneNumber` (string, required): The mobile number of the patient. Must be 10 digit and contain only 0-9 and it allows only numbers like ^(\+\d{1,3}[- ]?)?\d{10}$

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `408`: Request Timeout
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `429`: Too Many Requests
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
