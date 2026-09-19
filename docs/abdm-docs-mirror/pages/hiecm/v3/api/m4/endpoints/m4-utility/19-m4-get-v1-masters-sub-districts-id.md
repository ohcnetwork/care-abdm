# Get all sub districts 1

`GET /apis/v1/masters/sub-districts/{id}`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/sub-districts/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Path parameters

- `id` (integer, required)

## Responses

- `200`: OK
- `404`: Not Found
