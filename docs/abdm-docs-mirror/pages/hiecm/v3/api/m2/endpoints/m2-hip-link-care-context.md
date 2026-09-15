# Link care contexts to an ABHA address

`POST /hiecm/hip/v3/link/carecontext`

Also known as: HIP Initiated Care Context Linking (Single or Multiple).
Links one or more care contexts (health records) to a patient's ABHA address.
Use the same endpoint for both single and multiple care context linking, the `careContexts` array can contain one or many entries.

Requires the `X-Link-Token` header with a freshly generated link token.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/hip/v3/link/carecontext \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'X-Link-Token: <X_LINK_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": "91234567890123",
  "abhaAddress": "patient@sbx",
  "patient": [
    {
      "referenceNumber": "PAT-REF-001",
      "display": "Ramesh Kumar",
      "careContexts": [
        {
          "referenceNumber": "VISIT-2024-001",
          "display": "OPD Visit 10-Jan-2024"
        }
      ],
      "hiType": [
        "Prescription"
      ],
      "count": 1
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value, so this is how you match an asynchronous reply to the call that caused it. Store it before you send the request, not after.
- `TIMESTAMP` (string, required): The current time in ISO 8601, UTC, with milliseconds and a `Z` suffix, from a synchronised clock. The sandbox rejects IST and accepts UTC.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. A dedicated error code exists for an invalid value here, which tells you how often it is wrong.
- `X-HIP-ID` (string, required): Identifier of the Health Information Provider the request or callback belongs to. This is per facility, and it is what a callback arriving at your one bridge URL is routed on. The bridge URL and your credentials belong to the integration, not to the facility.
- `X-Link-Token` (string, required): Short-lived link token generated via POST /hiecm/v3/token/generate-token

## Body

- `abhaNumber` (string): 14-digit ABHA number (optional)
- `abhaAddress` (string, required): ABHA address of the patient
- `patient` (object[], required)
- `patient.referenceNumber` (string, required): HIP's internal patient reference number
- `patient.display` (string, required): Patient display name
- `patient.careContexts` (object[], required)
- `patient.hiType` (object[], required)
- `patient.count` (integer, required): Total number of care contexts in this entry

## Responses

- `202`: Care context linking accepted and queued
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. Returned as plain text ("Access Denied"), not JSON.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `404`: Resource not found
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal server error.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
