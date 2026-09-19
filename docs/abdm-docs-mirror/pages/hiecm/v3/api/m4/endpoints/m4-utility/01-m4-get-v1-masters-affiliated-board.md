# Get all affiliated board

`GET /apis/v1/masters/affiliated-board`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/affiliated-board \
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
    "name": "Central Board Of Secondary Education (CBSE)",
    "status": true,
    "visibleStatus": true,
    "stateId": null,
    "courseId": null,
    "councilBoard": false,
    "nationalBoard": true
  },
  {
    "id": 2,
    "name": "Council for the Indian School Certificate Examination (CISCE)",
    "status": true,
    "visibleStatus": true,
    "stateId": null,
    "courseId": null,
    "councilBoard": false,
    "nationalBoard": true
  },
  "... 1 more of the same shape"
]
```
