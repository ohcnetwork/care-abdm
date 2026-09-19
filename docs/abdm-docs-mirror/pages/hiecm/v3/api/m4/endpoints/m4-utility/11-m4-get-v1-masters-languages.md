# List government health programmes

`GET /apis/v1/masters/languages`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/languages \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Responses

- `200`: OK
- `404`: Not Found
