# Create facility suggestion

`POST /hprFacilitySuggestions`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/hprFacilitySuggestions \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "<NAME>",
  "address": "<ADDRESS>",
  "state": {
    "id": 0,
    "name": "<NAME>",
    "isoCode": "<ISO_CODE>",
    "status": false,
    "countryId": 0,
    "visibleStatus": false,
    "position": false,
    "councilLabel": "<COUNCIL_LABEL>",
    "systemOfMedicine": false
  },
  "district": {
    "id": 0,
    "stateId": 0,
    "districtName": "<DISTRICT_NAME>",
    "isoCode": "<ISO_CODE>",
    "status": false
  },
  "pincode": 0,
  "contactNo": 0,
  "email": "<EMAIL>",
  "contactName": "<CONTACT_NAME>",
  "status": "pending",
  "createdBy": 0,
  "updatedBy": 0,
  "facilityId": 0,
  "hprProfileId": 0,
  "facilityName": "<FACILITY_NAME>",
  "facilityOwnership": {
    "label": "<LABEL>",
    "value": "<VALUE>"
  },
  "systemMedicine": [
    {
      "id": "<ID>",
      "lastUpdateDate": "<LAST_UPDATE_DATE>",
      "dropOrder": 0,
      "creationDate": "<CREATION_DATE>",
      "activeYN": "<ACTIVE_YN>",
      "createdBy": "<CREATED_BY>",
      "lastUpdatedUser": "<LAST_UPDATED_USER>",
      "nhrrMedicineCode": "<NHRR_MEDICINE_CODE>",
      "value": "<VALUE>",
      "type": "<TYPE>"
    }
  ],
  "facilityType": {
    "id": "<ID>",
    "facilityType": "<FACILITY_TYPE>",
    "facilityTypeNdhm": "<FACILITY_TYPE_NDHM>",
    "opd": "<OPD>",
    "ipd": "<IPD>",
    "dayCare": "<DAY_CARE>",
    "other": "<OTHER>",
    "activeYN": "<ACTIVE_YN>",
    "createdBy": "<CREATED_BY>",
    "createdDate": "<CREATED_DATE>",
    "lastUpdatedUser": "<LAST_UPDATED_USER>",
    "lastUpdatedDate": "<LAST_UPDATED_DATE>",
    "linkToForm": "<LINK_TO_FORM>",
    "facilityCode": "<FACILITY_CODE>",
    "facilityCodeUfid": "<FACILITY_CODE_UFID>",
    "facilityOrder": 0
  },
  "department": "<DEPARTMENT>",
  "designation": "<DESIGNATION>",
  "ministry": {
    "ministry": "<MINISTRY>"
  },
  "psuName": "<PSU_NAME>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `name` (string)
- `address` (string)
- `state` (object)
- `state.id` (integer)
- `state.name` (string)
- `state.isoCode` (string)
- `state.status` (boolean)
- `state.countryId` (integer)
- `state.visibleStatus` (boolean)
- `state.position` (boolean)
- `state.councilLabel` (string)
- `state.systemOfMedicine` (boolean)
- `district` (object)
- `district.id` (integer)
- `district.stateId` (integer)
- `district.districtName` (string)
- `district.isoCode` (string)
- `district.status` (boolean)
- `pincode` (integer)
- `contactNo` (integer)
- `email` (string)
- `contactName` (string)
- `status` (string) One of: pending, approved, rejected.
- `createdBy` (integer)
- `updatedBy` (integer)
- `facilityId` (integer)
- `hprProfileId` (integer)
- `facilityName` (string)
- `facilityOwnership` (object)
- `facilityOwnership.label` (string)
- `facilityOwnership.value` (string)
- `systemMedicine` (object[])
- `systemMedicine.id` (string)
- `systemMedicine.lastUpdateDate` (string)
- `systemMedicine.dropOrder` (integer)
- `systemMedicine.creationDate` (string)
- `systemMedicine.activeYN` (string)
- `systemMedicine.createdBy` (string)
- `systemMedicine.lastUpdatedUser` (string)
- `systemMedicine.nhrrMedicineCode` (string)
- `systemMedicine.value` (string)
- `systemMedicine.type` (string)
- `facilityType` (object)
- `facilityType.id` (object)
- `facilityType.facilityType` (string)
- `facilityType.facilityTypeNdhm` (string)
- `facilityType.opd` (string)
- `facilityType.ipd` (string)
- `facilityType.dayCare` (string)
- `facilityType.other` (string)
- `facilityType.activeYN` (string)
- `facilityType.createdBy` (string)
- `facilityType.createdDate` (string)
- `facilityType.lastUpdatedUser` (string)
- `facilityType.lastUpdatedDate` (string)
- `facilityType.linkToForm` (string)
- `facilityType.facilityCode` (string)
- `facilityType.facilityCodeUfid` (string)
- `facilityType.facilityOrder` (integer)
- `department` (string)
- `designation` (string)
- `ministry` (object)
- `ministry.ministry` (string)
- `psuName` (string)

## Responses

- `200`: OK
- `404`: Not Found
