# Get medical council by system of medicine name

`GET /apis/v1/masters/medical-councils/name`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/medical-councils/name \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Query parameters

- `medicineName` (string, required)

## Responses

- `200`: OK
- `404`: Not Found
