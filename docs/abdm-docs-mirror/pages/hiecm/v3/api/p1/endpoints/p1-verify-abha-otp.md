# Verify ABHA OTP

`POST /profile/phr/verify`

Verifies the OTP sent for a profile change and returns the accounts and tokens it applies to.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/profile/phr/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "<SCOPE>"
  ],
  "authData": {
    "authMethods": [
      "<AUTH_METHODS>"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTP_VALUE>"
    },
    "password": {
      "abhaAddress": "<ABHA_ADDRESS>",
      "password": "<PASSWORD>"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `scope` (string[], required)
- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `authData.otp` (object)
- `authData.otp.txnId` (string, required)
- `authData.otp.otpValue` (string, required)
- `authData.password` (object)
- `authData.password.abhaAddress` (string, required)
- `authData.password.password` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "<TXN_ID>",
  "message": "<MESSAGE>",
  "authResult": "<AUTH_RESULT>",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "<FULL_NAME>",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "<STATUS>",
      "kycStatus": "<KYC_STATUS>"
    }
  ],
  "accounts": [
    {
      "mobile": "<MOBILE>",
      "firstName": "<FIRST_NAME>",
      "middleName": "<MIDDLE_NAME>",
      "lastName": "<LAST_NAME>",
      "name": "<NAME>",
      "yearOfBirth": "<YEAR_OF_BIRTH>",
      "dayOfBirth": "<DAY_OF_BIRTH>",
      "monthOfBirth": "<MONTH_OF_BIRTH>",
      "gender": "<GENDER>",
      "email": "<EMAIL>",
      "profilePhoto": "<PROFILE_PHOTO>",
      "status": "<STATUS>",
      "stateCode": "<STATE_CODE>",
      "districtCode": "<DISTRICT_CODE>",
      "subDistrictCode": "<SUB_DISTRICT_CODE>",
      "villageCode": "<VILLAGE_CODE>",
      "townCode": "<TOWN_CODE>",
      "wardCode": "<WARD_CODE>",
      "pincode": "<PINCODE>",
      "address": "<ADDRESS>",
      "kycPhoto": "<KYC_PHOTO>",
      "stateName": "<STATE_NAME>",
      "districtName": "<DISTRICT_NAME>",
      "subdistrictName": "<SUBDISTRICT_NAME>",
      "villageName": "<VILLAGE_NAME>",
      "townName": "<TOWN_NAME>",
      "wardName": "<WARD_NAME>",
      "authMethods": [
        "<AUTH_METHODS>"
      ],
      "kycVerified": false,
      "verificationStatus": "<VERIFICATION_STATUS>",
      "verificationType": "<VERIFICATION_TYPE>",
      "emailVerified": "<EMAIL_VERIFIED>",
      "ABHANumber": "<ABHANUMBER>",
      "preferredAbhaAddress": "<PREFERRED_ABHA_ADDRESS>"
    }
  ],
  "tokens": {
    "token": "<TOKEN>",
    "expiresIn": 0,
    "refreshToken": "<REFRESH_TOKEN>",
    "refreshExpiresIn": 0
  }
}
```
