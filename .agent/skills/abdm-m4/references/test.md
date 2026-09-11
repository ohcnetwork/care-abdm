# Test M4, facility and professional registries

Each case names the call it makes and what to see when it passes.

## Test cases

184 cases, from NHA's M4 matrix for HPR and HFR registration. "Mandatory" is NHA's own marking.

### Search facility: Search API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-001` | Optional | Search through facility id |  | Facility id should get filled |
| `HFR-002` | Conditional | search through facility name |  | Facility name should get filled |
| `HFR-003` | Conditional | To fill the facility ownership |  | Facility ownership should get filled |
| `HFR-004` | Conditional | To fill the facility state |  | Facility state should get filled |
| `HFR-005` | Optional | To fill the facility district |  | Facility district should get filled |
| `HFR-006` | Optional | To fill the facility sub-district |  | Facility subdistrictshould get filled |
| `HFR-007` | Optional | To fill the facility pincode |  | Facility pincode should get filled |
| `HFR-008` | Mandatory | To show number of pages |  | should have default value as 1 |
| `HFR-009` | Mandatory | To show number of facilities per page |  | should have default value as 10 |

### Registration: Registration Basic API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-010` | Mandatory | To Save the facilty basic details |  | Filled Facility Name |
| `HFR-011` | Mandatory | Fill the geographic location |  | Latitude has been filled as per the definition |
| `HFR-012` | Mandatory | HFR-012 |  | longitude has been filled as per the definition |
| `HFR-013` | Unmarked | To select the country |  |  |
| `HFR-014` | Mandatory | To select the State |  | State should get selected |
| `HFR-015` | Mandatory | To select the District |  | District should get selected |
| `HFR-016` | Mandatory | To select the Sub-district |  | Sub-District should get selected |
| `HFR-017` | Mandatory | To fill the facility address |  | Address should get filled |
| `HFR-018` | Optional | HFR-018 |  | Address should get filled |
| `HFR-019` | Mandatory | To enter the facility pincode |  | Pincode should get filled |
| `HFR-020` | Conditional | To select the facility working days |  | working days should get selected |
| `HFR-021` | Mandatory | To fill the opening hours of the facility |  | Facility Timings should get saved |
| `HFR-022` | Mandatory | To select the facility operational status |  | Facility operational status should get filled |
| `HFR-023` | Optional | To enter the facility landline number for public display |  | Landline number should get filled |
| `HFR-024` | Optional | To enter the facility mobile number for public display |  | Mobile number should get filled |
| `HFR-025` | Optional | To enter the email for public display |  | Facility email should get filled |
| `HFR-026` | Optional | To enter the hospital website link |  | Proper Website should get filled |
| `HFR-027` | Optional | facility file Uploads |  | Photograph should get saved |
| `HFR-028` | Optional | HFR-028 |  | Photograph should get saved |
| `HFR-029` | Optional | HFR-029 |  | Address proof type should get selected |
| `HFR-030` | Conditional | HFR-030 |  | Address proof should get saved |
| `HFR-031` | Mandatory | To provide the ownership details |  | Facility ownership should get saved |
| `HFR-032` | Conditional | HFR-032 |  | Facility ownership subtype should get saved |
| `HFR-033` | Conditional | HFR-033 |  |  |
| `HFR-034` | Mandatory | To provide the details of system of medicine |  | System of medicine should get saved |
| `HFR-035` | Mandatory | To enter the type of facility |  | Facility Type should get saved |
| `HFR-036` | Mandatory | HFR-036 |  | Facility sub type should get saved |
| `HFR-037` | Mandatory | To enter the type of services provided |  | Multiple type of service should get selected |
| `HFR-038` | Mandatory | To enter the Specialization |  | Multiple Specialization should get selected |

### Registration: Registration Additional API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-039` | Optional | Linked program Id |  | It should get filled |
| `HFR-040` | Optional | HFR-040 |  | It should get filled |
| `HFR-041` | Optional | HFR-041 |  | It should get filled |
| `HFR-042` | Optional | HFR-042 |  | It should get filled |
| `HFR-043` | Optional | HFR-043 |  | It should get filled |
| `HFR-044` | Optional | HFR-044 |  | It should get filled |
| `HFR-045` | Optional | HFR-045 |  | It should get filled |
| `HFR-046` | Optional | HFR-046 |  | It should get filled |

