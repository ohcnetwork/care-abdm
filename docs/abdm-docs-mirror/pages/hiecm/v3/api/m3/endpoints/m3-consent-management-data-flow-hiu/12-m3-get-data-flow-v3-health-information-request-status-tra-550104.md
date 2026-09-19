# Get the current status of the health information request

`GET /api/hiecm/data-flow/v3/health-information/request/status/{transaction-id}`

Allow Health Information Users (HIU) and Health Information Providers (HIP) to retrieve the current status of a specific Health Information Request. By providing the unique transaction ID, users can query the system to obtain real-time updates on the processing state of their request. This functionality is crucial for ensuring transparency and efficient communication between stakeholders in the health information exchange ecosystem. The API supports various status checks, including pending, in-progress, completed, and failed states.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/request/status/{transaction-id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Path parameters

- `transaction-id` (string, required): The health information request transaction id

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Access Denied
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "transactionId": "18235d89-cb13-479d-ad71-7a57d5f669a8",
  "status": "TRANSFERRED"
}
```
