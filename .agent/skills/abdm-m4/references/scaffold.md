# HIE-CM m4 build

Scaffolds an ABDM m4 integration one journey at a time. It covers creating an HPID, registering a professional on the HPR, and onboarding a facility to the HFR.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

## Journeys

### Registration API's Collection Via Aadhaar (`m4-registration-api-s-collection-via-aadhaar`)

**Act: the calls in this journey, in order**

#### 1. Generate Aadhaar link (`m4_post_aadhaar_generatelink`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/aadhaar/generateLink \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scopes": [
    "nhpr-register"
  ],
  "source": "NHPR"
}'
```

#### 2. Submit the is Aadhaar authenticated (`m4_post_aadhaar_isauthenticated`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/aadhaar/isAuthenticated \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "259813b1-a339-4482-8df5-16ee45b8dcf2"
}'
```

#### 3. Verify OTP (`m4_post_v2_registration_aadhaar_verifyotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v2/registration/aadhaar/verifyOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4"
}'
```

#### 4. Submit the demographic auth via mobile (`m4_post_v2_registration_aadhaar_demographicauthviamobile`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v2/registration/aadhaar/demographicAuthViaMobile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4",
  "mobileNumber": "JrHfDROoEcsYJ41g2wdkicsI7mT1ATCP347iqwBhWbfaEIgZ03/WHAYvDHRG2WXl4HBNuP2orD+3O75pN0xFhOz4oLXrePAxKTLK8uG5jdeAiGE2lKwOrShq9/gg+BckrQcDYjpMUePRuDau4mqLHa8FdSCQ8npGPY9KCpD2hZkscWNqZR68gRo/EwpY4u32kDzv5i1K/s+A7FNVwXqZS5AK2BadEhG5drSRk7P83eFxJZUlwtsvDK6iipOsM4VtMXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}'
```

#### 5. Submit the account exist (`m4_post_v1_registration_aadhaar_checkhpidaccountexist`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/registration/aadhaar/checkHpIdAccountExist \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4"
}'
```

#### 6. Get suggesstion (`m4_post_v1_registration_aadhaar_hpid_suggestion`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/registration/aadhaar/hpid/suggestion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "a825f76b-0696-40f3-864c-5a3a5b389a83"
}'
```

#### 7. Generate mobile OTP (`m4_post_v1_registration_aadhaar_generatemobileotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/registration/aadhaar/generateMobileOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "mobile": "981065XXXX",
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4"
}'
```

#### 8. Verify mobile OTP (`m4_post_v1_registration_aadhaar_verifymobileotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/registration/aadhaar/verifyMobileOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "otp": "<BASE64 ENCODED STRING>",
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4"
}'
```

#### 9. Create HPR ID V2 (`m4_post_v2_registration_aadhaar_createhpridwithpreverified`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v2/registration/aadhaar/createHprIdWithPreVerified \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "idType": "hpr_id",
  "domainName": "@hpr.abdm",
  "email": "<ABHA_ADDRESS>.com",
  "firstName": "Ayushman",
  "middleName": "Bharat",
  "lastName": "Mission",
  "password": "Ayushman@143",
  "profilePhoto": "<BASE64 ENCODED STRING>",
  "txnId": "c3b0c27d-e19d-4244-b8bb-3fa19285054a",
  "hprId": "<EMAIL>",
  "sourceType": "DRIVING_LICENSE",
  "hpCategoryCode": 1,
  "hpSubCategoryCode": 1,
  "clientId": "V4",
  "stateCode": "<STATE_CODE>",
  "districtCode": "<DISTRICT_CODE>",
  "council": false,
  "role": 0
}'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Onboarding APIs (`m4-onboarding-apis`)

**Act: the calls in this journey, in order**

#### 1. Get filtered address post (`m4_post_search_address_filter_deduplicate`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/search/address/filter/deduplicate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "Jethana",
  "address": "<ADDRESS>",
  "district": "511",
  "subDistrict": "5271",
  "village": "",
  "geolocation": "",
  "facilityId": "69765"
}'
```