### Registration: Registration Detailed API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-047` | Mandatory | systemOfMedicineCode |  | System of medicine should get selected |
| `HFR-048` | Mandatory | isSpecializationAvalaible |  |  |
| `HFR-049` | Conditional | specialities |  |  |
| `HFR-050` | Optional | countIPDBedsWithoutOxygen |  | Details should get filled |
| `HFR-051` | Optional | countIPDBedsWithOxygen |  | Details should get filled |
| `HFR-052` | Optional | countICUBedsWithVentilators |  | Details should get filled |
| `HFR-053` | Optional | countICUBedsWithoutVentilators |  | Details should get filled |
| `HFR-054` | Optional | countHDUBedsWithFunctionalVentilators |  | Details should get filled |
| `HFR-055` | Optional | countHDUBedsWithVentilators |  | Details should get filled |
| `HFR-056` | Optional | countHDUBedsWithoutVentilators |  | Details should get filled |
| `HFR-057` | Mandatory | totalNumberOfVentilators |  | Details should get filled |
| `HFR-058` | Optional | countDayCareBedsWithoutOxygen |  | Details should get filled |
| `HFR-059` | Optional | countDayCareBedsWithOxygen |  | Details should get filled |
| `HFR-060` | Mandatory | totalNumberOfBeds |  | Details should get filled |
| `HFR-061` | Optional | countDentalChairs |  | Details should get filled |

### Registration: Registration Submit API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-062` | Optional | sourceOfInformation |  | Facility shold get submitted |
| `HFR-063` | Optional | sourceUniqueID |  |  |

### Facility update: Registration Basic details update API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-064` | Mandatory | To edit the facilty basic details |  | Filled Facility Name |
| `HFR-065` | Mandatory | Change the geographic location |  | Latitude has been filled as per the definition |
| `HFR-066` | Mandatory | HFR-066 |  | longitude has been filled as per the definition |
| `HFR-067` | Unmarked | To select the country |  |  |
| `HFR-068` | Mandatory | To edit the State |  | State should get selected |
| `HFR-069` | Mandatory | To edit the District |  | District should get selected |
| `HFR-070` | Mandatory | To edit the Sub-district |  | Sub-District should get selected |
| `HFR-071` | Mandatory | To edit the facility address |  | Address should get filled |
| `HFR-072` | Optional | HFR-072 |  | Address should get filled |
| `HFR-073` | Mandatory | To edit the facility pincode |  | Pincode should get filled |
| `HFR-074` | Conditional | To edit the facility working days |  | working days should get selected |
| `HFR-075` | Mandatory | To edit the opening hours of the facility |  | Facility Timings should get saved |
| `HFR-076` | Mandatory | To edit the facility operational status |  | Facility operational status should get filled |
| `HFR-077` | Optional | To eidt the facility landline number for public display |  | Landline number should get filled |
| `HFR-078` | Optional | To edit the facility mobile number for public display |  | Mobile number should get filled |
| `HFR-079` | Optional | To edit the email for public display |  | Facility email should get filled |
| `HFR-080` | Optional | To edit the hospital website link |  | Proper Website should get filled |
| `HFR-081` | Optional | edit facility file Uploads |  | Photograph should get saved |
| `HFR-082` | Optional | HFR-082 |  | Photograph should get saved |
| `HFR-083` | Optional | HFR-083 |  | Address proof type should get selected |
| `HFR-084` | Conditional | HFR-084 |  | Address proof should get saved |
| `HFR-085` | Mandatory | To edit the ownership details |  | Facility ownership should get saved |
| `HFR-086` | Conditional | HFR-086 |  | Facility ownership subtype should get saved |
| `HFR-087` | Conditional | HFR-087 |  |  |
| `HFR-088` | Mandatory | To edit the details of system of medicine |  | System of medicine should get saved |
| `HFR-089` | Mandatory | To edit the type of facility |  | Facility Type should get saved |
| `HFR-090` | Mandatory | HFR-090 |  | Facility sub type should get saved |
| `HFR-091` | Mandatory | To edit the type of services provided |  | Multiple type of service should get selected |
| `HFR-092` | Mandatory | To edit the Specialization |  | Multiple Specialization should get selected |

### Facility update: Registration Additional details update API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-093` | Optional | Edit Linked program Id |  | It should get filled |
| `HFR-094` | Optional | HFR-094 |  | It should get filled |
| `HFR-095` | Optional | HFR-095 |  | It should get filled |
| `HFR-096` | Optional | HFR-096 |  | It should get filled |
| `HFR-097` | Optional | HFR-097 |  | It should get filled |
| `HFR-098` | Optional | HFR-098 |  | It should get filled |
| `HFR-099` | Optional | HFR-099 |  | It should get filled |
| `HFR-100` | Optional | HFR-100 |  | It should get filled |

