# Get account png card

`GET /v1/account/getIdCard`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/getIdCard \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-Token: <X_TOKEN>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Headers

- `X-Token` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "pdf": "JVBERi0xLjMK"
}
```
