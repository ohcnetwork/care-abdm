# Search Care Context Links

`GET /api/care-context-link/search/care-context-link`

Searches the person's care context links by the query parameters given.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/search/care-context-link \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
