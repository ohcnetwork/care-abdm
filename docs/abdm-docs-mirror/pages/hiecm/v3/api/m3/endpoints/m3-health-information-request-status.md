# Health Information Request Status

`GET /hiecm/data-flow/v3/health-information/request/status/{transaction-id}`

Polls the current status of a previously made health information request, by
transaction id. An alternative to waiting for the `on-request` and data flow
notify callbacks: useful if a callback was missed, or if the integration
prefers to poll rather than depend on inbound delivery.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/request/status/{transaction-id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value. In M3 a single consent can produce several callbacks, so keep the mapping from request id to consent request id rather than relying on ordering.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production.

## Path parameters

- `transaction-id` (string, required): The health information request transaction id, from the original request.

## Responses

- `200`: Current status of the health information request.
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Resource not found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "transactionId": "<TRANSACTION_ID>",
  "status": "<STATUS>"
}
```
