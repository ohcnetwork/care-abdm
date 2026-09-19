# Generate mobile OTP

`POST /v1/registration/aadhaar/generateMobileOTP`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/registration/aadhaar/generateMobileOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "mobile": "981065XXXX",
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `mobile` (string)
- `txnId` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "951b4258-2ac7-432c-8dbf-6ed990757b88",
  "mobileNumber": null
}
```
