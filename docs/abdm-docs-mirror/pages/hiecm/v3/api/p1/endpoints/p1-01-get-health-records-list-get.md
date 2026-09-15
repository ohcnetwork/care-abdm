# 01 - Get Health Records List [GET]

`GET /digi-locker/records/list`

Lists the health records held in the person's DigiLocker.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/digi-locker/records/list \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
