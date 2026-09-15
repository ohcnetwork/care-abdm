# 2. Verify Aadhaar

`POST /api/registration/abha/verify/aadhaar`

Verifies the Aadhaar OTP for a registration transaction and records the person's consent to use Aadhaar for ABHA.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/registration/abha/verify/aadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "aadhaar-gateway"
    ],
    "gateway": {
      "txnId": "<TXN_ID>"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `authData.gateway` (object, required)
- `authData.gateway.txnId` (string, required)
- `consent` (object, required)
- `consent.code` (string, required)
- `consent.version` (string, required)

## Responses

- `200`: No response body is documented for this request.
