# 1. Get All States

`GET /api/registration/phr/lgd/state`

Lists every state with its LGD code, for the address section of registration.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/registration/phr/lgd/state \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
