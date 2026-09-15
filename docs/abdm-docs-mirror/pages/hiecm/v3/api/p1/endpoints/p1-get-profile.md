# Get Profile

`GET /profile/phr`

Returns the signed-in person's ABHA profile: name, date of birth, gender and contact details.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/profile/phr \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "abhaAddress": "<ABHA_ADDRESS>",
  "fullName": "Hemant Bodhai",
  "firstName": "<FIRST_NAME>",
  "middleName": "",
  "lastName": "<LAST_NAME>",
  "dayOfBirth": "14",
  "monthOfBirth": "11",
  "yearOfBirth": "1995",
  "dateOfBirth": "14-11-1995",
  "gender": "M",
  "email": "<EMAIL>",
  "mobile": "<MOBILE>",
  "abhaNumber": "<ABHA_NUMBER>",
  "address": "<ADDRESS>",
  "stateName": "Maharashtra",
  "districtName": "Nashik",
  "pinCode": "<PIN_CODE>",
  "stateCode": "27",
  "districtCode": "123",
  "authMethods": [
    "MOBILE_OTP",
    "PASSWORD",
    "... 1 more of the same shape"
  ],
  "status": "ACTIVE",
  "emailVerified": "true",
  "mobileVerified": "true",
  "kycStatus": "VERIFIED",
  "abhaLinkedCount": "3"
}
```
