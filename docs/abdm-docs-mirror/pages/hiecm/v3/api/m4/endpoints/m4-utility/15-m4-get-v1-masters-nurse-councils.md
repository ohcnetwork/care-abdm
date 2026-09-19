# Get all nurse councils

`GET /apis/v1/masters/nurse-councils`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/nurse-councils \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": 1,
    "name": "Andhra Pradesh  Nurses Midwives And Health Visitors Council, Vijayawada",
    "status": true,
    "visibleStatus": true,
    "position": 0,
    "stateId": 2
  },
  {
    "id": 2,
    "name": "Arunachal Pradesh Nursing Council",
    "status": true,
    "visibleStatus": true,
    "position": 0,
    "stateId": 3
  },
  "... 1 more of the same shape"
]
```
