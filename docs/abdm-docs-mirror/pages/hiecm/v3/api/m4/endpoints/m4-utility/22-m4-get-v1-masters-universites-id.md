# Get university by college

`GET /apis/v1/masters/universites/{id}`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/universites/{id} \
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
    "id": 6046,
    "name": "Baba Farid University Of Health Sciences,faridkot",
    "status": true,
    "visibleStatus": true,
    "collegeId": 27,
    "collegeName": null,
    "deleted": false,
    "college": null
  }
]
```
