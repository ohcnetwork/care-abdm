# M4 operations and fields

Every Milestone 4 call for the [HPR](/docs/hiecm/v3/getting-started/glossary#hpr) and the [HFR](/docs/hiecm/v3/getting-started/glossary#hfr), with its parameters, its codes and the rules that apply to it. Two operations carry a published path and have their own pages under APIs. The rest are here.

Where do I get the paths this page does not give?

Method and path are not yet published for most calls below. Take them from the sandbox documentation, and use this page for the fields, codes and rules.

## Session token

The first call you make. Same session pattern as [M1](/docs/hiecm/v3/api/m1), issued by the [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) gateway.

|                  |                                                          |
| ---------------- | -------------------------------------------------------- |
| Method           | `POST`                                                   |
| URL              | `https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions`  |
| URL, second host | `https://live.abdm.gov.in/api/hiecm/gateway/v3/sessions` |

Both hosts are listed under [Base URLs](/docs/hiecm/v3/api/m4#base-urls).

Headers:

| Header       | Value                                              |
| ------------ | -------------------------------------------------- |
| `REQUEST-ID` | A fresh UUID for each call, for end to end tracing |
| `TIMESTAMP`  | The time the request was made, ISO 8601            |
| `X-CM-ID`    | `sbx` in sandbox, `abdm` in production             |

Request body:

```json
{  "clientId": "<CLIENT_ID_FROM_SANDBOX_SIGNUP>",  "clientSecret": "<CLIENT_SECRET_FROM_SANDBOX_SIGNUP>",  "grantType": "client_credentials"}
```

Response shape:

```json
{  "accessToken": "<JWT>",  "expiresIn": 1200,  "refreshExpiresIn": 1800,  "refreshToken": "<JWT>",  "tokenType": "bearer"}
```

Read `expiresIn` from your own response rather than hard coding a value.

Every later call carries this token. The `Authorization` header value is the word `Bearer`, one space, then the access token.

## Encryption

Three fields below are sent encrypted: the mobile number in mobile match, the [OTP](/docs/hiecm/v3/getting-started/glossary#otp) in the HPR mobile login, and the email and password in create HPID. All use the same public certificate, so fetch it once.

|                |                                                         |
| -------------- | ------------------------------------------------------- |
| Method         | `GET`                                                   |
| Sandbox URL    | `https://apihspsbx.abdm.gov.in/v4/int/api/v1/auth/cert` |
| Production URL | `https://apinhpr.abdm.gov.in/v4/int/api/v1/auth/cert`   |

The response is a PEM public key, beginning `-----BEGIN PUBLIC KEY-----`. The cipher is `RSA/ECB/PKCS1Padding`.

## HPID creation

Nine calls, in order. Method and path are not yet published for these.

| Step | Call                                | What it does                                                                                                                                        | Detail we have    |
| ---- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| 1    | Generate Aadhaar link               | Returns a `txnId` and a temporary URL for the professional to complete Aadhaar authentication on. The URL expires after 5 minutes                   | Behaviour only    |
| 2    | Check Aadhaar authentication status | Optional polling. Takes the `txnId`. Returns a bare boolean, not an object                                                                          | Behaviour only    |
| 3    | Verify OTP and fetch user details   | Takes the `txnId`. Returns demographic and address details from Aadhaar, with the mobile number masked                                              | Behaviour only    |
| 4    | Check HPID exists by Aadhaar        | Returns the [HPID](/docs/hiecm/v3/getting-started/glossary#hpid) already registered for this Aadhaar, if there is one                               | Behaviour only    |
| 5    | Mobile match                        | Checks whether the mobile number is the one on the Aadhaar record. The mobile number is encrypted. The response field is `demographicAuthViaMobile` | Behaviour only    |
| 6    | Generate mobile OTP                 | Only if `demographicAuthViaMobile` is false. Takes the mobile number and the `txnId`                                                                | Behaviour only    |
| 7    | Verify mobile OTP                   | Takes the OTP and the `txnId`                                                                                                                       | Behaviour only    |
| 8    | Username suggestions                | Takes the `txnId`. Returns suggested HPR usernames                                                                                                  | Behaviour only    |
| 9    | Create HPID                         | Takes the professional's details. Email and password are encrypted with the public certificate. Returns the HPID and an `hprToken`                  | Code tables below |

### Codes for create HPID

Category:

| Code | Name       |
| ---- | ---------- |
| 1    | Doctor     |
| 2    | Nurse      |
| 6    | Pharmacist |

Subcategory, as used by create HPID:

| Code | Name                                                | HPR type   |
| ---- | --------------------------------------------------- | ---------- |
| 1    | Modern Medicine                                     | doctor     |
| 2    | Dentist                                             | doctor     |
| 3    | Ayurveda                                            | doctor     |
| 4    | Unani                                               | doctor     |
| 5    | Siddha                                              | doctor     |
| 6    | Homoeopathy                                         | doctor     |
| 89   | Sowa-Rigpa                                          | doctor     |
| 220  | Yoga and Naturopathy                                | doctor     |
| 7    | Registered Auxiliary Nurse Midwife (RANM)           | nurse      |
| 8    | Registered Nurse (RN)                               | nurse      |
| 9    | Registered Nurse and Registered Midwife (RN and RM) | nurse      |
| 10   | Registered Lady Health Visitor (RLHV)               | nurse      |
| 33   | Pharmacist                                          | pharmacist |

Role:

| Code | Name                                         |
| ---- | -------------------------------------------- |
| 1    | Healthcare Professional                      |
| 2    | Facility Manager                             |
| 3    | Healthcare Professional and Facility Manager |

The subcategory codes differ between calls

Register professional and update professional use a second subcategory table, and its codes differ from the create HPID table above.

| Subcategory          | Code    |
| -------------------- | ------- |
| Dentistry            | 2       |
| Homoeopathy          | 3       |
| Ayurveda             | 4       |
| Unani                | 5       |
| Siddha               | 6       |
| Sowa-Rigpa           | 7       |
| Nurse categories     | 8 to 11 |
| Pharmacist           | 13      |
| Yoga and Naturopathy | 14      |

Fetch the codes from the HPRID subcategories master API rather than hard coding either table. See [HPR master data](#hpr-master-data).

## Getting an HPR token

The HPR token is not the gateway access token: it represents the professional, not your client. There are three ways to get one, and all three carry the gateway access token in the `Authorization` header as well.

### Login by password

One call. The professional supplies their HPR ID and password.

|        |                                    |
| ------ | ---------------------------------- |
| Method | `POST`                             |
| Path   | `/v4/int/api/v1/auth/authPassword` |

```json
{  "idType": "hpr_id",  "domainName": "@hpr.abdm",  "hprId": "<USERNAME_CHOSEN_AT_CREATE_HPID>@hpr.abdm",  "password": "<PASSWORD_THE_PROFESSIONAL_SET>"}
```

The `token` in the response is the HPR token. The HPR Swagger page at `https://apihspsbx.abdm.gov.in/v4/int/swagger-ui/index.html?urls.primaryName=HPR` lets you try the call in a browser.

The sample `expiresIn` is `1739710198`, which reads as a Unix timestamp rather than seconds. The other two login flows return `1800`. The call has not been run, so which reading is right is unknown.

### Login by mobile OTP

Four calls.

| Step                      | Method and path                                      | Body                                                                                                              |
| ------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 1. Send OTP               | `POST /v4/int/api/v2/auth/loginViaMobileSendOTP`     | `{ "mobile": "9999999999" }`                                                                                      |
| 2. Get public certificate | `GET /v4/int/api/v1/auth/cert`                       | None                                                                                                              |
| 3. Verify OTP             | Path not confirmed, see below                        | `{ "txnId": "<TXN_ID_FROM_STEP_1>", "otp": "<OTP_ENCRYPTED_WITH_THE_PUBLIC_CERT>", "mobile": "<MOBILE_NUMBER>" }` |
| 4. Login with HPR ID      | `POST /v4/int/api/v2/auth/login/userAuthorizedToken` | `{ "hpId": "<HPR_ID_FROM_STEP_3>", "txnId": "<TXN_ID_FROM_STEP_3>" }`                                             |

The verify OTP path is not yet published: the published value repeats the send OTP path, `loginViaMobileSendOTP`. Take the verify endpoint from the HPR Swagger page.

Step 1 response:

```json
{  "txnId": "061c660d-8752-4639-945d-e77a7ea6f564",  "mobileNumber": null}
```

Step 3 response, listing the HPR IDs linked to that mobile number:

```json
{  "txnId": "fc6d879c-e535-4ff1-9443-5dc6031efcc1",  "mobileLinkedHpIdDTO": [    {      "hprIdNumber": "**-****-0326-3829",      "name": "Test",      "hprId": "*****@hpr.abdm"    }  ]}
```

Step 4 response, which is the HPR token:

```json
{  "token": "<HPR_TOKEN_JWT>",  "expiresIn": 1800,  "refreshToken": "<REFRESH_JWT>",  "refreshExpiresIn": 10800}
```

### Login by Aadhaar OTP

Two calls.

| Step          | Method and path                                  | Body                                                                                                  |
| ------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| 1. Send OTP   | `POST /v4/int/api/v1/auth/init`                  | `{ "idType": "hpr_id", "domainName": "@hpr.abdm", "authMethod": "AADHAAR_OTP", "hprId": "<HPR_ID>" }` |
| 2. Verify OTP | `POST /v4/int/api/v1/auth/confirmWithAadhaarOtp` | `{ "otp": "<OTP>", "txnId": "<TXN_ID_FROM_STEP_1>" }`                                                 |

Step 1 returns `{ "txnId": "..." }`. Step 2 returns the same token object as step 4 of the mobile flow.

## Register professional

The one HPR write call with a published path.

|             |                                                                                  |
| ----------- | -------------------------------------------------------------------------------- |
| Method      | `POST`                                                                           |
| Sandbox URL | `https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/register-professional-new` |

The `hprToken` from create HPID goes in the payload, not the header. The gateway access token goes in the `Authorization` header.

The payload is grouped into personal information, communication address, registration data, qualification data and current work details. Selected fields and their rules:

| Field                                         | Mandatory   | Notes                                                                                             |
| --------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------- |
| `hprToken`                                    | Yes         | From create HPID, or from a login call                                                            |
| `healthProfessionalType`                      | Yes         | `doctor`, `nurse` or `pharmacist`. An empty or wrong value makes the whole request invalid        |
| `salutation`, `firstName`                     | Yes         | `middleName` and `lastName` are optional                                                          |
| `nationality`                                 | Yes         | ID from the countries master                                                                      |
| `languagesSpoken`                             | Yes         | Comma separated master codes, for example `1,5`                                                   |
| `isCommunicationAddressAsPerKYC`              | No          | `0` means the communication address fields below become mandatory. `1` means they do not          |
| `category`                                    | Yes         | Category code, for example `1` for doctor                                                         |
| `categoryId`                                  | Yes         | Subcategory code, for example `1` for Modern Medicine                                             |
| `registeredWithCouncil`, `registrationNumber` | Yes         | Council ID comes from the councils master                                                         |
| `nameOfDegreeOrDiplomaObtained`               | Yes         | ID from the courses master                                                                        |
| `college`, `university`                       | Yes         | IDs from the master data. Send `0` for "Any Other"                                                |
| `yearOfAwardingDegreeDiploma`                 | Yes         | `monthOfAwardingDegreeDiploma` is optional                                                        |
| `currentlyWorking`                            | Yes         | `0` or `1`. If `0`, `reasonForNotWorking` becomes mandatory                                       |
| `chooseWorkStatus`                            | Yes         | `0` private, `1` government, `2` both                                                             |
| `ministry`                                    | Conditional | Mandatory when `chooseWorkStatus` is `1` or `2`. Values from the get all ministry master          |
| `isPermanentOrRenewable`                      | Conditional | Mandatory for a doctor. If `Renewable`, `renewableDueDate` is mandatory. Not required for a nurse |

Three conditional rules apply separately:

- When `chooseWorkStatus` is `1` or `2`, `category` inside `personalInformation` must be `C` for central government or `S` for state. When it is `0`, send an empty string. Mandatory either way.
- When `chooseWorkStatus` is `1` or `2`, `facilityDeclarationData` is mandatory.
- Without `facilityId`, then `facilityName`, `facilityAddress`, `facilityPincode`, state, district and `facilityType` are mandatory. With it, `facilityDepartment` and `facilityDesignation` are mandatory.

### Degree codes

| Code | Degree | System of medicine |
| ---- | ------ | ------------------ |
| 4060 | MBBS   | Modern Medicine    |
| 4074 | BDS    | Dentistry          |
| 4079 | BAMS   | Ayurvedic          |
| 4082 | BUMS   | Unani              |
| 61   | BSMS   | Siddha             |
| 74   | BTMS   | Sowa-Rigpa         |
| 40   | BHMS   | Homoeopathy        |
| 9568 | BPharm | Pharmacist         |

### Attachments

Every attachment in the payload uses the same shape:

```json
{  "fileType": "image/jpeg",  "data": "<BASE64_ENCODED_FILE>"}
```

Accepted file types are JPEG, PNG and PDF, sent in `fileType`. Read the exact value back from your own response rather than hard coding one.

### A note on nurses

The SMD ID identifies doctors only. Searching nurse colleges by SMD returns a null college or university name. That is expected, not a failure. For nurses, SMD is always null.

## The other professional calls

| Call                                | Published parameters                                                                                                                        | Path        |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Retrieve professional document list | `hprid`                                                                                                                                     | Not in text |
| Upload documents                    | `hpr_token`, `document_id`, `document_type`, `data` (base64)                                                                                | Not in text |
| Update professional                 | The same field table as register professional, with `hprToken` from a login call                                                            | Not in text |
| Fetch professional details          | `id` (HPR ID, mandatory), `name` (minimum 3 letters), `contactNumber`, `state`, `registrationNumber`, `stateCouncilName`                    | Not in text |
| Search facility from HPR            | `ownershipCode`, `stateLGDCode`, `districtLGDCode`, `subdistrictLGDCode`, `pincode`, `facilityName`, `facilityId`, `page`, `resultsPerPage` | Not in text |

Upload rules: profile photo 1 MB or smaller, other documents 5 MB or smaller, accepted types png, jpeg, jpg and PDF. The document types are `profilePhoto`, `degreeCertificate`, `registrationCertificate`, `proofOfWorkCertificate`, `proofOfNameChangeRegCertificate` and `proofOfNameChangeQualCertificate`. Which identifier you send as `document_id` depends on the type:

| Document type                      | Identifier to use              |
| ---------------------------------- | ------------------------------ |
| `profilePhoto`                     | Parent identifier              |
| `degreeCertificate`                | Qualification block identifier |
| `registrationCertificate`          | Registration block identifier  |
| `proofOfWorkCertificate`           | Parent identifier              |
| `proofOfNameChangeRegCertificate`  | Registration block identifier  |
| `proofOfNameChangeQualCertificate` | Qualification block identifier |

## HFR onboarding

Five calls, in order. Method and path are not yet published; the parameter tables are.

### 1. Deduplicate search

Run this before you create anything, so you do not create a second record for a facility that already exists.

| Param         | Required | Notes                                         |
| ------------- | -------- | --------------------------------------------- |
| `facilityId`  | No       | 6 digit numeric facility unique ID            |
| `name`        | Yes      | Alphanumeric, one space between words         |
| `address`     | No       | Alphanumeric plus `-_.(),/`                   |
| `district`    | Yes      | District LGD code                             |
| `subDistrict` | Yes      | Sub district LGD code                         |
| `village`     | No       | Village LGD code                              |
| `geolocation` | No       | Latitude and longitude, 1 to 6 decimal places |

LGD codes come from the Local Government Directory at [lgdirectory.gov.in](https://lgdirectory.gov.in/), and from the LGD lookup calls below.

### 2. Basic facility information

Creates the record and returns a tracking ID that acts as the facility ID for every later call. Needs an HPR token in the header, generated from an HPR ID and password.

Mandatory fields:

| Param                                 | Notes                                                                                                                                                      |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `facilityName`                        | First character must be a letter or a digit                                                                                                                |
| `ownershipCode`                       | `G` government, `P` private, `PP` public private                                                                                                           |
| `ownershipSubTypeCode`                | `C` or `S` when ownership is `G`. `P` or `NP` when ownership is `P` or `PP`                                                                                |
| `ownershipSubTypeCode2`               | From the ownership subtype call                                                                                                                            |
| `workingInPsu`, `facPsuName`          | Only when ownership is `G` and subtype is `C`                                                                                                              |
| `systemOfMedicineCode`                | From master data with `type=MEDICINE`. Comma separate for several                                                                                          |
| `facilityTypeCode`, `facilitySubType` | From the facility type and facility subtype calls                                                                                                          |
| `specialityTypeCode`                  | From master data with `type=SPECIALITY-TYPE`                                                                                                               |
| `facilityOperationalStatus`           | From master data with `type=FACSTATUS`                                                                                                                     |
| `typeOfServiceCode`                   | From master data with `type=TYPESERVICE`. Not required for diagnostic laboratory, imaging centre, cath laboratory, dialysis centre, blood bank or pharmacy |
| `facilityAddressDetails`              | Country, state, district and sub district LGD codes, address line 1, pincode, latitude and longitude                                                       |
| `facilityUploads`                     | `facilityBoardPhoto` and `facilityBuildingPhoto`, each as a `name` and a base64 `value`, maximum 5 MB, extension in the name matching the file             |
| `timingsOfFacility`                   | `workingDays` and `openingHours`, mandatory when the facility is functional. Hours accept `10:00 AM-2:00 PM` or `24*7`                                     |

Optional fields include `facilityRegion` (`R` rural or `U` urban), the contact block, the address proof block and `abdmCompliantSoftware`.

### 3. Additional information

The tracking ID plus yes or no flags, each answered with a code from master data `type=GENERAL-INFO-OPTIONS`: `hasDialysisCenter`, `hasPharmacy`, `hasBloodBank`, `hasCathLab`, `hasDiagnosticLab`, `hasImagingCenter`. With an imaging centre, `servicesByImagingCenter` carries a service code and equipment count per service.

It also carries the facility's existing scheme identifiers, all optional: `nhrrId`, `nin`, `abpmjayId`, `rohiniId`, `echsId`, `cghsId`, `ceaRegistration` and `stateInsuranceSchemeId`.

### 4. Detailed information

The tracking ID plus the sections that apply, which depends on the facility type, the type of service and the system of medicine. The rules:

- Specialities are required for most facility types, but not for blood bank, cath laboratory, diagnostic laboratory, dialysis centre, imaging centre or pharmacy.
- Medical infrastructure is mandatory for IPD and day care. For IPD at least one bed count must be greater than zero; for day care at least one day care bed count must be.
- For OPD where the system of medicine is dentistry, `countDentalChairs` is mandatory.
- For imaging centre, diagnostic laboratory, blood bank and pharmacy, medical infrastructure is not required.
- `totalNumberOfBeds` must be equal to or greater than the sum of the individual bed counts.
- The pharmacy, blood bank, diagnostic and imaging sections are each required when the facility is of that type or offers that service.

### 5. Submit facility

| Param                 | Required | Notes                                                         |
| --------------------- | -------- | ------------------------------------------------------------- |
| `trackingId`          | Yes      | From the basic information call                               |
| `sourceOfInformation` | No       | Leave empty and the facility is treated as a submitted entity |
| `sourceUniqueID`      | No       | The facility's ID in your own source system                   |

Needs an `x-hpird-auth` token in the header. Until you make this call the facility stays in draft.

## Bridge linkage

Links one facility to one or more bridges. Path not in text.

| Param          | Required | Notes                                                                                                                                                                                                                                 |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `facilityId`   | Yes      | Starts with `IN`, 12 characters in total                                                                                                                                                                                              |
| `facilityName` | Yes      | Alphanumeric plus `-_.(),/`                                                                                                                                                                                                           |
| `bridgeId`     | Yes      | Alphanumeric                                                                                                                                                                                                                          |
| `hipName`      | Yes      | The name a patient sees in their [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) or [PHR](/docs/hiecm/v3/getting-started/glossary#phr) app. 15 characters or fewer, no special characters, unique for every bridge on a facility |
| `type`         | Yes      | `HIP` or `HIU`                                                                                                                                                                                                                        |
| `active`       | Yes      | `true` or `false`                                                                                                                                                                                                                     |

## HFR search and master data

Paths are not yet published. Two appear inside other parameter descriptions: `v1.5/facility/fetchfacilitytype` and `/v1.5/facility/get-specialities`.

| Call                    | Parameters                                                                                                                                                                                | Notes                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Master types            | None                                                                                                                                                                                      | A GET. Returns the list of master data set types                              |
| Master data             | `type`                                                                                                                                                                                    | The type comes from master types                                              |
| LGD states              | None                                                                                                                                                                                      | A GET. Returns states with their districts nested                             |
| LGD districts           | `stateCode`                                                                                                                                                                               |                                                                               |
| LGD sub districts       | `districtCode`                                                                                                                                                                            |                                                                               |
| Facility type           | `ownershipCode`, `systemOfMedicineCode`                                                                                                                                                   | Ownership accepts `G` or `P` here                                             |
| Facility subtype        | `facilityTypeCode`                                                                                                                                                                        |                                                                               |
| Ownership subtype       | `ownershipCode`, `ownerSubtypeCode`                                                                                                                                                       |                                                                               |
| Get specialities        | `systemOfMedicineCode`                                                                                                                                                                    | One system of medicine per call                                               |
| PSU details by ministry | Ministry code from ownership subtype                                                                                                                                                      |                                                                               |
| Search facility         | Either `facilityId`, or `ownershipCode` with `stateLGDCode` and `facilityName`. Plus `page` (minimum 1) and `resultsPerPage` (minimum 10)                                                 | Fuzzy match on name, exact match on everything else                           |
| Nearby search           | `centerLat`, `centerLon`, `radiusInKm`, `from`, `size` are mandatory. `abdmSoftware`, `facilityOwnership`, `hospitalSpecialityType`, `speciality` and `facilityName` are optional filters | Results are ordered by distance, nearest first                                |
| Send OTP to contact     | `facilityId`                                                                                                                                                                              | Returns a transaction ID and sends an OTP to the facility's registered mobile |
| Validate OTP            | `facilityId`, `sourceId`, `otp`, `source`, `transactionId`                                                                                                                                | `source` accepts `Government programs`                                        |

## HPR master data

There are 17 master data calls, in four groups:

- Qualifications: system of medicine, medical councils, languages, universities, courses, colleges
- Geography: countries, states, districts, sub districts
- Nursing bodies: nurse affiliated boards, nurse councils, nurse college by state, affiliated board by state councils
- Classification: get all ministry, HPRID categories, HPRID subcategories

The only master data paths the document carries in text:

| Call                    | Method and path                                           |
| ----------------------- | --------------------------------------------------------- |
| Countries               | `GET /v4/int/apis/v1/masters/countries/{country_id}`      |
| States                  | `GET /v4/int/apis/v1/masters/states/{state_id}`           |
| Districts               | `GET /v4/int/apis/v1/masters/district/{state_id}`         |
| Sub districts           | `GET /v4/int/apis/v1/masters/sub-districts/{district_id}` |
| Languages               | `GET /v4/int/apis/v1/masters/languages/{language_id}`     |
| Courses                 | `GET /v4/int/apis/v1/masters/courses`                     |
| Nurse affiliated boards | `GET /v4/int/apis/v1/masters/affiliated-board`            |

Three appear as complete URLs: countries, states and nurse affiliated boards. The other four appear only as path fragments inside field descriptions, so the `/v4/int/` prefix on those is our reading of the base URL, not a quote.

Path variables are optional. Drop one and you get the full list. Countries returns:

```json
{  "id": 356,  "alpha_2_code": "IN",  "alpha_3_code": "IND",  "enShortName": "India",  "nationality": "Indian"}
```

Two calls take parameters:

| Call                | Parameters                                                          |
| ------------------- | ------------------------------------------------------------------- |
| HPRID categories    | `role`: `1` healthcare professional, `2` facility manager, `3` both |
| HPRID subcategories | `role` as above, plus `categoryCode` from the categories call       |

A published system of medicine table carries a twelfth row, `12 Registered Pharmacist`, filed under `nurse`. Fetch the list from the master API rather than copying either table.

## Error codes

There are 150 error codes, all prefixed `HIS-`, in six groups.

| Range                  | What it covers                              | Examples                                                                                                                                                 |
| ---------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `HIS-400` to `HIS-504` | The HTTP level failures                     | `HIS-401` user is not authorized, `HIS-403` forbidden, `HIS-503` requested service is unavailable                                                        |
| `HIS-1xxx`             | Validation and facility errors, 103 of them | `HIS-1002` the field value should not be empty, `HIS-1124` bridge not linked, `HIS-1128` HIP name already exists, `HIS-1132` duplicate facility detected |
| `HIS-2xxx`             | Aadhaar, OTP and session errors             | `HIS-2022` invalid OTP, `HIS-2031` request expired, `HIS-2045` session expired                                                                           |
| `HIS-3xxx`             | Aadhaar data and HPID state                 | `HIS-3001` resident data not available, `HIS-3021` HPRID already exists, `HIS-3031` invalid token                                                        |
| `HIS-4xxx`             | Facility record errors                      | `HIS-4003` facility already exists, `HIS-4032` invalid state code, `HIS-4055` invalid image format                                                       |
| `HIS-5xxx`             | Registration workflow errors                | `HIS-5005` already registered, `HIS-5011` token expired                                                                                                  |

The full list is in the sandbox documentation for the [healthcare professional registry](https://sandbox.abdm.gov.in/sandbox/v3/new-documentation?doc=healthcare-professional-registry).

## Where to go next

- The interactive reference: [M4 API reference](/reference/hiecm-m4).
- The order of calls, as diagrams: [M4 user journeys](/docs/hiecm/v3/milestones/m4).
- A path missing here that you need now: ask on [support](/docs/support).
