# Get PHR Card

`GET /profile/phr/card`

Returns the person's ABHA card as an image for display or download.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/profile/phr/card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
