# Verify- mobile OTP

`POST /abha/api/v3/enrollment/auth/byAbdm`

Verify via Mobile OTP. After verifying OTP successfully mobile will be mobile number will be updated for further communication for perticular ABHA number. 
<br> <br>**Example of OTP Request**<br> **Mobile Update - Verify OTP:** When the user wants to verify the Mobile Number for communication purpose.<br> <br> <br><b>Note:</b><br> **1.**OTP will be valid for 10 minute only <br><br>

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp}}"
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
- `authData.otp` (object, required)
- `authData.otp.txnId` (string, required)
- `authData.otp.otpValue` (string, required)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful generation and delivery of an OTP (One-Time Password) for various services.<br><br> <strong>Types of OTP Responses:</strong> <ol> <li><strong> Mobile Update-Verify OTP-Positive flow:</strong> Indicates a successful request. The response includes a message indicating that the OTP has been verified successfully.</li> </ol> <ol start ="2"> <li><strong>Mobile Update-Verify OTP-OTP Expired:</strong> This error occurs when the OTP provided for verification has expired. The OTP must be used within the valid time frame to ensure secure authentication.</li> </ol>
- `400`: The 400 response code indicates a bad request. In this context, it refers to various errors encountered during the OTP (One-Time Password) verification process.<br><br> <ol> <li> <p><strong>Invalid OTP Value:</strong> This error occurs when the OTP value provided for verification is invalid. The OTP must be correctly formatted and match the one sent to the user’s registered mobile number</p> </li> </ol> <ol start="2"> <li> <p><strong>Invalid Transaction Id:</strong>  This error occurs when the transaction ID provided in the request is invalid. The transaction ID is essential for tracking the OTP request and ensuring that the correct OTP is verified.</p> </li> </ol> <ol start="3"> <li> <p><strong>Invalid Scope:</strong> This error occurs when the scope provided in the OTP verification request for mobile update is invalid. The scope specifies the purpose of the OTP verification, such as abha-enrol, mobile-verify, etc.</p> </li> </ol> <ol start="4"> <li> <p><strong>Invalid AuthMethod - :</strong>  This error occurs when the authentication method provided in the OTP verification request for mobile update is invalid. The authMethods field must contain valid authentication methods such as otp.</p> </li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication during the operation of the Invalid Credentials
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: The 500 response code indicates an Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "23acf181-339d-4771-b532-5c5df4a28d19",
  "authResult": "success",
  "message": "Mobile number is now successfully linked to your Account",
  "accounts": [
    {
      "ABHANumber": "<ABHA_NUMBER>"
    }
  ]
}
```
