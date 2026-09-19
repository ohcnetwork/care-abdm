# Verify OTP

`POST /v2/registration/aadhaar/verifyOTP`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v2/registration/aadhaar/verifyOTP \
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

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "951b4258-2ac7-432c-8dbf-6ed990757b88",
  "mobileNumber": null,
  "photo": "<BASE64 ENCODED STRING>",
  "gender": "M",
  "name": "Ayushman Bharat Mission",
  "email": null,
  "pincode": "<PINCODE>",
  "birthdate": "<DOB>",
  "careOf": "<NAME>",
  "house": "<ADDRESS>",
  "street": "<ADDRESS>",
  "landmark": null,
  "locality": "<ADDRESS>",
  "villageTownCity": "Sahibabad",
  "subDist": null,
  "district": "Ghaziabad",
  "state": "Uttar Pradesh",
  "postOffice": "Sahibabad",
  "address": "9th Floor, Tower-l, Jeevan Bharati Building, Connaught Place, New Delhi - 110001"
}
```
