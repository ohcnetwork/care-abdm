# PHR - Download File Chunk

`GET /api/care-context-link/phr/file/download`

Downloads one chunk of a record file. Use the metadata call for the chunk size.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/phr/file/download \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
