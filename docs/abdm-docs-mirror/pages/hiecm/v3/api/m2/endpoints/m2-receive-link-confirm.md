# Link On-Confirm, HIP confirms linked care contexts

`POST /hiecm/user-initiated-linking/v3/link/care-context/on-confirm`

**Async Callback:** After receiving a link confirm request at the HIP bridge URL
(`{bridgeUrl}/v0.5/links/link/confirm`) with the patient's OTP, the HIP validates
the OTP and calls this Gateway endpoint to confirm the linked care contexts.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'Content-Type: application/json' \
  --data '{
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
  ],
  "response": {
    "requestId": "req-uuid-from-link-confirm"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value, so this is how you match an asynchronous reply to the call that caused it. Store it before you send the request, not after.
- `TIMESTAMP` (string, required): The current time in ISO 8601, UTC, with milliseconds and a `Z` suffix, from a synchronised clock. The sandbox rejects IST and accepts UTC.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. A dedicated error code exists for an invalid value here, which tells you how often it is wrong.

## Body

- `patient` (object[], required)
- `patient.referenceNumber` (string, required): HIP's internal patient reference number
- `patient.display` (string, required): Patient display name
- `patient.careContexts` (object[], required)
- `patient.hiType` (object[], required)
- `patient.count` (integer, required): Total number of care contexts in this entry
- `response` (object, required): Echo of the requestId from the original Gateway-to-HIP request
- `response.requestId` (string, required): requestId received in the original Gateway request to HIP bridge

## Responses

- `202`: Link confirm response accepted by Gateway
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. Returned as plain text ("Access Denied"), not JSON.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal server error.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
