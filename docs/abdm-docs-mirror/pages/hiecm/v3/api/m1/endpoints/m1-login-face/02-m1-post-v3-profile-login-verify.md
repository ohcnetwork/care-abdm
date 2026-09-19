# Login profile verify

`POST /abha/api/v3/profile/login/verify`

"This API endpoint is used to verify the OTP (One-Time Password) for logging into an ABHA (Ayushman Bharat Health Account) profile. It is used to verify the OTP sent to the user’s registered mobile number or email address for the purpose of logging into their ABHA profile. The OTP is essential for verifying the user’s identity and ensuring secure access to their profile.<br> <br>**Example of OTP Request**<br> <br>Example 1:<br> **Login via ABHA Number - Using Aadhaar OTP:** This endpoint verifies the OTP sent to the user’s registered mobile number for logging into their ABHA profile using their ABHA number and Aadhaar OTP. <br> <br>Example 2:<br> **Login via ABHA Number - Using ABHA OTP:** This endpoint verifies the OTP sent to the user’s registered mobile number for logging into their ABHA profile using their ABHA number and ABHA OTP. <br> <br>Example3:<br> **Verify Password:** This endpoint verifies the user’s password for logging into their ABHA profile.<br> <br>Example 4:<br> **Login via Aadhaar:** verifies the OTP sent to the user’s registered mobile number for logging into their ABHA profile using their Aadhaar number..<br><br> Example 5:<br> **Login via Mobile number:** This endpoint verifies the OTP sent to the user’s registered mobile number for logging into their ABHA profile using their mobile number. <br><br> Example 6:<br> **ABHA PROFILE (Login via Biometric) -** Its used to verify the user’s identity using biometric data (such as fingerprints, face, Iris) for logging into their ABHA profile. The request body should include the scope, authentication methods, and biometric data. <br> <br> For Login via Biometric using face <br> <strong>scope: </strong> <code>ABHA-login</code>, <code> Aadhaar-face-verify </code> <br><br> For Login via Biometric using fingerprint <br> <strong>scope: </strong> <code>ABHA-login</code>, <code> Aadhaar-bio-verify </code> <br><br>For Login via Biometric using Iris <br> <strong>scope: </strong> <code>ABHA-login</code>, <code> Aadhaar-iris-verify </code> <br><br>Example 7:<br> **Find ABHA - Verify OTP:** It is used to verify the OTP to Fetch Complete ABHA Details along with JWT Tokens. <br><br><strong>Note: </strong> OTP will be valid for 10 minute only <br><br>Example 8:<br> **Find ABHA - Verify via Biometric:** It is used to find the ABHA details using Biometric(Fingerprint, Face, Iris) data in the form of PID.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-face-verify"
  ],
  "authData": {
    "authMethods": [
      "face"
    ],
    "face": {
      "txnId": "{{txnId}}",
      "faceAuthPid": "{{PID}}"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `scope` (string[], required)
- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `authData.otp` (object)
- `authData.otp.otpValue` (string, required)
- `authData.otp.txnId` (string, required)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful generation and delivery of an OTP (One-Time Password) for various services.<br><br> <strong>Types of OTP Responses:</strong> <ol> <li><strong>Login via ABHA Number - Using Aadhaar OTP (Positive Flow) :</strong> This endpoint handles the login process via ABHA number using an Aadhaar OTP. If the OTP entered by the user matches the OTP sent by Aadhaar, the system will authenticate the user and display the user's profile along with a JWT token and profile details.</li> <li><strong>Login via ABHA Number - Using ABHA OTP  (Positive Flow) :  </strong>This endpoint handles the login process via ABHA number using an ABHA OTP. If the OTP entered by the user matches the OTP sent by Aadhaar, the system will authenticate the user and display the user's profile along with a JWT token and profile details.</li> <li><strong>Login via Mobile Number - (Positive Flow) :  </strong>This endpoint handles the login process via mobile number using an mobile OTP. If the OTP entered by the user matches the OTP sent by Aadhaar, the system will authenticate the user and display the user's profile along with a JWT token and profile details.</li> <li><strong>Login via Password -  (Positive Flow) : </strong>This endpoint handles the login process via Password using password. If the password(encrypted) entered by the user matches the password already set by user, then the system will authenticate the user and display the user's profile along with a JWT token and profile details.</li> <li><strong>Login via Biometric - FingerPrint/Face/Iris -  (Positive Flow) : </strong>This endpoint handles the login process via encrypted PID. If the pid(encrypted) entered by the user matches the details of the user, then the system will authenticate the user and display the user's profile along with a JWT token and profile details.</li> <li><strong>Forgot ABHA via Aadhaar OTP - Positive Flow:</strong> This scenario describes the process of recovering an ABHA number using an Aadhaar OTP. The user provides their Aadhaar number and the correct OTP received on their registered mobile number. Upon successful verification, the ABHA number is recovered.</li> <li><strong>Forgot ABHA via Mobile OTP - Positive Flow:</strong> This scenario describes the process of recovering an ABHA number using a Mobile OTP. The user provides their registered Mobile number and the correct OTP received on their mobile number. Upon successful verification, the ABHA number is recovered.</li> <li><strong>Find ABHA via Biometric  - Positive Flow:</strong> This scenario describes the process of Finding an ABHA details using a Biometric . The user provides correct Biometric data in the form pid. Upon successful verification, the ABHA number is recovered.</li>
- `400`: Indicates various errors encountered during the search process, such as invalid identifiers or missing parameters.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized Access.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: The requested resource was not found. This can occur if the profile does not exist.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```
