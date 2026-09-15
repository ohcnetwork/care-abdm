# Delete

`DELETE /health/service/bookmark/delete/{id}`

Deletes one of the person's saved place bookmarks.

```bash
curl --request DELETE \
  --url https://phrsbx.abdm.gov.in/health/service/bookmark/delete/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `id` (string, required): Passed as a path segment.

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
