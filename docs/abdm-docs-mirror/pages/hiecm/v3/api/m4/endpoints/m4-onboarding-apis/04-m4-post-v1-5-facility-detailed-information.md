# Submit the v15Facility detailed information

`POST /v1.5/facility/detailed-information`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/detailed-information \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "trackingId": "80266",
  "specialities": [
    {
      "systemOfMedicineCode": "M",
      "isSpecializationAvalaible": "Y",
      "specialities": [
        "S29",
        "S30",
        "S31"
      ]
    },
    {
      "systemOfMedicineCode": "D",
      "isSpecializationAvalaible": "Y",
      "specialities": [
        "S50",
        "S51",
        "S46"
      ]
    },
    {
      "systemOfMedicineCode": "UN",
      "isSpecializationAvalaible": "Y",
      "specialities": [
        "S68",
        "S168",
        "S100"
      ]
    }
  ],
  "medicalInfrastructure": {
    "countIPDBedsWithoutOxygen": 2,
    "countIPDBedsWithOxygen": 3,
    "countICUBedsWithVentilators": 4,
    "countICUBedsWithoutVentilators": 1,
    "countHDUBedsWithVentilators": 5,
    "countHDUBedsWithoutVentilators": 6,
    "totalNumberOfVentilators": 7,
    "countDayCareBedsWithoutOxygen": 8,
    "countDayCareBedsWithOxygen": 9,
    "countDentalChairs": 1,
    "totalNumberOfBeds": 4
  },
  "pharmacyDetails": {
    "isJanAushadhiKendra": "Y",
    "janAushadhiKendraId": "jan-id",
    "drugLicenseNumber": "test1234",
    "pharmacyGstinNumber": "testg1234",
    "pharmacistRegistrationNumber": "reg1234"
  },
  "bloodBankDetails": {
    "isFacilityRegisteredInERaktkosh": "N",
    "eRaktoshId": "Y",
    "bloodBankLicenseNumber": "345-test-regno",
    "bloodStorageCenters": "Y",
    "storageCentersCount": 7,
    "bloodCollectedPerAnnum": "5",
    "bloodRequiredPerAnnum": "6"
  },
  "imagingServices": [
    {
      "service": "S136",
      "count": 77
    },
    {
      "service": "S139",
      "count": 99
    },
    {
      "service": "S138",
      "count": 76
    }
  ],
  "diagnosticServices": [
    ""
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `trackingId` (string)
- `specialities` (object[])
- `specialities.systemOfMedicineCode` (string)
- `specialities.isSpecializationAvalaible` (string)
- `specialities.specialities` (string[])
- `medicalInfrastructure` (object)
- `medicalInfrastructure.countLevel1IcuBedWithOutVentilators` (integer)
- `medicalInfrastructure.countIPDBedsWithoutOxygen` (integer)
- `medicalInfrastructure.countIPDBedsWithOxygen` (integer)
- `medicalInfrastructure.countICUBedsWithVentilators` (integer)
- `medicalInfrastructure.countICUBedsWithoutVentilators` (integer)
- `medicalInfrastructure.countHDUBedsWithVentilators` (integer)
- `medicalInfrastructure.countHDUBedsWithoutVentilators` (integer)
- `medicalInfrastructure.totalNumberOfVentilators` (integer)
- `medicalInfrastructure.countDayCareBedsWithoutOxygen` (integer)
- `medicalInfrastructure.countDayCareBedsWithOxygen` (integer)
- `medicalInfrastructure.countDentalChairs` (integer)
- `medicalInfrastructure.totalNumberOfBeds` (integer)
- `medicalInfrastructure.hasIcuBeds` (string)
- `medicalInfrastructure.countLevel1IcuBedWithVentilators` (integer)
- `medicalInfrastructure.CountLevel1IcuBedWithOutVentilators` (integer)
- `medicalInfrastructure.countLevel2IcuBeds` (integer)
- `medicalInfrastructure.countLevel3IcuBeds` (integer)
- `medicalInfrastructure.isIcuContactSameAsManager` (string)
- `medicalInfrastructure.cmoMoIcuControlMobile` (string)
- `pharmacyDetails` (object)
- `pharmacyDetails.isJanAushadhiKendra` (string)
- `pharmacyDetails.janAushadhiKendraId` (string)
- `pharmacyDetails.drugLicenseNumber` (string)
- `pharmacyDetails.pharmacyGstinNumber` (string)
- `pharmacyDetails.pharmacistRegistrationNumber` (string)
- `bloodBankDetails` (object)
- `bloodBankDetails.isFacilityRegisteredInERaktkosh` (string)
- `bloodBankDetails.eRaktoshId` (string)
- `bloodBankDetails.bloodBankLicenseNumber` (string)
- `bloodBankDetails.bloodStorageCenters` (string)
- `bloodBankDetails.storageCentersCount` (integer)
- `bloodBankDetails.bloodCollectedPerAnnum` (string)
- `bloodBankDetails.bloodRequiredPerAnnum` (string)
- `imagingServices` (object[])
- `imagingServices.service` (string)
- `imagingServices.count` (integer)
- `diagnosticServices` (string[])

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "trackingId": "76803",
  "status": "Saved",
  "message": "Facility details have been saved successfully. Please login at \" + hfrUrl\n\" and submit your facility details for approval.",
  "errorStatus": null
}
```
