# Send verify OTP

`POST /api/v2/auth/loginViaMobileSendOTP`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/api/v2/auth/loginViaMobileSendOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "4c8c4b29-6d7e-4446-8f73-4574d6d14f09",
  "mobile": "97624XXXXX"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `mobile` (string)
- `txnId` (string)
- `otp` (string)
- `hpid` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "28b4ce41-71df-48af-8b6c-13c30402816c",
  "mobileNumber": "******1234"
}
```