### Facility update: Registration Detailed details update API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-101` | Mandatory | To edit systemOfMedicine |  | System of medicine should get selected |
| `HFR-102` | Mandatory | to edit if Specialization is Avalaible |  |  |
| `HFR-103` | Conditional | To edit specialities |  |  |
| `HFR-104` | Optional | To edit countIPDBedsWithoutOxygen |  | Details should get filled |
| `HFR-105` | Optional | To edit countIPDBedsWithOxygen |  | Details should get filled |
| `HFR-106` | Optional | To edit countICUBedsWithVentilators |  | Details should get filled |
| `HFR-107` | Optional | To edit countICUBedsWithoutVentilators |  | Details should get filled |
| `HFR-108` | Optional | To edit countHDUBedsWithFunctionalVentilators |  | Details should get filled |
| `HFR-109` | Optional | To edit countHDUBedsWithVentilators |  | Details should get filled |
| `HFR-110` | Optional | To edit countHDUBedsWithoutVentilators |  | Details should get filled |
| `HFR-111` | Mandatory | To edit totalNumberOfVentilators |  | Details should get filled |
| `HFR-112` | Optional | To edit countDayCareBedsWithoutOxygen |  | Details should get filled |
| `HFR-113` | Optional | To edit countDayCareBedsWithOxygen |  | Details should get filled |
| `HFR-114` | Mandatory | To edit totalNumberOfBeds |  | Details should get filled |
| `HFR-115` | Optional | To edit countDentalChairs |  | Details should get filled |

### Facility update: Registration Resubmit API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-116` | Optional | sourceOfInformation |  | Facility shold get submitted |
| `HFR-117` | Optional | sourceUniqueID |  |  |

### Bridge linkage: Bridge linkage

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-118` | Mandatory | Fill the facility Id |  | Facility should get validated |
| `HFR-119` | Mandatory | Fill the facility Name |  | Facility Name should fetch |
| `HFR-120` | Mandatory | Fill the bridge Id |  | Bridge id should get validated |
| `HFR-121` | Mandatory | Fill the hip Name |  | Valid HIP name should get filled |
| `HFR-122` | Mandatory | Fill the HIP type |  |  |
| `HFR-123` | Mandatory | Provide details if the bridge is Active or not |  |  |

### Bridge linkage: Second Bridge linkage

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HFR-121` | Mandatory | Fill the hip Name |  | Valid HIP name should get filled and HIP name should not be repeated |

