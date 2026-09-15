# Claim a chosen ABHA address

`POST /v3/enrollment/enrol/abha-address`

Attaches the address the person picked to the ABHA number created
earlier. `preferred: 1` marks it as the one to show.

Until this succeeds the account has only the default address that the service
issues automatically, which is the fourteen digit number followed by
`@sbx` or `@abdm` and which nobody can remember.

The ABHA number comes back from this call as `healthIdNumber`, not as
`ABHANumber`. The enrol response spells the same value `ABHANumber`, so
a client that reuses its enrol parsing here reads nothing.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "abhaAddress": "<ABHA_ADDRESS>",
  "preferred": 1
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `txnId` (string, required)
- `abhaAddress` (string, required)
- `preferred` (integer, required)

## Responses

- `200`: Response body not fully documented. `healthIdNumber` is confirmed; the rest of the shape is not.
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
  "healthIdNumber": "<HEALTH_ID_NUMBER>"
}
```
