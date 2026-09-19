# Get user profile details

`GET /abha/api/v3/profile/account`

Manage ABHA (Ayushman Bharat Health Account) profiles. It allows users to fetch the user profile, ensuring that their details are accurate and up-to-date. This is essential for maintaining the integrity and security of the user’s health records.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
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

- `200`: The account information was successfully retrieved or updated.
- `400`: Indicates various errors encountered during the account management process, such as invalid identifiers or missing parameters.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The request was unauthorized. This can occur due to invalid credentials or token.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "ABHANumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>",
  "mobile": "******0903",
  "firstName": "Username",
  "middleName": "<NAME>",
  "lastName": "<NAME>",
  "name": "<NAME>",
  "yearOfBirth": "<DOB>",
  "dayOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "gender": "M",
  "profilePhoto": "<BASE64_PHOTO>",
  "status": "ACTIVE",
  "stateCode": "27",
  "districtCode": "478",
  "pincode": "<PINCODE>",
  "address": "<ADDRESS>",
  "kycPhoto": "<BASE64_PHOTO>",
  "stateName": "MAHARASHTRA",
  "districtName": "<ADDRESS>",
  "subdistrictName": "<ADDRESS>",
  "authMethods": [
    "MOBILE_OTP",
    "AADHAAR_BIO",
    "... 3 more of the same shape"
  ],
  "tags": {},
  "kycVerified": true,
  "verificationStatus": "VERIFIED",
  "verificationType": "AADHAAR",
  "localizedDetails": {
    "name": "<NAME>",
    "stateName": "महाराष्ट्र",
    "districtName": "<ADDRESS>",
    "villageName": "<ADDRESS>",
    "townName": "<ADDRESS>",
    "gender": "पुरुष",
    "localizedLabels": {
      "name": "नाव",
      "abhaNumber": "आभा क्रमांक",
      "abhaAddress": "आभा पत्ता",
      "gender": "लिंग",
      "dob": "जन्मतारीख",
      "mobile": "मोबाईल"
    }
  },
  "createdDate": "07-05-2024"
}
```
