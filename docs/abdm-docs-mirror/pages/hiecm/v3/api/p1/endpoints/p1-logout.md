# Logout

`GET /profile/phr/request/logout`

Ends the session and invalidates its tokens.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/profile/phr/request/logout \
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
  "message": "You have been logged out",
  "timestamp": "2023-07-27 13:36:28"
}
```