#### 2. Submit the v15Basic facility information (`m4_post_v1_5_facility_basic_information`)

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

#### 3. Submit the v15Facility additional information (`m4_post_v1_5_facility_additional_information`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/additional-information \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "trackingId": "80266",
  "linkedProgramIds": {
    "nhrrId": "1234",
    "nin": "1234",
    "abpmjayId": "1234",
    "rohiniId": "1234",
    "echsId": "1234",
    "cghsId": "1234",
    "ceaRegistration": "1234",
    "stateInsuranceSchemeId": "1234"
  },
  "generalInformation": {
    "hasDialysisCenter": "YALL",
    "hasPharmacy": "YALL",
    "hasBloodBank": "YALL",
    "hasCathLab": "YALL",
    "hasDiagnosticLab": "YALL",
    "hasImagingCenter": "YALL",
    "servicesByImagingCenter": [
      {
        "service": "S36",
        "count": 7
      },
      {
        "service": "S16",
        "count": 5
      },
      {
        "service": "S23",
        "count": 3
      }
    ]
  }
}'
```

#### 4. Submit the v15Facility detailed information (`m4_post_v1_5_facility_detailed_information`)

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

#### 5. Submit the v15Submit facility details (`m4_post_v1_5_facility_submit_facility`)

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

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Multiple HRP API (`m4-multiple-hrp-api`)

**Act: the calls in this journey, in order**

#### 1. Submit the facility add and update (`m4_post_v1_bridges_mutiplehrpaddupdateservices`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/bridges/MutipleHRPAddUpdateServices \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "IN0610090166",
  "facilityName": "Singla Eye Center",
  "HRP": [
    {
      "bridgeId": "SBX_00XXXX",
      "hipName": "Singla Eye Center",
      "type": "HIP",
      "active": true
    }
  ]
}'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Utilities (`m4-utilities`)

**Act: the calls in this journey, in order**

#### 1. Get PSU details by ministry (`m4_get_getpsudetailsbyministry`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/getPsuDetailsByMinistry \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 2. Get all facility sub type by facility type (`m4_post_v1_5_facility_fetch_facility_sub_type`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/fetch-facility-Sub-type \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityTypeCode": "2"
}'
```

#### 3. Get all facility type by ownership and sys of med (`m4_post_v1_5_facility_fetch_facility_type`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/fetch-facility-type \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "ownershipCode": "G",
  "systemOfMedicineCode": "M"
}'
```

#### 4. Get master data (`m4_get_v1_5_facility_get_master_data`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-master-data \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 5. Get all master types (`m4_get_v1_5_facility_get_master_types`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-master-types \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 6. Get all sub types by owner ship type and sub type (`m4_post_v1_5_facility_get_owner_subtype`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-owner-subtype \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "ownershipCode": "P",
  "ownerSubtypeCode": "NP"
}'
```

#### 7. Get all specialities by system of medicine code (`m4_post_v1_5_facility_get_specialities`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-specialities \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "systemOfMedicineCode": "D"
}'
```

#### 8. Get all district by state ID (`m4_get_v1_5_facility_lgd_districts`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/lgd/districts \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 9. Get all states by LGD (`m4_get_v1_5_facility_lgd_states`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/lgd/states \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 10. Get all sub district by district code (`m4_get_v1_5_facility_lgd_subdistricts`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/lgd/subdistricts \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
[
  {
    "code": "6752",
    "name": "Assar"
  },
  {
    "code": "65",
    "name": "Bhaderwah"
  },
  {
    "code": "6747",
    "name": "Bhagwah"
  }
]
```

### Search (`m4-search`)

**Act: the calls in this journey, in order**

#### 1. Get facility and infrastructure within radius with filter (`m4_post_facilitymanagement_v1_5_facility_bygeolocation_se_907b10`)

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

