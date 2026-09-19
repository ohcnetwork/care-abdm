# Perform HIP initiated linking

`POST /api/hiecm/hip/v3/link/carecontext`

<p><b>Note: </b>While generating the link-token the user/patient is providing both ABHA_number and ABHA_address, then at the time of linking both must be mandatory. If not one should be mandatory either 'ABHA_number' or 'ABHA_address'.</p><br><p> This API endpoint is used by the Ayushman Bharat Digital Mission (ABDM) system to store care context or health record references. Upon successful validation of the ABHA (Ayushman Bharat Health Account) address and the associated link token, the system securely records the relevant care context information. This process ensures that health records are accurately linked and accessible, facilitating efficient and seamless health information exchange across the network. The API plays a critical role in maintaining the integrity and continuity of patient health records, thereby supporting comprehensive and coordinated care.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/hip/v3/link/carecontext \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'X-LINK-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": 12345678901234,
  "abhaAddress": "<ABHA_ADDRESS>",
  "patient": [
    {
      "referenceNumber": "TMH-PUID-001",
      "display": "String",
      "careContexts": [
        {
          "referenceNumber": "TMH-PUID-001",
          "display": "display 1"
        }
      ],
      "hiTypes": "DiagnosticReport",
      "count": 1
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended
- `X-LINK-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Body

- `abhaNumber` (number): The abha number of the patient. Should be only 14 digit and it allows numeric character like ^\\d{14}$
- `abhaAddress` (string, required): The abha address of the patient. Should start with Alphanumeric . and  _  in the middle and must be ending with @abdm or @sbx also allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.]+[a-zA-Z0-9]@(abdm|sbx)$
- `patient` (object[], required)
- `patient.referenceNumber` (string, required): Patient identifier with which patient is registered in the facility/hospital or patient can also pass his abha_address in the reference number. Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\-@,. "':|()/]{0,255}$
- `patient.display` (string, required): The display text for patient reference(regex:^[a-zA-Z0-9_\-@,. "':|()/]{0,255}$)
- `patient.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `patient.careContexts.referenceNumber` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data) and it should be unique for each care-context.Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\-@,. ()/:\\]{0,255}$
- `patient.careContexts.display` (string, required): The display text for care context reference(regex:^[a-zA-Z0-9_\-@,. "':|()/]{0,255}$)
- `patient.hiTypes` (string, required): Types of health information document. One of: DiagnosticReport, DischargeSummary, HealthDocumentRecord, ImmunizationRecord, OPConsultation, Prescription, WellnessRecord, Invoice.
- `patient.count` (number, required): The count should match with the number of care contexts

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
