# Answer the care context discovery

`POST /api/hiecm/user-initiated-linking/v3/patient/care-context/on-discover`

Is invoked by the Hospital Management Information System (HMIS) or Laboratory Information Management System (LIMS) or HIP application to share the response of the /api/hiecm/user-initiated-linking/v3/patient/care-context/on-discover API. It facilitates the communication of discovered health records back to the patient or user. By using this API, the HMIS/LIMS application ensures that the patient’s health information is accurately and promptly shared, supporting efficient and transparent health information exchange. This process is crucial for maintaining the integrity and continuity of patient care, enabling patients to have comprehensive access to their health records.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/user-initiated-linking/v3/patient/care-context/on-discover \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "f901b782-bfdf-4224-9f8d-da2cadc20c0d",
  "patient": [
    {
      "referenceNumber": "<ABHA_ADDRESS>",
      "display": "12345",
      "careContexts": [
        {
          "referenceNumber": "abc123",
          "display": "12345"
        }
      ],
      "hiType": "Prescription",
      "count": 1
    }
  ],
  "matchedBy": [
    "MR"
  ],
  "error": {
    "code": "ABDM-9999",
    "message": "Unknown exception"
  },
  "response": {
    "requestId": "f29f0e59-8388-4698-9fe6-05db67aeac46"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Body

- `transactionId` (string, required): UUID from discover request callback to track the entire user link flow
- `patient` (object[], required)
- `patient.referenceNumber` (string, required): A patient identifier with which patient is registered in the facility/hospital.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `patient.display` (string, required): Display text for patient reference. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `patient.careContexts.referenceNumber` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data).Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `patient.careContexts.display` (string, required): Display text for care context reference. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.hiType` (string, required): The health information type One of: DiagnosticReport, DischargeSummary, HealthDocumentRecord, ImmunizationRecord, OPConsultation, Prescription, WellnessRecord, Invoice.
- `patient.count` (integer, required): The count should match the number of care contexts in the payload
- `matchedBy` (string[], required)
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-9999 - Unknown exception. May be returned either bare (`ABDM-9999`) or with a trailing ": " separator (`ABDM-9999: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message. Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\-@,. ":]{0,255}$
- `response` (object, required): The request id is from the /discover callback. Allows alpha numeric characters and special characters like "^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}"
- `response.requestId` (string, required): The request id that was passed

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
