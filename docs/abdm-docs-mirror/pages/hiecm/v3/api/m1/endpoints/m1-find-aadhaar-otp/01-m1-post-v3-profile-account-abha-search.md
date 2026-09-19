# Search ABHA profile

`POST /abha/api/v3/profile/account/abha/search`

Search for ABHA (Ayushman Bharat Health Account) profiles. It allows users to retrieve information about their ABHA profiles using mobile numbers. This is essential for verifying the user’s identity and ensuring secure access to their ABHA profile. <br><br> <strong>Note: </strong> You need to use the Encryption API first. Only an RSA-encrypted mobile number should be in the request body.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search-abha"
  ],
  "mobile": "{{rsaMobileEncryptionOutput}}"
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `scope` (string[], required)
- `mobile` (string, required)

## Responses

- `200`: Successfully retrieved ABHA details.
- `400`: Invalid mobile number.
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
    "txnId": "d5b1fb36-e0be-401d-b4cf-cc71c5aca98a",
    "ABHA": [
      {
        "index": 1,
        "ABHANumber": "xx-xxxx-xxxx-XX31",
        "name": "<NAME>",
        "gender": "F",
        "kycVerified": "true",
        "authMethods": [
          "AADHAAR_OTP",
          "MOBILE_OTP",
          "... 2 more of the same shape"
        ]
      }
    ]
  }
]
```
