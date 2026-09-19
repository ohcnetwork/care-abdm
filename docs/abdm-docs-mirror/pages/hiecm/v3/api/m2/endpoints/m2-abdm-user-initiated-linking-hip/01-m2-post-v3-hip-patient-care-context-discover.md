# Discover care contexts associated with a patient

`POST /api/v3/hip/patient/care-context/discover`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
The discover API endpoint facilitates the discovery of care contexts linked to a specific patient. When a request is made to this endpoint, it returns detailed information about the patient, including verified and unverified identifiers, ensuring accurate patient identification and continuity of care.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hip/patient/care-context/discover \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "f901b782-bfdf-4224-9f8d-da2cadc20c0d",
  "patient": {
    "id": "<ABHA_ADDRESS>",
    "verifiedIdentifiers": [
      {
        "type": "MR",
        "value": "+919876543210"
      }
    ],
    "unverifiedIdentifiers": [
      {
        "type": "MOBILE",
        "value": "+9198765*****"
      }
    ],
    "name": "<NAME>",
    "gender": "M",
    "yearOfBirth": 9999
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds.
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Body

- `transactionId` (string, required): UUID
- `patient` (object, required)
- `patient.id` (string, required): A patient identifier with which patient is registered in the facility/hospital
- `patient.verifiedIdentifiers` (object[], required)
- `patient.verifiedIdentifiers.type` (string, required) One of: MR, MOBILE, ABHA_NUMBER, ABHA_ADDRESS, EMAIL.
- `patient.verifiedIdentifiers.value` (string, required): Allows alphanumeric characters and special characters like "^(\\+)?[a-zA-Z0-9_\\-@,. ]{0,255}$".
- `patient.unverifiedIdentifiers` (object[]): Identifiers with which the HIP will search for the patient in its own records.
- `patient.unverifiedIdentifiers.type` (string, required) One of: MR, MOBILE, ABHA_NUMBER, ABHA_ADDRESS, EMAIL.
- `patient.unverifiedIdentifiers.value` (string, required): Allows alphanumeric characters and special characters like "^(\\+)?[a-zA-Z0-9_\\-@,. ]{0,255}$".
- `patient.name` (string, required)
- `patient.gender` (string, required) One of: M, F, O, D, T, U.
- `patient.yearOfBirth` (number, required)

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
