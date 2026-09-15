# M4 HPR and HFR errors

Seeing a symptom rather than a code? Start at [Troubleshooting](/docs/hiecm/v3/troubleshooting/).

## Codes

The ranges below, with examples. The full list is in the sandbox documentation for the healthcare professional registry. Code, message and error name are as published. The action column reads the message text by a documented rule, and says Unclassified where the rule could not classify one.

| Code       | Message                                                                 | What to do     |
| ---------- | ----------------------------------------------------------------------- | -------------- |
| `HIS-400`  | Request is invalid. Please enter the correct data.                      | Fix request    |
| `HIS-401`  | User is not authorized.                                                 | Cannot proceed |
| `HIS-403`  | Forbidden.                                                              | Cannot proceed |
| `HIS-422`  | Unable to process the current request due to wrong data.                | Unclassified   |
| `HIS-500`  | An unexpected error has occurred. Please try again in some time {0}{1}. | Retry          |
| `HIS-503`  | Requested service is unavailable.                                       | Retry          |
| `HIS-504`  | Database exception occurred while processing request.                   | Unclassified   |
| `HIS-1001` | Doctor info not found for healthProfessionalId: (.\*)                   | Fix request    |
| `HIS-1002` | The field value should not be empty.                                    | Unclassified   |
| `HIS-1003` | Invalid pattern found.                                                  | Fix request    |
| `HIS-1004` | Type mismatched. Please send the correct type.                          | Fix request    |
| `HIS-1005` | Please try logging in with the correct details.                         | Unclassified   |
| `HIS-1006` | Authentication is not initiated with provided method.                   | Unclassified   |
| `HIS-1007` | The user is disabled.                                                   | Unclassified   |
| `HIS-1008` | Invalid HPID/USERID.                                                    | Fix request    |
| `HIS-1009` | Error while connecting to UIDAI service.                                | Unclassified   |
| `HIS-1010` | Password must follow required format.                                   | Fix request    |
| `HIS-1011` | Please enter valid mobile number.                                       | Unclassified   |
| `HIS-1012` | Please enter valid Aadhaar number.                                      | Unclassified   |
| `HIS-1013` | Incorrect OTP entered.                                                  | Fix request    |
| `HIS-1014` | Field contains only alphabets.                                          | Unclassified   |
| `HIS-1015` | HPID already exists.                                                    | Fix request    |
| `HIS-1016` | HPID not available.                                                     | Unclassified   |
| `HIS-1018` | HPID creation allowed only for specific regions.                        | Unclassified   |
| `HIS-1019` | HP Facility ID not available.                                           | Unclassified   |
| `HIS-1020` | Facility already registered with HPID.                                  | Fix request    |
| `HIS-1021` | Current and new password cannot be same.                                | Unclassified   |
| `HIS-1022` | Please verify captcha.                                                  | Unclassified   |
| `HIS-1023` | Please wait before sending another OTP.                                 | Unclassified   |
| `HIS-1024` | Invalid state.                                                          | Fix request    |
| `HIS-1025` | Invalid district.                                                       | Fix request    |
| `HIS-1026` | Transaction not found.                                                  | Fix request    |
| `HIS-1027` | Benefit not integrated.                                                 | Unclassified   |
| `HIS-1028` | Aadhaar required for KYC.                                               | Fix request    |
| `HIS-1029` | HPID already linked with Aadhaar.                                       | Fix request    |
| `HIS-1030` | Name mismatch with Aadhaar records.                                     | Fix request    |
| `HIS-1031` | Password not set for HPID.                                              | Unclassified   |
| `HIS-1032` | Integrated program not found.                                           | Fix request    |
| `HIS-1033` | Authentication failed.                                                  | Unclassified   |
| `HIS-1034` | Invalid date format.                                                    | Fix request    |
| `HIS-1035` | Invalid Healthcare Professional ID.                                     | Fix request    |
| `HIS-1036` | ID type and domain not configured.                                      | Unclassified   |
| `HIS-1039` | Max login attempts exceeded.                                            | Unclassified   |
| `HIS-1040` | File size exceeds limit.                                                | Unclassified   |
| `HIS-1041` | Max OTP attempts reached.                                               | Unclassified   |
| `HIS-1042` | Invalid OIDC transition.                                                | Fix request    |
| `HIS-1043` | Redirect URL mismatch.                                                  | Fix request    |
| `HIS-1044` | Access code expired.                                                    | Fix request    |
| `HIS-1045` | Mobile update failed.                                                   | Unclassified   |
| `HIS-1046` | Same mobile number not allowed.                                         | Fix request    |
| `HIS-1047` | Input must be encrypted.                                                | Unclassified   |
| `HIS-1048` | Unable to fetch document details.                                       | Unclassified   |
| `HIS-1054` | Invalid document type.                                                  | Fix request    |
| `HIS-1055` | Invalid gender code.                                                    | Fix request    |
| `HIS-1056` | HPID not created via driving licence.                                   | Unclassified   |
| `HIS-1057` | Document details not available.                                         | Unclassified   |
| `HIS-1059` | Invalid data provided.                                                  | Fix request    |
| `HIS-1060` | OTP expired or invalid.                                                 | Fix request    |
| `HIS-1061` | Invalid category ID.                                                    | Fix request    |
| `HIS-1062` | Invalid sub category ID.                                                | Fix request    |
| `HIS-1063` | Invalid image uploaded.                                                 | Fix request    |
| `HIS-1064` | Invalid image size.                                                     | Fix request    |
| `HIS-1065` | Consent required.                                                       | Cannot proceed |
| `HIS-1066` | Incorrect captcha.                                                      | Fix request    |
| `HIS-1067` | Invalid credentials.                                                    | Fix request    |
| `HIS-1068` | Mobile verification required.                                           | Fix request    |
| `HIS-1069` | No HPID found for Aadhaar.                                              | Unclassified   |
| `HIS-1070` | Required field is empty.                                                | Fix request    |
| `HIS-1071` | Old password does not match.                                            | Unclassified   |
| `HIS-1072` | Mobile number not registered.                                           | Cannot proceed |
| `HIS-1073` | New password cannot be same as old password.                            | Unclassified   |
| `HIS-1100` | Invalid Bridge ID.                                                      | Fix request    |
| `HIS-1101` | Bridge ID already registered.                                           | Fix request    |
| `HIS-1102` | Self transfer not allowed.                                              | Fix request    |
| `HIS-1103` | Facility transfer request already initiated.                            | Fix request    |
| `HIS-1104` | Linked program already in use.                                          | Fix request    |
| `HIS-1105` | Operation not allowed.                                                  | Fix request    |
| `HIS-1106` | Required fields missing.                                                | Fix request    |
| `HIS-1107` | Reassign to same manager not allowed.                                   | Fix request    |
| `HIS-1108` | Invalid attempt.                                                        | Fix request    |
| `HIS-1109` | Professional type mismatch.                                             | Fix request    |
| `HIS-1110` | Not a Central Government facility.                                      | Unclassified   |
| `HIS-1111` | Not a State facility.                                                   | Unclassified   |
| `HIS-1112` | Not a Government facility.                                              | Unclassified   |
| `HIS-1113` | Invalid facility ID format.                                             | Fix request    |
| `HIS-1114` | Invalid pin code.                                                       | Fix request    |
| `HIS-1115` | Invalid ownership code.                                                 | Fix request    |
| `HIS-1116` | HPR ID required.                                                        | Fix request    |
| `HIS-1117` | Transaction ID required.                                                | Fix request    |
| `HIS-1118` | Invalid password format.                                                | Fix request    |
| `HIS-1119` | Invalid token.                                                          | Fix request    |
| `HIS-1120` | Invalid facility ID or name.                                            | Fix request    |
| `HIS-1121` | Invalid facility details.                                               | Fix request    |
| `HIS-1122` | User not government type.                                               | Unclassified   |
| `HIS-1123` | Request body missing fields.                                            | Fix request    |
| `HIS-1124` | Bridge not linked.                                                      | Unclassified   |
| `HIS-1125` | Invalid HIP name.                                                       | Fix request    |
| `HIS-1126` | Invalid Bridge ID.                                                      | Fix request    |
| `HIS-1127` | Invalid HIP ID.                                                         | Fix request    |
| `HIS-1128` | HIP name already exists.                                                | Fix request    |
| `HIS-1129` | Invalid HIP name format.                                                | Fix request    |
| `HIS-1130` | Bridge request failed.                                                  | Unclassified   |
| `HIS-1131` | Geolocation limit exceeded.                                             | Unclassified   |
| `HIS-1132` | Duplicate facility detected.                                            | Fix request    |
| `HIS-1148` | Not a government facility.                                              | Unclassified   |
| `HIS-1149` | Not a private facility.                                                 | Unclassified   |
| `HIS-1150` | Invalid private facility.                                               | Fix request    |
| `HIS-1151` | Facility ministry mismatch.                                             | Fix request    |
| `HIS-1152` | Mobile number not found.                                                | Fix request    |
| `HIS-1153` | PSU mismatch.                                                           | Fix request    |
| `HIS-2001` | Invalid Aadhaar number.                                                 | Fix request    |
| `HIS-2004` | OTP system error.                                                       | Unclassified   |
| `HIS-2022` | Invalid OTP.                                                            | Fix request    |
| `HIS-2031` | Request expired.                                                        | Fix request    |
| `HIS-2045` | Session expired.                                                        | Fix request    |
| `HIS-2055` | Invalid gender.                                                         | Fix request    |
| `HIS-2057` | Invalid category.                                                       | Fix request    |
| `HIS-2062` | Invalid medical council.                                                | Fix request    |
| `HIS-2075` | Invalid reason of not working.                                          | Fix request    |
| `HIS-2076` | Invalid work status.                                                    | Fix request    |
| `HIS-2081` | Invalid boolean value.                                                  | Fix request    |
| `HIS-2082` | Invalid reason of not working.                                          | Fix request    |
| `HIS-2083` | Invalid ministry.                                                       | Fix request    |
| `HIS-2084` | Invalid category.                                                       | Fix request    |
| `HIS-2085` | Validation / verification failure.                                      | Unclassified   |
| `HIS-2094` | Work status not required.                                               | Fix request    |
| `HIS-2095` | Facility declaration not required.                                      | Fix request    |
| `HIS-2096` | Select State Govt facility.                                             | Unclassified   |
| `HIS-2097` | Select Central Govt facility.                                           | Unclassified   |
| `HIS-3001` | Resident data not available.                                            | Unclassified   |
| `HIS-3006` | Document mismatch.                                                      | Fix request    |
| `HIS-3015` | Server timeout.                                                         | Retry          |
| `HIS-3021` | HPRID already exists.                                                   | Fix request    |
| `HIS-3031` | Invalid token.                                                          | Fix request    |
| `HIS-4003` | Facility already exists.                                                | Fix request    |
| `HIS-4015` | Invalid ownership subtype.                                              | Fix request    |
| `HIS-4020` | Invalid longitude.                                                      | Fix request    |
| `HIS-4032` | Invalid state code.                                                     | Fix request    |
| `HIS-4044` | Invalid page number.                                                    | Fix request    |
| `HIS-4055` | Invalid image format.                                                   | Fix request    |
| `HIS-4061` | Facility status change not allowed.                                     | Fix request    |
| `HIS-5001` | Workflow not defined.                                                   | Unclassified   |
| `HIS-5002` | Qualification missing.                                                  | Fix request    |
| `HIS-5005` | Already registered.                                                     | Fix request    |
| `HIS-5006` | Invalid practitioner DTO.                                               | Fix request    |
| `HIS-5007` | Invalid personal DTO.                                                   | Fix request    |
| `HIS-5008` | Invalid academic DTO.                                                   | Fix request    |
| `HIS-5009` | Invalid registration DTO.                                               | Fix request    |
| `HIS-5010` | Invalid work DTO.                                                       | Fix request    |
| `HIS-5011` | Token expired.                                                          | Fix request    |

