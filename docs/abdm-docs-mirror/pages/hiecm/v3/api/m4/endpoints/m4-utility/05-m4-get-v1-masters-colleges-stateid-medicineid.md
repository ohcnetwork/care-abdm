# Get college by state and medicine ID

`GET /apis/v1/masters/colleges/{stateId}/{medicineId}`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/colleges/{stateId}/{medicineId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Path parameters

- `stateId` (integer, required)
- `medicineId` (string, required)

## Responses

- `200`: OK
- `404`: Not Found
