# Link his/her health records

`POST /api/hiecm/user-initiated-linking/v3/link/care-context/init`

Be invoked by the patient or user to link their health records. By using this API, patients can initiate the process of associating their health information with their ABHA (Ayushman Bharat Health Account) address. This functionality empowers patients to actively manage and consolidate their health records, ensuring that all relevant care contexts are accurately linked and accessible. The API supports a seamless and efficient health information exchange, enhancing the overall quality and continuity of care within the healthcare ecosystem.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/hiecm/user-initiated-linking/v3/link/care-context/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "f901b782-bfdf-4224-9f8d-da2cadc20c0d",
  "patient": [
    {
      "referenceNumber": "<ABHA_ADDRESS>",
      "display": "Test",
      "careContexts": [
        {
          "referenceNumber": "abc123",
          "display": "Sugar Test"
        }
      ],
      "hiType": "OPConsultation",
      "count": 1
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

- `transactionId` (string, required): UUID from discover request callback to track the entire user link flow
- `patient` (object[], required)
- `patient.referenceNumber` (string, required): A patient identifier with which patient is registered in the facility/hospital.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `patient.display` (string, required): Display text for patient reference.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `patient.careContexts.referenceNumber` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data).Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `patient.careContexts.display` (string): Display text for care context reference.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.hiType` (string, required): The health information type One of: DiagnosticReport, DischargeSummary, HealthDocumentRecord, ImmunizationRecord, OPConsultation, Prescription, WellnessRecord, Invoice.
- `patient.count` (integer, required): The count should match the number of care contexts in the payload

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
