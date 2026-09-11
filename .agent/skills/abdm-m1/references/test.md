# Test M1, ABHA identity

Each case names the call it makes and what to see when it passes.

## Test cases

122 cases, from NHA's M1 matrix for ABHA identity, registration and login. "Mandatory" is NHA's own marking.

### ABHA Creation Through Aadhaar OTP

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `CRT_ABHA_101` | Mandatory | Create ABHA Option |  | User will have an option to create ABHA |
| `CRT_ABHA_102` | Mandatory | Consent collection |  | User provides consent for sharing of Aadhaar details and creation of ABHA. System records user consent for co… |
| `CRT_ABHA_103` | Optional | Suggestions:- Consent collection should be multilingual |  | User provides consent for sharing of Aadhaar details and creation of ABHA. System records user consent for co… |
| `CRT_ABHA_104` | Mandatory | Aadhaar collection and Error Message |  | User is prompted to enter correct Aadhaar Number In case user enters an invalid Aadhaar number (A valid Aadha… |
| `CRT_ABHA_105` | Mandatory | Aadhaar OTP Collection |  | User will be able to enter a valid Aadhaar OTP (A valid Aadhaar OTP is a 6-digit number). Example - Modified … |
| `CRT_ABHA_106` | Mandatory | Resend OTP |  | User will able to send OTP again and verify it |
| `CRT_ABHA_107` | Mandatory | OTP based Aadhaar Authentication |  | System authenticates the user's Aadhaar through OTP In case of incorrect OTP, the system displays an error In… |
| `CRT_ABHA_108` | Optional | Communication Mobile Number verification-I |  | Redirect to the ABHA creation screen. |
| `CRT_ABHA_109` | Mandatory | Communication Mobile Number verification-II |  | System verifies the communication mobile number |
| `CRT_ABHA_112` | Conditional | Suggested ABHA Address |  | System should prompt / display the available or suggested ABHA addresses. System should allow the user to pro… |
| `CRT_ABHA_113` | Mandatory | Display of ABHA Number |  | User should be able to view the generated ABHA Number and linked ABHA address |
| `CRT_ABHA_114` | Conditional | View and Download ABHA details. (If integrators is generating ABHA card) |  | User should be able to view their ABHA Card with all the demographc details as mentioned in cell H26 |
| `CRT_ABHA_115` | Conditional | View and Download ABHA details. (If integrators is not generating ABHA card) |  | User should be able to view card with ABHA number and ABHA address and the details should be saved in HIMS sy… |

### ABHA Creation Through Aadhaar Biometric

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `CRT_ABHA_201` | Optional | Create ABHA Option |  | User will have a choice to create ABHA using Aadhaar Biometrics |
| `CRT_ABHA_202` | Optional | Consent collection |  | User provides consent for sharing of Aadhaar details and creation of ABHA. System records user consent for co… |
| `CRT_ABHA_203` | Optional | Suggestions:- Consent collection should be multilingual |  | User provides consent for sharing of Aadhaar details and creation of ABHA. System records user consent for co… |
| `CRT_ABHA_204` | Optional | Aadhaar collection and Error Message |  | User is prompted to enter correct Aadhaar Number In case user enters an invalid Aadhaar number (A valid Aadha… |
| `CRT_ABHA_205` | Optional | Biometric based Aadhaar Authentication |  | System authenticates the user's Aadhaar though user's biometrics In case of incorrect biometrics, the system … |
| `CRT_ABHA_206` | Optional | Communication Mobile Number verification-I |  | Redirect to the ABHA creation screen. |
| `CRT_ABHA_207` | Optional | Communication Mobile Number verification-II |  | System verifies the communication mobile number |
| `CRT_ABHA_208` | Optional | Display of ABHA Number |  | User should be able to view the generated ABHA Number |
| `CRT_ABHA_209` | Conditional | View and Download ABHA details. (If integrators is generating ABHA card) |  | User should be able to view their ABHA Card |
| `CRT_ABHA_210` | Conditional | View and Download ABHA details. (If integrators is not generating ABHA card) |  | User should be able to view card with ABHA number and ABHA address and the details should be saved in HIMS sy… |

### ABHA Creation Through Demo Auth/ Offline Mode (Available Only for trusted entities. All government Entities are eligible.

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `CRT_ABHA_301` | Mandatory | Create ABHA Option |  | The system must provide an option to create ABHA through Aadhaar Demographic/ Offline Mode |
| `CRT_ABHA_302` | Mandatory | Consent collection |  | User provides consent for sharing of Aadhaar details and creation of ABHA. System records user consent for co… |
| `CRT_ABHA_303` | Optional | Suggestions:- Consent collection should be multilingual |  | User provides consent for sharing of Aadhaar details and creation of ABHA. System records user consent for co… |
| `CRT_ABHA_304` | Mandatory | Aadhaar collection and Error Message |  | User is prompted to enter correct Aadhaar Number In case user enters an invalid Aadhaar number (A valid Aadha… |
| `CRT_ABHA_305` | Mandatory | Demographic Information based authentication |  | 1. System authenticates the user's Aadhaar though user's demographic data. 2.The fields for name, date of bir… |
| `CRT_ABHA_306` | Mandatory | Profile Completion |  | System should accepts user's profile information - |
| `CRT_ABHA_307` | Mandatory | Display of ABHA Number |  | User should be able to view the generated ABHA Number |
| `CRT_ABHA_308` | Conditional | View and Download ABHA details. (If integrators is generating ABHA card) |  | User should be able to view their ABHA Card |
| `CRT_ABHA_309` | Conditional | View and Download ABHA details. (If integrators is not generating ABHA card) |  | User should be able to view card with ABHA number and ABHA address.and the details should be saved in HIMS sy… |

### ABHA Creation Through Driving License / PAN

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `CRT_ABHA_401` | Optional | Create ABHA Option |  | User will have a choice to create ABHA using Aadhaar Biometrics |
| `CRT_ABHA_402` | Optional | Consent Collection |  | User provides consent for sharing of Aadhaar details and creation of ABHA. System records user consent for co… |
| `CRT_ABHA_403` | Optional | Communication Mobile Number |  | User will be able to enter their Mobile Number |
| `CRT_ABHA_404` | Optional | Mobile Number Verification |  | In case of incorrect OTP, the system displays an error In case of correct OTP, the system allows the user to … |
| `CRT_ABHA_405` | Optional | Document Verification |  | System validates user's Driving License / PAN |
| `CRT_ABHA_406` | Optional | Document Upload |  | Document photos are uploaded in the system |
| `CRT_ABHA_407` | Optional | Manual Verification and ABHA Creation |  | Documents are manually verified. In case the document is valid, the operator approves ABHA creation. In case … |
| `CRT_ABHA_408` | Optional | Display of ABHA Number |  | User should be able to view the generated ABHA Number |
| `CRT_ABHA_410` | Optional | View and Download ABHA details. (If integrators is generating ABHA card) |  | User should be able to view their ABHA Card and the details should be saved in HIMS system and linked with th… |
| `CRT_ABHA_411` | Optional | View and Download ABHA details. (If integrators is not generating ABHA card) |  | User should be able to view card with ABHA number and ABHA address. |

### ABHA Verification (VRFY_ABHA_101 to VRFY_ABHA_102)

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `VRFY_ABHA_101` | Mandatory | ABHA Number Verification using Aadhaar OTP |  | 1. In case of correct OTP, the verification is complete and the System can fetch user's ABHA profile - name, … |
| `VRFY_ABHA_102` | Mandatory | ABHA Address Verification using Aadhaar OTP |  | 1. In case of correct OTP, the verification is complete and the System can fetch user's ABHA profile - name, … |

### ABHA Verification (VRFY_ABHA_201 to VRFY_ABHA_202)

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `VRFY_ABHA_201` | Mandatory | ABHA Number verification using mobile OTP(ABHA Linked Mobile Number ) |  | 1. In case of correct OTP, the verification is complete and the System can fetch user's ABHA profile - name, … |
| `VRFY_ABHA_202` | Mandatory | ABHA Address verification using mobile OTP(ABHA Linked Mobile Number ) |  | 1. In case of correct OTP, the verification is complete and the System can fetch user's ABHA profile - name, … |

### ABHA Verification (VRFY_ABHA_301 to VRFY_ABHA_305)

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `VRFY_ABHA_301` | Mandatory | Fetch ABHA details using Mobile (communication)authentication . Multi authentication feature also need to be … |  | Display relevant error messgae. |
| `VRFY_ABHA_302` | Mandatory | ABHA Details not exists to communicated Mobile Number |  | System will display an error message i.e. " ABHA Number not found We did not find any ABHA number linked to t… |
| `VRFY_ABHA_303` | Mandatory | ABHA Details exists to communicated Mobile Number. |  | 1. Fetching ABHA Details. 2. Register and Linked in their HIMS OR OR benefciary can download the ABHA card. |
| `VRFY_ABHA_304` | Mandatory | Incorrect OTP |  | Display relevant error messgae. |
| `VRFY_ABHA_305` | Mandatory | Resend OTP Functionality |  | Resend OTP Functionality |

### Fetching ABHA details using Aadhaar Number

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `VRFY_ABHA_401` | Mandatory | Fetch ABHA details using Aadhaar Number |  | Display relevant error messgae. |
| `VRFY_ABHA_402` | Mandatory | Incorrect OTP |  | Display relevant error messgae. |
| `VRFY_ABHA_403` | Mandatory | ABHA Details not exists to Aadhaar Number |  | Display relevant error messgae. |
| `VRFY_ABHA_404` | Mandatory | ABHA Details exists to Aadhaar Number |  | 1. Display ABHA Profile details. 2. Download ABHA Card. 3. Register and linked in their HIMS beneficary's ID … |
| `VRFY_ABHA_405` | Mandatory | Resend OTP Functionality |  | Display relevant error messgae. |

### ABHA Verification (Applicable for Government Entites)

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `VRFY_ABHA_501` | Optional | ABHA Number verification using Aadhaar Biometric - Fingerprint |  | In case the biometrics match, the verification is complete and the System can fetch user's ABHA profile - nam… |
| `VRFY_ABHA_502` | Optional | ABHA Address verification using Aadhaar Biometric - Fingerprint |  | In case the biometrics match, the verification is complete and the System can fetch user's ABHA profile - nam… |

### Reading ABHA Info using ABHA QR Code

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `VRFY_ABHA_501` | Optional | Reading ABHA Profile Info using ABHA QR Code |  | System reads the user information from the ABHA QR code - name, date of birth, gender, mobile and other detai… |

### Profile Update

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `PROF_ABHA_601` | Optional | Mobile Update |  | Mobile number on ABHA profile is updated |
| `PROF_ABHA_602` | Optional | Photo Update |  | Photo on ABHA profile is updated |
| `PROF_ABHA_603` | Optional | Email Update |  | Email ID on ABHA profile is updated |
| `PROF_ABHA_604` | Optional | Re-KYC |  | KYC details on ABHA profile are updated |
| `PROF_ABHA_605` | Optional | Delete ABHA |  | ABHA Number should be deleted. The system should not allow login through the same ABHA |

### Verify one ABHA Number is linked to the unique patient ID in HIMS

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `TAGGING_UNIQUEPATIENTID_UNIQUEABHANUMBER` | Mandatory | Verify one ABHA Number is linked to the unique patient ID in HIMS |  | HIMS is able to tag Patient ID with ABHA number. |

### Share Profile

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `SHARE_PATIENT_PROFILE_701` | Mandatory | Share Patient Profile |  | 1. Log into PHR app. 2. User will scan the QR code which is placed at the facility premises/registration desk… |

### Further checks this portal suggests

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `B1` | Portal check | Create the ABHA number | `POST /v3/enrollment/enrol/byAadhaar` | The person types the code and comes out with a 14 digit ABHA number. |
| `B2` | Portal check | Reject a wrong Aadhaar OTP | `POST /v3/enrollment/enrol/byAadhaar` | A wrong code fails cleanly and creates nothing. |
| `B3` | Portal check | Reject a reused transaction id | `POST /v3/enrollment/enrol/byAadhaar` | A finished attempt cannot be replayed to create a second ABHA. |
| `C1` | Portal check | Verify the communication mobile | `POST /v3/enrollment/auth/byAbdm` | The number the person named is now on their profile. |
| `C2` | Portal check | Keep the two OTP systems apart | `POST /v3/enrollment/enrol/byAadhaar` | A code from NHA is refused at the Aadhaar endpoint. |
| `C3` | Portal check | Accept a non Aadhaar mobile number | `POST /v3/enrollment/request/otp` | A family phone or a changed number works as the communication number. |
| `B4` | Portal check | Link the chosen ABHA address | `POST /v3/enrollment/enrol/abha-address` | The address the person chose is the address they end up with. |
| `CRT_BIO_201` | Portal check | Capture a fingerprint or iris |  | An Aadhaar registered device produces a signed capture of the person's fingerprint or iris. |
| `CRT_BIO_202` | Portal check | Create the ABHA from the scan | `POST /v3/enrollment/enrol/byAadhaar` | The person gets a 14 digit ABHA number without typing a code. |
| `CRT_BIO_203` | Portal check | Start a face authentication | `POST /v3/enrollment/enrol/auth/init` | The portal shows a QR code for the person to scan with the ABHA app. |
| `CRT_BIO_204` | Portal check | Poll for the captured block | `POST /v3/enrollment/enrol/capturePID` | The portal waits until the person has finished on their phone, then moves on. |
| `CRT_BIO_205` | Portal check | Create the ABHA from the face | `POST /v3/enrollment/enrol/byAadhaar` | The person gets a 14 digit ABHA number after face authentication. |
| `CRT_DEMO_301` | Portal check | Create the ABHA from demographics | `POST /v3/enrollment/enrol/byAadhaar` | The person gets a 14 digit ABHA number with no code and no scan. |
| `CRT_DEMO_302` | Portal check | List the child accounts | `GET /v3/enrollment/profile/children` | The children mapped to a parent's ABHA number come back. |
| `CRT_DOC_401` | Portal check | Request a mobile OTP | `POST /v3/enrollment/request/otp` | A code reaches the mobile number the person gave. |
| `CRT_DOC_402` | Portal check | Verify the mobile OTP | `POST /v3/enrollment/auth/byAbdm` | The mobile number is confirmed before the document goes anywhere. |
| `CRT_DOC_403` | Portal check | Create the ABHA from the document | `POST /v3/enrollment/enrol/byDocument` | The person gets an ABHA number from an identity document instead of Aadhaar. |
| `VER_AADHAAR_501` | Portal check | Request a login OTP from Aadhaar | `POST /v3/profile/login/request/otp` | A code reaches the mobile number linked to the person's Aadhaar. |
| `D2` | Portal check | Verify the login OTP | `POST /v3/profile/login/verify` | A person who knows their 14 digit number is signed in. |
| `VER_AADHAAR_502` | Portal check | Request an Aadhaar login OTP | `POST /v3.1/profile/login/request/otp` | A person who typed their Aadhaar number gets a code. |
| `VER_AADHAAR_503` | Portal check | Verify the Aadhaar login OTP | `POST /v3.1/profile/login/verify` | The person is signed in with their Aadhaar number. |
| `VER_MOBILE_601` | Portal check | Request a login OTP by mobile | `POST /v3/profile/login/request/otp` | A code reaches the person, and the screen names the masked number it went to. |
| `VER_MOBILE_602` | Portal check | Verify the mobile OTP | `POST /v3/profile/login/verify` | The code is accepted and the accounts on that number are offered. |
| `D1` | Portal check | Pick an account and sign in | `POST /v3/profile/login/verify/user` | The person picks their ABHA from the list and is logged in. |
| `D3` | Portal check | Reject a wrong login OTP | `POST /v3/profile/login/verify` | A wrong code does not log anybody in. |
| `VER_MOBILE_603` | Portal check | Sign in by ABHA number | `POST /v3/profile/login/request/otp` | A person who knows their 14 digit number signs in with a code from NHA. |
| `VER_BIO_701` | Portal check | Start a face login transaction | `POST /v3/enrollment/enrol/auth/init` | The portal shows a QR code for the person to scan with the ABHA app. |
| `VER_BIO_702` | Portal check | Verify the face capture | `POST /v3.1/profile/login/verify` | The person is signed in after face authentication. |
| `VER_BIO_703` | Portal check | Sign in by fingerprint or iris | `POST /v3.1/profile/login/verify` | The person is signed in with a scan from an Aadhaar registered device. |
| `FND_MOBILE_801` | Portal check | Encrypt the mobile number | `POST /v3/phr/app/enrollment/encrypt` | The mobile number leaves your system scrambled. |
| `FND_MOBILE_802` | Portal check | Search for the accounts | `POST /v3/profile/account/abha/search` | The ABHA accounts held against that mobile number come back. |
| `FND_MOBILE_803` | Portal check | Request a login OTP | `POST /v3/profile/login/request/otp` | A code reaches the person for the account they chose. |
| `FND_MOBILE_804` | Portal check | Verify the OTP and sign in | `POST /v3/profile/login/verify` | The person is signed in to the ABHA they picked. |
| `FND_AADHAAR_901` | Portal check | Find the ABHA behind an Aadhaar | `GET /v3/profile/benefit/search/abhaByAadhaar` | The ABHA number recorded against that Aadhaar number comes back. |
| `FND_AADHAAR_902` | Portal check | Find the Aadhaar behind an ABHA | `GET /v3/profile/benefit/search/aadhaarByAbha` | The Aadhaar number recorded against that ABHA number comes back. |
| `F5` | Portal check | Reject a restricted endpoint |  | A private integrator is turned away from the benefit endpoints. |
| `QR_ABHA_1001` | Portal check | Get the ABHA QR code | `GET /v3/profile/account/qrCode` | The person sees the QR code that shares their ABHA at a facility desk. |
| `QR_ABHA_1002` | Portal check | Generate the ABHA card | `GET /v3/profile/account/abha-card` | The person sees their ABHA card. |
| `QR_ABHA_1003` | Portal check | Download the ABHA card | `GET /v3/profile/account/download-abha-card` | The person can save their ABHA card as a file. |
| `E3` | Portal check | Check the card and code render |  | The card and the QR code both come back and can be shown to the person. |
| `UPD_ABHA_1101` | Portal check | Request a new number OTP | `POST /v3/profile/account/request/otp` | A code reaches the number the person wants to move to. |
| `C4` | Portal check | Verify the profile change | `POST /v3/profile/account/verify` | The new number shows on the person's profile. |
| `UPD_ABHA_1102` | Portal check | Change email, password or KYC | `POST /v3/profile/account/request/otp` | The same pair of calls covers the other profile changes. |
| `UPD_ABHA_1103` | Portal check | Update self declared details | `PATCH /v3/profile/account` | The person's self declared details change on their profile. |
| `E1` | Portal check | Read the profile back | `GET /v3/profile/account` | The profile shows the ABHA number, address and mobile the person created. |
| `E2` | Portal check | Check both tokens are needed | `GET /v3/profile/account` | The profile comes back only when your system and the person both prove themselves. |
| `SHR_ABHA_1201` | Portal check | Share the profile at the desk |  | The person shares their ABHA address and profile with the facility after consenting. |
| `A1` | Portal check | Get a gateway access token | `POST /api/hiecm/gateway/v3/sessions` | Your system can prove who it is to NHA. |
| `A3` | Portal check | Encrypt the sensitive fields | `POST /v3/phr/app/enrollment/encrypt` | The Aadhaar number, mobile number and code that leave your system are scrambled, not readable. |
| `A2` | Portal check | Reject a call with no token | `GET /v3/profile/account` | A call that carries no token is refused. |
| `D4` | Portal check | Refresh the user token | `GET /v3/profile/account/request/token` | A session longer than half an hour keeps working without showing the person an error. |
| `D5` | Portal check | End the session | `GET /v3/profile/account/request/logout` | When the person logs out, their token stops working. |
| `F1` | Portal check | Reject an unknown path |  | A wrong URL gives a clear not found. |
| `F2` | Portal check | Reject an empty body | `POST /v3/profile/login/verify` | An empty request names the fields it wanted. |
| `F3` | Portal check | Reject a malformed token |  | A broken Authorization value is refused. |
| `F4` | Portal check | Reject a short ABHA number |  | A 13 digit ABHA number is refused. |