#### 2. Search facility (`m4_post_facilitymanagement_v1_5_facility_search`)

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

**Exit condition (Observe until this is true)**

A 200 whose body matches:

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

### HFR-HRP Linkage APIs (`m4-hfr-hrp-linkage-apis`)

**Act: the calls in this journey, in order**

#### 1. Send OTP to contact (`m4_post_v1_5_facility_sendotptocontact`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/sendOtpToContact \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "IN2810002702"
}'
```

#### 2. Validate OTP (`m4_post_v1_5_facility_validateotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/validateOtp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "IN2810002702",
  "sourceId": "AB-PMJAY",
  "otp": "885210",
  "source": "AB-PMJAY",
  "transactionId": "2ddfc7ec-9a9f-412c-8c50-c2be92da5781"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "facilityId": "IN2810002702",
  "status": "success",
  "message": "OTP validated successfully!!! Hospital id linked to HFR",
  "errorStatus": null
}
```

### Authentication (`m4-authentication`)

**Act: the calls in this journey, in order**

#### 1. Login via password (`m4_post_v1_auth_authpassword`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/api/v1/auth/authPassword \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "idType": "",
  "domainName": "",
  "hprId": "<HPR_ID>",
  "password": "XXXX@992"
}'
```

#### 2. Get public certificate (`m4_get_v1_auth_cert`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/api/v1/auth/cert \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 3. Verify Aadhaar OTP 1 (`m4_post_v1_auth_confirmwithaadhaarotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/api/v1/auth/confirmWithAadhaarOtp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "otp": "308709",
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4"
}'
```

#### 4. Send via Aadhaar OTP (`m4_post_v1_auth_init`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/api/v1/auth/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "idType": "",
  "domainName": "",
  "authMethod": "AADHAAR_OTP",
  "hprId": "<HPR_ID>"
}'
```

#### 5. Send verify OTP (`m4_post_v2_auth_loginviamobilesendotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/api/v2/auth/loginViaMobileSendOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "4c8c4b29-6d7e-4446-8f73-4574d6d14f09",
  "mobile": "97624XXXXX"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "28b4ce41-71df-48af-8b6c-13c30402816c",
  "mobileNumber": "******1234"
}
```

### Verification (`m4-verification`)

**Act: the calls in this journey, in order**

#### 1. Generate mobile OTP 2 (`m4_post_v1_doctors_generate_mobile_otp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/generate-mobile-otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "officialMobile": "<BASE64 ENCODED STRING>"
}'
```

#### 2. Send verification email (`m4_post_v1_doctors_generate_verification_email`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/generate-verification-email \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "emailAddress": "<ABHA_ADDRESS>.com",
  "otp_type": ""
}'
```

#### 3. Submit the regenerate mobile OTP (`m4_post_v1_doctors_regenerate_mobile_otp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/regenerate-mobile-otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "officialMobile": "PFiI0AQJkAKIdLL6ytdJLKFObqXab9rwTvOEPHflksQBkMzIIb8HMDYUzZfN3AUdefedSbb+B4sPwi72lsaaNRkpXygWRF0GWntEwD/WL80JbXaW9DJkwPpDEzQpMYKKT17iCTp7pQer8337NZofO1D1aYiDfEnA9E1HMTyPCGFjvmbcL32hNqGsgpHKYNh4rHXCo4RwP5UQKWDYI1jLZqbWLp0a9GQu9nC1hyP5IR5LRCASzvhiRfrRk+Y660xuDSCvOKb+uUPcN3ZFA==xxxxxxxx"
}'
```

#### 4. Resend verification email (`m4_post_v1_doctors_resent_verify_email`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/resent-verify-email \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "emailAddress": "<ABHA_ADDRESS>.com",
  "otp_type": ""
}'
```