## Code ranges

| Range                | What it covers                              | Examples                                                                                                                                         |
| -------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `HIS-400 to HIS-504` | The HTTP level failures                     | HIS-401 user is not authorized, HIS-403 forbidden, HIS-503 requested service is unavailable                                                      |
| `HIS-1xxx`           | Validation and facility errors, 103 of them | HIS-1002 the field value should not be empty, HIS-1124 bridge not linked, HIS-1128 HIP name already exists, HIS-1132 duplicate facility detected |
| `HIS-2xxx`           | Aadhaar, OTP and session errors             | HIS-2022 invalid OTP, HIS-2031 request expired, HIS-2045 session expired                                                                         |
| `HIS-3xxx`           | Aadhaar data and HPID state                 | HIS-3001 resident data not available, HIS-3021 HPRID already exists, HIS-3031 invalid token                                                      |
| `HIS-4xxx`           | Facility record errors                      | HIS-4003 facility already exists, HIS-4032 invalid state code, HIS-4055 invalid image format                                                     |
| `HIS-5xxx`           | Registration workflow errors                | HIS-5005 already registered, HIS-5011 token expired                                                                                              |

Every code above is recorded in the specification that owns it. The aggregated list across modules is at [error codes](/docs/hiecm/v3/reference/error-codes).

[Next Still stuck? Ask for help Where to file what you hit, so the answer lands back in these pages.](/docs/support)
