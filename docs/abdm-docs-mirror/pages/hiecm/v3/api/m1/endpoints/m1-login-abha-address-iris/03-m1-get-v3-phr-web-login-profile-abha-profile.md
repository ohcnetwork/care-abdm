# Retrieve the user’s ABHA profile

`GET /abha/api/v3/phr/web/login/profile/abha-profile`

Retrieve the user’s ABHA (Ayushman Bharat Health Account) profile. Access to this profile is granted after the successful verification of the OTP, ensuring the user’s profile information is secure.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha-profile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `X-token` (string, required)
- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it signifies that the user was successfully verified with the OTP in the previous API call. A valid JWT token was provided, which authenticated the user and allowed access to their profile. As a result, the user profile was successfully retrieved, including all ABHA profile details.
- `400`: A  Bad Request error with the description “invalid X-token”  indicates that the server received a request with an invalid or missing authentication token.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates that the request was not authorized due to invalid credentials. Ensure that your API invocation includes the appropriate authorization header.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "abhaAddress": "<ABHA_ADDRESS>",
  "fullName": "<NAME>",
  "profilePhoto": "<BASE64_PHOTO>",
  "firstName": "<NAME>",
  "middleName": "<NAME>",
  "lastName": "<NAME>",
  "dayOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "yearOfBirth": "<DOB>",
  "dateOfBirth": "<DOB>",
  "gender": "M",
  "email": "<EMAIL>",
  "mobile": "<MOBILE_NUMBER>",
  "abhaNumber": "<ABHA_NUMBER>",
  "address": "<ADDRESS>",
  "stateName": "MAHARASHTRA",
  "pinCode": "<PINCODE>",
  "stateCode": "27",
  "districtCode": "487",
  "authMethods": [
    "AADHAAR_OTP",
    "MOBILE_OTP"
  ],
  "status": "ACTIVE",
  "subDistrictCode": "",
  "subDistrictName": "",
  "emailVerified": "false",
  "mobileVerified": "true",
  "kycStatus": "VERIFIED"
}
```
