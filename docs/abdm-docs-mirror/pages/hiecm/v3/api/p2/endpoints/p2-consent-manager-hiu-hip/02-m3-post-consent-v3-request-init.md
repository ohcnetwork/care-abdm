# Initiate the consent request

`POST /api/hiecm/consent/v3/request/init`

Create a consent request by a Health Information User (HIU) to access a patient’s health data. By invoking this API, the HIU initiates the process of obtaining the necessary permissions from the patient to retrieve their health information. This consent request is a critical component of the health information exchange framework, ensuring that patient data is accessed in a secure, authorised, and transparent manner. The API supports the establishment of trust and compliance with privacy regulations, facilitating seamless and ethical health information exchange.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "consent": {
    "purpose": {
      "text": "Care Management",
      "code": "CAREMGT",
      "refUri": "www.abc.com"
    },
    "patient": {
      "id": "<ABHA_ADDRESS>"
    },
    "hip": {
      "id": "cowin_hip_01",
      "name": "Cowin",
      "type": "HIP"
    },
    "hiu": {
      "id": "cowin_hiu_01",
      "name": "Cowin",
      "type": "HIU"
    },
    "careContexts": [
      {
        "patientReference": "batman@tmh",
        "careContextReference": "Episode1"
      }
    ],
    "requester": {
      "name": "<ABHA_ADDRESS>",
      "identifier": {
        "value": "REG1",
        "type": "MH1001",
        "system": "https://www.sample.com"
      }
    },
    "hiTypes": [
      "Prescription"
    ],
    "permission": {
      "accessMode": "VIEW",
      "dateRange": {
        "from": "2021-09-28T12:30:08.573Z",
        "to": "2021-09-28T12:30:08.573Z"
      },
      "dataEraseAt": "2021-09-28T12:30:08.573Z",
      "frequency": {
        "unit": "HOUR",
        "value": 1,
        "repeats": 0
      }
    }
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

- `consent` (object, required)
- `consent.purpose` (object, required)
- `consent.purpose.text` (string, required) One of: Care Management, Break the Glass, Public Health, Healthcare Payment, Disease Specific Healthcare Research, Self Requested.
- `consent.purpose.code` (string, required) One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQT.
- `consent.purpose.refUri` (string, required): The reference URL. Should be a valid URL. Allow alpha numeric characters and special charactes like  "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `consent.patient` (object, required)
- `consent.patient.id` (string, required): The abha address of the patient. It must start with Alphanumeric . and  _  in the middle and must be ending with @abdm or @sbx. Allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.\-!]+[a-zA-Z0-9]@(abdm|sbx)$
- `consent.hip` (object): Identifier and name of the health information provider.
- `consent.hip.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `consent.hip.name` (string, required): The name of the health information provider. Allows alpha numeric and special characters like "^[a-zA-Z]+[A-Za-z0-9_\\-@,().\\s\\xa0:/]+"
- `consent.hip.type` (string): The type of the health information provider. Allows alpha numeric and special characters like  "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `consent.hiu` (object, required)
- `consent.hiu.id` (string, required): The service ID of the health information user.  Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `consent.hiu.name` (string, required): The name of the health information user. Allows alpha numeric and special characters like "^[a-zA-Z]+[A-Za-z0-9_\\-@,().\\s\\xa0:/]+"
- `consent.hiu.type` (string): The type of the health information user. Allows alpha numeric and special characters like  "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `consent.careContexts` (object[]): List of care contexts linked at the HIP end for the identified patient.
- `consent.careContexts.patientReference` (string, required): A patient identifier with which patient is registered in the facility/hospital like abhaAddress @sbx. Allows alpha numeric and special characters like "^[a-zA-Z0-9_\\-@,().\"/: ]{0,255}$"
- `consent.careContexts.careContextReference` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data). Allows alpha numeric and special characters like  "^[a-zA-Z0-9_\\-@,().\"/:| ]{0,255}$"
- `consent.requester` (object, required)
- `consent.requester.name` (string, required): The name of the requester
- `consent.requester.identifier` (object, required)
- `consent.requester.identifier.value` (string, required): The type of the identification. Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `consent.requester.identifier.type` (string, required): The identification value. Allows alpha numeric character and special characters like  "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `consent.requester.identifier.system` (string, required): Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `consent.hiTypes` (string[], required): Types of health information document.
- `consent.permission` (object, required)
- `consent.permission.accessMode` (string, required) One of: VIEW, STORE, STREAM, QUERY.
- `consent.permission.dateRange` (object, required)
- `consent.permission.dateRange.from` (string, required): Should be UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `consent.permission.dateRange.to` (string, required): Should be UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `consent.permission.dataEraseAt` (string, required): The date at which the consent expire. Should be UTC.  Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$" date time in ISO format
- `consent.permission.frequency` (object, required)
- `consent.permission.frequency.unit` (string, required) One of: HOUR, DAY, WEEK, MONTH, YEAR.
- `consent.permission.frequency.value` (number, required): The frequency unit value. Should be be a integer
- `consent.permission.frequency.repeats` (number, required): Should be be a integer

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
