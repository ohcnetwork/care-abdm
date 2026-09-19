# Send OTP ReKyc, update Mobile, child ABHA KYC request OTP

`POST /abha/api/v3/profile/account/request/otp`

Request an OTP (One-Time Password) for verifying an ABHA (Ayushman Bharat Health Account) profile. The OTP is sent to the user’s registered mobile number or email address, ensuring secure access to their ABHA profile. This is essential for verifying the user’s identity and ensuring secure access to their ABHA profile.<br> <br>**Example of OTP Request**<br> <br>Example1:<br> **Update Email:** This action allows users to update their email address by sending an OTP to the new email address. The OTP is essential for verifying the user’s identity and ensuring secure access to their profile. <br> <br>Example2:<br> **Update Mobile:** This action allows users to update their mobile number by sending an OTP to the new mobile number. The OTP is essential for verifying the user’s identity and ensuring secure access to their profile. <br> <br>Example3:<br> **Re-KYC - Send OTP:** This action allows users to re-verify their KYC (Know Your Customer) details by sending an OTP to the registered mobile number linked with their Aadhaar. The OTP is essential for verifying the user’s identity and ensuring secure access to their profile.<br><br> <br>Example8:<br> **PASSWORD_UPDATE_REQUEST_OTP - Aadhaar:** This action allows users to request an OTP for updating their password using their Aadhaar number. The OTP is essential for verifying the user’s identity and ensuring secure password updates. "<br><br><br>Example9:<br> **CHILD ABHA KYC - Request OTP:** This action allows users to initiate KYC verification for a Child ABHA by requesting an OTP on the Aadhaar-linked mobile number of the child/guardian. This OTP is used to complete the Re-KYC process for a Child ABHA account and ensure the linked Aadhaar details are verified.<br><br><b>Note:</b><br> **1.**OTP will be valid for 10 minute only <br><br>

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/otp \
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
  "loginHint": "aadhaar",
  "loginId": "{{encrypted aadhaar number}}",
  "otpSystem": "aadhaar"
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
- `loginHint` (string, required)
- `loginId` (string, required)
- `otpSystem` (string, required)

## Responses

