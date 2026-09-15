# Session-Token

`POST /api/global/get/session`

Issues the access token every PHR application call carries as a bearer token, with its refresh token and both expiry windows.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/global/get/session \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `403`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "accessToken": "<ACCESSTOKEN>",
  "expiresIn": 1200,
  "refreshExpiresIn": 1800,
  "refreshToken": "<REFRESHTOKEN>",
  "tokenType": "<TOKENTYPE>"
}
```
