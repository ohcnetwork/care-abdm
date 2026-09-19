# Get affiliated board by state ID

`GET /apis/v1/masters/affiliated-board/states/{id}`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/affiliated-board/states/{id} \
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
    "id": 38,
    "name": "Maharashtra  State Board of Secondary  and Higher Secondary  Education,   Pune",
    "status": true,
    "visibleStatus": true,
    "stateId": 20,
    "courseId": null,
    "councilBoard": false,
    "nationalBoard": false
  },
  {
    "id": 821,
    "name": "MAHARASHTRA NURSING COUNCIL, MUMBAI",
    "status": true,
    "visibleStatus": true,
    "stateId": 20,
    "courseId": null,
    "councilBoard": true,
    "nationalBoard": false
  },
  "... 1 more of the same shape"
]
```
