# Receive the discovered care contexts of a patient

`POST /api/v3/hiu/patient/care-context/on-discover`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
The on-discover API endpoint allows HIUs to receive and process the care contexts associated with a patient. When a request is made to this endpoint, it returns a detailed response containing the patient’s care contexts, transaction details, and any errors that occurred. This ensures that HIUs have the necessary information to manage patient care effectively. <p><strong>NOTE:</strong> In the request body, either 'patient' or 'error' must be included. <ol type = "a"> <li>In case of success scenario, patient object is mandatory and error object is optional</li> <br> <li>In case of error scenario, error object is mandatory and patient object is optional</li> <br> <li>Response is mandatory in both scenarios</li> </ol>

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/v3/hiu/patient/care-context/on-discover \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "f901b782-bfdf-4224-9f8d-da2cadc20c0d",
  "patient": [
    {
      "referenceNumber": "abc123",
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
  "createdAt": "2024-12-31T05:45:35.429Z",
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

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `transactionId` (string, required)
- `patient` (object[], required)
- `patient.referenceNumber` (string, required): A patient identifier with which patient is registered in the facility/hospital.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `patient.display` (string): Display text for patient reference.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `patient.careContexts.referenceNumber` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data).Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. ()/:\\\\]{0,255}$"
- `patient.careContexts.display` (string, required): Display text for care context reference. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.hiType` (string, required): The health information type One of: DiagnosticReport, DischargeSummary, HealthDocumentRecord, ImmunizationRecord, OPConsultation, Prescription, WellnessRecord, Invoice.
- `patient.count` (integer, required): The count should match the number of care contexts in the payload
- `createdAt` (string, required)
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message
- `response` (object, required)
- `response.requestId` (string, required): The request id that was passed.Allows alpha numeric characters and special characters like "^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"

## Responses

- `200`: Ok
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "transactionId": "0d36501c-551a-4bb5-b247-eec4bb42984b",
  "patient": [
    {
      "referenceNumber": "example01",
      "display": "abcd-display",
      "careContexts": [
        {
          "referenceNumber": "abcd",
          "display": "123-display"
        }
      ],
      "hiType": "Prescription",
      "count": 1
    }
  ],
  "createdAt": "2023-06-13T08:05:43.030Z",
  "response": {
    "requestId": "d89525a2-3a3f-4d39-98b5-477afb1865f6"
  }
}
```