### HPR: Fetch Professionals details (HPR-002 to HPR-011)

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HPR-002` | Mandatory | Create your Healthcare Professional ID via Aadhaar |  | The system must provide an option to create HPR through Aadhaar |
| `HPR-003` | Mandatory | consent collection |  | Please refer the cell no -M5 |
| `HPR-004` | Mandatory | Suggestions:- Consent collection should be multilingual |  | User provides consent for sharing of Aadhaar details and creation of HPR. System records user consent for com… |
| `HPR-005` | Mandatory | Aadhaar collection and Error Message |  | User is prompted to enter correct Aadhaar Number |
| `HPR-006` | Mandatory | Captcha |  | system should allow user to enter captcha, before submitting Aadhaar details |
| `HPR-007` | Mandatory | Aadhaar OTP Collection |  | User receives Aadhaar OTP and System must allow the user to enter Aadhaar OTP. |
| `HPR-008` | Mandatory | Resend OTP |  | User will able to send OTP again and verify it |
| `HPR-010` | Mandatory | Communication Mobile Number verification-I |  | 1. If communication mobile number is same as Aadhaar linked mobile number then it should directly go to HPR c… |
| `HPR-011` | Mandatory | Communication Mobile Number verification-II |  | If communication mobile number is not same as Aadhaar linked mobile number then system must ask for the OTP t… |

### HPR: Register In HPR

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HPR-018` | Mandatory | hprToken |  | Received Token |
| `HPR-019` | Optional | profilePhoto |  | Photo will be displayed |
| `HPR-020` | Mandatory | Healthcare Professional ID |  | Healthcare Professional ID is successfully genearted |
| `HPR-022` | Optional | Mobile Number |  | input your mobile no for the official communication |
| `HPR-024` | Optional | Email and Email Status |  | input your email for the official communication |
| `HPR-026` | Mandatory | Salutation * |  | The system will provide a salutation as a mandatory field, offering options such as 'Dr,' 'Mr,' 'Ms,' from ma… |
| `HPR-027` | Mandatory | First Name * |  | First name is fetched from the Aadhaar database. |
| `HPR-028` | Mandatory | Middle Name |  | Middle Name is fetched from the Aadhaar database. |
| `HPR-029` | Mandatory | Last Name |  | Last name is fetched from the Aadhaar database. |
| `HPR-030` | Optional | Father's Name |  | User is able to fill the Father's Name. |
| `HPR-031` | Optional | Mother's Name |  | User is able to fill the Mother's Name. |
| `HPR-032` | Optional | Spouse's Name |  | User is able to fill the Spouse Name. |
| `HPR-033` | Mandatory | Nationality |  | The system should allow the user to select their country from a dropdown menu, with India being the default o… |
| `HPR-036` | Mandatory | Languages spoken * |  | The system should allow the user to input their preferred language by selecting from a multi-selection dropdo… |
| `HPR-037` | Mandatory | Address as per KYC : |  | The address will be automatically retrieved from the Aadhaar database which will be Non Editable field |
| `HPR-038` | Optional | Is this communication address same as your address as per KYC ? |  | The system should provide the option for the user to indicate whether the communication address is the same a… |
| `HPR-039` | Optional | Communication Address * |  | The system should allow the user to input their address |
| `HPR-040` | Optional | Name * |  | The system should allow the user to input the name of the communication person. |
| `HPR-041` | Optional | Country* |  | The system should allow the user to select their country from a dropdown menu |
| `HPR-042` | Optional | State/Union Territory * |  | The system should allow the user to select their communication state from a dropdown menu. |
| `HPR-043` | Optional | District * |  | The system should allow the user to select their communication district from a dropdown menu |
| `HPR-044` | Optional | Sub District |  | The system should allow the user to select their communication sub-district from a dropdown menu |
| `HPR-045` | Optional | City/Town/Village |  | The system should allow the user to input the name of the city. |
| `HPR-046` | Optional | Postal Code(PIN) * |  | The system should allow the user to input the postal code of the communication address. |
| `HPR-054` | Mandatory | category |  | system should allow user to select one category from drop down (Doctor - Modern Medicine, Unani etc.) |
| `HPR-055` | Mandatory | categoryId |  | system should allow user to select categoryId from drop down |
| `HPR-056` | Mandatory | registeredWithCouncil |  | system should allow user to select council from dropdown |
| `HPR-057` | Mandatory | registrationNumber |  | system should allow user to input registrationNumber |
| `HPR-058` | Mandatory | registrationDate |  | system should allow user to input registrationDate |
| `HPR-059` | Mandatory | registrationCertificate |  | base64 encoded image |
| `HPR-060` | Optional | isNameDifferentInCertificate |  | system should ask for yes or no if it is yes then ask for document pdf/png/jpeg/jpg upto 5 MB |
| `HPR-061` | Optional | proofOfNameChangeCertificate |  | system should ask for yes or no if it is yes then ask for document pdf/png/jpeg/jpg upto 5 MB |
| `HPR-062` | Mandatory | nameOfDegreeOrDiplomaObtained |  | system should allow user to select name of degree |
| `HPR-063` | Mandatory | country |  | system should allow user to select country from the dropdown |
| `HPR-064` | Mandatory | state |  | system should allow user to select communciation state from the dropdown |
| `HPR-065` | Mandatory | college |  | system should allow user to select college from the dropdown |
| `HPR-066` | Mandatory | university |  | system should allow user to select university from the dropdown |
| `HPR-067` | Optional | monthOfAwardingDegreeDiploma |  | system should allow user to input month of awarding degree |
| `HPR-068` | Mandatory | yearOfAwardingDegreeDiploma |  | system should allow user to input year of awarding degree |
| `HPR-069` | Mandatory | degreeCertificate |  | base64 encoded image |
| `HPR-070` | Mandatory | isNameDifferentInCertificate |  | system should allow user to input yes or no if name is different in certificate |
| `HPR-071` | Optional | proofOfNameChangeCertificate |  | Base 64- system should ask for yes or no if it is yes then ask for document pdf/png/jpeg/jpg upto 5 MB |
| `HPR-072` | Mandatory | Are you currentlty working (Yes/No) |  | Dropdown field |
| `HPR-073` | Mandatory | IF No, so please ask the reason for non working |  | Fillup the dropdown menu from master sheet and other free text option should be available for user to enter |
| `HPR-074` | Mandatory | If Yes, So radio button (Govt, Pvt or Both) |  |  |
| `HPR-075` | Mandatory | If Govt /Both, so document attachment is mandatory to upload upto 5 mb |  | Need to upload Payslip, recent transfer order etc. (In case of pvt no document is require) |
| `HPR-076` | Mandatory | If Govt/Both so facility decalartion is mandatory (Professinal can search the facility via name/Facility id) |  |  |
| `HPR-077` | Mandatory | Preview Profile & Submit |  | On submit button user profile will submit and message will come on SMS/Email. |

### HPR: Fetch Professionals details (HPR-078)

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HPR-078` | Optional | fetchProfessionalsdetails |  | After successful user creation system will display all the details to user |

### HPR: Update Professionals details

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HPR-079` | Mandatory | update-professional |  | If user want to update their inputed details in system then system should allow user to update their details |

### HPR: Upload Document API

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HPR-080` | Optional | Upload- Document |  | This API will help integrators, if document is not ready during the HPR creation so professional can upload t… |
