# Discover his/her health records

`POST /api/hiecm/user-initiated-linking/v3/patient/care-context/discover`

Be invoked by the patient or user through the Personal Health Record (PHR) application to discover their health records. By using this API, patients can initiate a search to locate and access their health information across various Health Information Providers (HIPs). This functionality empowers patients to have greater control and visibility over their health data, facilitating a more informed and engaged approach to managing their health. The API supports the seamless retrieval of health records, ensuring that patients can easily discover and review their care contexts.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/hiecm/user-initiated-linking/v3/patient/care-context/discover \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hip": {
    "id": "cowin_hip_01"
  },
  "unverifiedIdentifiers": [
    {
      "type": "MOBILE",
      "value": "+9198765*****"
    }
  ]
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

- `hip` (object, required): Identifier and name of the health information provider.
- `hip.id` (string, required): The service ID of the health information provider
- `unverifiedIdentifiers` (object[], required): Identifiers with which the HIP will search for the patient in its own records.
- `unverifiedIdentifiers.type` (string, required) One of: MR, MOBILE, ABHA_NUMBER, ABHA_ADDRESS.
- `unverifiedIdentifiers.value` (string, required): Allows alphanumeric characters and special characters like "^(\\+)?[a-zA-Z0-9_\\-@,. ]{0,255}$"

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