#### 5. Verify email OTP (`m4_post_v1_doctors_verify_email_otp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/verify-email-otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "hpr_id": "<HPR_ID>",
  "officialEmail": "<ABHA_ADDRESS>.com",
  "emailOtp": 515999
}'
```

#### 6. Verify mobile OTP (`m4_post_v1_doctors_verify_mobile_otp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/verify-mobile-otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "txnId": "dd392164-0f4a-4894-8d64-1fce027ee033",
  "otp": "<BASE64 ENCODED STRING>"
}'
```

#### 7. Send OTP if doctor verified (`m4_post_v1_sendotpifdoctorverified`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/sendOtpIfDoctorVerified \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>",
  "mobileNumber": "<MOBILE_NUMBER>"
}'
```

#### 8. Verify doctor verification OTP (`m4_post_v1_verifydoctorverificationotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/verifyDoctorVerificationOtp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "otp": "<OTP>"
}'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Hpid (`m4-hpid`)

**Act: the calls in this journey, in order**

#### 1. Get admin token (`m4_post_getmanagementtoken`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/getManagementToken \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "username": "<USERNAME>",
  "password": "<PASSWORD>",
  "resend": false
}'
```

#### 2. Submit the healdthloginwithmobile (`m4_post_healdthloginwithmobile`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/healdthloginwithmobile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "issueToken": "<ISSUE_TOKEN>",
  "token": "<TOKEN>"
}'
```

#### 3. Update role and category (`m4_post_profile_updaterole`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/profile/updateRole \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "firstName": "Ayushman",
  "lastName": "Mission",
  "middleName": "Bharat",
  "hprId": "<EMAIL>",
  "password": "Abdm@143",
  "email": "<ABHA_ADDRESS>.com",
  "profilePhoto": "<BASE64 ENCODED STRING>",
  "stateCode": "7",
  "districtCode": "71",
  "subdistrictCode": "1",
  "villageCode": "<VILLAGE_CODE>",
  "townCode": "<TOWN_CODE>",
  "wardCode": "<WARD_CODE>",
  "pincode": 110001,
  "address": "9th Floor, Tower-l, Jeevan Bharati Building, Connaught Place, New Delhi - 110001",
  "yearOfBirth": "2021",
  "monthOfBirth": "8",
  "dayOfBirth": "15",
  "hpCategoryCode": "1",
  "hpSubCategoryCode": "1",
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11",
  "role": "<ROLE>",
  "consentToDelete": false
}'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Util (`m4-util`)

**Act: the calls in this journey, in order**

#### 1. Fetch HPID categories (`m4_get_hpid_get_categories`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/hpid/get/categories \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 2. Fetch HPID sub categories from category (`m4_get_hpid_get_subcategories`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/hpid/get/subCategories \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
[
  {
    "code": "220",
    "name": "Yoga and Naturopathy"
  },
  {
    "code": "1",
    "name": "Modern Medicine"
  },
  {
    "code": "2",
    "name": "Dentist"
  }
]
```

### Profile (`m4-profile`)

**Act: the calls in this journey, in order**

#### 1. Change password (`m4_post_password_change_bypassword`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/change/byPassword \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "newPassword": "<BASE64 ENCODED STRING>",
  "oldPassword": "<BASE64 ENCODED STRING>"
}'
```

#### 2. Recover password via Aadhaar (`m4_post_password_recover_byaadhaar`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/recover/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>"
}'
```

#### 3. Generate mobile OTP 1 (`m4_post_password_recover_bymobile_sendmobileotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/recover/byMobile/sendMobileOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "amol.xxxxxx"
}'
```

#### 4. Verify mobile OTP 1 (`m4_post_password_recover_bymobile_verifymobileotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/recover/byMobile/verifyMobileOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "7ebad8aa-127b-492f-bd0e-56da716bd39e",
  "otp": "<BASE64 ENCODED STRING>"
}'
```

#### 5. Recover password confirm by Aadhaar (`m4_post_password_recover_confirmbyaadhaar`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/recover/confirmByAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "otp": "<BASE64 ENCODED STRING>",
  "txnId": "9b78fdfb-3ba4-4707-8913-63c7c5e3a743"
}'
```

