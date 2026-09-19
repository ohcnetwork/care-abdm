# Get facility and infrastructure within radius with filter

`POST /FacilityManagement/v1.5/facility/bygeoLocation/searchFacilityAndInfrastructureWithinRadiusWithFilter`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/FacilityManagement/v1.5/facility/bygeoLocation/searchFacilityAndInfrastructureWithinRadiusWithFilter \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "centerLat": "<CENTER_LAT>",
  "centerLon": "<CENTER_LON>",
  "radiusInKm": "<RADIUS_IN_KM>",
  "speciality": "<SPECIALITY>",
  "facilityOwnership": "<FACILITY_OWNERSHIP>",
  "abdmSoftware": "<ABDM_SOFTWARE>",
  "hospitalSpecialityType": "<HOSPITAL_SPECIALITY_TYPE>",
  "facilityName": "<FACILITY_NAME>",
  "facilityStatus": "<FACILITY_STATUS>",
  "som": "<SOM>",
  "gender": "<GENDER>",
  "doctorName": "<DOCTOR_NAME>",
  "doctorSystemOfMedicine": "<DOCTOR_SYSTEM_OF_MEDICINE>",
  "languages": "<LANGUAGES>",
  "isIcuBedsAvailable": "<IS_ICU_BEDS_AVAILABLE>",
  "size": "<SIZE>",
  "from": "<FROM>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `centerLat` (string)
- `centerLon` (string)
- `radiusInKm` (string)
- `speciality` (string)
- `facilityOwnership` (string)
- `abdmSoftware` (string)
- `hospitalSpecialityType` (string)
- `facilityName` (string)
- `facilityStatus` (string)
- `som` (string)
- `gender` (string)
- `doctorName` (string)
- `doctorSystemOfMedicine` (string)
- `languages` (string)
- `isIcuBedsAvailable` (string)
- `size` (string)
- `from` (string)

## Responses

- `200`: OK
- `404`: Not Found
