# Register / Update Bridge Services (HIU)

`POST /v4/int/v1/bridges/MutipleHRPAddUpdateServices`

Registers or updates one or more HIU service entries under a facility
in the HSP Registry. Set `type` to `"HIU"` for Health Information User registration.
**Base URL:** `https://apihspsbx.abdm.gov.in`

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/v4/int/v1/bridges/MutipleHRPAddUpdateServices \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "IN07100XXXXX",
  "facilityName": "City Health HIU",
  "HRP": [
    {
      "bridgeId": "BRIDGE_HIU_001",
      "hipName": "City Health HIU",
      "type": "HIU",
      "active": true
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): JWT Bearer token from `POST /api/hiecm/gateway/v3/sessions`. Header: `Authorization: Bearer {accessToken}`

## Body

- `facilityId` (string, required)
- `facilityName` (string, required)
- `HRP` (object[], required)
- `HRP.bridgeId` (string, required)
- `HRP.hipName` (string, required)
- `HRP.type` (string, required) One of: HIP, HIU.
- `HRP.active` (boolean, required)

## Responses

- `200`: HIU service registered/updated successfully
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/gateway/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
