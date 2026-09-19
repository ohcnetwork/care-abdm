# Disable the auto-approval policy

`POST /api/hiecm/consent/v3/auto/approve/{auto-approval-id}/disable`

Disable an existing auto-approval policy. By invoking this API, users can deactivate the automatic approval of consent requests for the specified Health Information User (HIU). This functionality is essential for maintaining control over consent management, allowing users to modify or revoke auto-approval settings as needed.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/hiecm/consent/v3/auto/approve/{auto-approval-id}/disable \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Path parameters

- `auto-approval-id` (string, required): The auto approval id

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 202 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Successfully disabled auto approval policy",
  "error": {
    "code": "ABDM-1001",
    "message": "unable to connect database"
  }
}
```