#### 6. Reset password and session (`m4_post_password_reset_password`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/reset/password \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "newPassword": "<NEW_PASSWORD>",
  "otp": "<OTP>",
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11"
}'
```

#### 7. Reset password (`m4_post_password_resetpassword`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/resetPassword \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "9b78fdfb-3ba4-4707-8913-63c7c5e3a743",
  "newPassword": "<BASE64 ENCODED STRING>"
}'
```

#### 8. Get account png card (`m4_get_v1_account_getidcard`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/getIdCard \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-Token: <X_TOKEN>'
```

#### 9. Get user profile by JWT (`m4_get_v1_account_information`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/information \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 10. Generate Aadhaar OTPFor re KYC (`m4_post_v1_account_rekyc_generateaadhaarotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/reKYC/generateAadhaarOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 11. Verify Aadhaar OTP (`m4_post_v1_account_rekyc_verifyaadhaarotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/reKYC/verifyAadhaarOTP \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "authType": "AADHAAR_OTP",
  "hprId": "<HPR_ID>",
  "password": "<PASSWORD>",
  "aadhaar": "<AADHAAR>",
  "mobileNumber": "<MOBILE_NUMBER>",
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11",
  "otp": "<OTP>",
  "resend": false,
  "aadhaarVerifyOtpRequestDto": {
    "aadhaarNumber": "<AADHAAR_NUMBER>",
    "otp": "<OTP>",
    "faceAuthPid": "<FACE_AUTH_PID>",
    "aadhaarLogType": "<AADHAAR_LOG_TYPE>",
    "transactionId": "<TRANSACTION_ID>",
    "txnId": "<TXN_ID>"
  }
}'
```

#### 12. Verify Aadhaar OTPGet details (`m4_post_v1_account_rekyc_verifyaadhaarotpgetdetails`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/reKYC/verifyAadhaarOTPGetDetails \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "authType": "AADHAAR_OTP",
  "hprId": "<HPR_ID>",
  "password": "<PASSWORD>",
  "aadhaar": "<AADHAAR>",
  "mobileNumber": "<MOBILE_NUMBER>",
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11",
  "otp": "<OTP>",
  "resend": false,
  "aadhaarVerifyOtpRequestDto": {
    "aadhaarNumber": "<AADHAAR_NUMBER>",
    "otp": "<OTP>",
    "faceAuthPid": "<FACE_AUTH_PID>",
    "aadhaarLogType": "<AADHAAR_LOG_TYPE>",
    "transactionId": "<TRANSACTION_ID>",
    "txnId": "<TXN_ID>"
  }
}'
```

#### 13. Get user details (`m4_get_v1_account_user_details_hprid`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/account/user-details/{hprId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 14. Logout (`m4_get_v4_auth_logout`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v4/auth/logout \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Forgot Healthcare Professional ID/number (`m4-forgot-healthcare-professional-id-number`)

**Act: the calls in this journey, in order**

#### 1. Submit the retrieval health ID by Aadhaar (`m4_post_v1_forgot_hprid_aadhaar`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/forgot/hprId/aadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "otp": "<BASE64 ENCODED STRING>",
  "txnId": "4c115e27-a602-4320-b4cd-ee658539e2f0"
}'
```

