# Link delink existing facility

`POST /relinkOrDelinkProfessionalFromFacility`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/relinkOrDelinkProfessionalFromFacility \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>",
  "facilityId": "<FACILITY_ID>",
  "action": "<ACTION>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hprId` (string)
- `facilityId` (string)
- `action` (string)

## Responses

- `200`: OK
- `404`: Not Found
