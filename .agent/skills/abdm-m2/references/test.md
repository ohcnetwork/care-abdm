# Test M2, linking and sharing

Each case names the call it makes and what to see when it passes.

## Test cases

46 cases, from NHA's M2 matrix for Care context linking and data sharing. "Mandatory" is NHA's own marking.

### Health Record Creation

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `Health_RECORD_CREATION_101` | Mandatory | Creation of Health Records |  | ABDM mandates only the sharing of digital health record in FHIR format. Expected result is generation of digi… |

### HIP Initiated Health Record Linking Using Mobile OTP

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INTI_LINK_201` | Optional | Link record via mobile OTP |  | The user/ patient should receive an OTP on the mobile number registered with ABHA address. |
| `HIP_INTI_LINK_202` | Optional | Receive OTP |  | OTP should be received on the registered mobile number |
| `HIP_INTI_LINK_203` | Optional | OTP validation |  | In case of correct OTP, the ABHA address of patient is validated. In case of incorrect OTP, the system throws… |
| `HIP_INTI_LINK_204` | Optional | Creation of new Token |  | New Linking token should be created |
| `HIP_INTI_LINK_205` | Optional | Linking of Health Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |
| `HIP_INTI_LINK_206` | Optional | Pull Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |

### HIP Initiated Health Record Linking Using Aadhaar OTP

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INTI_LINK_301` | Optional | Link record via aadhaar linked mobile OTP |  | The user/ patient should receive an OTP on the aadhaar linked mobile number registered with ABHA address. |
| `HIP_INTI_LINK_302` | Optional | Receive OTP |  | OTP should be received on the registered Aadhaar linked mobile number |
| `HIP_INTI_LINK_303` | Optional | OTP validation |  | In case of correct OTP, the user is validated. In case of incorrect OTP, the System throws an error. The link… |
| `HIP_INTI_LINK_304` | Optional | Creation of new Token |  | New Linking token should be created |
| `HIP_INTI_LINK_305` | Optional | Linking of Health Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |
| `HIP_INTI_LINK_306` | Optional | Pull Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |

### HIP Initiated Health Record Linking Using Direct Auth

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INTI_LINK_401` | Optional | Direct Auth mode for Linking of Health Records |  | The request for linking of Health record should be initiated using Direct auth mode. Health record will be li… |
| `HIP_INTI_LINK_402` | Optional | Notification on PHR App |  | User should get a notification on their PHR app for approval of request sent by HIP. |
| `HIP_INTI_LINK_403` | Optional | Creation of Linking Token |  | New Linking token should be created |
| `HIP_INTI_LINK_404` | Optional | Linking of Health Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |
| `HIP_INTI_LINK_405` | Optional | Pull Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |

### Grant Consent Request

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INIT_GRANT_CONSENT_` | Conditional | HIP must save consent (s)granted for a ABHA address in their system |  | Consent request seen in HMIS |

### Revoke Consent Request

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INIT_REVOKE_CONSENT` | Conditional | HIP must delete consents for a ABHA address in their system when it is revoked |  | Consent revoked seen in HMIS |

### Exprire Consent Request

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INIT_EXPIRE_CONSENT` | Conditional | HIP must delete consents for a ABHA address in their system when it is expired |  | Consent expired seen in HMIS |

### HIP Initiated Health Record Linking Using Demographic Auth

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INTI_LINK_501` | Conditional | Link record via Demographic Auth |  | HIP should have all the demographic details like Name , Date of Birth, Gender and Mobile number. |
| `HIP_INTI_LINK_502` | Conditional | Sharing demographic details |  | HIP should have all the demographic details like Name , Date of Birth, Gender and Mobile number |
| `HIP_INTI_LINK_503` | Conditional | Validate the demographic details |  | The demographic details should be validated by gateway. The linking token generated on successful authenticat… |
| `HIP_INTI_LINK_504` | Conditional | Creation of Linking Token |  | New Linking token should be created |
| `HIP_INTI_LINK_505` | Conditional | Linking of Health Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |
| `HIP_INTI_LINK_506` | Conditional | Pull Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |

### User Initiated Health Record Linking

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `USER_INIT_LINK_601` | Unmarked | Login into PHR App |  | The User should be able to login into PHR app |
| `USER_INIT_LINK_602` | Mandatory | Search for Facility/ HIP |  | The user should be able to search for the Health provider. |
| `USER_INIT_LINK_603` | Mandatory | Share User Profile Details with Facility/ HIP |  | The Gateway send the request to the HIP to identify the patient in th HIP System. The Facility/ HIP will rece… |
| `USER_INIT_LINK_604` | Mandatory | Fetch Health Records |  | In case Health Records are available with Facility/ HIP, the user will receive the list of health records ava… |
| `USER_INIT_LINK_605` | Mandatory | Provide Consent for Health Record Linking |  | In case the OTP is correct, selected health records are linked with ABHA. Selected Health record should only … |
| `USER_INIT_LINK_606` | Mandatory | Validate request |  | The request should be validated by CM |
| `USER_INIT_LINK_607` | Mandatory | Pull Records |  | Health record linking can now be initiated using the generated linking token. User can now pull the linked he… |

### Sending Notification for deep link workflow

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INIT_NOTIFY_HIECM` | Mandatory | sending notification to the patient on their mobile with deep link |  | SMS sent with deep link- 1. Beneficary will share their mobile number, not an ABHA address or ABHA Number. 2.… |

### Data transfer & share

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIP_INIT_SHARE_CARECONTEXT` | Mandatory | HIP must share health records associated with care context on request |  | 1. Health records will be successfully received in the PHR app 2. Health records must be properly decryptable… |

### Further checks this portal suggests

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `LNK_01` | Portal check | Group every new record into a care context |  | Two visits for one patient show as two entries in a PHR app, each named so the patient knows which visit it w… |
| `LNK_02` | Portal check | Store the link token at registration and validate it before every use |  | Linking works while the token is valid. An expired or missing token triggers regeneration, not a link attempt. |
| `LNK_03` | Portal check | Link a care context for a patient who gave you their ABHA address |  | The link is acknowledged and the record appears in the patient's PHR app with no action from the patient. |
| `NTF_01` | Portal check | Tell NHA a record is ready for a patient who has no ABHA address |  | The patient receives an SMS with a link that opens a PHR app, or offers to install one. |
| `DSC_01` | Portal check | Match an inbound discovery request and return the patient's care contexts | webhook `[object Object]` | A patient who has visited your facility sees their visits, named recognisably. A patient who has never visite… |
| `DAT_01` | Portal check | Validate a FHIR bundle against the NRCeS implementation guide |  | The validator reports no structural or profile error, for one bundle per HI type you support. |
| `DAT_02` | Portal check | Refuse a health information request that falls outside the consent | webhook `[object Object]` | Nothing is sent, and the failure carries the matching error code. |
| `DAT_03` | Portal check | Encrypt a bundle so only the requester can read it |  | Decrypting your output with the matching private key returns the original bundle byte for byte. |
| `DAT_04` | Portal check | Deliver a record you created to the ABHA PHR app end to end |  | The record displays, readable, in the ABHA PHR app, without you touching the app in between. |
| `DAT_05` | Portal check | Close the transfer with a completion notification, inside the timeout | `null health-information/notify` | A transfer that succeeded is recorded as succeeded on both sides, within 20 minutes of the request arriving. |
