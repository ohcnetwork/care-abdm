# 4. Check PHR Address Existence

`GET /api/registration/phr/exists`

Checks whether an ABHA address is already taken before the person tries to register it.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/registration/phr/exists \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
