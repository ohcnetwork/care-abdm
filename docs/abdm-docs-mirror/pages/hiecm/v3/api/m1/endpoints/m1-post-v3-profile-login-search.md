# Search ABHA account existence

`POST /abha/api/v3/profile/login/search`

Verify the existence of an Ayushman Bharat Health Account (ABHA) before proceeding with the OTP request for ABHA login. The request body must include the abhaNumber, which the user should provide. If the specified abhaNumber exists, the response will contain the basic details of the corresponding ABHA account.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "ABHANumber": "91-1760-5301-xxxx"
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `ABHANumber` (string, required)

## Responses

- `200`: Successfully retrieved ABHA details.
- `400`: Invalid ABHA number.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Missing Credentials.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: User not found.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Internal Server Error.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "preferredAbhaAddress": "<ABHA_ADDRESS>",
    "ABHANumber": "<ABHA_NUMBER>",
    "authMethods": [
      "DEMOGRAPHICS",
      "AADHAAR_OTP",
      "... 2 more of the same shape"
    ],
    "blockedAuthMethods": [
      "<BLOCKED_AUTH_METHODS>"
    ],
    "status": "ACTIVE",
    "verificationStatus": "VERIFIED",
    "mobile": "**********",
    "verificationType": "AADHAAR",
    "isDocumentAccount": false
  }
]
```
