# Choose which ABHA to sign in to

`POST /v3/profile/login/verify/user`

Used when one mobile number carries several ABHA accounts, which is
common in a family. Send the `txnId` from the verify call and the ABHA
number the person picked.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'T-token: <T_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "ABHANumber": "<ABHA_NUMBER>",
  "txnId": "<TXN_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `T-token` (string, required): The transaction token that carries state between the two halves of a login. Required for account selection. See the shared `TToken` parameter for the general description.

## Body

- `ABHANumber` (string, required)
- `txnId` (string, required)

## Responses

- `200`: The user token and refresh token, with their expiries.
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
  "token": "<TOKEN>",
  "expiresIn": 0,
  "refreshToken": "<REFRESH_TOKEN>",
  "refreshExpiresIn": 0
}
```
