# Get college by state

`GET /apis/v1/masters/colleges/{id}`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/colleges/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Path parameters

- `id` (integer, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": 21,
    "name": "Dayanand Medical College And Hospital",
    "status": true,
    "visibleStatus": true,
    "createdAt": "2023-08-17T16:58:31.000Z",
    "systemOfMedicineId": 1,
    "stateId": 27,
    "courseId": null,
    "stateName": "Maharashtra",
    "systemOfMedicineName": null,
    "deleted": false
  },
  {
    "id": 22,
    "name": "Gian Sagar Medical College And Hospital",
    "status": true,
    "visibleStatus": true,
    "createdAt": "2023-08-17T16:58:31.000Z",
    "systemOfMedicineId": 1,
    "stateId": 27,
    "courseId": null,
    "stateName": "Maharashtra",
    "systemOfMedicineName": null,
    "deleted": false
  },
  "... 1 more of the same shape"
]
```
