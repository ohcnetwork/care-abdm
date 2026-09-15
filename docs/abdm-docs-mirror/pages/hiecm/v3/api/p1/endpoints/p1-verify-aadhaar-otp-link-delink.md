# Verify AADHAAR Otp - Link-DeLink

`POST /login/profile/verify`

Verifies the Aadhaar OTP for a link or delink transaction and returns the accounts it applies to.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/login/profile/verify \
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
- `authData.otp` (object, required)
- `authData.otp.txnId` (string, required)
- `authData.otp.otpValue` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

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
