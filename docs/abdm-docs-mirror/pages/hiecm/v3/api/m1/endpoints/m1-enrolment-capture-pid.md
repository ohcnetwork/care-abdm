# Submit a captured biometric or face authentication block

`POST /v3/enrollment/enrol/capturePID`

Hands over the PID block produced by the Aadhaar RD service. The block is
encrypted by the device and is time limited, so send it as soon as the
capture returns rather than storing it.

This is a polling loop. All three states come back as HTTP 200, so
branch on `status` and not on the status code. `PENDING` and `VERIFIED`
both mean the capture has not landed yet and carry the same message,
`Awaiting PID capture`. Only `COMPLETE` carries the `txnId` you take
into the next call. Keep polling until you see it.

One caveat about where these came from. NHA saved the `COMPLETE`
example against `enrollment/enrol/capturePID`, and saved the `PENDING`
and `VERIFIED` examples against `enrollment/enrol/internal/capturePID`,
a path that appears nowhere else in the collection and that NHA's M1
document never mentions. Whether the two paths are one endpoint is
unresolved here.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/capturePID \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "face-verify"
  ],
  "txnId": "<TXN_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `scope` (string[], required)
- `txnId` (string, required)

## Responses

- `200`: The capture status, a message, and the transaction id.
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized, missing, invalid, or expired Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "status": "VERIFIED",
  "message": "Awaiting PID capture"
}
```
