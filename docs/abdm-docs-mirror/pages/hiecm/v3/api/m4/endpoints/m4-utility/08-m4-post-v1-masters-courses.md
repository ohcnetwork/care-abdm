# List courses

`POST /apis/v1/masters/courses`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/courses \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "systemOfMedicine": "Registered Auxiliary Nurse Midwife(RANM)",
  "hprType": "nurse",
  "qualificationCount": 0
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `id` (integer)
- `name` (string)
- `systemOfMedicineId` (integer)
- `visibleStatus` (boolean)
- `status` (boolean)
- `sortOrder` (boolean)
- `courseCategory` (string) One of: basic, additional.
- `systemOfMedicine` (string)
- `hprType` (string) One of: doctor, nurse, facility_manager, asha, paharmacist, anganwadi, administrator, paramedical, pharmacist.
- `qualificationCount` (integer)
- `international` (boolean)
- `createdBy` (integer)
- `acronym` (string)
- `priority` (string)

## Responses

- `200`: OK
- `404`: Not Found
