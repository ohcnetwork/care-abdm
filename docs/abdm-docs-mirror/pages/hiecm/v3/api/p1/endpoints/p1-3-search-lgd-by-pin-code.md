# 3. Search LGD by Pin Code

`GET /api/registration/phr/lgd/search`

Resolves a PIN code to its state and district LGD codes, so the address can be filled from the PIN alone.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/registration/phr/lgd/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
