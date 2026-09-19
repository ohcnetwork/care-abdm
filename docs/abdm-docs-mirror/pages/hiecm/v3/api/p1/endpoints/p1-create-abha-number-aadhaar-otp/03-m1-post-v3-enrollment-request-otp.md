# Request enrolment OTP

`POST /abha/api/v3/enrollment/request/otp`

Generate and send an OTP (One-Time Password) to the user’s registered mobile number. The OTP is essential for verifying the user’s identity and ensuring secure access to the ABHA (Ayushman Bharat Health Account) enrolment process. Depending on the type of identifier provided (Aadhaar Number, ABHA Number, or Mobile Number), the OTP will be generated and sent to the corresponding registered mobile number.
<br> <br> </ol>**Usage of this API for below scenarios: OTP Request**<br><br> **1. AADHAR OTP:**When the user wants to enrol using their Aadhar Number, an OTP is sent to the mobile number registered with their Aadhar linked mobile number. For this pass loginHint as "Aadhar-number". <br> **2. Mobile OTP:** When the user wants to enrol using their Mobile Number, an OTP is sent to the provided mobile number. For this pass loginHint as "mobile-number".<br><b>Note:</b><br> **1.**OTP will be valid for 10 minute only <br><br>

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "{{encrypted mobileNumber}}",
  "otpSystem": "abdm"
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `scope` (string[], required)
- `loginHint` (string, required)
- `loginId` (string, required)
- `otpSystem` (string, required)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful generation and delivery of an OTP (One-Time Password) for various services.<br><br> <strong>Types of OTP Responses:</strong> <ol> <li><strong>AADHAAR OTP Response:</strong> This OTP is generated for authentication or verification purposes related to AADHAAR, the unique identification number issued by the Indian government.</li> </ol> <ol start ="2"> <li><strong>ABHA OTP Response:</strong> This OTP is generated for authentication or verification purposes related to ABHA (Ayushman Bharat Health Account), which is part of India’s health ID system</li> </ol> <ol start="3"> <li><strong>Mobile OTP Response.</strong> This OTP is generated for general mobile number verification purposes, such as logging into an account, completing a transaction, or verifying identity</li> </ol> <ol start ="4"> <li><strong>Email OTP Response:</strong> This OTP is generated for verification purposes of Email, the OTP is send to the registered email address </li> </ol>
- `400`: The 400 response code indicates a bad request. In this context, it refers to various errors encountered during the OTP (One-Time Password) generation or validation process.<br><br> <strong>Types of OTP Response Errors:</strong> <ol> <li><strong>ABHA enrolment via Aadhar - Invalid Scope</strong>: This error occurs when the scope provided in the OTP request is invalid. The scope specifies the purpose of the OTP request, such as abha-enrol, mobile-verify, etc.</li> </ol> <ol start="2"> <li><strong>ABHA enrolment via Aadhar  -Send OTP- Invalid LoginId</strong>: This error occurs when the login ID provided for the Aadhaar OTP is invalid. The login ID should be the encrypted Aadhaar number.</li> </ol> <ol start="3"> <li><strong>Mobile Update -Send OTP- Invalid Scope</strong>:  This error occurs when the scope provided in the OTP request for mobile update is invalid.</li> </ol> <ol start="4"> <li><strong>Mobile Update -Send OTP- Invalid LoginId</strong>: This error occurs when the login ID provided for the mobile OTP is invalid. The login ID should be the encrypted mobile number.</li> </ol> <ol start="5"> <li><strong>Mobile Update -Send OTP- Invalid LoginHint</strong>: This error occurs when the login hint provided for the mobile OTP is invalid. The login hint should indicate the type of identifier being used, such as mobile.</li> </ol>  <ol start="6"> <li><strong>ABHA Creation via Aadhar- Invalid Scope</strong>: This error occurs when the scope provided in the OTP request for ABHA creation via Aadhaar is invalid.</li> </ol> <ol start="7"> <li><strong>ABHA Creation via Aadhar- Invalid Login Hint</strong>: This error occurs when the login hint provided for the Aadhaar OTP is invalid. The login hint should indicate the type of identifier being used, such as aadhaar.</li> </ol> <ol start="8"> <li><strong>ABHA enrolment via Aadhar  - Invalid Scope</strong>: The scope of the OTP response is invalid.</li> </ol><ol start="9"> <li><strong>ABHA Verify via Email- Invalid Scope</strong>: This error occurs when the scope provided in the OTP request for ABHA creation via email is invalid.</li> </ol> <ol start="10"> <li><strong>ABHA Verify via Email- Invalid Login Hint</strong>: This error occurs when the login hint provided for the email OTP is invalid. The login hint should indicate the type of identifier being used, such as aadhaar.</li> </ol> <ol start="11"> <li><strong>ABHA Verify via Email  - Invalid LoginHint</strong>: This error occurs when the email ID provided for the email OTP is invalid. The login ID should be the encrypted email address..</li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication during the operation of the Invalid Credentials <br><br> <strong>Types of OTP Response Errors:</strong> <ol> <li><strong>ABHA Enrolment via Aadhaar - Invalid Access Token</strong>: This error occurs when the access token provided for authorization is invalid. The access token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol> <ol start="2"> <li><strong>Mobile Update - Send OTP - Invalid Access Token</strong>: This error occurs when the access token provided for authorization is invalid. The access token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol> <ol start="3"> <li><strong>ABHA Creation via Aadhaar OTP - Invalid Access Token</strong>:  This error occurs when the access token provided for authorization is invalid. The access token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol> <ol start="4"> <li><strong>EMail verification via  OTP - Invalid Access Token</strong>:  This error occurs when the access token provided for authorization is invalid. The access token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol>
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "c6a49f66-c740-4a7d-a93d-8c0431bbb8f3",
  "message": "OTP is sent to Aadhaar registered mobile number ending with*******0903"
}
```
