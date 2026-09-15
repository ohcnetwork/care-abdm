# M1 ABHA identity errors

Seeing a symptom rather than a code? Start at [Troubleshooting](/docs/hiecm/v3/troubleshooting/).

## Four error shapes, not one

Do not write a parser that expects a single shape.

### Shape 1: the wrapped ABDM error

```json
{    "error": {        "code": "ABDM-1204",        "message": "UIDAI Error code : 300 : Biometric data did not match."    }}
```

The code lives at `error.code`. This comes from the ABHA service's own business logic.

### Shape 2: the flat ABDM error

```json
{    "code": "ABDM-1094",    "message": "Access to this feature is restricted. Please contact NHA to enable it.",    "timestamp": "2024-10-25 15:02:34"}
```

Same family of codes, no `error` wrapper, plus a `timestamp`. The collection shows `ABDM-1094` in both shapes on different calls, so the wrapper is not tied to the code. Read `error.code` first and fall back to a top level `code`.

### Shape 3: field validation

```json
{    "txnId": "Invalid Transaction Id",    "timestamp": "2025-01-15 13:21:16"}
```

No code at all. The key names the field you got wrong. Several bad fields produce several keys:

```json
{    "scope": "Invalid Scope",    "authData": "Invalid Auth Data",    "timestamp": "2025-01-15 13:39:03"}
```

Treat every key except `timestamp` as a field name. These always arrive as HTTP 400.

Two of these read almost the same and mean opposite halves of the same step.

| Body                                | What failed                                           | What to change                                                                         |
| ----------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `{"loginId": "Invalid LoginId"}`    | The service could not decrypt the value               | The key or the padding. Observed with the wrong padding on 2026-09-09                  |
| `{"loginId": "LoginId is invalid"}` | It decrypted, then the plaintext failed a format rule | The plaintext shape. Observed with an ABHA number sent as 14 bare digits on 2026-09-11 |

The second is the one that costs an afternoon, because the value really was encrypted and really was the right number. An ABHA number keeps its dashes, `NN-NNNN-NNNN-NNNN`. The plaintext shape for every encrypted field is in [encryption](/docs/hiecm/v3/concepts/encryption).

### Shape 4: the API gateway error

```json
{    "code": "900901",    "message": "Invalid Credentials",    "description": "Invalid JWT token. Make sure you have provided the correct security credentials"}
```

A numeric code, not an `ABDM-` code, plus a `description` field the other shapes lack. This comes from the API gateway in front of the ABHA service, before your request reaches the business logic. It almost always means the `Authorization` header is wrong or expired.

## Codes

Code, message and error name are as published. The action column reads the message text by a documented rule, and says Unclassified where the rule could not classify one.

