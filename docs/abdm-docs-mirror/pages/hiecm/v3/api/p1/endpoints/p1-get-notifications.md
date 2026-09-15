# Get notifications

`GET /notification/get-notification`

Lists the notifications delivered to the signed-in ABHA address.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/notification/get-notification \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
