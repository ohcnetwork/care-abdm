# Receive the HIP token on generate token

`POST /api/v3/hip/token/on-generate-token`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
"This API endpoint serves as a callback for the /api/hiecm/v3/token/generate-token API which will by the HIE-CM, the HIE-CM will validate the request and if everything is correct, a link token will be generated and is provided in the call-back API, or If anything incorrect in the request which demographics details then it will give the error in the same call back API. It is used to handle the response from the token generation process, ensuring that the HIP can securely manage and use the generated link token. This callback mechanism is essential for maintaining the integrity and security of the token-based linking process, supporting seamless and efficient health information exchange within the healthcare ecosystem."

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hip/token/on-generate-token \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized. The request carried no valid credentials, or the access token has expired. Obtain a fresh token from the session API and retry.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
