# Verify OTP ReKyc, update Mobile, CHILD ABHA KYC

`POST /abha/api/v3/profile/account/verify`

Verify an OTP (One-Time Password) for various purposes such as ReKyc, Update Mobile,Update Email,Set Password etc. <br> <br>**Example of OTP Request**<br><br>Example1:<br> **Verify Password:** This scenario involves verifying an OTP sent to the user’s registered contact method to verify their password.<br><br>Example2:<br> **Re-KYC:** This scenario involves verifying an OTP sent to the user’s registered contact method to perform re-KYC (Know Your Customer) verification.<br> <br>Example3:<br> **Update Mobile-Verify OTP:** This scenario involves verifying an OTP sent to the user’s new mobile number to update their mobile number in the ABHA profile.<br> <br>Example8:<br> **Update Email-Verify OTP:** This scenario involves verifying an OTP sent to the user’s new email address to update their email address in the ABHA profile.<br> <br>Example9:<br> **Set Password:** This scenario involves setting a new password for the user’s ABHA account.<br> <br>Example10:<br> **Update Old Password:** This scenario involves updating the user’s password using their old password.<br> <br> <br>Example11:<br> **CHILD ABHA KYC - Verify OTP:** This action allows users to complete the KYC verification for a Child ABHA by verifying the OTP sent to the Aadhaar-linked mobile number of the child/guardian. Successful verification completes the Re-KYC process for the Child ABHA account.<br><br><b>Note:</b><br> **1.** OTP will be valid for 10 minute only <br><br>

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "re-kyc"
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

- `X-token` (string, required)
- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `scope` (string[], required)
- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `authData.otp` (object)
- `authData.otp.txnId` (string, required)
- `authData.otp.otpValue` (string, required)
- `reasons` (string[])

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful verification of an OTP (One-Time Password) for various services.<br><br> <strong>Types of OTP Verifications:</strong> <ol> <li><strong>PASSWORD_VERIFY_OTP- Positive Flow : </strong>The 200 response code indicates a successful request. In this context, it refers to the successful verification of the OTP (One-Time Password) for password verification purposes.</li> </ol> <ol start="2"> <li><strong>Re-KYC- Positive Flow :</strong> The 200 response code indicates a successful request. In this context, it refers to the successful completion of the Re-KYC process.</li> </ol> <ol start ="3"> <li><strong>Update Mobile- Positive Flow: </strong> The 200 OK response code indicates a successful request. In this context, it refers to the successful update of the mobile number.</li> </ol> <ol start ="4"> <li><strong>Update Email- Positive Flow:</strong> The 200 OK response code indicates a successful request. In this context, it refers to the successful update of the email address.</li> </ol> <ol start="5"> <li><strong>PASSWORD UPDATE-OLD PASSWORD- Positive Flow:</strong>The 200 OK response code indicates a successful request. In this context, it refers to the successful update of the password when the old password is verified.</li> </ol> <ol start="6"> <li><strong>CHILD ABHA KYC - Verify OTP- Positive Flow:</strong>This action allows users to complete the KYC verification for a Child ABHA by verifying the OTP sent to the Aadhaar-linked mobile number of the child/guardian. Successful verification completes the Re-KYC process for the Child ABHA account.</li> </ol>
- `400`: The 400 response code indicates a bad request. In this context, it refers to various errors encountered during the OTP (One-Time Password) generation or validation process.<br><br> <strong>Types of OTP Response Errors:</strong> <ol> <li><strong>Update Email - Invalid Scope</strong>: The scope of the OTP response is invalid.</li> </ol> <ol start="2"> <li><strong>Update Email- Invalid Auth Methods</strong>: The authentication method provided is invalid.</li> </ol> <ol start="3"> <li><strong>Update Email -Invalid X-token</strong>: The X-token provided is invalid or expired.</li> </ol> <ol start="4"> <li><strong>Update Email -Invalid OTP Value</strong>: The OTP value provided is invalid.</li> </ol> <ol start="5"> <li><strong>Update Mobile -Invalid Transaction Id</strong>: The transaction ID provided is invalid.</li> </ol> <ol start="6"> <li><strong>Update Mobile - Invalid Scope</strong>: The scope of the OTP response is invalid.</li> </ol> <ol start="7"> <li><strong>Update Mobile - Invalid Auth Methods:</strong>: The authentication method provided is invalid..</li> </ol> <ol start="8"> <li><strong>Update Mobile -  Invalid X-token:</strong>: The X-token provided is invalid or expired.</li> </ol> <ol start="9"> <li><strong>Update Mobile-Invalid OTP Value</strong>: The OTP value provided is invalid.</li> </ol> <ol start="10"> <li><strong>Re-KYC- Invalid Transaction Id</strong>: The transaction ID provided is invalid.</li> </ol> <ol start="11"> <li><strong>Re-KYC  - Invalid Transaction Id</strong>: The transaction ID provided is invalid.</li> </ol>  <ol start="12"> <li><strong>Re-KYC- Invalid Auth Method</strong>:  The authentication method provided is invalid..</li> </ol> <ol start="13"> <li><strong>Re-KYC - Invalid X-token</strong>: The X-token provided is invalid or expired.</li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication during the operation of the Invalid Credentials.<br><br> <strong>Types of OTP Response Errors:</strong> <ol> <li><strong>Update Email-X-token expired</strong>: The X-token provided for updating the email address has expired.</li> </ol> <ol start="2"> <li><strong>Update Mobile-Invalid access token</strong>: The access token provided for updating the mobile number is invalid.</li> </ol> <ol start="3"> <li><strong>Update Mobile-X-token expired</strong>: The X-token provided for updating the mobile number has expired.</li> </ol> <ol start="4"> <li><strong>Re-KYC - Invalid access token:</strong>: The access token provided for Re-KYC is invalid.</li> </ol> <ol start="5"> <li><strong>Re-KYC-X-token expired</strong>: The X-token provided for Re-KYC has expired..</li> </ol> <ol start="6"> <li><strong>Password_Set-Invalid access token</strong>:  The access token provided for setting the password is invalid.</li> </ol> <ol start="7"> <li><strong>Password_Set-X-token expired</strong>: The ABHA number provided for ABHA OTP is invalid.</li> </ol> <ol start="8"> <li><strong>PASSWORD_UPDATE-OLD PASSWORD-Invalid access token</strong>: The access token provided for updating the password using the old password is invalid.</li> </ol> <ol start="9"> <li><strong>PASSWORD_UPDATE-OLD PASSWORD-X-token expired</strong>: The X-token provided for updating the password using the old password has expired.</li> </ol>
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `422`: The 422 Unprocessable Entity response for this endpoint indicates that the server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions.<br><br> <strong>Types of OTP Response Errors:</strong> <ol> <li><strong>Re-KYC-Invalid OTP</strong>: The OTP provided for Re-KYC is invalid.</li> </ol> <ol start="2"> <li><strong>PASSWORD VERIFY OTP-Invalid OTP-AADHAAR</strong>: The OTP provided for Aadhaar verification during password verification is invalid.</li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "6e3c1761-8e4c-44a3-929e-32b2c16083d5",
  "authResult": "success",
  "message": "Password updated successfully",
  "accounts": [
    {
      "ABHANumber": "<ABHA_NUMBER>"
    }
  ]
}
```
