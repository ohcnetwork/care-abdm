# Initiate a consent request

`POST /hiecm/consent/v3/request/init`

Also known as: Consent Init Request.
Initiates a new consent request for a patient's health records.

The Gateway notifies the patient via the ABHA App. The patient can approve or deny.
The HIU receives the patient's decision via a callback to `{hiuBridgeUrl}/v0.5/consents/hiu/notify`.

**Key fields:**
- `purpose.code`, ABDM-defined purpose codes (e.g. `CAREMGT`, `BTG`, `PUBHLTH`, `HPAYMT`, `DSRCH`, `PATRQST`)
- `hiTypes`, Health Information types requested
- `permission.accessMode`, `VIEW` (read-only) or `STORE`
- `permission.dataEraseAt`, Consent expiry after which data access is revoked

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'Content-Type: application/json' \
  --data '{
  "consent": {
    "purpose": {
      "text": "Care Management",
      "code": "CAREMGT",
      "refUri": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
    },
    "patient": {
      "id": "patient@sbx"
    },
    "hiu": {
      "id": "HIU_SERVICE_ID",
      "name": "City Health HIU"
    },
    "hip": null,
    "careContexts": null,
    "requester": {
      "name": "Dr. Sharma",
      "identifier": {
        "type": "REGNO",
        "value": "MCI-12345",
        "system": "https://www.mciindia.org"
      }
    },
    "hiTypes": [
      "Prescription",
      "DiagnosticReport"
    ],
    "permission": {
      "accessMode": "VIEW",
      "dateRange": {
        "from": "2023-01-01T00:00:00.000Z",
        "to": "2024-01-01T00:00:00.000Z"
      },
      "dataEraseAt": "2025-01-01T00:00:00.000Z",
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

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value. In M3 a single consent can produce several callbacks, so keep the mapping from request id to consent request id rather than relying on ordering.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production.

## Body

- `consent` (object, required)
- `consent.purpose` (object, required)
- `consent.purpose.text` (string, required)
- `consent.purpose.code` (string, required): ABDM consent purpose codes: - CAREMGT: Care Management - BTG: Break the Glass (emergency) - PUBHLTH: Public Health - HPAYMT: Health Payment - DSRCH: Disease Specific Healthcare Research - PATRQST: Patient Requested One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQST.
- `consent.purpose.refUri` (string)
- `consent.patient` (object, required)
- `consent.patient.id` (string, required): Patient's ABHA address
- `consent.hiu` (object, required)
- `consent.hiu.id` (string, required): HIU service ID
- `consent.hiu.name` (string, required): HIU display name.
- `consent.hiu.type` (string): Not otherwise constrained.
- `consent.hip` (object,null): Specific HIP to request from (null = any HIP)
- `consent.hip.id` (string, required)
- `consent.hip.name` (string, required): HIP display name.
- `consent.hip.type` (string): Not otherwise constrained.
- `consent.careContexts` (array,null): Specific care contexts (null = all matching contexts)
- `consent.requester` (object, required)
- `consent.requester.name` (string, required): Doctor / requester name
- `consent.requester.identifier` (object, required)
- `consent.requester.identifier.type` (string) One of: REGNO, NMC, MCI, AYUSH.
- `consent.requester.identifier.value` (string)
- `consent.requester.identifier.system` (string)
- `consent.hiTypes` (object[], required): Health Information types being requested
- `consent.permission` (object, required)

## Responses

- `202`: Consent request initiated successfully
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 202 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "consentRequestId": "<CONSENT_REQUEST_ID>"
}
```
