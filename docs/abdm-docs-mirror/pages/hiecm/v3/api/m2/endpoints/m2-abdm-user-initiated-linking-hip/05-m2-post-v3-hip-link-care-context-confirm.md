# Confirm the linking of care contexts for a patient

`POST /api/v3/hip/link/care-context/confirm`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
The confirm API endpoint facilitates the confirmation of care context linking for a patient. When a request is made to this endpoint, it verifies the linking process using a provided token and reference number. This ensures that the care contexts are accurately linked to the patient’s ABHA (Ayushman Bharat Health Account) address.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hip/link/care-context/confirm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "confirmation": {
    "token": 123456,
    "linkRefNumber": "d353b782-bfdf-4224-9f8d-da2cadc20c0d"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Body

- `confirmation` (object, required)
- `confirmation.token` (integer, required): The token number. Must be 6 digit and contain only 0-9
- `confirmation.linkRefNumber` (string, required): The link reference number random uuid. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
