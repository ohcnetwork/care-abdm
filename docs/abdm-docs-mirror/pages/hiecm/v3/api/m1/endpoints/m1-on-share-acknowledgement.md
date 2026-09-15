# Send Share Acknowledgement (HIP → Gateway)

`POST /patient-share/v3/on-share`

HIP sends an acknowledgement back to the ABDM Gateway after receiving
and processing the patient's shared profile.
Typically includes a token/queue number assigned to the patient.
**Server:** `https://dev.abdm.gov.in/api/hiecm`

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/patient-share/v3/on-share \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "SUCCESS",
    "abhaAddress": "johnkumar@sbx",
    "profile": {
      "context": "123",
      "tokenNumber": "TKN-0042"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `acknowledgement` (object, required)
- `acknowledgement.status` (string, required): Processing result One of: SUCCESS, FAILURE.
- `acknowledgement.abhaAddress` (string, required): ABHA Address of the patient who shared their profile
- `acknowledgement.profile` (object): Present on SUCCESS, echoes context and provides assigned token
- `acknowledgement.profile.context` (string): Context value from the original share request
- `acknowledgement.profile.tokenNumber` (string): Queue/token number assigned to the patient by the HIP
- `acknowledgement.error` (object): Present on FAILURE
- `acknowledgement.error.code` (string)
- `acknowledgement.error.message` (string)

## Responses

- `200`: Acknowledgement accepted by Gateway
