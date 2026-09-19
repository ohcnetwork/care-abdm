# Verify Aadhaar OTPGet details

`POST /v1/account/reKYC/verifyAadhaarOTPGetDetails`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/reKYC/verifyAadhaarOTPGetDetails \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "authType": "AADHAAR_OTP",
  "hprId": "<HPR_ID>",
  "password": "<PASSWORD>",
  "aadhaar": "<AADHAAR>",
  "mobileNumber": "<MOBILE_NUMBER>",
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11",
  "otp": "<OTP>",
  "resend": false,
  "aadhaarVerifyOtpRequestDto": {
    "aadhaarNumber": "<AADHAAR_NUMBER>",
    "otp": "<OTP>",
    "faceAuthPid": "<FACE_AUTH_PID>",
    "aadhaarLogType": "<AADHAAR_LOG_TYPE>",
    "transactionId": "<TRANSACTION_ID>",
    "txnId": "<TXN_ID>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `authType` (string) One of: AADHAAR_OTP, USERNAME_PASSWORD, MOBILE_OTP.
- `hprId` (string)
- `password` (string)
- `aadhaar` (string)
- `mobileNumber` (string)
- `txnId` (string)
- `otp` (string)
- `resend` (boolean)
- `aadhaarVerifyOtpRequestDto` (object)
- `aadhaarVerifyOtpRequestDto.aadhaarNumber` (string)
- `aadhaarVerifyOtpRequestDto.otp` (string)
- `aadhaarVerifyOtpRequestDto.faceAuthPid` (string)
- `aadhaarVerifyOtpRequestDto.aadhaarLogType` (string)
- `aadhaarVerifyOtpRequestDto.transactionId` (string)
- `aadhaarVerifyOtpRequestDto.txnId` (string)

## Responses

- `200`: OK
- `404`: Not Found
