# Register / Update HIP-HIU Services (Facility Registry)

`POST /v1/bridges/MutipleHRPAddUpdateServices`

Register or update HIP/HIU services in the Facility Registry.
Must be called after updating the bridge URL.
**Server:** `https://facilitysbx.abdm.gov.in`

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v1/bridges/MutipleHRPAddUpdateServices \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "IN0710000001",
  "facilityName": "City General Hospital",
  "HRP": [
    {
      "bridgeId": "your-client-id",
      "hipName": "City General Hospital",
      "hipId": "CityGeneralHospital_HIP",
      "hipType": "HOSPITAL",
      "facilityName": "City General Hospital"
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `facilityId` (string, required): Facility identifier from the Health Facility Registry
- `facilityName` (string, required): Name of the healthcare facility
- `HRP` (object[], required): List of HIP/HIU/HRP services to register
- `HRP.bridgeId` (string, required): Your client ID (bridge identifier)
- `HRP.hipName` (string, required): Display name of the HIP
- `HRP.hipId` (string, required): Unique HIP service identifier
- `HRP.hipType` (string, required) One of: HOSPITAL, CLINIC, LAB, PHARMACY, WELLNESS, DIAGNOSTIC, OTHER.
- `HRP.facilityName` (string, required)

## Responses

- `200`: Services registered / updated successfully

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "<MESSAGE>"
}
```
