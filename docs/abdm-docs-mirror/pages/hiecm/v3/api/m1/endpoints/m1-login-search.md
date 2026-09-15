# Search ABHA Profile (for Password Login)

`POST /profile/login/search`

Look up a profile by ABHA Number as the first step of the password login flow.
Returns basic profile info to confirm the correct account before requesting password.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/profile/login/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "ABHANumber": "<ABHANUMBER>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `ABHANumber` (string, required): 14-digit ABHA number (with or without hyphens)

## Responses

- `200`: Profile found
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized, missing, invalid, or expired Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `404`: Resource not found
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "ABHANumber": "<ABHANUMBER>",
  "name": "<NAME>",
  "kycStatus": "VERIFIED",
  "gender": "M",
  "mobile": "<MOBILE>"
}
```
