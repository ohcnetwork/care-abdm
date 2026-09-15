# 10 - Get HIP Refresh Records [GET]

`GET /digi-locker/hip/pull/records`

Returns the records a refresh pulled from a HIP into DigiLocker, once the pull has completed.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/digi-locker/hip/pull/records \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
