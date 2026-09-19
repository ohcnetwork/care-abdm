# Get PSU details by ministry

`GET /getPsuDetailsByMinistry`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/getPsuDetailsByMinistry \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `ministry` (string)

## Responses

- `200`: OK
- `404`: Not Found
