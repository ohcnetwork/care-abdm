# Gateway session errors

Seeing a symptom rather than a code? Start at [Troubleshooting](/docs/hiecm/v3/troubleshooting/).

## Codes

Code, message and error name are as published. The action column reads the message text by a documented rule, and says Unclassified where the rule could not classify one.

| Code        | Message                                                                                                                 | What to do     |
| ----------- | ----------------------------------------------------------------------------------------------------------------------- | -------------- |
| `ABDM-1053` | Problem occurred while loading overlay image                                                                            | Unclassified   |
| `ABDM-1068` | Both Patient and Error details cannot be null                                                                           | Fix request    |
| `ABDM-1069` | Invalid Authentication type                                                                                             | Fix request    |
| `ABDM-1073` | if is applicable for all HIP's is true;then HIP object must be null                                                     | Unclassified   |
| `ABDM-1076` | One or more invalid HIP is exist in the request                                                                         | Fix request    |
| `ABDM-1088` | Captcha verification failed, Please enter valid code.                                                                   | Unclassified   |
| `ABDM-1089` | Payment information cannot be null                                                                                      | Fix request    |
| `ABDM-1096` | Duplicate Gateway Consent Manager request                                                                               | Cannot proceed |
| `ABDM-1097` | Duplicate Gateway Consent Manager patch request                                                                         | Cannot proceed |
| `ABDM-1098` | Duplicate Gateway Government Program request                                                                            | Fix request    |
| `ABDM-1123` | User authentication failed                                                                                              | Unclassified   |
| `ABDM-1125` | ABHA number and ABHA address cannot be null                                                                             | Fix request    |
| `ABDM-1128` | T-Token Expired                                                                                                         | Fix request    |
| `ABDM-1129` | Invalid T-Token                                                                                                         | Fix request    |
| `ABDM-1130` | Invalid X-Token                                                                                                         | Fix request    |
| `ABDM-1131` | X-Token Expired                                                                                                         | Fix request    |
| `ABDM-1208` | Abha Profile Gateway is unavailable                                                                                     | Retry          |
| `ABDM-1209` | PHR DB service unavailable                                                                                              | Retry          |
| `ABDM-1210` | Login via Email Address OTP is not allowed                                                                              | Fix request    |
| `ABDM-1212` | Email address not found.                                                                                                | Fix request    |
| `ABDM-1213` | User not active.                                                                                                        | Unclassified   |
| `ABDM-1214` | Mobile/Email verification is pending.                                                                                   | Unclassified   |
| `ABDM-1215` | Login via Mobile Number OTP is not allowed                                                                              | Fix request    |
| `ABDM-1216` | The ABHA Address is deactivated.                                                                                        | Cannot proceed |
| `ABDM-1217` | Login is not allowed                                                                                                    | Fix request    |
| `ABDM-1221` | Face verification has been failed, please try again.                                                                    | Retry          |
| `ABDM-1222` | Fingerprint verification has been failed, please try again.                                                             | Retry          |
| `ABDM-1223` | IRIS verification has been failed, please try again.                                                                    | Retry          |
| `ABDM-1300` | Provided emailId doesn't match with existing emailId                                                                    | Unclassified   |
| `ABDM-1301` | The mobile number you have entered has already been verified. Please provide an alternate mobile number.                | Fix request    |
| `ABDM-1302` | The emailId you have entered has already been verified. Please provide an alternate emailId.                            | Fix request    |
| `ABDM-1303` | Your mobile number is not linked to the ABHA number. Please update your mobile number in ABHA or try using Aadhaar OTP. | Unclassified   |
| `ABDM-1304` | Mobile number is not linked to your ABHA address. Please update your mobile number in ABHA.                             | Unclassified   |
| `ABDM-1305` | Mobile number is missing for this ABHA address. Please update your mobile number.                                       | Fix request    |
| `ABDM-1308` | This account is deactivated. Please reactivate it from ABHA portal.                                                     | Cannot proceed |
| `ABDM-1506` | Invalid callback resp id                                                                                                | Fix request    |
| `ABDM-1919` | Invalid Refresh token                                                                                                   | Fix request    |
| `ABDM-1920` | Invalid grant type                                                                                                      | Fix request    |
| `ABDM-1921` | Invalid client id                                                                                                       | Fix request    |
| `ABDM-1922` | Invalid client secret                                                                                                   | Fix request    |
| `ABDM-1923` | Invalid client id and secret                                                                                            | Fix request    |
| `ABDM-1931` | Service-Id= (.\*?) is already exists                                                                                    | Fix request    |
| `ABDM-1932` | HFR request failed, rollback successful for hfr-id= (\S+)\s\*                                                           | Unclassified   |
| `ABDM-1933` | Bridge registry request is invalid                                                                                      | Fix request    |
| `ABDM-1935` | All the provided service IDs do not match with the client ID                                                            | Unclassified   |
| `ABDM-9008` | No CR Mapped with Abha Address                                                                                          | Unclassified   |

Every code above is recorded in the specification that owns it. The aggregated list across modules is at [error codes](/docs/hiecm/v3/reference/error-codes).

[Next Still stuck? Ask for help Where to file what you hit, so the answer lands back in these pages.](/docs/support)
