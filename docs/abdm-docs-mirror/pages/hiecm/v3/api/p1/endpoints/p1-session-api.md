# Session API

`POST /api/hiecm/gateway/v3/sessions`

Issues a gateway session token from a client id and secret. The token is the bearer credential for calls on the gateway host.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "<CLIENT_ID>",
  "clientSecret": "<CLIENTSECRET>",
  "grantType": "client_credentials"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `clientId` (string, required)
- `clientSecret` (string, required)
- `grantType` (string, required)

## Responses

- `200`: No response body is documented for this request.
