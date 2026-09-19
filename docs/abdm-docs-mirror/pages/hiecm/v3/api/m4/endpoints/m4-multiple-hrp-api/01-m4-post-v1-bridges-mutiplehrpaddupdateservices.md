# Submit the facility add and update

`POST /v1/bridges/MutipleHRPAddUpdateServices`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/bridges/MutipleHRPAddUpdateServices \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "IN0610090166",
  "facilityName": "Singla Eye Center",
  "HRP": [
    {
      "bridgeId": "SBX_00XXXX",
      "hipName": "Singla Eye Center",
      "type": "HIP",
      "active": true
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `facilityId` (string, required)
- `facilityName` (string, required)
- `HRP` (object[])
- `HRP.bridgeId` (string, required)
- `HRP.hipName` (string, required)
- `HRP.type` (string, required)
- `HRP.active` (boolean, required)

## Responses

- `200`: OK
- `404`: Not Found
