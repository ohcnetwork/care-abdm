# 03 - Get Access Token / OAuth Callback [GET]

`GET /digi-locker/getCode`

Completes the DigiLocker OAuth flow: exchanges the authorisation code DigiLocker redirected back with for an access token.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/digi-locker/getCode \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
