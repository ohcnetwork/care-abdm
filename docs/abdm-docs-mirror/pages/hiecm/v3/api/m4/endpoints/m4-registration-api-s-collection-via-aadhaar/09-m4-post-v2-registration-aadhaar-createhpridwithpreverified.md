# Create HPR ID V2

`POST /v2/registration/aadhaar/createHprIdWithPreVerified`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v2/registration/aadhaar/createHprIdWithPreVerified \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "idType": "hpr_id",
  "domainName": "@hpr.abdm",
  "email": "<ABHA_ADDRESS>.com",
  "firstName": "Ayushman",
  "middleName": "Bharat",
  "lastName": "Mission",
  "password": "Ayushman@143",
  "profilePhoto": "<BASE64 ENCODED STRING>",
  "txnId": "c3b0c27d-e19d-4244-b8bb-3fa19285054a",
  "hprId": "<EMAIL>",
  "sourceType": "DRIVING_LICENSE",
  "hpCategoryCode": 1,
  "hpSubCategoryCode": 1,
  "clientId": "V4",
  "stateCode": "<STATE_CODE>",
  "districtCode": "<DISTRICT_CODE>",
  "council": false,
  "role": 0
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `idType` (string)
- `domainName` (string)
- `email` (string, required): Email Address of the user.
- `firstName` (string): First Name of the user).
- `middleName` (string): Middle name of the user
- `lastName` (string): Last name of the user
- `password` (string): Passwords for authentication
- `profilePhoto` (string): Profile photo of the user (Uploaded by the user).
- `txnId` (string, required): Transaction ID
- `hprId` (string): Healthcare Professional ID Alias.
- `sourceType` (string) One of: DRIVING_LICENSE, AADHAAR.
- `hpCategoryCode` (integer)
- `hpSubCategoryCode` (integer)
- `clientId` (string)
- `stateCode` (string)
- `districtCode` (string)
- `council` (boolean)
- `role` (integer)

## Responses

- `200`: OK
- `404`: Not Found
