# Initiate the linking of care contexts for a patient

`POST /api/v3/hip/link/care-context/init`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
The init API endpoint facilitates the initial linking of care contexts to a patient’s ABHA address. When a request is made to this endpoint, it returns a response containing the transaction ID, ABHA address, patient details, and any errors encountered. This ensures that patient care contexts are accurately linked and managed within the healthcare system.<br> <ol type='a'><b>Note:</b><br><il>Incase of success, HIP will get the patient details in the callback.</il><br><il>In case of failure, HIP will get the error response in the callback.</il></ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hip/link/care-context/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "f901b782-bfdf-4224-9f8d-da2cadc20c0d",
  "abhaAddress": "<ABHA_ADDRESS>",
  "patient": [
    {
      "referenceNumber": "abc123",
      "display": "Test",
      "careContexts": [
        {
          "referenceNumber": "abc123",
          "display": "Blood Test"
        }
      ],
      "hiType": "Prescription",
      "count": 1
    }
  ],
  "error": {
    "code": "ABDM-1001",
    "message": "No data found"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Body

- `transactionId` (string, required)
- `abhaAddress` (string, required): A patient identifier with which patient is registered in the facility/hospital.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\-@,. ()/:\\]{0,255}$"
- `patient` (object[], required)
- `patient.referenceNumber` (string, required): A patient identifier with which patient is registered in the facility/hospital. Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\-@,. ()/:\\]{0,255}$"
- `patient.display` (string, required): The display text of patient.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `patient.careContexts.referenceNumber` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data).Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\-@,. ()/:\\]{0,255}$"
- `patient.careContexts.display` (string, required): The display of care context.Allows alpha numeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \"':|()/]{0,255}$"
- `patient.hiType` (string, required): The health information type One of: DiagnosticReport, DischargeSummary, HealthDocumentRecord, ImmunizationRecord, OPConsultation, Prescription, WellnessRecord, Invoice.
- `patient.count` (integer): The count should match the number of care contexts in the payload
- `error` (object): The error code and message, if any occurred.
- `error.code` (string, required): ABDM-1001 - No data found. May be returned either bare (`ABDM-1001`) or with a trailing ": " separator (`ABDM-1001: `); match on the code itself and tolerate the separator.
- `error.message` (string, required): The appropriate error message

## Responses

- `200`: Ok
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "transactionId": "c1ce50dc-d1f7-4a31-987a-c6bf6d08ad5a",
  "abhaAddress": "<ABHA_ADDRESS>",
  "patient": [
    {
      "referenceNumber": "<ABHA_ADDRESS>",
      "careContexts": [
        {
          "referenceNumber": "New test 1"
        }
      ],
      "hiType": "OPConsultation",
      "count": 1
    }
  ]
}
```
