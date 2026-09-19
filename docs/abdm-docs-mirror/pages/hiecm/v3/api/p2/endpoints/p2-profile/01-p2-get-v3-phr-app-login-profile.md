# Get profile

`GET /abha/api/v3/phr/app/login/profile`

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/profile \
  --header 'X-token: Bearer <JWT TOKEN>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

## Headers

- `X-token` (string, required)
- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Responses

- `200`: OK
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "abhaAddress": "<ABHA_ADDRESS>",
  "fullName": "John Doe",
  "firstName": "John",
  "middleName": "",
  "lastName": "Doe",
  "dayOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "yearOfBirth": "<DOB>",
  "dateOfBirth": "<DOB>",
  "gender": "M",
  "email": "<EMAIL>",
  "mobile": "******0903",
  "abhaNumber": "<ABHA_NUMBER>",
  "address": "<ADDRESS>",
  "stateName": "Maharashtra",
  "districtName": "<ADDRESS>",
  "pinCode": "<PINCODE>",
  "stateCode": "27",
  "districtCode": "123",
  "authMethods": [
    "MOBILE_OTP",
    "PASSWORD",
    "... 1 more of the same shape"
  ],
  "status": "ACTIVE",
  "emailVerified": "true",
  "mobileVerified": "true",
  "kycStatus": "VERIFIED",
  "abhaLinkedCount": "3"
}
```
