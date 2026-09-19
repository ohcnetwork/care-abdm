# Enrol ABHA address

`POST /abha/api/v3/phr/app/enrollment/enrol`

Flows in the Postman collection:
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via Mobile › Enrol ABHA Address
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-ABHA OTP › Enrol ABHA Address
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-Aadhaar OTP › Enrol ABHA Address

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/enrol \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "27d444b7-2a3d-46d8-bf67-e5590b6c46b6",
  "phrDetails": {
    "mobile": "<BASE64_PHOTO>",
    "firstName": "John",
    "middleName": "",
    "lastName": "Doe",
    "yearOfBirth": "<DOB>",
    "dayOfBirth": "",
    "monthOfBirth": "<DOB>",
    "gender": "M",
    "email": "",
    "profilePhoto": "",
    "address": "<ADDRESS>",
    "stateName": "Maharashtra",
    "stateCode": "27",
    "districtName": "<ADDRESS>",
    "districtCode": "123",
    "pinCode": "<PINCODE>",
    "abhaAddress": "<ABHA_ADDRESS>",
    "password": "<BASE64_PHOTO>"
  }
}'
```

## Headers

- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Body

- `txnId` (string)
- `phrDetails` (object)
- `phrDetails.mobile` (string)
- `phrDetails.firstName` (string)
- `phrDetails.middleName` (string)
- `phrDetails.lastName` (string)
- `phrDetails.yearOfBirth` (string)
- `phrDetails.dayOfBirth` (string)
- `phrDetails.monthOfBirth` (string)
- `phrDetails.gender` (string)
- `phrDetails.email` (string)
- `phrDetails.profilePhoto` (string)
- `phrDetails.address` (string)
- `phrDetails.stateName` (string)
- `phrDetails.stateCode` (string)
- `phrDetails.districtName` (string)
- `phrDetails.districtCode` (string)
- `phrDetails.pinCode` (string)
- `phrDetails.abhaAddress` (string)
- `phrDetails.password` (string)

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "6907ebb5-ff71-47f9-8052-6dd5554df5df",
  "message": "ABHA Address Created Successfully",
  "phrDetails": {
    "firstName": "John",
    "middleName": "",
    "lastName": "Doe",
    "fullName": "John Doe",
    "dayOfBirth": "<DOB>",
    "monthOfBirth": "<DOB>",
    "yearOfBirth": "<DOB>",
    "dateOfBirth": "<DOB>",
    "gender": "M",
    "email": "<EMAIL>",
    "mobile": "******1234",
    "address": "<ADDRESS>",
    "stateName": "Maharashtra",
    "districtName": "<ADDRESS>",
    "pinCode": "<PINCODE>",
    "abhaAddress": [
      "<ABHA_ADDRESS>",
      "<ABHA_ADDRESS>",
      "... 1 more of the same shape"
    ],
    "stateCode": "27",
    "districtCode": "123"
  },
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<JWT TOKEN>",
    "refreshExpiresIn": 1296000
  }
}
```
