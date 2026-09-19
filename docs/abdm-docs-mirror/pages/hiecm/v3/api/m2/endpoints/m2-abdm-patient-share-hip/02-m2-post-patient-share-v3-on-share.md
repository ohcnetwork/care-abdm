# Answer the patient share request

`POST /api/hiecm/patient-share/v3/on-share`

Share the response of HIECM's /api/hiecm/patient-share/v3/on-share API. <ol type='1'> <li> <b>Header</b> <ol type='a'> <br/> <li>AUTHORIZATION will be provided by the gateway session API after the successful verification of client ID and Secret [ Example: <TOKEN> ]</li> <li>REQUEST-ID unique UUID[ Example: 18235d89-cb13-479d-ad71-7a57d5f669a8 ]</li> <li>TIMESTAMP actual time of the requested was initiated[ Example: 2022-10-06T10:10:00.587Z ]</li> <li>X-CM-ID consent manager ID[ Example: sbx ]</li> </ol> </li> <br/> <li> <b>Request Body</b> <ol type='a'><br/><li>Incase of success scenario,acknowledgement is mandatory and error is optional </li> <li>Incase of failure scenario,error is mandatory and acknowledgment is optional</li> <li>response is mandatory object in both the cases</li> </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/patient-share/v3/on-share \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `408`: Request Timeout
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `429`: Too Many Requests
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
