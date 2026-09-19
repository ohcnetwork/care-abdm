# Receive the consent decision

`POST /api/v3/consent/request/hip/notify`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
Notification of consents to health information providers consent request granted, consent revoked, consent expired. Only the GRANTED, REVOKED and EXPIRED status notifications will be sent to HIP. If consent is granted, status=GRANTED, then consentDetail contains the consent artefact details and signature is available. If consent is revoked, then status=REVOKED, and consentId specifes which consent artefact is revoked. If the consent has expired, then status=EXPIRED, and consentId specifies which consent artefact has expired. Note, this is also responsibility of the HIP to keep track of consent expiry. Any data request on expired consent artefact must not be done.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/consent/request/hip/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "status": "GRANTED",
    "consentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "consentDetail": {
      "schemaVersion": "v3",
      "consentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "createdAt": "2024-05-01T05:10:20.123Z",
      "patient": {
        "id": "<ABHA_ADDRESS>"
      },
      "careContexts": [
        {
          "patientReference": "batman@tmh",
          "careContextReference": "Episode1"
        }
      ],
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "www.abc.com"
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
      "consentManager": {
        "id": "abdm"
      },
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
    },
    "signature": "e8nY601CYDsC0FKoDjSp+7GeQ2s2R8oZncLCz5ce+pEuDOr5bZV0aaHjwJg4b9S9V+twjt4hbojx3fl7egrt8+0c+lfPTi5/bBUAQXCABTfFmtFU7jn65HlTt8kgkiONx26ZBhJ0wX3xjYI72PPtzYIiT5Q08YtDoILA62KceioV7lwuKssw7wC4ECbBAvRuXT121TmtrPhf+0myJATSnaajS06S6OthrKfZLNTUFf3pFiJzqouSTrjNblOX6DT2+JuO3rom1Szz/03c0HQG+wWASv+PO3J6uRs0UI4JvKmM/4tP+Z+/HPKM15K5U5K+4pqf6czKrbIDpkT/kP8bGg==",
    "grantAcknowledgement": false
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

- `notification` (object, required)
- `notification.status` (string, required) One of: GRANTED, EXPIRED, DENIED, REQUESTED, REVOKED.
- `notification.consentId` (string, required): Allows alpha numeric character and special characters like "^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}$";
- `notification.consentDetail` (object, required)
- `notification.consentDetail.schemaVersion` (string, required)
- `notification.consentDetail.consentId` (string, required): Allows alpha numeric character and special characters like "^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}$";
- `notification.consentDetail.createdAt` (string, required): Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `notification.consentDetail.patient` (object, required)
- `notification.consentDetail.patient.id` (string, required): The abha address of the patient. Allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.]+[a-zA-Z0-9]@(abdm|sbx)$
- `notification.consentDetail.careContexts` (object[], required): List of care contexts linked at the HIP end for the identified patient.
- `notification.consentDetail.careContexts.patientReference` (string, required): A patient identifier with which patient is registered in the facility/hospital. Allows alpha numeric and special characters like "^[a-zA-Z0-9_\\-@,().\"/: ]{0,255}$"
- `notification.consentDetail.careContexts.careContextReference` (string, required): An identifier of patient's care context created in HIP. A care context is a group of patient's health data (Not the actual health data). Allows alpha numeric and special characters like  "^[a-zA-Z0-9_\\-@,().\"/:| ]{0,255}$"
- `notification.consentDetail.purpose` (object, required)
- `notification.consentDetail.purpose.text` (string, required) One of: Care Management, Break the Glass, Public Health, Healthcare Payment, Disease Specific Healthcare Research, Self Requested.
- `notification.consentDetail.purpose.code` (string, required) One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQT.
- `notification.consentDetail.purpose.refUri` (string, required): The reference URL. Should be a valid URL. Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `notification.consentDetail.hip` (object, required): Identifier and name of the health information provider.
- `notification.consentDetail.hip.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `notification.consentDetail.hip.name` (string, required): The name of the health information provider. Allows alpha numeric and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `notification.consentDetail.hip.type` (string): The type of the health information provider. Allows alpha numeric and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `notification.consentDetail.hiu` (object, required)
- `notification.consentDetail.hiu.id` (string, required): The service ID of the health information user.  Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `notification.consentDetail.hiu.name` (string, required): The name of the health information user. Allows alpha numeric and special characters like ^[a-zA-Z]+[A-Za-z0-9_\\-@,().\\s\\xa0:/]+
- `notification.consentDetail.hiu.type` (string): The type of the health information user. Allows alpha numeric and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `notification.consentDetail.consentManager` (object, required)
- `notification.consentDetail.consentManager.id` (string, required)
- `notification.consentDetail.requester` (object, required)
- `notification.consentDetail.requester.name` (string, required): The name of the requester
- `notification.consentDetail.requester.identifier` (object, required)
- `notification.consentDetail.hiTypes` (string[], required): Types of health information document.
- `notification.consentDetail.permission` (object, required)
- `notification.consentDetail.permission.accessMode` (string, required) One of: VIEW, STORE, STREAM, QUERY.
- `notification.consentDetail.permission.dateRange` (object, required)
- `notification.consentDetail.permission.dataEraseAt` (string, required): The date at which the consent expire. Should be UTC date time in ISO format.Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `notification.consentDetail.permission.frequency` (object, required)
- `notification.signature` (string, required)
- `notification.grantAcknowledgement` (boolean, required)

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
