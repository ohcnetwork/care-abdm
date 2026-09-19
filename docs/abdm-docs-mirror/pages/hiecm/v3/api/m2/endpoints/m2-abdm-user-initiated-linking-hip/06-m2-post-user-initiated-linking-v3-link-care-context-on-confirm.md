# Link care context on confirm

`POST /api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm`

Share the response of the /api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm API. By using this API, the HIP communicates the outcome of the care context confirmation process, ensuring that the system accurately reflects the status of the operation. This process is essential for maintaining the integrity and synchronization of patient health records, supporting seamless and efficient health information exchange within the healthcare ecosystem. <br><ol type="a"><li>In case of success scenario, patient object is mandatory and error object is optional</li>
 <br>
 <li>In case of error scenario, error object is mandatory and patient object is optional</li>
 <br>
 <li>Response is mandatory in both scenarios</li>
 </ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
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
  "error": {
    "code": "ABDM-1001",
    "message": "No data found"
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

- `patient` (object[], required)
- `patient.referenceNumber` (string, required): A patient identifier with which patient is registered in the facility/hospital.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `patient.display` (string, required): Display text for patient reference. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `patient.careContexts.referenceNumber` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data).Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `patient.careContexts.display` (string, required): Display text for care context reference. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.hiType` (string, required): The health information type One of: DiagnosticReport, DischargeSummary, HealthDocumentRecord, ImmunizationRecord, OPConsultation, Prescription, WellnessRecord, Invoice.
- `patient.count` (integer, required): The count should match the number of care contexts in the payload
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message
- `response` (object, required): The request id is from the link/confirm callback. Allows alpha numeric characters and special characters like "^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}"
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
