# Search for benefits associated with a user’s profile

`POST /abha/api/v3/profile/benefit/search`

Search for benefits associated with a user’s profile. It allows users to retrieve information about various benefits they are eligible for or currently enrolled in, based on their ABHA (Ayushman Bharat Health Account) profile.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}"
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)
- `BENEFIT_NAME` (string, required)

## Body

- `scope` (string[], required)
- `loginHint` (string, required)
- `loginId` (string, required)

## Responses

- `200`: <strong>Successful Response </strong><br>Indicates that the request was processed correctly and the expected result was returned. this is represented by a 200 status code, meaning the operation was successful.
- `400`: <strong>Bad Request</strong><br>Indicates that the server cannot process the request due to a client error. The server returns a 400 status code when the request is malformed, such as missing required parameters or having invalid syntax
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: <strong>Unauthorized</strong><br>Indicates that the request requires user authentication. The server returns a 401 status code when the client has not provided valid authentication credentials.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: <strong>Not Found</strong><br> Indicates that the server cannot find the requested resource. The server returns a 404 status code when the resource is not available at the given URL.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: <strong>Internal Server Error</strong><br>An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "benefitName": "healthid api",
    "abhaNumber": "<ABHA_NUMBER>",
    "status": 1
  }
]
```
