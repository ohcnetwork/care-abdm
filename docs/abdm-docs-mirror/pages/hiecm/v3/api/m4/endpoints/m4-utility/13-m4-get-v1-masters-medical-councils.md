# Get all medical council

`GET /apis/v1/masters/medical-councils`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/medical-councils \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Responses

- `200`: OK
- `404`: Not Found
