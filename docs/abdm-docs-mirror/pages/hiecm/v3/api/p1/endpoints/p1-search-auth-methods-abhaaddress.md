# Search Auth Methods - ABHAAddress

`POST /login/phr/search`

Returns the authentication methods available for an ABHA address, so the login can offer only the ones that will work.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/login/phr/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `abhaAddress` (string, required)

## Responses

- `200`: No response body is documented for this request.
