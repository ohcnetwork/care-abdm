# 5. Get PHR Suggestions

`GET /api/registration/abha/suggestion`

Suggests available ABHA addresses for the registration transaction, built from the person's verified profile.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/registration/abha/suggestion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
