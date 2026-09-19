# Verify OTP Aadhaar Number, mobile Number, verify via biometric

`POST /abha/api/v3/phr/web/login/abha/verify`

Verify a One-Time Password (OTP) for user authentication, enabling secure access to user profiles. The OTP verification process ensures that only authorised users can log into their profiles, thereby enhancing security.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "41e59beb-6ee7-421e-a844-3652b2482038",
      "otpValue": "{{encryptedOtpValue}}"
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
- `authData.authMethods` (string[])

## Responses

- `200`: The 200 response code indicates a successful request. In this context, the entered OTP was verified, confirming the user’s identity and  the account was  accessed by verified user.<br><br> <li><strong>ABHA Address Verification via Mobile OTP:</strong> This action allows users to verify their ABHA address using an OTP sent to the mobile number registered with their Abha address. This ensures that the user’s ABHA address is securely verified.</li><br><li><strong>ABHA Address Verification via Aadhaar OTP:</strong> This action allows users to verify their ABHA address using an OTP sent to the mobile number registered with their Aadhaar. This ensures that the user’s ABHA address is securely verified.</li><br><li><strong>ABHA Address Verification via Biometric :</strong> This action allows users to verify their ABHA address using Biometric Authentication modes(Fingerprint, Face, Iris) . This ensures that the user’s ABHA address is securely verified.</li>
- `400`: The 400 response code indicates a client error. In this context.<br><br> <strong>Types of OTP Responses:</strong> <ol> <li><strong>Invalid Scope::</strong>The scope of the OTP response is invalid .</li> </ol> <ol start ="2"> <li><strong>Invalid Auth Methods:</strong> The authentication methods used for OTP verification are invalid.</li> </ol> <ol start ="3"> <li><strong>Invalid Transaction Id:</strong> The transaction ID provided for OTP verification is invalid.</li> </ol><ol start ="4"> <li><strong>Biometric Data did not match:</strong> The Biometric data entered in the form of pid did not match with your profile.</li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates a access denial.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "OTP verified successfully",
  "authResult": "success",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "<NAME>",
      "profilePhoto": "<BASE64_PHOTO>",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "VERIFIED"
    }
  ],
  "tokens": {
    "token": "<TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<TOKEN>",
    "refreshExpiresIn": 1296000
  }
}
```