- `200`: The OTP was successfully sent to the user’s registered contact method.<br><br> <strong>Types of OTP Responses:</strong> <ol> <li><strong>Update Mobile - Positive Flow:</strong> This action allows users to update their mobile number by sending an OTP to the new mobile number. The OTP is essential for verifying the user’s identity and ensuring secure access to their profile.</li> </ol> <ol start ="2"> <li><strong>Re-KYC- Positive Flow:</strong> This action allows users to re-verify their KYC (Know Your Customer) details by sending an OTP to the registered mobile number linked with their Aadhaar. The OTP is essential for verifying the user’s identity and ensuring secure access to their profile.</li> </ol> <ol start="3"> <li><strong>Update Email- Positive flow.</strong> This action allows users to update their email address by sending an OTP to the new email address. The OTP is essential for verifying the user’s identity and ensuring secure access to their profile</li> </ol><ol start ="4"> <li><strong> Change Password via ABHA OTP- Positive Flow:</strong>This action allows users to request an OTP for updating their password using their ABHA (Ayushman Bharat Health Account) number. The OTP is sent to the mobile number registered with the ABHA number. Upon successful verification of the OTP, the user can proceed to update their password.</li> </ol> <ol start ="5"> <li><strong> Change Password via Aadhaar OTP- Positive Flow:</strong>This action allows users to request an OTP for updating their password using their Aadhaar number. The OTP is sent to the mobile number registered with the Aadhaar Number. Upon successful verification of the OTP, the user can proceed to update their password.</li> </ol> <ol start= "6"><li>**CHILD ABHA KYC - Positive Flow** This action allows users to initiate KYC verification for a Child ABHA by requesting an OTP on the Aadhaar-linked mobile number of the child/guardian. This OTP is used to complete the Re-KYC process for a Child ABHA account and ensure the linked Aadhaar details are verified.<br></li></ol>
- `400`: The request was invalid. This can occur due to various reasons such as invalid login ID, invalid scope, etc. <br><br> <strong>Types of OTP Responses </strong><ol start="1"> <li><strong>Update Email - Invalid LoginId.</strong> This error occurs when the login ID provided for the email update OTP is invalid. The login ID should be the encrypted email address.</li> </ol><ol start ="2"> <li><strong>Update Email- Invalid Login Hint:</strong>This error occurs when the login hint provided for the email update OTP is invalid. The login hint should indicate the type of identifier being used, such as email.</li> </ol> <ol start="3"> <li><strong>Update Email- Invalid X-token.</strong> This error occurs when the X-token provided for the email update OTP is invalid. The X-token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol> <ol start ="4"> <li><strong>Update Mobile- Invalid LoginId:</strong> This error occurs when the login ID provided for the mobile update OTP is invalid. The login ID should be the encrypted mobile number.</li> </ol> <ol start="5"> <li><strong>Update Mobile- Invalid Login Hint.</strong> This error occurs when the login hint provided for the mobile update OTP is invalid. The login hint should indicate the type of identifier being used, such as mobile.</li> </ol> <ol start ="6"> <li><strong>Update Mobile- Already verified mobile number :</strong> This OTP is generated for authentication or verification purposes related to DL,the unique identification number issued by the Indian government</li> </ol> <ol start="7"> <li><strong>Update Mobile-Invalid Scope.</strong> This error occurs when the scope provided in the OTP request for mobile update is invalid. The scope specifies the purpose of the OTP request, such as abha-enrol, mobile-verify, etc.</li> </ol> <ol start ="8"> <li><strong>Update Mobile - Already Verified Mobile Number:</strong> This error occurs when the mobile number provided for the update is already verified. The system recognizes that the mobile number is already linked and verified with the user’s profile.</li> </ol> <ol start="9"> <li><strong>ReKyc - Invalid Scope.</strong> This error occurs when the scope provided in the OTP request for re-KYC is invalid. The scope specifies the purpose of the OTP request, such as re-kyc, kyc-update, etc.</li> </ol> <ol start ="10"> <li><strong>ReKyc - Invalid X-token:</strong> This error occurs when the X-token provided for the re-KYC OTP is invalid. The X-token is essential for authenticating the request, and an invalid token means the server cannot verify the user’s identity.</li> </ol> <ol start="11"> <li><strong>ReKyc- Invalid LoginId.</strong> This error occurs when the login ID provided for the re-KYC OTP is invalid. The login ID should be the encrypted identifier, such as Aadhaar number or mobile number.</li> </ol> <ol start ="12"> <li><strong>ReKyc - Invalid Login Hint:</strong> This error occurs when the login hint provided for the re-KYC OTP is invalid. The login hint should indicate the type of identifier being used, such as Aadhaar or mobile.</li> </ol> <ol start="13"> <li><strong>Password_Update_Request_OTP_Aadhaar-Invalid Scope.</strong> This error occurs when the scope provided in the OTP request for updating the password using Aadhaar is invalid. The scope specifies the purpose of the OTP request, such as password-update, aadhaar-verify, etc.</li> </ol> <ol start ="14"> <li><strong>Password_Update_Request_OTP_Aadhaar-Invalid LoginId:</strong> This OTP is generated for authentication or verification purposes related to DL, the unique identification number issued by the Indian government</li> </ol> <ol start="15"> <li><strong>Password_Update_Request_OTP_Aadhaar-Invalid LoginHint.</strong> This error occurs when the login ID provided for the password update OTP using Aadhaar is invalid. The login ID should be the encrypted Aadhaar number.</li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The request was unauthorized. This can occur due to invalid credentials or token.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Internal Server Error               .
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "c2095ea0-52ed-44ee-b8fc-02375b874e7a",
  "message": "OTP is sent to Aadhaar registered mobile number ending with *******0903"
}
```
