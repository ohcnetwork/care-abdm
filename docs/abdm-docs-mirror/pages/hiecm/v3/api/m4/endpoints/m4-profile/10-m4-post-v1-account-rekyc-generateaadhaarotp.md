# Generate Aadhaar OTPFor re KYC

`POST /v1/account/reKYC/generateAadhaarOTP`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/reKYC/generateAadhaarOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Responses

- `200`: OK
- `404`: Not Found
