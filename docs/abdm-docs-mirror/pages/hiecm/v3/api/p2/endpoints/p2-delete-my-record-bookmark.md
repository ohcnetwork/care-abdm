# Delete My Record Bookmark

`DELETE /api/care-context-link/my-record/bookmark`

Removes a bookmark from a self-uploaded record.

```bash
curl --request DELETE \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/my-record/bookmark \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
