# Receive the provide fetched consent artefact details to HIU

`POST /api/v3/hiu/consent/on-fetch`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This API endpoint is part of the Ayushman Bharat Digital Mission (ABDM) Health Information Exchange - Consent Management (HIE-CM) system. It is called by the Consent Management (CM) system to fetch a consent artefact. By invoking this API, the CM system retrieves the detailed information of a specific consent artefact, ensuring that the consent data is accurately and securely accessed. This functionality is essential for maintaining the integrity and synchronization of consent records, supporting secure and compliant health information exchange within the healthcare ecosystem.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hiu/consent/on-fetch \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "consent": {
    "status": "GRANTED",
    "consentDetail": {
      "consentId": "e5ec415f-c098-40f6-a0db-faa162fc5295",
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
      "hiTypes": [
        "Prescription"
      ],
      "patient": {
        "id": "<ABHA_ADDRESS>"
      },
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "www.abc.com"
      },
      "createdAt": "2021-09-28T12:30:08.573Z",
      "requester": {
        "name": "<ABHA_ADDRESS>",
        "identifier": {
          "value": "REG1",
          "type": "MH1001",
          "system": "https://www.sample.com"
        }
      },
      "permission": {
        "accessMode": "VIEW",
        "dateRange": {
          "from": "2021-09-28T12:30:08.573Z",
          "to": "2021-09-28T12:30:08.573Z"
        }
      },
      "dataEraseAt": "2021-09-28T12:30:08.573Z",
      "frequency": {
        "unit": "HOUR",
        "value": 1,
        "repeats": 0
      },
      "lastUpdated": "2021-09-28T12:30:08.573Z",
      "careContexts": [
        {
          "patientReference": "batman@tmh",
          "careContextReference": "Episode1"
        }
      ],
      "schemaVersion": "v3",
      "consentManager": {
        "id": "abdm"
      }
    },
    "signature": "Signature of CM as defined in W3C standards; Base64 encoded"
  },
  "error": null,
  "response": {
    "requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"
  },
  "resp": null
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `consent` (object, required)
- `consent.status` (string, required) One of: GRANTED, DENIED, EXPIRED, REVOKED.
- `consent.consentDetail` (object, required)
- `consent.consentDetail.consentId` (string, required): Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `consent.consentDetail.hip` (object): Identifier and name of the health information provider.
- `consent.consentDetail.hip.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `consent.consentDetail.hip.name` (string, required): The name of the health information provider. Allows alpha numeric and special characters like _\-@,():/
- `consent.consentDetail.hip.type` (string): The type of the health information provider. Allows alpha numeric and special characters like _\-@,. ":/
- `consent.consentDetail.hiu` (object, required)
- `consent.consentDetail.hiu.id` (string, required): The service ID of the health information user.  Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `consent.consentDetail.hiu.name` (string, required): The name of the health information user. Allows alpha numeric and special characters like _\-@,():/
- `consent.consentDetail.hiu.type` (string): The type of the health information user. Allows alpha numeric and special characters like _\-@,. ":/
- `consent.consentDetail.hiTypes` (string[], required): Types of health information document.
- `consent.consentDetail.patient` (object, required)
- `consent.consentDetail.patient.id` (string, required): The abha address of the patient. allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.]+[a-zA-Z0-9]@(abdm|sbx)$
- `consent.consentDetail.purpose` (object, required)
- `consent.consentDetail.purpose.text` (string, required) One of: Care Management, Break the Glass, Public Health, Healthcare Payment, Disease Specific Healthcare Research, Self Requested.
- `consent.consentDetail.purpose.code` (string, required) One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQT.
- `consent.consentDetail.purpose.refUri` (string, required): The reference URL. Should be a valid URL.Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `consent.consentDetail.createdAt` (string, required)
- `consent.consentDetail.requester` (object, required)
- `consent.consentDetail.requester.name` (string, required): The name of the requester
- `consent.consentDetail.requester.identifier` (object, required)
- `consent.consentDetail.permission` (object, required)
- `consent.consentDetail.permission.accessMode` (string, required) One of: VIEW, STORE, STREAM, QUERY.
- `consent.consentDetail.permission.dateRange` (object, required)
- `consent.consentDetail.dataEraseAt` (string, required): The date at which the consent expire. Should be UTC date time in ISO format. Allows alpha numeric character and special characters like ^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$
- `consent.consentDetail.frequency` (object, required)
- `consent.consentDetail.frequency.unit` (string, required) One of: HOUR, DAY, WEEK, MONTH, YEAR.
- `consent.consentDetail.frequency.value` (number, required): The frequency unit value. Should be be a integer. Allows numeric character like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `consent.consentDetail.frequency.repeats` (number, required): Should be be a integer.Allows numeric character like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `consent.consentDetail.lastUpdated` (string, required): lastUpdated of the consent.  Should be UTC date time in ISO format. Allows alpha numeric character and special characters like ^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$
- `consent.consentDetail.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `consent.consentDetail.careContexts.patientReference` (string, required): A patient identifier with which patient is registered in the facility/hospital. Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\-@,. "':|()/]{0,255}$
- `consent.consentDetail.careContexts.careContextReference` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data). Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\-@,. "':|()/]{0,255}$
- `consent.consentDetail.schemaVersion` (string, required)
- `consent.consentDetail.consentManager` (object, required)
- `consent.consentDetail.consentManager.id` (string, required)
- `consent.signature` (string, required)
- `error` (object, required): The error code and message, if any occurred.
- `response` (object, required)
- `response.requestId` (string, required): The requestId that was passed.Allows alpha numeric character and special characters like ^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}
- `resp` (string)

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
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
