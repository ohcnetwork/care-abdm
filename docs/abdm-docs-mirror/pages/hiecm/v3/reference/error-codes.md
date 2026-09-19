# Error codes

Seeing a symptom rather than a code? Start at [Troubleshooting](/docs/hiecm/v3/troubleshooting/).

A code is on this page because a response example in a specification returns it.

## M1 ABHA identity

| Code        | HTTP | Message                                                                                                                         | Returned by                                |
| ----------- | ---- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `900900`    | 500  | Unclassified Authentication Failure                                                                                             | `m1_post_v3_enrollment_auth_byabdm`        |
| `900901`    | 401  | Invalid Credentials                                                                                                             | `m1_post_v3_enrollment_request_otp`        |
| `900902`    | 401  | Missing Credentials                                                                                                             | `m1_post_v3_profile_benefit_search`        |
| `ABDM-1017` | 400  | Invalid transaction, either the transaction is expired or not found                                                             | `m1_post_v3_enrollment_enrol_capturepid`   |
| `ABDM-1021` | 401  | Lack of required priviledges                                                                                                    | `m1_post_v3_enrollment_enrol_byaadhaar`    |
| `ABDM-1094` | 401  | X-token expired                                                                                                                 | `m1_post_v3_enrollment_enrol_byaadhaar`    |
| `ABDM-1114` | 404  | No ABHA user registered with this Aadhaar number.                                                                               | `m1_post_v3_profile_login_verify`          |
| `ABDM-1124` | 422  | The mobile number provided by you is already linked to 6 ABHA Numbers. Please provide a different Mobile Number.                | `m1_post_v3_enrollment_enrol_byaadhaar`    |
| `ABDM-1138` | 400  | The benefit record has already been de-linked                                                                                   | `m1_post_v3_profile_benefit_linkanddelink` |
| `ABDM-1157` | 422  | Child ABHA’s account limit has been exceeded for the requested Abha ID number ‘\<ABHA\_NUMBER>                                  | `m1_post_v3_enrollment_enrol_byaadhaar`    |
| `ABDM-1160` | 422  | Non KYC CHILD ABHA is allowed to update their profile only once                                                                 | `m1_patch_v3_profile_account`              |
| `ABDM-1204` | 422  | UIDAI Error code : 400 : Invalid Aadhaar OTP value.                                                                             | `m1_post_v3_enrollment_enrol_byaadhaar`    |
| `ABDM-1207` | 422  | The information you provided does not match the details on record with Aadhaar. Please verify and provide accurate information. | `m1_post_v3_enrollment_enrol_byaadhaar`    |
| `ABDM-1211` | 400  | User not found.                                                                                                                 | `m1_post_v3_phr_web_login_abha_search`     |

## P1 Registration and login

| Code        | HTTP | Message                        | Returned by                                 |
| ----------- | ---- | ------------------------------ | ------------------------------------------- |
| `900902`    | 401  | Missing Credentials            | `p1_get_v3_phr_app_enrollment_isexists`     |
| `ABDM-1107` | 400  | Invalid combinations of scopes | `p1_post_v3_phr_app_login_verify`           |
| `ABDM-1211` | 400  | User not found.                | `p1_post_v3_phr_app_login_search`           |
| `ABDM-9999` | 400  | Invalid LoginId                | `p1_post_v3_phr_app_enrollment_request_otp` |

## P2 Management

| Code        | HTTP | Message             | Returned by                                    |
| ----------- | ---- | ------------------- | ---------------------------------------------- |
| `900902`    | 401  | Missing Credentials | `p2_get_v3_phr_app_login_profile`              |
| `ABDM-9999` | 400  | Invalid LoginId     | `p2_post_v3_phr_app_login_profile_request_otp` |

20 codes are recorded. A code you meet that is not here is one the specifications do not carry yet.
