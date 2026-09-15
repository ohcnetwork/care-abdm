# AS - RecordShare History

`GET /scan-share/share-record/audit-history`

Lists the record shares the person has made, with the sending and receiving facilities and the counter they were shared at.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/scan-share/share-record/audit-history \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "requestId": "<TXN_ID>",
    "abhaAddress": "<ABHA_ADDRESS>",
    "senderFacilityId": "sbx_aaroga_setu_aws",
    "senderFacilityName": "Sandbox Aaroga-Setu-Aws",
    "receiverFacilityId": "IN2810001317",
    "receiverFacilityName": "MEDIPLUS HOSPITAL ",
    "counterCode": "1",
    "transactionId": "<TXN_ID>",
    "status": "TRANSFERRED",
    "sharedRecordCount": 2,
    "consent": {
      "accessMode": "VIEW",
      "dataEraseAt": "2026-05-30T11:54:00.000Z",
      "careContexts": [
        {
          "patientReference": "manish_191@sbx",
          "careContextReference": "03dc029b-f580-5b19-baff-47a707221658_20260518134701945848"
        },
        {
          "patientReference": "manish_191@sbx",
          "careContextReference": "03dc029b-f580-5b19-baff-47a707221658_20260518130702309469"
        }
      ]
    },
    "dateCreated": "2026-05-29T11:54:54.528Z",
    "dateModified": "2026-05-29T11:54:56.315Z"
  },
  {
    "requestId": "<TXN_ID>",
    "abhaAddress": "<ABHA_ADDRESS>",
    "senderFacilityId": "sbx_aaroga_setu_aws",
    "senderFacilityName": "Sandbox Aaroga-Setu-Aws",
    "receiverFacilityId": "IN2810001317",
    "receiverFacilityName": "MEDIPLUS HOSPITAL ",
    "counterCode": "1",
    "transactionId": "<TXN_ID>",
    "status": "TRANSFERRED",
    "sharedRecordCount": 3,
    "consent": {
      "accessMode": "VIEW",
      "dataEraseAt": "2026-05-30T11:22:00.000Z",
      "careContexts": [
        {
          "patientReference": "manish_191@sbx",
          "careContextReference": "03dc029b-f580-5b19-baff-47a707221658_20260518134701945848"
        },
        {
          "patientReference": "manish_191@sbx",
          "careContextReference": "03dc029b-f580-5b19-baff-47a707221658_20260518130702309469"
        },
        "... 1 more of the same shape"
      ]
    },
    "dateCreated": "2026-05-29T11:22:41.680Z",
    "dateModified": "2026-05-29T11:22:45.987Z"
  },
  "... 1 more of the same shape"
]
```
