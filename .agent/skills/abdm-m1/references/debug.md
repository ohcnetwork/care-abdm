# HIE-CM m1 debug

Every error below is an OODA loop: observe the error code and last request id, orient against the matched code, decide the fix, act, and observe whether the original step now succeeds. Applying a fix is not the exit condition; the original step succeeding is.

Loop limit: 5 passes per error.

## Errors

### 900900

**Specification example:** HTTP 500, `Unclassified Authentication Failure`, on `m1_post_v3_enrollment_auth_byabdm`.

**Exit condition: the original call now succeeds.**

### 900901

**Specification example:** HTTP 401, `Invalid Credentials`, on `m1_post_v3_enrollment_request_otp`.

**Exit condition: the original call now succeeds.**

### 900902

**Specification example:** HTTP 401, `Missing Credentials`, on `m1_post_v3_profile_benefit_search`.

**Exit condition: the original call now succeeds.**

### ABDM-1017

**Specification example:** HTTP 400, `Invalid transaction, either the transaction is expired or not found`, on `m1_post_v3_enrollment_enrol_capturepid`.

**Exit condition: the original call now succeeds.**

### ABDM-1021

**Specification example:** HTTP 401, `Lack of required priviledges`, on `m1_post_v3_enrollment_enrol_byaadhaar`.

**Exit condition: the original call now succeeds.**

### ABDM-1094

**Specification example:** HTTP 401, `X-token expired`, on `m1_post_v3_enrollment_enrol_byaadhaar`.

**Exit condition: the original call now succeeds.**

### ABDM-1114

**Specification example:** HTTP 404, `No ABHA user registered with this Aadhaar number.`, on `m1_post_v3_profile_login_verify`.

**Exit condition: the original call now succeeds.**

### ABDM-1124

**Specification example:** HTTP 422, `The mobile number provided by you is already linked to 6 ABHA Numbers. Please provide a different Mobile Number.`, on `m1_post_v3_enrollment_enrol_byaadhaar`.

**Exit condition: the original call now succeeds.**

### ABDM-1138

**Specification example:** HTTP 400, `The benefit record has already been de-linked`, on `m1_post_v3_profile_benefit_linkanddelink`.

**Exit condition: the original call now succeeds.**

### ABDM-1157

**Specification example:** HTTP 422, `Child ABHA’s account limit has been exceeded for the requested Abha ID number ‘<ABHA_NUMBER>`, on `m1_post_v3_enrollment_enrol_byaadhaar`.

**Exit condition: the original call now succeeds.**

### ABDM-1160

**Specification example:** HTTP 422, `Non KYC CHILD ABHA is allowed to update their profile only once`, on `m1_patch_v3_profile_account`.

**Exit condition: the original call now succeeds.**

### ABDM-1204

**Specification example:** HTTP 422, `UIDAI Error code : 400 : Invalid Aadhaar OTP value.`, on `m1_post_v3_enrollment_enrol_byaadhaar`.

**Exit condition: the original call now succeeds.**

### ABDM-1207

**Specification example:** HTTP 422, `The information you provided does not match the details on record with Aadhaar. Please verify and provide accurate information.`, on `m1_post_v3_enrollment_enrol_byaadhaar`.

**Exit condition: the original call now succeeds.**

### ABDM-1211

**Specification example:** HTTP 400, `User not found.`, on `m1_post_v3_phr_web_login_abha_search`.

**Exit condition: the original call now succeeds.**

## Where the detail is

- The operation that returns each code: /docs/hiecm/v3/api/m1

## Every code in the specification

### Codes

| Code | HTTP | Message | Returned by |
| --- | --- | --- | --- |
| `900900` | 500 | Unclassified Authentication Failure | `m1_post_v3_enrollment_auth_byabdm` |
| `900901` | 401 | Invalid Credentials | `m1_post_v3_enrollment_request_otp` |
| `900902` | 401 | Missing Credentials | `m1_post_v3_profile_benefit_search` |
| `ABDM-1017` | 400 | Invalid transaction, either the transaction is expired or not found | `m1_post_v3_enrollment_enrol_capturepid` |
| `ABDM-1021` | 401 | Lack of required priviledges | `m1_post_v3_enrollment_enrol_byaadhaar` |
| `ABDM-1094` | 401 | X-token expired | `m1_post_v3_enrollment_enrol_byaadhaar` |
| `ABDM-1114` | 404 | No ABHA user registered with this Aadhaar number. | `m1_post_v3_profile_login_verify` |
| `ABDM-1124` | 422 | The mobile number provided by you is already linked to 6 ABHA Numbers. Please provide a different Mobile Numb… | `m1_post_v3_enrollment_enrol_byaadhaar` |
| `ABDM-1138` | 400 | The benefit record has already been de-linked | `m1_post_v3_profile_benefit_linkanddelink` |
| `ABDM-1157` | 422 | Child ABHA’s account limit has been exceeded for the requested Abha ID number ‘<ABHA_NUMBER> | `m1_post_v3_enrollment_enrol_byaadhaar` |
| `ABDM-1160` | 422 | Non KYC CHILD ABHA is allowed to update their profile only once | `m1_patch_v3_profile_account` |
| `ABDM-1204` | 422 | UIDAI Error code : 400 : Invalid Aadhaar OTP value. | `m1_post_v3_enrollment_enrol_byaadhaar` |
| `ABDM-1207` | 422 | The information you provided does not match the details on record with Aadhaar. Please verify and provide acc… | `m1_post_v3_enrollment_enrol_byaadhaar` |
| `ABDM-1211` | 400 | User not found. | `m1_post_v3_phr_web_login_abha_search` |

A code you meet that is not above is one the specifications do not carry yet. Read the code together with the message: a code can appear twice with different meanings.
