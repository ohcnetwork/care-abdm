# Submit the account exist

`POST /v1/registration/aadhaar/checkHpIdAccountExist`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/registration/aadhaar/checkHpIdAccountExist \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `txnId` (string)
- `preverifiedCheck` (boolean)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "token": "<JWT TOKEN>",
  "hprIdNumber": "<HPR_ID>",
  "categoryId": 100,
  "subCategoryId": 85,
  "txnId": "79dbf65d-affa-4249-8935-3d01676d8b82",
  "name": "Ayushman Bharat Mission",
  "gender": "M",
  "yearOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "dayOfBirth": "<DOB>",
  "firstName": "Ayushman",
  "middleName": "",
  "lastName": "Mission",
  "stateCode": "9",
  "districtCode": "145",
  "stateName": "Uttar Pradesh",
  "districtName": "<ADDRESS>",
  "address": "9th Floor, Tower-l, Jeevan Bharati Building, Connaught Place, New Delhi - 110001",
  "pincode": "<PINCODE>",
  "profilePhoto": "<BASE64 ENCODED STRING>",
  "mobile": null,
  "hprId": "<EMAIL>",
  "new": false
}
```
