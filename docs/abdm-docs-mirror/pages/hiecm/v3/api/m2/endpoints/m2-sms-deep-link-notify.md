# Send an SMS with a deep link to the ABHA App

`POST /hiecm/hip/v3/link/patient/links/sms/notify2`

Also known as: SMS Deep Link Notify.
Requests ABDM to send an SMS to a patient's mobile number containing a deep link
to download/open the ABHA App. Used when a patient is not yet on ABDM and the HIP
wants to invite them to link their health records.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/hip/v3/link/patient/links/sms/notify2 \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'Content-Type: application/json' \
  --data '{
  "requestId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "timestamp": "2024-01-10T12:00:00.000Z",
  "notification": {
    "phoneNo": "917812345678",
    "hip": {
      "name": "S Y Hospital",
      "id": "HIP_SERVICE_ID"
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

## Body

- `requestId` (string, required): Unique request ID (UUIDv4)
- `timestamp` (string, required)
- `notification` (object, required)
- `notification.phoneNo` (string, required): Patient mobile number with country code (e.g. 917812345678)
- `notification.hip` (object, required)
- `notification.hip.name` (string, required)
- `notification.hip.id` (string, required)

## Responses

- `202`: SMS notification queued
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
