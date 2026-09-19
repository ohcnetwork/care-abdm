# Notify HIU subscription

`POST /api/v3/hiu/subscription/notify`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This API endpoint serves as a callback to notify the subscribed Health Information User (HIU) when a care context is linked or updated for a patient. By invoking this API, the HIU is informed about any changes or additions to the patient’s care context, ensuring that they have the most current and accurate health information. This functionality is essential for maintaining the integrity and synchronization of patient health records, supporting efficient and transparent health information exchange within the healthcare ecosystem.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hiu/subscription/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "event": {
    "id": "f29f0e59-8388-4698-9fe6-05db67aeac46",
    "published": "2024-09-10T04:27:47.696Z",
    "category": "LINK",
    "subscriptionId": "5dd76bb8-0eaf-4952-9db4-4c6fe844c257",
    "content": {
      "patient": {
        "id": "<ABHA_ADDRESS>"
      },
      "hip": {
        "id": "INDIA_HIP"
      },
      "contexts": [
        {
          "careContexts": [],
          "hiType": "HealthDocumentRecord"
        }
      ]
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `event` (object, required)
- `event.id` (string, required): the event Id .Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `event.published` (string, required): UTC. Allows alpha numeric character and special characters like \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$
- `event.category` (string, required) One of: LINK, DATA.
- `event.subscriptionId` (string, required)
- `event.content` (object, required)
- `event.content.patient` (object, required)
- `event.content.patient.id` (string, required): The abha address of the patient. Must start with Alphanumeric . and  _  in the middle and must be ending with @abdm or @sbx and Allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.\\-!]+[a-zA-Z0-9]@(abdm|sbx)$
- `event.content.hip` (object, required): Identifier and name of the health information provider.
- `event.content.hip.id` (string, required): service Id. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `event.content.contexts` (object[], required)
- `event.content.contexts.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `event.content.contexts.hiType` (string, required) One of: DiagnosticReport, DischargeSummary, HealthDocumentRecord, ImmunizationRecord, OPConsultation, Prescription, WellnessRecord, Invoice.

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
