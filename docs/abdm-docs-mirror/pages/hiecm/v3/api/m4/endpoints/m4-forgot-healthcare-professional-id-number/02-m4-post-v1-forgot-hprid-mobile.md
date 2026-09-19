# Submit the retrieval health ID by mobile

`POST /v1/forgot/hprId/mobile`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/forgot/hprId/mobile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11",
  "name": "<NAME>",
  "gender": "<GENDER>",
  "yearOfBirth": "<YEAR_OF_BIRTH>",
  "monthOfBirth": "<MONTH_OF_BIRTH>",
  "dayOfBirth": "<DAY_OF_BIRTH>",
  "firstName": "<FIRST_NAME>",
  "lastName": "<LAST_NAME>",
  "middleName": "<MIDDLE_NAME>",
  "otp": "<OTP>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `txnId` (string, required)
- `name` (string, required)
- `gender` (string, required)
- `yearOfBirth` (string, required)
- `monthOfBirth` (string)
- `dayOfBirth` (string)
- `firstName` (string, required)
- `lastName` (string)
- `middleName` (string)
- `otp` (string, required)

## Responses

- `200`: OK
- `404`: Not Found
