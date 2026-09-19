# Get user details

`GET /v1/account/user-details/{hprId}`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/user-details/{hprId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Path parameters

- `hprId` (string, required)

## Responses

- `200`: OK
- `404`: Not Found
