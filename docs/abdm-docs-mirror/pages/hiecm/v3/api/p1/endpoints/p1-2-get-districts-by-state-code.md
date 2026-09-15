# 2. Get Districts by State Code

`GET /api/registration/phr/lgd/district`

Lists the districts of a state, keyed by LGD code, for the address section of registration.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/registration/phr/lgd/district \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
