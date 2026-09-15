# The patient's decision, sent to the record holder

`POST /api/v3/consent/request/hip/notify`

The same decision sent to the system that holds the records, with all care context references.

`status` only ever carries `GRANTED`, `REVOKED` or `EXPIRED` on this callback.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/api/v3/consent/request/hip/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "status": "GRANTED",
  "consentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "consentDetail": {
    "schemaVersion": "v3",
    "consentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "createdAt": "2024-05-01T05:10:20.123Z",
    "patient": {
      "id": "abdulkalam@abdm"
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
      "name": "abdulkalam@abdm",
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
  "signature": "scrubbed-base64-signature",
  "grantAcknowledgement": false
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Body

- `status` (string, required): The values actually sent to a HIP on this callback. One of: GRANTED, REVOKED, EXPIRED.
- `consentId` (string, required)
- `consentDetail` (object, required)
- `consentDetail.schemaVersion` (string, required)
- `consentDetail.consentId` (string, required)
- `consentDetail.createdAt` (string, required)
- `consentDetail.patient` (object, required)
- `consentDetail.patient.id` (string, required)
- `consentDetail.careContexts` (object[], required)
- `consentDetail.careContexts.patientReference` (string, required)
- `consentDetail.careContexts.careContextReference` (string, required)
- `consentDetail.purpose` (object, required)
- `consentDetail.purpose.text` (string, required)
- `consentDetail.purpose.code` (string, required)
- `consentDetail.purpose.refUri` (string, required)
- `consentDetail.hip` (object, required)
- `consentDetail.hip.id` (string, required)
- `consentDetail.hip.name` (string, required)
- `consentDetail.hip.type` (string)
- `consentDetail.hiu` (object, required)
- `consentDetail.hiu.id` (string, required)
- `consentDetail.hiu.name` (string, required)
- `consentDetail.hiu.type` (string)
- `consentDetail.consentManager` (object, required)
- `consentDetail.consentManager.id` (string, required)
- `consentDetail.requester` (object, required)
- `consentDetail.requester.name` (string, required)
- `consentDetail.requester.identifier` (object, required)
- `consentDetail.requester.identifier.value` (string, required)
- `consentDetail.requester.identifier.type` (string, required)
- `consentDetail.requester.identifier.system` (string, required)
- `consentDetail.hiTypes` (object[], required)
- `consentDetail.permission` (object, required)
- `consentDetail.permission.accessMode` (string, required) One of: VIEW, STORE, QUERY, STREAM.
- `consentDetail.permission.dateRange` (object, required)
- `consentDetail.permission.dateRange.from` (string): Start of the data access window
- `consentDetail.permission.dateRange.to` (string): End of the data access window
- `consentDetail.permission.dataEraseAt` (string, required): Consent expiry, after this the HIU must delete the data
- `consentDetail.permission.frequency` (object, required)
- `consentDetail.permission.frequency.unit` (string) One of: HOUR, DAY, WEEK, MONTH, YEAR.
- `consentDetail.permission.frequency.value` (integer): Frequency value
- `consentDetail.permission.frequency.repeats` (integer): Number of repeats (0 = unlimited during consent period)
- `signature` (string, required): Base64-encoded digital signature of the consent artefact.
- `grantAcknowledgement` (boolean, required): Required; no further semantics are documented for this field beyond the boolean value.

## Responses

- `200`: Your bridge acknowledged the callback with 200 OK. The gateway validates the body you send back, so a 200 carrying the wrong body is still a failure.
