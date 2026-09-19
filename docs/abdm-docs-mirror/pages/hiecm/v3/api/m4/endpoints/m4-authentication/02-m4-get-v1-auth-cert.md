# Get public certificate

`GET /api/v1/auth/cert`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/api/v1/auth/cert \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `publicCertificateRequestDto` (object, required)

## Responses

- `200`: OK
- `404`: Not Found
