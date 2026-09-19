# Update the user ABHA profile Photo, update the child ABHA profile

`PATCH /abha/api/v3/profile/account`

Update the ABHA (Ayushman Bharat Health Account) profile. It is particularly useful for updating the profile and information of individuals. The endpoint allows users to update essential details such as the ABHA number, date of birth, name, and gender.<br><br>Note: Non-KYC (Know Your Customer) verified ABHA users are permitted to update their profile only once. After the initial update, any further attempts to modify the profile will result in an error. This restriction ensures data integrity and prevents unauthorised changes.

```bash
curl --request PATCH \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: <X_TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": "<ABHA_NUMBER>",
  "dob": "<DOB>",
  "name": "<NAME>",
  "gender": "F"
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `X-token` (string, required): The user token from a login or enrolment response.
- `TIMESTAMP` (string, required)
- `REQUEST-ID` (string, required)
- `BENEFIT_NAME` (string, required)

## Body

- `abhaNumber` (string, required)
- `dob` (string, required)
- `name` (string, required)
- `gender` (string, required)

## Responses

- `200`: Indicates a successful request. The response includes the updated child ABHA profile details
- `400`: This error indicates that the request contains a field that is not valid for updating. In the context of updating a resource, certain fields may be restricted or immutable
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Indicates an unauthorized request due to invalid credentials
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: This error indicates that the system could not find a user account associated with the provided ABHA (Ayushman Bharat Health Account) number or other identifying information. This can happen if the ABHA number is incorrect, the user does not exist in the system, or there is a mismatch in the provided details
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `422`: This error indicates that a non-KYC (Know Your Customer) verified CHILD ABHA (Ayushman Bharat Health Account) user is permitted to update their profile only once. After the initial update, any further attempts to modify the profile will result in this error. This restriction is likely in place to ensure data integrity and prevent unauthorized changes.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "ABHANumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>",
  "mobile": "******0903",
  "firstName": "<NAME>",
  "middleName": "<NAME>",
  "lastName": "<NAME>",
  "yearOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "dayOfBirth": "<DOB>",
  "gender": "F",
  "status": "ACTIVE",
  "stateCode": 27,
  "districtCode": 290,
  "stateName": "Maharashtra",
  "districtName": "<ADDRESS>",
  "subdistrictName": "<ADDRESS>",
  "authMethods": [
    "MOBILE_OTP"
  ],
  "tags": {},
  "kycVerified": false,
  "verificationStatus": "VERIFIED",
  "verificationType": "CHILD_ABHA",
  "createdDate": "10-05-2024"
}
```
