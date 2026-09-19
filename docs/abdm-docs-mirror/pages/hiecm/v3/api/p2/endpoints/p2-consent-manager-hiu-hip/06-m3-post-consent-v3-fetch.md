# Fetch the consent details

`POST /api/hiecm/consent/v3/fetch`

Fetch the details of a consent using the consent artefact ID. By invoking this API, HIUs can retrieve comprehensive information about a specific consent, including its status, scope, and any associated conditions. This functionality is essential for ensuring that HIUs have access to accurate and up-to-date consent information, supporting secure and compliant health information exchange. The API facilitates efficient management and verification of consents, enhancing the overall integrity of the consent management process.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/fetch \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "consentId": "5f7a535d-a3fd-416b-b069-c97d021fbacd"
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `consentId` (string, required): The id of the consent artefact that needs to be fetched. Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
