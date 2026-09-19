# Generate link token to link the health records

`POST /api/hiecm/v3/token/generate-token`

Generate a link token which will be valid for 6 months.. This token can be used for Health Information Provider (HIP) Initiated Linking, enabling HIPs to securely link patient health records to their ABHA (Ayushman Bharat Health Account) address. The generated token ensures that the linking process is authenticated and authorised, maintaining the integrity and security of health information exchange. This functionality is crucial for facilitating seamless and efficient linking of health records within the healthcare ecosystem.<ol type='a'><li><b>Authorisation:</b> We are passing the access-token in the authorisation [Example: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJBbFJiNVd]</li></ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/v3/token/generate-token \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": 12345678901234,
  "abhaAddress": "<ABHA_ADDRESS>",
  "name": "first_name + middle_name + last_name",
  "gender": "M",
  "yearOfBirth": 9999
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Body

- `abhaNumber` (number): it can be null if abhaNumber is not linked with abhaAddress. Allows numeric character like ^\d{14}$
- `abhaAddress` (string, required): abhaAddress of the user/patient. Allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.]+[a-zA-Z0-9]@(abdm|sbx)$
- `name` (string, required): Only alphabets and special characters like ',.- are allowed like ^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$
- `gender` (string, required): Allows M, F, O, D, T, U as a input
- `yearOfBirth` (number, required): Year of birth must be 4 digit, ranging between 1900 and 2200

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
