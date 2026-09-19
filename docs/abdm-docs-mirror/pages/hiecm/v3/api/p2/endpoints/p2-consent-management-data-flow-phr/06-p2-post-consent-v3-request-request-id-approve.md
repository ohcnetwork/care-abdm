# Approve the consent request raised by HIU from PHR/mobile application

`POST /api/hiecm/consent/v3/request/{request-id}/approve`

Approve a consent request, specifying their preferred data access parameters. By invoking this API, the user grants permission for the Health Information User (HIU) to access their health data under the defined conditions. This approval process is essential for ensuring that patient data is shared securely and in accordance with the user’s preferences, supporting a transparent and compliant health information exchange. The API facilitates the establishment of trust and adherence to privacy regulations, enabling ethical and efficient access to health information.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/hiecm/consent/v3/request/{request-id}/approve \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "consents": [
    {
      "hiTypes": [
        "Prescription"
      ],
      "hip": {
        "id": "ABCD_12345",
        "name": "ABCD Hospital",
        "type": "HIP"
      },
      "careContexts": [
        {
          "patientReference": "batman@tmh",
          "careContextReference": "Episode1"
        }
      ],
      "permission": {
        "dateRange": {
          "from": "2021-09-28T12:30:08.573Z",
          "to": "2021-09-28T12:30:08.573Z"
        },
        "frequency": {
          "unit": "HOUR",
          "value": 1,
          "repeats": 0
        },
        "accessMode": "VIEW",
        "dataEraseAt": "2021-09-28T12:30:08.573Z"
      }
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
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Path parameters

- `request-id` (string, required): The consent request id

## Body

- `consents` (object[], required)
- `consents.hiTypes` (string[], required): Types of health information document.
- `consents.hip` (object, required): Identifier and name of the health information provider.
- `consents.hip.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like[A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `consents.hip.name` (string, required): The name of the health information provider. Allows alpha numeric and special characters like "^[a-zA-Z]+[A-Za-z0-9_\\-@,().\\s\\xa0:/]+"
- `consents.hip.type` (string): The type of the health information provider. Allows alpha numeric and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `consents.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `consents.careContexts.patientReference` (string, required): A patient identifier with which patient is registered in the facility/hospital. Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `consents.careContexts.careContextReference` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data). Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\\-@,().\"/:| ]{0,255}$
- `consents.permission` (object, required)
- `consents.permission.dateRange` (object, required)
- `consents.permission.dateRange.from` (string, required): Should be UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `consents.permission.dateRange.to` (string, required): Should be UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `consents.permission.frequency` (object, required)
- `consents.permission.frequency.unit` (string, required) One of: HOUR, DAY, WEEK, MONTH, YEAR.
- `consents.permission.frequency.value` (number, required): The frequency unit value. Should be be a integer.Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `consents.permission.frequency.repeats` (number, required): Should be be a integer
- `consents.permission.accessMode` (string, required) One of: VIEW, STORE, STREAM, QUERY.
- `consents.permission.dataEraseAt` (string, required): The date at which the consent expire. Should be UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 202 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Successful creation of consent artefact.",
  "consentIds": [
    {
      "id": "f29f0e59-8388-4698-9fe6-05db67aeac46"
    }
  ]
}
```
