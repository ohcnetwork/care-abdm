# Login request OTP

`POST /abha/api/v3/profile/login/request/otp`

"This API endpoint is used to request an OTP (One-Time Password) for logging into an ABHA (Ayushman Bharat Health Account) profile. It is used to send the OTP to the user’s registered mobile number or email address for the purpose of logging into their ABHA profile. The OTP is essential for verifying the user’s identity and ensuring secure access to their profile.<br> <br>**Example of OTP Request**<br> <br>Example 1:<br> **Login via ABHA Number - Using Aadhaar OTP:** This endpoint sends the OTP to the user’s registered mobile number for logging into their ABHA profile using their ABHA number and Aadhaar.<br> <br>Example 2:<br> **Login via ABHA Number - Using ABHA OTP:** This endpoint sends the OTP to the user’s registered mobile number for logging into their ABHA profile using their ABHA number and ABHA number. <br> <br>Example 3:<br> **Login via Aadhaar:** This endpoint sends the OTP to the user’s registered mobile number for logging into their ABHA profile using their Aadhaar number.<br><br> Example 4:<br> **Login via Mobile number:** This endpoint sends the OTP to the user’s registered mobile number for logging into their ABHA profile using their mobile number. <br><br> Example 5:<br> **ABHA PROFILE (Login via Biometric) -** It is used to send the OTP to user registered mobile number for logging into their ABHA profile. The request body should include the scope, loginHint loginId, otpSystem. <br> <br> For Login via Biometric using face <br> <strong>scope: </strong> <code>ABHA-login</code>, <code> Aadhaar-face-verify </code> <br><br> For Login via Biometric using fingerprint <br> <strong>scope: </strong> <code>ABHA-login</code>, <code> Aadhaar-bio-verify </code> <br><br>For Login via Biometric using Iris <br> <strong>scope: </strong> <code>ABHA-login</code>, <code> Aadhaar-iris-verify </code> <br><br>Example 6:<br> **Find ABHA - Send OTP:** It is used to send OTP on user registered Mobile number to fetch complete ABHA Details along with JWT Tokens. <br><br> For requesting an OTP incase of Find ABHA, the loginHint will be <code>index </code> and loginId will be RSA encrypted index key to fetch the complete ABHA details of that particular ABHA number. <br><br>Example 7:<br> **Find ABHA - FingerprintAuth / IrisAuth:** It is used to request Biometric authentication (Fingerprint/Iris) to fetch complete ABHA Details along with JWT Tokens. <br><br> For authentication request incase of Find ABHA, the loginHint will be <code>index </code> and loginId will be RSA encrypted index key to fetch the complete ABHA details of that particular ABHA number. <br><br>Example:8<br> **Find ABHA - FaceAuth:** This API will help to generate transaction ID. This transaction ID will be used for whole face authentication process. <br><br> The user can submit this transaction ID to the <strong>ABHA</strong> app using either intent-based sharing or by generating a QR code. <br><br>User can use this transaction ID to generate QR code using any QR generator tool. Open ABHA app and scan this QR code on ABHA App to start and complete the face capture process.<br><br>The data format of the QR code should follow this pattern: <br>https://<PHR-env-base-URL>/face-auth?txnId=<txn-ID-from-the-response-of-init-API>. <br><br><strong>For example:</strong> "https://phrsbx.ABDM.gov.in/face-auth?txnId=bac7251b-cd25-44d5-9707-f3d2ba181c1c" <br><br> For Sandbox - PHR-env-base-URL - https://phrsbx.ABDM.gov.in<br> For Production - PHR-env-base-URL - https://phr.ABDM.gov.in <br><br><strong>Note: </strong> OTP will be valid for 10 minute only <br><br>

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "search-abha",
    "aadhaar-bio-verify"
  ],
  "loginHint": "index",
  "loginId": "{{rsaIndexEncryptionOutput}}",
  "otpSystem": "aadhaar",
  "txnId": "{{searchTxnId}}"
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

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful generation and delivery of an OTP (One-Time Password) for various services.<br><br> <strong>Types of OTP Responses:</strong> <ol> <li><strong>Login Via Mobile Number - Positive flow:</strong> This action allows users to log in to their ABHA (Ayushman Bharat Health Account) using their mobile number. An OTP (One-Time Password) is sent to the provided mobile number. This ensures that the user’s identity is securely verified before granting access to their ABHA profile.</li> <br> <li><strong>Login Via ABHA Number using ABHA OTP - Positive flow:</strong> This action allows users to log in to their ABHA using their ABHA Number. An OTP is sent to the mobile number registered with the ABHA Number. This ensures that the user’s identity is securely verified before granting access to their ABHA profile.</li> </ol> <ol start="3"> <li><strong>Login Via ABHA Number - Using Aadhaar OTP-positive flow:</strong> This action allows users to log in to their ABHA using their Aadhaar Number. An OTP is sent to the mobile number registered with the aadhaar Number. This ensures that the user’s identity is securely verified before granting access to their ABHA profile.</li> </ol> <ol start ="4"> <li><strong>Login via Aadhaar- Positive Flow.</strong> This action allows users to log in to their ABHA using their Aadhaar number. An OTP is sent to the mobile number registered with the Aadhaar. This ensures that the user’s identity is securely verified before granting access to their ABHA profile.</li> </ol> <ol start ="5"> <li><strong>Forgot ABHA via Mobile OTP- Positive flow:</strong> This action allows users to retrieve their ABHA number by sending an OTP to the mobile number registered with their ABHA profile. This ensures that the user’s identity is securely verified before retrieving the ABHA number</li> <br> <li><strong>Forgot ABHA via Aadhaar OTP- Positive Flow:</strong>  This action allows users to retrieve their ABHA number by sending an OTP to the mobile number registered with their Aadhaar. This ensures that the user’s identity is securely verified before retrieving the ABHA number.</li> <br>
- `400`: Indicates various errors encountered during the OTP generation process .<br><br> <strong>Types of OTP Responses:</strong> <ol> <li><strong>Login Via Mobile Number - Invalid LoginHint:</strong> This action attempts to log in to ABHA (Ayushman Bharat Health Account) using an invalid loginHint. The loginHint provided does not match the expected values.</li> <li><strong>Login Via ABHA Number - Using ABHA OTP - Invalid Scope</strong>  This action attempts to log in to ABHA using an invalid scope. The scope provided does not match the expected values for the OTP request.</li> </ol> <ol start ="2"> </ol>  <ol start ="3"></li> <li><strong>Login via Aadhaar - Invalid Login Hint:</strong> This action attempts to log in to ABHA using an invalid loginHint. The loginHint provided does not match the expected values.</li> <li><strong>Login via Aadhaar OTP - Invalid Scope:</strong> This action attempts to log in to ABHA using an invalid scope. The scope provided does not match the expected values for the OTP request</li> <li><strong>Login via Aadhaar OTP - Invalid LoginId:</strong> This action attempts to log in to ABHA using an invalid loginId. The loginId provided does not match the expected format or value</li> <li><strong>Login via Aadhaar OTP - Invalid Login Hint:</strong> This action attempts to log in to ABHA using an invalid loginHint. The loginHint provided does not match the expected values</li> <li><strong>Login Via ABHA Number - Using ABHA OTP - Invalid LoginHint:</strong>  This action attempts to log in to ABHA using an invalid loginHint. The loginHint provided does not match the expected values</li> <li><strong>Login Via ABHA Number - Using ABHA OTP - Invalid LoginId:</strong> This action attempts to log in to ABHA using an invalid loginId. The loginId provided does not match the expected format or value.</li> <li><strong>Login via Aadhaar - Invalid Scope:</strong> This action attempts to log in to ABHA using an invalid scope. The scope provided does not match the expected values for the OTP request.</li>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication during the operation of the Invalid Credentials.<br><br> <strong>Types of OTP Response Errors:</strong> <ol> <li><strong>Login Via Mobile Number - Invalid Access Token</strong>: This action attempts to log in to ABHA (Ayushman Bharat Health Account) using a mobile number, but fails due to an invalid access token. The access token provided for authorization is invalid, meaning the server cannot verify the user’s identity.</li> </ol> <ol start="2"> <li><strong>Login via Aadhaar - Invalid Access Token</strong>:  This action attempts to log in to ABHA using an Aadhaar number, but fails due to an invalid access token. The access token provided for authorization is invalid, meaning the server cannot verify the user’s identity.</li> </ol> </ol> <ol start="3"> <li><strong>Login Via ABHA Number - Using ABHA OTP - Invalid Access Token</strong>:This action attempts to log in to ABHA using an ABHA number and ABHA OTP, but fails due to an invalid access token. The access token provided for authorization is invalid, meaning the server cannot verify the user’s identity.</li> </ol> <ol start="4"> <li><strong>Login Via ABHA Number - Using Aadhaar OTP - Invalid Access Token</strong>: This action attempts to log in to ABHA using an ABHA number and Aadhaar OTP, but fails due to an invalid access token. The access token provided for authorization is invalid, meaning the server cannot verify the user’s identity..</li> </ol>
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
  "message": "OTP sent to Aadhaar registered mobile number ending with ******0903"
}
```
