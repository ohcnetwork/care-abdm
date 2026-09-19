# Enrol by Aadhaar

`POST /abha/api/v3/enrollment/enrol/byAadhaar`

Create an ABHA (Ayushman Bharat Health Account) number for an individual using their Aadhaar number. The ABHA number is a unique identifier that helps in authenticating individuals and linking their health records across multiple systems and stakeholders, ensuring that medical records are issued to the correct individual and accessed by authorised Health Information Users with appropriate consent.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "bio"
    ],
    "bio": {
      "aadhaar": "{{encrypted aadhaar number}}",
      "fingerPrintAuthPid": "{{fingerPrintAuthPid}}",
      "mobile": "{{mobile number}}"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `TIMESTAMP` (string, required)
- `REQUEST-ID` (string, required)
- `BENEFIT_NAME` (string): **Applicable for user who is enrolling via Benefit Program.**
- `X-token` (string): **Applicable for child abha creation. X-token of Parent user, user can get X-token after login to the system**

## Body

- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `consent` (object, required)
- `consent.code` (string)
- `consent.version` (string)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful generation and delivery of an OTP (One-Time Password) for various services.<br><br> <strong>Types of OTP Responses:</strong> <ol> <li><strong>Create ABHA by Verifying OTP - Positive Flow:</strong> his API endpoint is used to create an ABHA (Ayushman Bharat Health Account) number by verifying an OTP sent to the user’s registered mobile number. The ABHA number uniquely identifies individuals and helps in authenticating them and linking their health records across multiple systems.</li> </ol> <ol start ="2"> <li><strong>CHILD ABHA - Positive Flow:</strong> This API endpoint is used to create a CHILD ABHA number for a minor using their demographic details. The CHILD ABHA number helps in uniquely identifying minors and linking their health records across multiple systems.</li> </ol> <ol start="3"> <li><strong>CHILD ABHA - Account Already Exists.</strong> This error occurs when an attempt is made to create a CHILD ABHA number for a minor who already has an existing ABHA number.</li> </ol> <ol start ="4"> <li><strong>DemoAuth API - In Case of Existing ABHA Numbe:</strong> This API endpoint is used for the demo authentication of an individual using their Aadhaar number. It verifies the demographic details against the Aadhaar database and generates an ABHA number if the details match. If an ABHA number already exists, it will return the existing ABHA number</li> </ol> <ol start ="5"> <li><strong>DemoAuth API - New ABHA Creation :</strong> This API endpoint is used for the demo authentication of an individual using their Aadhaar number. It verifies the demographic details against the Aadhaar database and generates a new ABHA number if the details match and no existing ABHA number is found.</li> </ol>
- `400`: The 400 response code indicates a bad request. In this context, it refers to various errors encountered during the OTP (One-Time Password) verification process.<br><br> <ol> <li> <p><strong>Create ABHA by Verifying OTP - Invalid Transaction Id:</strong>This API endpoint is used to create an ABHA (Ayushman Bharat Health Account) number by verifying an OTP sent to the user’s registered mobile number. The ABHA number uniquely identifies individuals and helps in authenticating them and linking their health records across multiple systems..</p> </li> </ol> <ol start="2"> <li> <p><strong>Create ABHA by Verifying OTP - Invalid authMethod:</strong> This API endpoint is used to create an ABHA number by verifying an OTP sent to the user’s registered mobile number. The ABHA number uniquely identifies individuals and helps in authenticating them and linking their health records across multiple systems.</p> </li> </ol> <ol start="3"> <li> <p><strong>Create ABHA by Verifying OTP - Invalid Mobile Number:</strong> This API endpoint is used to create an ABHA number by verifying an OTP sent to the user’s registered mobile number. The ABHA number uniquely identifies individuals and helps in authenticating them and linking their health records across multiple systems.</p> </li> </ol> <ol start="4"> <li> <p><strong>DemoAuth API - State District Not Matching - :</strong> This API endpoint is used for the demo authentication of an individual using their Aadhaar number. It verifies the demographic details against the Aadhaar database and generates an ABHA number if the details match.</p> </li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication during the operation of the Invalid Credentials.<br><br> <strong>Types of OTP Response Errors:</strong> <ol> <li><strong>Aadhaar Bio - Invalid Benefit Name</strong>: This error occurs when the access token provided for authorization is invalid. The access token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol> <ol start="2"> <li><strong>DemoAuth API - Invalid Benefit Name</strong>: This error occurs when the access token provided for authorization is invalid. The access token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity..</li> </ol> <ol start="3"> <li><strong>CHILD ABHA - Invalid Benefit Name</strong>: This error occurs when the access token provided for authorization is invalid. The access token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol> <ol start="4"> <li><strong> CHILD ABHA - Access Issue</strong>: This error occurs when the access token provided for authorization is invalid. The access token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol> <ol start="5"> <li><strong>CHILD ABHA - X-token Expired</strong>: This error occurs when the X-token provided for authorization has expired. The X-token is essential for authenticating the request, and an expired token means the server cannot verify the user’s identity.</li> </ol>
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `422`: The 422 response code Indicates an unprocessable entity due to errors such as invalid OTP value.<br><br> <strong>Types of OTP Response Errors:</strong> <ol> <li><strong>Create ABHA by Verifying OTP - Invalid OTP Value</strong>: This API endpoint is used to create an ABHA (Ayushman Bharat Health Account) number by verifying an OTP sent to the user’s registered mobile number. The ABHA number uniquely identifies individuals and helps in authenticating them and linking their health records across multiple systems ,This error occurs when the OTP value provided in the request is invalid. The OTP must be correctly formatted and match the one sent to the user’s registered mobile number.</li> </ol> <ol start="2"> <li><strong>Aadhaar Bio - Invalid Certificate</strong>: This error occurs when the certificate provided for Aadhaar biometric authentication is invalid.</li> </ol> <ol start="3"> <li><strong>DemoAuth API - 6 ABHA Linked to Mobile</strong>: This error occurs when the mobile number provided is already linked to 6 ABHA numbers. The mobile number must be unique or linked to fewer than 6 ABHA numbers.</li> </ol> <ol start="4"> <li><strong>  DemoAuth API - Details Not Matches Against Aadhaar</strong>: This error occurs when the information provided does not match the details on record with Aadhaar. The demographic details must be accurate and match the Aadhaar records.</li> </ol> <ol start="5"> <li><strong>CHILD ABHA - CHILD LIMIT</strong>: This error occurs when the limit for creating or updating CHILD ABHA profiles has been exceeded. The request cannot be processed as the limit has been reached.</li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "This account already exist",
  "txnId": "b89ec10d-71fa-4280-83b3-1fedad66b5f5",
  "tokens": {
    "token": "<TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<TOKEN>",
    "refreshExpiresIn": 1296000
  },
  "ABHAProfile": {
    "firstName": "Username",
    "middleName": "<NAME>",
    "lastName": "<NAME>",
    "dob": "<DOB>",
    "gender": "M",
    "photo": "<BASE64_PHOTO>",
    "mobile": "******0903",
    "phrAddress": [
      "<ABHA_ADDRESS>"
    ],
    "address": "<ADDRESS>",
    "districtCode": "478",
    "stateCode": "27",
    "pinCode": "<PINCODE>",
    "abhaType": "STANDARD",
    "stateName": "MAHARASHTRA",
    "districtName": "<ADDRESS>",
    "ABHANumber": "<ABHA_NUMBER>",
    "abhaStatus": "ACTIVE"
  },
  "isNew": false
}
```