#### 2. Submit the retrieval health ID by mobile (`m4_post_v1_forgot_hprid_mobile`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/forgot/hprId/mobile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11",
  "name": "<NAME>",
  "gender": "<GENDER>",
  "yearOfBirth": "<YEAR_OF_BIRTH>",
  "monthOfBirth": "<MONTH_OF_BIRTH>",
  "dayOfBirth": "<DAY_OF_BIRTH>",
  "firstName": "<FIRST_NAME>",
  "lastName": "<LAST_NAME>",
  "middleName": "<MIDDLE_NAME>",
  "otp": "<OTP>"
}'
```

#### 3. Generate mobile OTP (`m4_post_v1_forgot_hprid_mobile_generateotp`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/forgot/hprId/mobile/generateOtp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "mobileNumber": "VPoaDCJBNyGhJiX+sAh9yRq1WXAfRXkgcE31/0U2DMkH/+nvpspAA4GEmkbideZhKsSLYnFA1lHPkBH7PS6Bg4jz0aSdDAoovnYgVftJ/suP4mzhhg1Hrf7zQFPriHiraNlsIzsDeLl3ckGejNiCmXhfhBBw==xxxxxxxxxxxxx"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "132dd7dd-ca5a-4ec1-a36c-093c007bf794",
  "msg": "Please enter OTP sent on your mobile number ******2021",
  "mobileNumber": "******2021"
}
```

### Searched (`m4-searched`)

**Act: the calls in this journey, in order**

#### 1. Get the exists by HPR ID (`m4_get_v1_search_existsbyhprid_hprid`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/search/existsByHprId/{hprId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 2. Search user by HPR ID (`m4_get_v1_search_searchbyhprid_hprid`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/search/searchByHprId/{hprId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 3. Search user by mobile no (`m4_get_v1_search_searchbymobile_mobile`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/search/searchByMobile/{mobile} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
[
  {
    "hprIdNumber": "<HPR_ID>",
    "name": "Ayushman Bharat Mission",
    "authMethods": [
      "PASSWORD",
      "MOBILE_OTP",
      "AADHAAR_OTP"
    ],
    "hprId": "<EMAIL>",
    "categoryId": "1",
    "subCategoryId": "1"
  }
]
```

### Enrollment (`m4-enrollment`)

**Act: the calls in this journey, in order**

#### 1. Register professional (`m4_post_v1_doctors_register_professional_new`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/register-professional-new \
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

#### 2. Update professional (`m4_post_v1_doctors_update_professional_new`)

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

#### 3. Fetch documents (`m4_post_v1_doctors_fetch_documents_list`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/fetch-documents-list \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprid": "<HPR_ID>"
}'
```

#### 4. Upload documents (`m4_post_v1_uploads_upload_document`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/uploads/upload-document \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "document": [
    {
      "document_id": 20931,
      "document_type": "registrationCertificate",
      "fileType": "",
      "data": "JVBERi0xLjMK"
    }
  ]
}'
```

#### 5. Get professional info (`m4_post_v1_doctors_fetch_professional_info`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/fetch-professional-info \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "practitioner": {
    "id": "<HPR_ID>",
    "name": "",
    "contactNumber": "976243XXXX",
    "state": "UTTAR PRADESH",
    "registrationNumber": ""
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "practitioners": [
    [
      {
        "identifier": 38053,
        "active": false,
        "name": "Ayushman Bharat Mission",
        "gender": "Male",
        "salutation": "Mr",
        "communicationLanguage": " English ",
        "registrations": [
          {
            "identifier": 25989,
            "category": "Dentistry",
            "nuidnumber": null,
            "nuidvalidtill": null,
            "systemOfMedicide": null,
            "isRenewable": "false",
            "dueDate": null,
            "councilName": "Karnataka State Dental Council",
            "registeredAt": null,
            "registrationNumber": "REG12032",
            "registrationDate": "2024-12-01"
          }
        ],
        "qualifications": [
          {
            "identifier": 12835,
            "courseName": "Bds - Bachelor Of Dental Surgery",
            "collegeName": "A.j. Institute Of Dental Sciences, Mangalore",
            "universityName": "Rajiv Gandhi University Of Health Sciences (rguhs)",
            "qualificationYear": "2024",
            "qualificationMonth": ""
          }
        ],
        "hpr_id": "<HPR_ID>",
        "application_status": null,
        "is_council_verified": "true",
        "is_work_verified": null,
        "email": "",
        "mobileNumber": "******2125",
        "hpr_category": "doctor"
      }
    ]
  ],
  "message": "Data fetched successfully"
}
```

