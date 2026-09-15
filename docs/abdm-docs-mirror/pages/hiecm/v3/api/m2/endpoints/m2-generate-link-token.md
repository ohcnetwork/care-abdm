# Generate Link Token

`POST /hiecm/v3/token/generate-token`

Generates a short-lived link token for a specific patient identified by their ABHA number/address.
The link token is passed as `X-Link-Token` header when calling the care context linking API.
Must be called immediately before the linking call, tokens expire quickly.

This call is accepted with `202` and carries no token. The token
itself arrives on the `m2_on_generate_token_result` callback, at the
callback URL registered for your bridge.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/v3/token/generate-token \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": 91234567890123,
  "abhaAddress": "patient@sbx",
  "name": "Ramesh Kumar",
  "gender": "M",
  "yearOfBirth": 1985
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

- `abhaNumber` (integer): 14-digit ABHA number (optional if abhaAddress provided)
- `abhaAddress` (string, required): ABHA address (PHR address) e.g. user@sbx
- `name` (string, required)
- `gender` (string, required) One of: M, F, O.
- `yearOfBirth` (integer, required)

## Responses

- `202`: Accepted. No body. The token arrives on the m2_on_generate_token_result callback.
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
- `503`: Service unavailable. Returned by the link token generation operation.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
