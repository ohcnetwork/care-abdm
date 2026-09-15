# Link Care Context Notify

`POST /hiecm/hip/v3/link/context/notify`

Sends an explicit notification to the ABDM Gateway about a newly linked care context.
This is called after successful care context linking to ensure the patient's ABHA App
receives a timely notification with the care context details.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/hip/v3/link/context/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "patient": {
      "id": "patient@sbx"
    },
    "careContext": {
      "patientReference": "patient@sbx",
      "careContextReference": "VISIT-2024-001"
    },
    "hiTypes": [
      "Prescription"
    ],
    "date": "2024-01-10T12:00:00.000Z",
    "hip": {
      "id": "HIP_SERVICE_ID",
      "name": "S Y Hospital",
      "type": "HIP"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value, so this is how you match an asynchronous reply to the call that caused it. Store it before you send the request, not after.
- `TIMESTAMP` (string, required): The current time in ISO 8601, UTC, with milliseconds and a `Z` suffix, from a synchronised clock. The sandbox rejects IST and accepts UTC.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. A dedicated error code exists for an invalid value here, which tells you how often it is wrong.
- `X-HIP-ID` (string, required): Identifier of the Health Information Provider the request or callback belongs to. This is per facility, and it is what a callback arriving at your one bridge URL is routed on. The bridge URL and your credentials belong to the integration, not to the facility.

## Body

- `notification` (object, required)
- `notification.patient` (object, required)
- `notification.patient.id` (string): Patient ABHA address
- `notification.careContext` (object, required)
- `notification.careContext.patientReference` (string)
- `notification.careContext.careContextReference` (string)
- `notification.hiTypes` (object[], required)
- `notification.date` (string, required)
- `notification.hip` (object, required): `id`, `name` and `type` are all required. What `name` and `type` contain beyond a string is not documented.
- `notification.hip.id` (string, required)
- `notification.hip.name` (string, required)
- `notification.hip.type` (string, required)

## Responses

- `202`: Notification accepted
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