### Utility (`m4-utility`)

**Act: the calls in this journey, in order**

#### 1. Get all affiliated board (`m4_get_v1_masters_affiliated_board`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/affiliated-board \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 2. Get affiliated board by state ID (`m4_get_v1_masters_affiliated_board_states_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/affiliated-board/states/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 3. Get affiliated board by ID (`m4_get_v1_masters_affiliated_board_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/affiliated-board/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 4. Get college by state (`m4_get_v1_masters_colleges_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/colleges/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 5. Get college by state and medicine ID (`m4_get_v1_masters_colleges_stateid_medicineid`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/colleges/{stateId}/{medicineId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 6. Get all countries (`m4_get_v1_masters_countries`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/countries \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 7. Get countries by ID (`m4_get_v1_masters_countries_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/countries/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 8. List courses (`m4_post_v1_masters_courses`)

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

#### 9. Get all districts (`m4_get_v1_masters_district`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/district \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 10. Get districts by state (`m4_get_v1_masters_district_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/district/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 11. List government health programmes (`m4_get_v1_masters_languages`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/languages \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 12. Get pi languages by ID (`m4_get_v1_masters_languages_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/languages/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 13. Get all medical council (`m4_get_v1_masters_medical_councils`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/medical-councils \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 14. Get medical council by system of medicine name (`m4_get_v1_masters_medical_councils_name`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/medical-councils/name \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 15. Get all nurse councils (`m4_get_v1_masters_nurse_councils`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/nurse-councils \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 16. Get all states (`m4_get_v1_masters_states`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/states \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 17. Get status (`m4_get_v1_masters_states_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/states/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 18. Get all sub districts (`m4_get_v1_masters_sub_districts`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/sub-districts \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 19. Get all sub districts 1 (`m4_get_v1_masters_sub_districts_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/sub-districts/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 20. Get all medical system (`m4_get_v1_masters_system_of_medicines`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/system-of-medicines \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 21. List all university (`m4_get_v1_masters_universites`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/universites \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 22. Get university by college (`m4_get_v1_masters_universites_id`)

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/masters/universites/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

#### 23. Get facilities created by HPR ID (`m4_post_getfacilitycreatedbyhprid`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/getFacilityCreatedByHprId \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>",
  "source": "<SOURCE>"
}'
```

#### 24. Get facilities declared by HPR ID (`m4_post_getfacilitydeclaredbyhprid`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/getFacilityDeclaredByHprId \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>",
  "source": "<SOURCE>"
}'
```

#### 25. Update status (`m4_put_hprworkdetails_status`)

```bash
curl --request PUT \
  --url https://apihspsbx.abdm.gov.in/v4/int/hprWorkDetails/status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "status": "<STATUS>",
  "facilityId": "<FACILITY_ID>",
  "professionalHprId": "<PROFESSIONAL_HPR_ID>",
  "managerHprId": "<MANAGER_HPR_ID>",
  "isHpr": false
}'
```

#### 26. Link delink existing facility (`m4_post_relinkordelinkprofessionalfromfacility`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/relinkOrDelinkProfessionalFromFacility \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>",
  "facilityId": "<FACILITY_ID>",
  "action": "<ACTION>"
}'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Hpr (`m4-hpr`)

**Act: the calls in this journey, in order**

#### 1. Fetch professional facility (`m4_post_fetchprofessionalfacility`)

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/fetchProfessionalFacility \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "<FACILITY_ID>",
  "page": 0,
  "size": 0
}'
```

#### 2. Create facility suggestion (`m4_post_hprfacilitysuggestions`)

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

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

## Where the detail is

- Every operation, with its body fields and responses: /docs/hiecm/v3/api/m4
