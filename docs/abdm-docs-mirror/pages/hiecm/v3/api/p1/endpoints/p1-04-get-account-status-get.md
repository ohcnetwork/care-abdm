# 04 - Get Account Status [GET]

`GET /digi-locker/status`

Reports whether the person's DigiLocker account is connected and ready to receive records.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/digi-locker/status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
