# 02 - Get DigiLocker Account [GET]

`GET /digi-locker/account`

Returns the DigiLocker account linked to the signed-in ABHA address, if one has been connected.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/digi-locker/account \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
