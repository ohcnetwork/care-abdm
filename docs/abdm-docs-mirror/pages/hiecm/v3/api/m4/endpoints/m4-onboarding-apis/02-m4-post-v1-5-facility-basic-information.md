# Submit the v15Basic facility information

`POST /v1.5/facility/basic-information`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/basic-information \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'x-hprid-auth: <X_HPRID_AUTH>' \
  --header 'Content-Type: application/json' \
  --data '{
  "trackingId": "",
  "facilityInformation": {
    "facilityName": "Sahyadri Hospital",
    "facilityAddressDetails": {
      "country": "India",
      "stateLGDCode": "24",
      "districtLGDCode": "438",
      "subDistrictLGDCode": "6512",
      "facilityRegion": "U",
      "villageCityTownLGDCode": "",
      "addressLine1": "townhall, Pune",
      "addressLine2": "Pune",
      "pincode": "<PINCODE>",
      "latitude": "23.068570",
      "longitude": "23.068570"
    },
    "facilityContactInformation": {
      "facilityEmailId": "<ABHA_ADDRESS>.com",
      "facilityContactNumber": "976243xxxx",
      "websiteLink": "nha.abdm.gov.in",
      "facilityLandlineNumber": "",
      "facilityStdCode": ""
    },
    "ownershipCode": "G",
    "ownershipSubTypeCode": "C",
    "ownershipSubTypeCode2": "MOHF",
    "systemOfMedicineCode": "M,D,UN",
    "typeOfServiceCode": "IPD,OPD",
    "facilityTypeCode": "5",
    "specialityTypeCode": "SINGLE",
    "facilityUploads": {
      "facilityBoardPhoto": {
        "name": "",
        "value": ""
      },
      "facilityBuildingPhoto": {
        "name": "",
        "value": ""
      }
    },
    "facilitySubType": "47",
    "facilityOperationalStatus": "F",
    "timingsOfFacility": [
      {
        "workingDays": "MON",
        "openingHours": "9:00 AM - 6:00 PM"
      },
      {
        "workingDays": "TUE",
        "openingHours": "9:00 AM - 4:00 PM"
      },
      {
        "workingDays": "WED",
        "openingHours": "9:00 AM - 6:00 PM"
      }
    ],
    "abdmCompliantSoftware": [
      {
        "existingSoftwares": [
          ""
        ],
        "anyOther": ""
      }
    ]
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Headers

- `x-hprid-auth` (string, required)

## Body

- `facilityInformation` (object)
- `facilityInformation.facilityName` (string)
- `facilityInformation.facilityAddressDetails` (object)
- `facilityInformation.facilityContactInformation` (object)
- `facilityInformation.ownershipCode` (string)
- `facilityInformation.ownershipSubTypeCode` (string)
- `facilityInformation.ownershipSubTypeCode2` (string)
- `facilityInformation.typeOfServiceCode` (string)
- `facilityInformation.systemOfMedicineCode` (string)
- `facilityInformation.facilityTypeCode` (string)
- `facilityInformation.specialityTypeCode` (string)
- `facilityInformation.facilityUploads` (object)
- `facilityInformation.facilityAddressProof` (object[])
- `facilityInformation.facilitySubType` (string)
- `facilityInformation.workingInPsu` (boolean)
- `facilityInformation.facPsuName` (string)
- `facilityInformation.facilityOperationalStatus` (string)
- `facilityInformation.timingsOfFacility` (object[])
- `facilityInformation.abdmCompliantSoftware` (object[])
- `trackingId` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "trackingId": "76803",
  "status": "success",
  "message": "Facility is saved successfully",
  "errorStatus": null
}
```
