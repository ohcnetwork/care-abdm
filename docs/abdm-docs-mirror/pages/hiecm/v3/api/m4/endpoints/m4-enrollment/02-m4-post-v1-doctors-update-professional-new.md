# Update professional

`POST /apis/v1/doctors/update-professional-new`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/update-professional-new \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprToken": "<JWT TOKEN>",
  "practitioner": {
    "healthProfessionalType": "doctor",
    "profilePhoto": "<BASE64 ENCODED STRING>",
    "officialMobileCode": "",
    "officialMobile": "97624xxxxx",
    "officialMobileStatus": "",
    "officialEmail": "",
    "officialEmailStatus": "",
    "visibleProfilePicture": "0",
    "profileVisibleToPublic": "1",
    "personalInformation": {
      "salutation": "1",
      "firstName": "Ayushman",
      "middleName": "",
      "lastName": "Mission",
      "nationality": "356",
      "fatherName": "",
      "motherName": "",
      "spouseName": "",
      "gender": "M",
      "dateOfBirth": "<DOB>",
      "placeOfBirthState": "68",
      "district": "",
      "subDistrict": "",
      "city": "",
      "languagesSpoken": "1,2",
      "category": "C"
    },
    "addressAsPerKYC": "",
    "communicationAddress": {
      "isCommunicationAddressAsPerKYC": "false",
      "address": "",
      "name": "",
      "country": "",
      "state": "",
      "district": "",
      "subDistrict": "",
      "city": "",
      "pincode": ""
    },
    "contactInformation": {
      "publicMobileNumber": "",
      "publicMobileNumberCode": "",
      "publicMobileNumberStatus": "",
      "landLineNumber": "",
      "landLineNumberCode": "",
      "publicEmail": "",
      "publicEmailStatus": ""
    },
    "registrationAcademic": {
      "category": "1",
      "registrationData": [
        {
          "registeredWithCouncil": "47",
          "registrationNumber": "REG12032",
          "registrationDate": "2024-12-01",
          "registrationCertificate": {
            "fileType": "pdf",
            "data": "<BASE64 ENCODED STRING>"
          },
          "isPermanentOrRenewable": "Permanent",
          "renewableDueDate": "",
          "categoryId": "2",
          "isNameDifferentInCertificate": "false",
          "proofOfNameChangeCertificate": "",
          "qualifications": [
            {
              "nameOfDegreeOrDiplomaObtained": "4074",
              "country": "356",
              "state": "27",
              "college": "1022",
              "university": "6372",
              "yearOfAwardingDegreeDiploma": "2024",
              "monthOfAwardingDegreeDiploma": "February",
              "degreeCertificate": {
                "fileType": "pdf",
                "data": "<BASE64 ENCODED STRING>"
              },
              "isNameDifferentInCertificate": "false",
              "proofOfNameChangeCertificate": ""
            },
            {
              "nameOfDegreeOrDiplomaObtained": "Graduation",
              "country": "United States Of America",
              "state": "united",
              "college": "united School",
              "university": "united University",
              "yearOfAwardingDegreeDiploma": "2024",
              "monthOfAwardingDegreeDiploma": "February",
              "degreeCertificate": {
                "fileType": "pdf",
                "data": "<BASE64 ENCODED STRING>"
              },
              "isNameDifferentInCertificate": "true",
              "proofOfNameChangeCertificate": "<BASE64 ENCODED STRING>"
            }
          ]
        }
      ]
    },
    "currentWorkDetails": {
      "currentlyWorking": "0",
      "purposeOfWork": "Administrative",
      "chooseWorkStatus": "1",
      "reasonForNotWorking": "Retired",
      "certificateAttachment": "<BASE64 ENCODED STRING>",
      "facilityDeclarationData": {
        "facilityId": "IN2710000059",
        "facilityName": "",
        "facilityAddress": "",
        "facilityPincode": "",
        "state": "",
        "district": "",
        "facilityType": "",
        "facilityDepartment": "Surgery",
        "facilityDesignation": "MD",
        "ministry": {
          "ministry": "MinistryMOR ( Mo Railways )"
        }
      }
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `practitioner` (object)
- `practitioner.personalInformation` (object)
- `practitioner.communicationAddress` (object)
- `practitioner.contactInformation` (object)
- `practitioner.registrationAcademic` (object)
- `practitioner.specialities` (object[])
- `practitioner.currentWorkDetails` (object)
- `practitioner.apiClientId` (string)
- `practitioner.profilePhoto` (string)
- `practitioner.healthProfessionalType` (string)
- `practitioner.officialMobileCode` (string)
- `practitioner.officialMobile` (string)
- `practitioner.officialMobileStatus` (string)
- `practitioner.officialEmail` (string)
- `practitioner.officialEmailStatus` (string)
- `practitioner.visibleProfilePicture` (string)
- `practitioner.profileVisibleToPublic` (string)
- `practitioner.addressAsPerKYC` (string)
- `hprToken` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "referenceNumber": "5b17ca73-f069-4018-91a0-665df0117d43",
  "status": "true",
  "message": "Congratulations! Your profile has been submitted successfully for verification.",
  "error": null,
  "hprId": "<HPR_ID>"
}
```
