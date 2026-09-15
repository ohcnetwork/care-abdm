# Refresh Token

`GET /profile/phr/request/token`

Exchanges a refresh token for a new access token, so the session continues without signing in again.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/profile/phr/request/token \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "tokens": {
    "token": "<TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<REFRESHTOKEN>",
    "refreshExpiresIn": 1296000
  }
}
```
