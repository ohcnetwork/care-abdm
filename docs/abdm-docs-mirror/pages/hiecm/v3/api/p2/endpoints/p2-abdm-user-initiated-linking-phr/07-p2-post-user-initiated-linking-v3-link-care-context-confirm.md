# Confirm his/her health records

`POST /api/hiecm/user-initiated-linking/v3/link/care-context/confirm`

Be invoked by the patient or user to confirm their health records. By using this API, patients can validate and confirm the linkage of their health information to their ABHA (Ayushman Bharat Health Account) address. This confirmation process ensures that all relevant care contexts are accurately linked and verified, providing patients with control over their health data. The API supports a seamless and efficient health information exchange, enhancing the overall quality and continuity of care within the healthcare ecosystem.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/hiecm/user-initiated-linking/v3/link/care-context/confirm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "token": 123456,
  "linkRefNumber": "d353b782-bfdf-4224-9f8d-da2cadc20c0d"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Body

- `token` (integer, required): The token number. Must be 6 digit and contain only 0-9. Allows the numerical values like "[\\d]*$"
- `linkRefNumber` (string, required): The link reference number from the /on-init call back . Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
