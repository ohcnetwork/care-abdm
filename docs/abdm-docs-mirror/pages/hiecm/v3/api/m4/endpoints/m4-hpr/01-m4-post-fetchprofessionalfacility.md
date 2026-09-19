# Fetch professional facility

`POST /fetchProfessionalFacility`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/fetchProfessionalFacility \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "<FACILITY_ID>",
  "page": 0,
  "size": 0
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `facilityId` (string)
- `page` (integer)
- `size` (integer)

## Responses

- `200`: OK
- `404`: Not Found
