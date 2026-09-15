# Download PHR Card

`GET /phr/web/login/profile/abha/phr-card`

Download the PHR / ABHA Address card image.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/phr/web/login/profile/abha/phr-card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-Token: <X_TOKEN>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>'
```

## Authorization

- `Authorization` (bearer token, required): JWT Bearer token from `POST /api/hiecm/gateway/v3/sessions`. Header: `Authorization: Bearer {accessToken}`
- `X-Token` (apiKey, required): Short-lived session token returned in login/verify responses. Required for all `/profile/account/*` operations. Header: `X-Token: {token}`

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Responses

- `200`: PHR Card image (PNG)
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized, missing, invalid, or expired Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
