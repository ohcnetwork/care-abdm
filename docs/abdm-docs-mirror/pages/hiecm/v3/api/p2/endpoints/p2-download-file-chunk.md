# Download File Chunk

`GET /api/care-context-link/file/download`

Downloads one chunk of a record file. Use the metadata call for the chunk size.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/file/download \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
