# Update status

`PUT /hprWorkDetails/status`

```bash
curl --request PUT \
  --url https://apihspsbx.abdm.gov.in/v4/int/hprWorkDetails/status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "status": "<STATUS>",
  "facilityId": "<FACILITY_ID>",
  "professionalHprId": "<PROFESSIONAL_HPR_ID>",
  "managerHprId": "<MANAGER_HPR_ID>",
  "isHpr": false
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `status` (string)
- `facilityId` (string)
- `professionalHprId` (string)
- `managerHprId` (string)
- `isHpr` (boolean)

## Responses

- `200`: OK
- `404`: Not Found
