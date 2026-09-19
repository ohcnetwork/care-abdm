# Suggest an ABHA address

`POST /abha/api/v3/phr/app/enrollment/suggestion`

Flows in the Postman collection:
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via Mobile › Suggestion API
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-ABHA OTP › Suggestion API
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-Aadhaar OTP › Suggestion API

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/suggestion \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "ee10d1c7-e25f-40e0-a3a1-df4c1dda02211",
  "firstName": "John",
  "lastName": "Doe",
  "dayOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "yearOfBirth": "<DOB>",
  "email": ""
}'
```

## Headers

- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Body

- `txnId` (string)
- `firstName` (string)
- `lastName` (string)
- `dayOfBirth` (string)
- `monthOfBirth` (string)
- `yearOfBirth` (string)
- `email` (string)

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "4765527e-898b-4a62-91ec-be041fbf60f8",
  "abhaAddressList": [
    "<ABHA_ADDRESS>",
    "<ABHA_ADDRESS>",
    "... 1 more of the same shape"
  ]
}
```
