# Submit the v15Submit facility details

`POST /v1.5/facility/submit-facility`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/submit-facility \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'x-hprid-auth: <X_HPRID_AUTH>' \
  --header 'x-hprid-auth-verifier: <X_HPRID_AUTH_VERIFIER>' \
  --header 'Content-Type: application/json' \
  --data '{
  "trackingId": "80266",
  "sourceOfInformation": "HRP_SUB_1",
  "sourceUniqueID": "1234",
  "facilitySuperUser": "STATE_SUPER_1"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Headers

- `x-hprid-auth` (string, required)
- `x-hprid-auth-verifier` (string)

## Body

- `trackingId` (string, required)
- `sourceOfInformation` (string)
- `sourceUniqueID` (string)
- `facilitySuperUser` (string)

## Responses

- `200`: OK
- `404`: Not Found
