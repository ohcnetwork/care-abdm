# 06 - Read Uploaded Record [GET]

`GET /digi-locker/records/read`

Returns the content of one record the person uploaded to DigiLocker.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/digi-locker/records/read \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
