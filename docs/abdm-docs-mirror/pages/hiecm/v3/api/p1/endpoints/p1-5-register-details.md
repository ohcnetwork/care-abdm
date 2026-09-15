# 5. Register Details

`POST /api/registration/phr/register/details`

Completes mobile-based registration by submitting the person's profile details against the verified transaction, and creates the ABHA address.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/registration/phr/register/details \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "phrDetails": {
    "mobile": "<MOBILE>",
    "firstName": "<FIRST_NAME>",
    "middleName": "",
    "lastName": "<LAST_NAME>",
    "yearOfBirth": "1999",
    "dayOfBirth": "14",
    "monthOfBirth": "10",
    "gender": "M",
    "email": "<EMAIL>",
    "profilePhoto": "",
    "address": "<ADDRESS>",
    "stateName": "Tamil Nadu",
    "stateCode": "33",
    "districtName": "Thiruvallur",
    "districtCode": "601",
    "pinCode": "<PIN_CODE>",
    "abhaAddress": "<ABHA_ADDRESS>",
    "password": "<PASSWORD>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `txnId` (string, required)
- `phrDetails` (object, required)
- `phrDetails.mobile` (string, required)
- `phrDetails.firstName` (string, required)
- `phrDetails.middleName` (string, required)
- `phrDetails.lastName` (string, required)
- `phrDetails.yearOfBirth` (string, required)
- `phrDetails.dayOfBirth` (string, required)
- `phrDetails.monthOfBirth` (string, required)
- `phrDetails.gender` (string, required)
- `phrDetails.email` (string, required)
- `phrDetails.profilePhoto` (string, required)
- `phrDetails.address` (string, required)
- `phrDetails.stateName` (string, required)
- `phrDetails.stateCode` (string, required)
- `phrDetails.districtName` (string, required)
- `phrDetails.districtCode` (string, required)
- `phrDetails.pinCode` (string, required)
- `phrDetails.abhaAddress` (string, required)
- `phrDetails.password` (string, required)

## Responses

- `200`: No response body is documented for this request.