| Code        | Message                                                                                                                                                                                 | What to do       |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `ABDM-1001` | Subscription source update returned empty                                                                                                                                               | Unclassified     |
| `ABDM-1002` | Invalid frequency unit, it must be in HOUR, WEEK, DAY, MONTH, YEAR                                                                                                                      | Fix request      |
| `ABDM-1006` | Invalid HIType, it must be in Prescription,DiagnosticReport,OPConsultation,DischargeSummary,ImmunizationRecord,HealthDocumentRecord,WellnessRecord,Invoice                              | Fix request      |
| `ABDM-1008` | SMS service currently disabled                                                                                                                                                          | Unclassified     |
| `ABDM-1009` | Email service currently disabled                                                                                                                                                        | Unclassified     |
| `ABDM-1010` | No pending care context found for this abha address                                                                                                                                     | Unclassified     |
| `ABDM-1013` | Invalid ABHA Number                                                                                                                                                                     | Fix request      |
| `ABDM-1016` | Invalid Timestamp                                                                                                                                                                       | Fix request      |
| `ABDM-1017` | Invalid Transaction Id                                                                                                                                                                  | Fix request      |
| `ABDM-1019` | Dependent Service Unavailable                                                                                                                                                           | Retry            |
| `ABDM-1021` | Lack of required priviledges                                                                                                                                                            | Fix request      |
| `ABDM-1022` | Too many requests                                                                                                                                                                       | Retry            |
| `ABDM-1029` | Redis server is unavailable                                                                                                                                                             | Retry            |
| `ABDM-1030` | Request id not found                                                                                                                                                                    | Fix request      |
| `ABDM-1034` | Notification service unavailable                                                                                                                                                        | Retry            |
| `ABDM-1045` | Database Access is restricted                                                                                                                                                           | Unclassified     |
| `ABDM-1047` | Purpose does not exist                                                                                                                                                                  | Fix request      |
| `ABDM-1048` | Timeout                                                                                                                                                                                 | Retry            |
| `ABDM-1065` | Health facility does not exist                                                                                                                                                          | Fix request      |
| `ABDM-1066` | Please enter a valid Password                                                                                                                                                           | Unclassified     |
| `ABDM-1094` | Access to this feature is restricted. Please contact NHA to enable it.                                                                                                                  | Fix auth         |
| `ABDM-1094` | Invalid Benefit Name                                                                                                                                                                    | Fix auth         |
| `ABDM-1100` | You have requested multiple OTPs Or Exceeded maximum number of attempts for OTP match in this transaction. Please try again in 30 minutes.                                              | Retry            |
| `ABDM-1101` | This ABHA Address already exists. Please create with unique ABHA address                                                                                                                | Fix request      |
| `ABDM-1102` | Mobile number verification is pending.                                                                                                                                                  | Unclassified     |
| `ABDM-1103` | Cannot link with CHILD ABHA Number                                                                                                                                                      | Unclassified     |
| `ABDM-1104` | Cannot link with same ABHA Number                                                                                                                                                       | Unclassified     |
| `ABDM-1105` | Invalid request for parent linking                                                                                                                                                      | Fix request      |
| `ABDM-1107` | Invalid combinations of scopes                                                                                                                                                          | Fix request      |
| `ABDM-1108` | Notification DB service unavailable                                                                                                                                                     | Retry            |
| `ABDM-1109` | Invalid On discovery response                                                                                                                                                           | Fix request      |
| `ABDM-1110` | Your new password must be different from your old password. Please enter a unique new password.                                                                                         | Unclassified     |
| `ABDM-1111` | Invalid old password, please try with valid password.                                                                                                                                   | Fix request      |
| `ABDM-1112` | The provided gender does not match the gender in DigiLocker records                                                                                                                     | Unclassified     |
| `ABDM-1113` | Duplicate health information provider data flow response data flow resoponse                                                                                                            | Fix request      |
| `ABDM-1114` | The provided name does not match the name in DigiLocker records                                                                                                                         | Unclassified     |
| `ABDM-1115` | Invalid patient information. At least one patient information is required.                                                                                                              | Fix request      |
| `ABDM-1116` | generate\_and\_save\_link\_token : 'NoneType' object has no attribute 'get'                                                                                                             | Unclassified     |
| `ABDM-1117` | Auto approval id is already active                                                                                                                                                      | Fix request      |
| `ABDM-1118` | Login via ABHA Number OTP is not allowed                                                                                                                                                | Fix request      |
| `ABDM-1119` | Login via Aadhaar OTP is not allowed                                                                                                                                                    | Fix request      |
| `ABDM-1121` | Invalid Enrolment Number                                                                                                                                                                | Fix request      |
| `ABDM-1122` | Request can not be processed                                                                                                                                                            | Unclassified     |
| `ABDM-1124` | The mobile number provided by you is already linked to 6 ABHA Numbers. Please provide a different Mobile Number.                                                                        | Fix request      |
| `ABDM-1126` | F-Token Expired                                                                                                                                                                         | Fix request      |
| `ABDM-1127` | Invalid F-Token                                                                                                                                                                         | Fix request      |
| `ABDM-1132` | Kindly enter valid linked ABHA Address                                                                                                                                                  | Unclassified     |
| `ABDM-1133` | Please enter a valid captcha result. Entered captcha result is incorrect.                                                                                                               | Fix request      |
| `ABDM-1134` | Deactivated ABHA Account                                                                                                                                                                | Cannot proceed   |
| `ABDM-1135` | The email address provided by you is already linked to 6 ABHA Numbers. Please provide a different email Id.                                                                             | Fix request      |
| `ABDM-1136` | message should not be null or empty.                                                                                                                                                    | Unclassified     |
| `ABDM-1137` | Benefit Name Not Found                                                                                                                                                                  | Fix request      |
| `ABDM-1138` | The benefit record has already been de-linked                                                                                                                                           | Treat as success |
| `ABDM-1139` | Benefit record not found                                                                                                                                                                | Fix request      |
| `ABDM-1140` | The benefit record has already been linked                                                                                                                                              | Treat as success |
| `ABDM-1141` | An existing ABHA number created using this Aadhaar number has been found. It is advisable to delete this account and use ABHA number ((\[0-9]{2}(?:-\[0-9]{4}){3})) for future purpose. | Unclassified     |
| `ABDM-1142` | Please enter a valid captcha. Entered captcha is expired.                                                                                                                               | Fix request      |
| `ABDM-1143` | Captcha limit exceeded.                                                                                                                                                                 | Unclassified     |
| `ABDM-1144` | Incorrect facility ID or password.                                                                                                                                                      | Fix request      |
| `ABDM-1155` | Parents must be 18 years of age or older to create a Child ABHA Account                                                                                                                 | Unclassified     |
| `ABDM-1156` | Please ensure that the mobile number is mapped to the parent's ABHA number                                                                                                              | Unclassified     |
| `ABDM-1157` | Child ABHA’s account limit has been exceeded for the requested Abha ID number ‘(.\*?)                                                                                                   | Unclassified     |
| `ABDM-1158` | Invalid X-Token                                                                                                                                                                         | Fix request      |
| `ABDM-1159` | Children’s ages should be below '(.\*?)' years as of the current date                                                                                                                   | Unclassified     |
| `ABDM-1160` | Non KYC CHILD ABHA is allowed to update their profile only once                                                                                                                         | Unclassified     |
| `ABDM-1200` | LGD Gateway is unavailable                                                                                                                                                              | Retry            |
| `ABDM-1201` | IDP Gateway is unavailable                                                                                                                                                              | Retry            |
| `ABDM-1202` | Document Gateway is unavailable                                                                                                                                                         | Retry            |
| `ABDM-1203` | TEST                                                                                                                                                                                    | Unclassified     |
| `ABDM-1204` | A UIDAI failure passed through. The UIDAI code and text sit inside the message string                                                                                                   | Fix request      |
| `ABDM-1205` | Document DB Gateway is unavailable                                                                                                                                                      | Retry            |
| `ABDM-1206` | Aadhaar Gateway is unavailable                                                                                                                                                          | Retry            |
| `ABDM-1207` | The information you provided does not match the details on record with Aadhaar. Please verify and provide accurate information.                                                         | Fix request      |
| `ABDM-1211` | Email Sending Limit Exceeded                                                                                                                                                            | Unclassified     |
| `ABDM-1218` | Role for the user does not exist.                                                                                                                                                       | Fix request      |
| `ABDM-1219` | Your ABHA is linked with govt benefit programme, so it can not be deleted- ABDM, National Health Authority.                                                                             | Unclassified     |
| `ABDM-1220` | Sorry, Unable to process your request at this time. Please try again later.                                                                                                             | Retry            |
| `ABDM-1224` | Login via Biometric is not allowed.                                                                                                                                                     | Fix auth         |
| `ABDM-1226` | Vault service unavailable                                                                                                                                                               | Retry            |
| `ABDM-1227` | This client ID has reached the maximum limit of 100 ABHA account creations.                                                                                                             | Unclassified     |
| `ABDM-1228` | Your ABHA is linked with govt benefit programme, so it can not be deactivated- ABDM, National Health Authority.                                                                         | Cannot proceed   |
| `ABDM-9999` | Recorded as `ABDM-9999: `with an `ABDM-1094` message stuck to the front of the text                                                                                                     | Fix auth         |

## Untagged codes

The same collection, and the only source that recorded HTTP statuses.

| Code     | HTTP | Message                                                                                                                                   | What to do  |
| -------- | ---- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `900901` | 401  | Invalid Credentials, invalid JWT token. From the API gateway in front of the ABHA service, before your request reaches the business logic | Fix auth    |
| `900900` | 500  | Unclassified authentication failure. The one saved example had a bad path and a bad token together, so read it as a client error first    | Fix auth    |
| `404`    | 404  | No matching resource found for given API Request\`. A wrong path, not a missing record                                                    | Fix request |

## UIDAI codes

Codes from the Unique Identification Authority of India, passed through inside the message of ABDM-1204. More codes pass through than are listed here, so parse the message.

| Code  | Message                | What to do |
| ----- | ---------------------- | ---------- |
| `300` | Biometric mismatch     |            |
| `561` | Request expired        |            |
| `563` | Duplicate request      |            |
| `810` | Missing biometric data |            |

Every code above is recorded in the specification that owns it. The aggregated list across modules is at [error codes](/docs/hiecm/v3/reference/error-codes).

[Next Still stuck? Ask for help Where to file what you hit, so the answer lands back in these pages.](/docs/support)
