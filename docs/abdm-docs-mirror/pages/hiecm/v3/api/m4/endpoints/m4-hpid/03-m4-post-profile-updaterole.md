# Update role and category

`POST /profile/updateRole`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/profile/updateRole \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "firstName": "Ayushman",
  "lastName": "Mission",
  "middleName": "Bharat",
  "hprId": "<EMAIL>",
  "password": "Abdm@143",
  "email": "<ABHA_ADDRESS>.com",
  "profilePhoto": "<BASE64 ENCODED STRING>",
  "stateCode": "7",
  "districtCode": "71",
  "subdistrictCode": "1",
  "villageCode": "<VILLAGE_CODE>",
  "townCode": "<TOWN_CODE>",
  "wardCode": "<WARD_CODE>",
  "pincode": 110001,
  "address": "9th Floor, Tower-l, Jeevan Bharati Building, Connaught Place, New Delhi - 110001",
  "yearOfBirth": "2021",
  "monthOfBirth": "8",
  "dayOfBirth": "15",
  "hpCategoryCode": "1",
  "hpSubCategoryCode": "1",
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11",
  "role": "<ROLE>",
  "consentToDelete": false
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `firstName` (string): First Name of the user).
- `lastName` (string): Last name of the user
- `middleName` (string): Middle name of the user
- `hprId` (string): Healthcare Professional ID Alias.
- `password` (string): User Authentication password.
- `email` (string): Email Address of the user.
- `profilePhoto` (string): Profile photo of the user (Uploaded by the user).
- `stateCode` (string): State Code of the user (LGD).
- `districtCode` (string): District Code of the user (LGD).
- `subdistrictCode` (string): Sub District Code of the user (LGD).
- `villageCode` (string): Village Code of the user (LGD).
- `townCode` (string): Town Code of the user (LGD).
- `wardCode` (string): Ward Code of the user (LGD).
- `pincode` (integer): Pincode of the user.
- `address` (string): Address of the user.
- `yearOfBirth` (string): Year of birth of the user.
- `monthOfBirth` (string): Month of birth of the user.
- `dayOfBirth` (string): Day of birth of the user.
- `hpCategoryCode` (string)
- `hpSubCategoryCode` (string)
- `txnId` (string)
- `role` (string)
- `consentToDelete` (boolean)

## Responses

- `200`: OK
- `404`: Not Found
