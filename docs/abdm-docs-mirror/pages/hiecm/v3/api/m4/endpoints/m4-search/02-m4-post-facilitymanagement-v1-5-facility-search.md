# Search facility

`POST /FacilityManagement/v1.5/facility/search`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/FacilityManagement/v1.5/facility/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "ownershipCode": "P",
  "subDistrictLGDCode": "",
  "pincode": "",
  "facilityName": "hospital",
  "facilityId": "",
  "page": 1,
  "resultsPerPage": 10,
  "stateLGDCode": "27",
  "districtLGDCode": ""
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `ownershipCode` (string)
- `subDistrictLGDCode` (string)
- `pincode` (string)
- `facilityName` (string)
- `facilityId` (string)
- `page` (integer)
- `resultsPerPage` (integer)
- `stateLGDCode` (string)
- `districtLGDCode` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "facilities": [
    {
      "ownership": "GOVERNMENT",
      "systemOfMedicineCode": "P,M",
      "systemOfMedicine": "Physiotherapy,Modern Medicine(Allopathy)",
      "facilityType": "Hospital",
      "stateName": "Bihar",
      "stateLGDCode": "10",
      "districtName": "<ADDRESS>",
      "districtLGDCode": "212",
      "subDistrictName": "<ADDRESS>",
      "subDistrictLGDCode": "1400",
      "villageCityTownName": null,
      "villageCityTownLGDCode": null,
      "address": "<ADDRESS>",
      "pincode": "<PINCODE>",
      "latitude": "25.635802000000098",
      "longitude": "85.10391099999993",
      "facilityId": "",
      "facilityName": "Asian City Hospital",
      "facilityStatus": "Submitted",
      "ownershipCode": "G",
      "facilityTypeCode": "H"
    }
  ],
  "message": "Request processed successfully",
  "totalFacilities": 1,
  "numberOfPages": 1
}
```
