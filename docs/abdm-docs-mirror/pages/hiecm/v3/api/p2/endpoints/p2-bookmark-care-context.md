# Bookmark Care Context

`POST /api/care-context-link/bookmark/{careContextLinkId}`

Bookmarks a linked care context so it is easy to find again in the person's records.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/bookmark/{careContextLinkId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `careContextLinkId` (string, required): Passed as a path segment.

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
