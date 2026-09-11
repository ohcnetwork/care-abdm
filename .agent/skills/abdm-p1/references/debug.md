# HIE-CM P1 debug

Diagnoses a failed PHR application call, anywhere in P1, P2 or P3. Every error below is an OODA loop: observe the error code and last request id, orient against the matched error atom below (list a second hypothesis if the match is not exact), decide the fix, act, and observe whether the *original* step now succeeds. Applying a fix is not the exit condition; the original step succeeding is.

Loop limit: 5 passes per error. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Errors

### AS-1013, no records were found for that health address (`hiecm.error.as-1013`)

**Observed as**

Discovery asked a facility for records held against this person and the
facility answered with none. That is an answer, not a fault.

**Fix**

Show the specified wording, "No health records found", rather than an
error. Offer the person a way to check the details they are searching
with, since a mismatch and a genuine absence look identical from here.

**Exit condition: the original call now succeeds**

Discovery against a facility the person did visit returns care contexts
rather than none.

### AS-1018, the transaction id is wrong or has expired (`hiecm.error.as-1018`)

**Observed as**

Registration and login run as a transaction. Each step carries the id
of the one before. That transaction has closed, which is why a step that
worked minutes ago fails now.

**Fix**

Start the flow again rather than retrying with the same id. Where this
happens often, the screen is holding people too long between steps.

**Exit condition: the original call now succeeds**

The flow restarted from its first step is accepted, and the later steps
carry the new transaction id.

### AS-1038, the OTP is wrong or has expired (`hiecm.error.as-1038`)

**Observed as**

Every route into a PHR account is checked by a code sent to a phone.
This is the code being refused. The message does not separate wrong from
expired, so your screen should not claim to know which it was.

**Fix**

Send a new code once the 60 second lock releases, and clear the field
first. Do not retry the same code: it is refused for the same reason a
second time.

**Exit condition: the original call now succeeds**

A freshly sent code is accepted and the person is signed in, or the
address is created.

### AS-1066, that care context is already linked (`hiecm.error.as-1066`)

**Observed as**

Discovery returned a care context that the person's account already
holds. Linking it again would create a duplicate, so it is refused.

**Fix**

Treat it as done rather than as a failure. Filter it out of the list and
show the specified message when everything discovered is already linked.

**Exit condition: the original call now succeeds**

The care context is present on the person's account, which was the
outcome the link was for.

### AS-1073, the consent artefact has expired (`hiecm.error.as-1073`)

**Observed as**

A consent artefact carries a validity period. It has passed. Records
cannot be fetched under an expired artefact, and no retry changes that.

**Fix**

Raise a fresh consent request. Do not retry against the old artefact,
and do not present the expiry to the person as an error in your
application.

**Exit condition: the original call now succeeds**

A fetch under a currently valid artefact is accepted and the records
arrive.

### AS-1109, that auto approval policy is already disabled (`hiecm.error.as-1109`)

**Observed as**

Auto approval is a policy the person can switch off at any time. This
one is already switched off, so the call had nothing to do.

**Fix**

Treat it as success and refresh the screen. The person asked for the
policy to be off, and it is off.

**Exit condition: the original call now succeeds**

Reading the policy shows it disabled, which is the state the call was
asking for.

## Where the detail is

- Every operation in this milestone, with its body fields and responses: /docs/hiecm/v3/api/p1
- The flows as diagrams: /docs/hiecm/v3/milestones/p1
- Every error code across milestones: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary

## Every recorded code

### Codes

Code and message are as published. The action column reads the message text by a documented rule. These codes are the PHR facing wording of the core ABDM codes, row for row.

| Code | Message | What to do |
| --- | --- | --- |
| `AS-1001` | Database connection failed. Please try again later. | Retry |
| `AS-1002` | No results found for the given input. | Fix request |
| `AS-1003` | There seems to be a data integrity issue. Please contact support team. | Unclassified |
| `AS-1004` | Email gateway is temporarily unavailable. | Retry |
| `AS-1005` | SMS gateway is temporarily unavailable. | Retry |
| `AS-1006` | The recipient information is invalid. Please check and try again. | Retry |
| `AS-1007` | Request could not be processed due to invalid data format. Please review and try again. | Retry |
| `AS-1008` | Timeout error: Unable to connect to the server. | Retry |
| `AS-1009` | SMS service is temporarily unavailable. | Retry |
| `AS-1010` | Email service is temporarily unavailable. | Retry |
| `AS-1011` | Validation failed. | Unclassified |
| `AS-1012` | Gateway database unavailable | Retry |
| `AS-1013` | No records found against the entered ABHA Address | Fix request |
| `AS-1014` | Please enter a valid ABHA number. | Fix request |
| `AS-1015` | Please enter a valid mobile number and email address . | Fix request |
| `AS-1016` | Invalid Response | Fix request |
| `AS-1017` | The timestamp format is incorrect. | Fix request |
| `AS-1018` | Transaction ID is incorrect or has expired. | Cannot proceed |
| `AS-1019` | Share Profile database unavailable | Retry |
| `AS-1020` | Dependent Service is unavailable. | Retry |
| `AS-1021` | Unknown database | Unclassified |
| `AS-1022` | Permission denied - required privileges are missing. | Cannot proceed |
| `AS-1023` | You have made too many requests. Please wait a moment and try again. | Retry |
| `AS-1024` | Please enter a valid and registered user ID. | Fix request |
| `AS-1025` | Dependent Service is unavailable. | Retry |
| `AS-1026` | The selected service is invalid. Please check and try again. | Retry |
| `AS-1027` | The entered Bridge ID does not exist. Please verify and try again. | Retry |
| `AS-1028` | Link token is incorrect or has expired. | Cannot proceed |
| `AS-1029` | Your account is currently blocked. Please try again after 24 hours. | Cannot proceed |
| `AS-1030` | The requested HIP service is currently not accessible. Please try again later. | Retry |
| `AS-1031` | Redis server is temporarily unavailable. | Retry |
| `AS-1032` | The request ID is invalid. Please check and try again. | Retry |
| `AS-1033` | Invalid request. Please check and try again. | Retry |
| `AS-1034` | The request header is invalid or missing required information. Please try again. | Retry |
| `AS-1035` | The requested HIU service is currently not accessible. Please try again later. | Retry |
| `AS-1036` | Notification service is temporarily unavailable | Retry |
| `AS-1037` | Please enter a valid and registered HIP Id. | Fix request |
| `AS-1038` | The entered OTP is incorrect or has expired. Please re-enter the correct OTP. | Cannot proceed |
| `AS-1039` | The entered information doesn’t match our records. Please verify and try again. | Retry |
| `AS-1040` | The number of care contexts does not match the expected count. Please verify the data. | Unclassified |
| `AS-1041` | ABHA address does not match the linked token. Please check and try again. | Retry |
| `AS-1042` | The consent request ID is invalid . Please verify and try again. | Cannot proceed |
| `AS-1043` | Please enter a valid and registered HIU Id. | Fix request |
| `AS-1044` | Please enter a valid and registered Locker Id. | Fix request |
| `AS-1045` | Acknowledgement is invalid or not properly formatted. Please try again. | Retry |
| `AS-1046` | Provider is Mandatory | Unclassified |
| `AS-1047` | Please enter a valid and registered provider Id. | Fix request |
| `AS-1048` | The ABHA address you entered doesn’t match the KYC details. Please verify and try again. | Retry |
| `AS-1049` | Failed to send the broadcast message. Please try again later. | Retry |
| `AS-1050` | You do not have permission to access the database. Please contact your administrator. | Unclassified |
| `AS-1051` | The selected purpose is invalid. Please verify and try again | Retry |
| `AS-1052` | The selected purpose is does not exist. Please verify and try again | Retry |
| `AS-1053` | Validation failed | Unclassified |
| `AS-1054` | Request timed out. Please try again. | Retry |
| `AS-1055` | The profile share intent keys are invalid. Please check and try again. | Retry |
| `AS-1056` | The profile share metadata keys are invalid. Please review the shared data. | Fix request |
| `AS-1057` | The ABHA number or ABHA address entered is invalid. Please check and try again. | Retry |
| `AS-1058` | There was an issue while encoding the content. Please try again. | Retry |
| `AS-1059` | The Transaction ID or response’s Request ID is invalid. Please verify and retry. | Fix request |
| `AS-1060` | Unable to load overlay image. Please refresh or try again later. | Retry |
| `AS-1061` | The entered data already exists in the system. | Fix request |
| `AS-1062` | We couldn’t convert the file to PNG format. Please try again or check the file type. | Retry |
| `AS-1063` | The subscription request ID is invalid. Please check and try again. | Retry |
| `AS-1064` | An error occurred while generating the QR code. Please retry after some time. | Unclassified |
| `AS-1065` | The HIP ID or PHR address is invalid. Please check and try again. | Retry |
| `AS-1066` | The selected care context is already associated with your ABHA address. | Fix request |
| `AS-1067` | The link reference number is invalid. Please check and try again. | Retry |
| `AS-1068` | The care context information provided is invalid. Please verify and retry. | Fix request |
| `AS-1069` | The health information types provided are invalid. | Fix request |
| `AS-1070` | The number of care contexts does not match the expected count. Please review the request. | Unclassified |
| `AS-1071` | The patient reference number is invalid. Please check and try again. | Retry |
| `AS-1072` | Patient display information is invalid or missing. | Fix request |
| `AS-1073` | The consent artefact has expired. Please generate a new one to proceed. | Cannot proceed |
| `AS-1074` | The ABHA number you entered doesn’t match the linked token. Please verify and try again. | Retry |
| `AS-1075` | The ABHA number you entered doesn’t match the linked token. Please verify and try again. | Retry |
| `AS-1076` | Consent has not been granted. | Cannot proceed |
| `AS-1077` | The ABHA number you entered doesn’t match the linked token. Please verify and try again. | Retry |
| `AS-1078` | The HIP Id doesn’t match the linked token. Please verify and try again. | Retry |
| `AS-1079` | The selected date range is invalid. | Fix request |
| `AS-1080` | The request could not be processed because the request body is missing. | Fix request |
| `AS-1081` | A request with this request ID already exists. | Fix request |
| `AS-1082` | Invalid X Auth token | Fix request |
| `AS-1083` | Health facility does not exist. Please check and try again. | Retry |
| `AS-1084` | JWT token is invalid | Fix request |
| `AS-1085` | Please enter a valid password. | Fix request |
| `AS-1086` | Request body is not required. | Fix request |
| `AS-1087` | Both patient details and error information are missing. Please provide at least one. | Fix request |
| `AS-1088` | The authentication type provided is invalid. Please check and try again. | Retry |
| `AS-1089` | A consent request with the same details already exists. | Cannot proceed |
| `AS-1090` | The login credentials provided are incorrect. Please try again. | Retry |
| `AS-1091` | At least one source must be included in the request. | Unclassified |
| `AS-1092` | This user is not part of your organisation. Access denied. | Cannot proceed |
| `AS-1093` | The consent PIN entered is invalid. Please check and try again. | Cannot proceed |
| `AS-1094` | At least one source must be included in the request. | Unclassified |
| `AS-1095` | User not found. Please verify and try again. | Retry |
| `AS-1096` | The provided consent PIN does not exist. | Cannot proceed |
| `AS-1097` | HIP object must be empty when consent is applicable to all HIPs. | Cannot proceed |
| `AS-1098` | Your user or manager profile is not e signed. | Unclassified |
| `AS-1099` | HIP object cannot be null in excluded sources | Unclassified |
| `AS-1100` | Organisation was not found | Fix request |
| `AS-1101` | Included sources must contain a valid HIP object. | Unclassified |
| `AS-1102` | User ID already exist | Fix request |
| `AS-1103` | One or more HIPs provided in the request are invalid. | Fix request |
| `AS-1104` | The registration number provided is incorrect. | Fix request |
| `AS-1105` | Auto approval policy id doesn't exist. | Unclassified |
| `AS-1106` | The uploaded file format is not supported. Please upload a valid format. | Fix request |
| `AS-1107` | The auto-approval ID provided is invalid. | Fix request |
| `AS-1108` | Document upload failed. Please try again. | Retry |
| `AS-1109` | This auto-approval ID has already been disabled. | Fix request |
| `AS-1110` | Failed to update user status. Please try again later. | Retry |
| `AS-1111` | This subscription request has already been processed. | Fix request |
| `AS-1112` | Upload your organisation ID card image to proceed. | Unclassified |
| `AS-1113` | The consent artefact ID is invalid. Please verify and try again. | Cannot proceed |
| `AS-1114` | Upload your organisation ID card image to proceed. | Unclassified |
| `AS-1115` | Subscription approval data is invalid in payload. Please check and try again. | Retry |
| `AS-1116` | Upload your organisation’s registration certificate to continue. | Unclassified |
| `AS-1117` | A care context exists without an associated HIP ID. Please correct the request. | Unclassified |
| `AS-1118` | Duplicate consent approve request | Cannot proceed |
| `AS-1119` | Upload an official authority letter from your organisation. | Unclassified |
| `AS-1120` | The subscription ID is invalid. Please check and try again. | Retry |
| `AS-1121` | The user is not associated with your organisation. Access denied. | Cannot proceed |
| `AS-1122` | ABHA number does not match the X Auth token. Please verify your session. | Unclassified |
| `AS-1123` | Aadhaar details do not match our records. Please review and select the correct information. | Fix request |
| `AS-1124` | Aadhaar details do not match our records. Please review and select the correct information. | Fix request |
| `AS-1125` | ABHA number does not match the X Auth token. Please verify your session. | Unclassified |
| `AS-1126` | User not found. Please verify and try again. | Retry |
| `AS-1127` | Patient profile does not match the X Auth token. Please verify your session. | Unclassified |
| `AS-1128` | No transaction found for the provided UUID. | Unclassified |
| `AS-1129` | A patient share request with the same details already exists. | Fix request |
| `AS-1130` | Sorry, your session is expired. Please login to continue. | Cannot proceed |
| `AS-1131` | Health information cannot be null | Fix request |
| `AS-1132` | Captcha verification failed. Please enter the correct code to continue. | Fix request |
| `AS-1133` | Payment information cannot be null | Fix request |
| `AS-1134` | Captcha expired or not loaded. Please reload and try again. | Cannot proceed |
| `AS-1135` | Duplicate HIP link request | Unclassified |
| `AS-1136` | You can export up to 500 records at a time. | Unclassified |
| `AS-1137` | A similar request to get links already exists. Please try again later. | Retry |
| `AS-1138` | The ABHA number must be 14 digits. Please correct it and try again. | Retry |
| `AS-1139` | Duplicate Link token request | Unclassified |
| `AS-1140` | A valid consent was not found for this request. | Cannot proceed |
| `AS-1141` | A bridge request with these details already exists. | Fix request |
| `AS-1142` | The transaction ID or consent artefact ID provided is invalid. Please verify and try again. | Cannot proceed |
| `AS-1143` | A bridge patch request for this transaction already exists. | Fix request |
| `AS-1144` | You are not authorized to update the status | Cannot proceed |
| `AS-1145` | A bridge service request with the same details already exists. | Fix request |
| `AS-1146` | Please enter a valid registered email address. | Fix request |
| `AS-1147` | Duplicate Gateway Consent Manager request | Cannot proceed |
| `AS-1148` | Duplicate Gateway Consent Manager patch request | Cannot proceed |
| `AS-1149` | Duplicate Gateway Government Program request | Unclassified |
| `AS-1150` | Duplicate Subscription request | Unclassified |
| `AS-1151` | Duplicate Subscription Approve request | Unclassified |
| `AS-1152` | You've reached the maximum number of OTP attempts or the OTP wasn’t generated. Please wait 30 minutes and try… | Retry |
| `AS-1153` | Duplicate Health Information request | Fix request |
| `AS-1154` | This ABHA Address already exists. Please create with unique ABHA address. | Fix request |
| `AS-1155` | Profile information cannot be empty | Fix request |
| `AS-1156` | Mobile number verification is pending. | Unclassified |
| `AS-1157` | Duplicate Discovery request | Unclassified |
| `AS-1158` | Linking with CHILD ABHA Number is not allowed. | Unclassified |
| `AS-1159` | Duplicate Init request | Unclassified |
| `AS-1160` | You cannot link with sameABHA Number.Please use a different ABHA Number. | Unclassified |
| `AS-1161` | Duplicate Confirm request | Unclassified |
| `AS-1162` | The request for linking a parent profile is invalid. Please check the details and try again. | Retry |
| `AS-1163` | Duplicate On discovery request | Unclassified |
| `AS-1164` | Duplicate On init request | Unclassified |
| `AS-1165` | The selected scopes combination are not valid together. | Unclassified |
| `AS-1166` | Duplicate On confirm request | Unclassified |
| `AS-1167` | Notification service is currently unavailable. Please try again later. | Retry |
| `AS-1168` | The On-Discovery response received is invalid. Please try again. | Retry |
| `AS-1169` | ABHA database is currently unavailable. Please try again later. | Retry |
| `AS-1170` | Invalid On init response | Fix request |
| `AS-1171` | Your new password must be different from your old password. Please enter a unique new password. | Fix request |
| `AS-1172` | Invalid On confirm response | Fix request |
| `AS-1173` | The old password entered is incorrect. Please try again with a valid password. | Retry |
| `AS-1174` | The consent artefact ID is either invalid or has expired. | Cannot proceed |
| `AS-1175` | Please ensure both old and new passwords are encrypted | Unclassified |
| `AS-1176` | Duplicate health information provider data flow response | Fix request |
| `AS-1177` | Please enter a valid Captcha | Fix request |
| `AS-1178` | Duplicate health information notification request | Fix request |
| `AS-1179` | User not found. Please verify and try again. | Retry |
| `AS-1180` | Patient information is invalid. Please provide at least one valid patient detail. | Fix request |
| `AS-1181` | Mobile number not found. | Fix request |
| `AS-1182` | The Auto approval request is invalid | Fix request |
| `AS-1183` | Aadhaar details not found in the system. | Fix request |
| `AS-1184` | This auto approval id is already active | Fix request |
| `AS-1185` | Login using password is not allowed. Please use other login methods. | Unclassified |
| `AS-1186` | Duplicate auto approval request | Unclassified |
| `AS-1187` | Login via ABHA Number OTP is not allowed. Please use other login methods. | Unclassified |
| `AS-1188` | Invalid subscription edit payload | Fix request |
| `AS-1189` | Login via Aadhaar OTP is not allowed. Please use other login methods. | Unclassified |
| `AS-1190` | No care context is available for this patient. | Unclassified |
| `AS-1191` | Missing or invalid request ID header. Please ensure a valid REQUEST_ID is provided. | Fix request |
| `AS-1192` | The enrolment number entered is invalid. Please verify and try again. | Retry |
| `AS-1193` | Your request could not be processed at the moment. Please try again later. | Retry |
| `AS-1194` | User authentication failed | Unclassified |
| `AS-1195` | The mobile number provided by you is already linked to 6 ABHA numbers. Please provide a different mobile numb… | Fix request |
| `AS-1196` | The mobile number provided by you is already linked to 6 ABHA numbers. Please provide a different mobile numb… | Fix request |
| `AS-1197` | Both ABHA number and ABHA address cannot be null | Unclassified |
| `AS-1198` | Sorry, your session is expired. Please login to continue. | Cannot proceed |
| `AS-1199` | Invalid F-Token | Fix request |
| `AS-1200` | Sorry, your session is expired. Please try again. | Cannot proceed |
| `AS-1201` | Invalid T-Token | Fix request |
| `AS-1202` | Invalid X-Token | Fix request |
| `AS-1203` | X-Token Expired | Cannot proceed |
| `AS-1204` | Kindly enter valid linked ABHA Address | Fix request |
| `AS-1205` | The captcha result entered is incorrect. Please try again with the correct value. | Retry |
| `AS-1206` | This ABHA account has been deactivated. | Cannot proceed |
| `AS-1207` | The email address provided by you is already linked to 6 ABHA Numbers. Please provide a different email addre… | Fix request |
| `AS-1208` | Message cannot be null or empty. | Unclassified |
| `AS-1209` | Benefit name not found. Please check the entered details. | Fix request |
| `AS-1210` | This benefit record has already been de-linked. | Fix request |
| `AS-1211` | No benefit record found for the given details. | Unclassified |
| `AS-1212` | The benefit record has already been linked | Fix request |
| `AS-1213` | This account already exist | Fix request |
| `AS-1214` | Captcha has expired. Please enter a new captcha. | Cannot proceed |
| `AS-1215` | Captcha attempts exceeded. | Unclassified |
| `AS-1216` | Captcha attempts exceeded. | Unclassified |
| `AS-1217` | This subscription is already enabled | Fix request |
| `AS-1218` | The facility ID or password is incorrect. Please check and try again. | Retry |
| `AS-1219` | This subscription is already disabled. | Fix request |
| `AS-1220` | Subscription is not in revoked state | Unclassified |
| `AS-1221` | Subscription is not in granted stat | Unclassified |
| `AS-1222` | This subscription ID does not belong to the patient. | Unclassified |
| `AS-1223` | The requested intent type is not supported at the HIP. | Unclassified |
| `AS-1224` | Bridge API version cannot be null | Unclassified |
| `AS-1225` | Health locker has already been set up for this user. | Fix request |
| `AS-1226` | No active subscription found for the selected health locker. | Unclassified |
| `AS-1227` | Unable to create auto-approval consent for the health locker. Please try again later. | Cannot proceed |
| `AS-1228` | Unable to save user health locker details. | Unclassified |
| `AS-1229` | Parents must be 18 years of age or older to create a Child ABHA Account | Unclassified |
| `AS-1230` | Please ensure that the mobile number is mapped to the parent’s ABHA number | Unclassified |
| `AS-1231` | Maximum number of Child ABHA accounts reached for the given ABHA number ‘%s’ | Unclassified |
| `AS-1232` | Invalid X-Token | Fix request |
| `AS-1233` | Children must be under '%s' years of age as of today to create a Child ABHA. | Unclassified |
| `AS-1234` | Non KYC CHILD ABHA is allowed to update their profile only once | Unclassified |
| `AS-1235` | The ABHA address entered is invalid. Please verify and try again. | Retry |
| `AS-1236` | LGD Gateway is currently unavailable. Please try again later. | Retry |
| `AS-1237` | IDP Gateway is currently unavailable. Please try again later. | Retry |
| `AS-1238` | Document Gateway is currently unavailable. Please try again later. | Retry |
| `AS-1239` | TEST | Unclassified |
| `AS-1240` | TEST | Unclassified |
| `AS-1241` | Document DB Gateway is currently unavailable. Please try again later. | Retry |
| `AS-1242` | Aadhaar Gateway is currently unavailable. Please try again later. | Retry |
| `AS-1243` | The information you provided does not match the details on record with Aadhaar. Please verify and provide acc… | Fix request |
| `AS-1244` | The information you provided does not match the details on record with Aadhaar. Please verify and provide acc… | Fix request |
| `AS-1245` | ABHA profile gateway is currently unavailable.Please try again later. | Retry |
| `AS-1246` | PHR DB service is currently unavailable. Please try again later. | Retry |
| `AS-1247` | Duplicate Notification request | Unclassified |
| `AS-1248` | Login via Email Address OTP is not allowed. Please use other login methods. | Unclassified |
| `AS-1249` | You have exceeded the email sending limit. Please wait before trying again. | Unclassified |
| `AS-1250` | User not found. Please verify and try again. | Retry |
| `AS-1251` | Email address not found. | Fix request |
| `AS-1252` | User not active. | Unclassified |
| `AS-1253` | Mobile/Email verification is pending. | Unclassified |
| `AS-1254` | Login via Mobile Number OTP is not allowed. Please use other login methods. | Unclassified |
| `AS-1255` | The ABHA Address is deactivated. | Cannot proceed |
| `AS-1256` | Login is not allowed | Unclassified |
| `AS-1257` | No role has been assigned to this user. | Unclassified |
| `AS-1258` | Notification templates not found | Fix request |
| `AS-1259` | Your ABHA is linked with govt benefit programme, so it can not be deleted- ABDM, National Health Authority. | Unclassified |
| `AS-1260` | Sorry, Unable to process your request at this time. Please try again later. | Retry |
| `AS-1261` | Face verification has been failed, please try again. | Retry |
| `AS-1262` | Fingerprint verification has been failed, please try again. | Retry |
| `AS-1263` | IRIS verification has been failed, please try again. | Retry |
| `AS-1264` | Biometric login is currently not allowed. Please use an alternate login method. | Unclassified |
| `AS-1265` | The email ID provided does not match the one registered. Please check and try again. | Retry |
| `AS-1266` | Mobile number is not linked to your ABHA address. Please update your mobile number in ABHA. | Unclassified |
| `AS-1267` | HIP is currently unavailable. Please try again later. | Retry |
| `AS-1268` | Your mobile number is not linked to the ABHA number. Please update your mobile number in ABHA or try to regis… | Unclassified |
| `AS-1269` | No acknowledgement was received from the HIP. Please try again later. | Retry |
| `AS-1270` | Invalid callback resp id | Fix request |
| `AS-1271` | Invalid Refresh token | Fix request |
| `AS-1272` | The grant type is invalid. Please check the request and try again. | Retry |
| `AS-1273` | The client ID is invalid. Please verify and try again. | Retry |
| `AS-1274` | The client secret is invalid. Please verify and try again. | Retry |
| `AS-1275` | Both client ID and secret are invalid. Please verify and try again. | Retry |
| `AS-1276` | Service ID ‘%s’ already exists. Please use a different service ID. | Fix request |
| `AS-1277` | HFR request failed, but rollback was successful for HFR ID ‘%s’. | Unclassified |
| `AS-1278` | The bridge registry request is invalid. Please verify and try again. | Retry |
| `AS-1279` | All the provided service IDs do not match with the client ID | Unclassified |
| `AS-1280` | HIP did not acknowledge the HIP consent notify. Please try again after some time | Cannot proceed |
| `AS-1281` | An unknown error occurred. Please try again later | Retry |
| `AS-1282` | Invalid X Auth token | Fix request |
| `AS-1283` | Patient profile mismatch with X Auth token | Fix request |
| `AS-1284` | Access Denied | Cannot proceed |
| `AS-1285` | Cannot process the request at the moment, please try later. | Retry |
| `AS-1286` | Open order not found | Fix request |
| `AS-1287` | Error in making call to target system Content type 'text/html' not supported for bodyType=java.util.HashMap<?… | Unclassified |
| `AS-1288` | Cannot find any linked ABHA address. Please create ABHA address first. | Unclassified |
| `AS-1289` | OTP is not verified for this transaction | Unclassified |
| `AS-1290` | User is not kyc verified | Unclassified |
| `AS-1291` | Self-relationship not allowed | Unclassified |
| `AS-1292` | Duplicate relationship not allowed.A relationship already exists between %s and %s | Fix request |
| `AS-1293` | We are facing some issue in server connectivity. Please try again | Retry |
| `AS-1294` | UIDAI Error code : 300 : Biometric data did not match. | Unclassified |
| `AS-1295` | The mobile number you have entered does not match with any of the records Please enter a different number | Fix request |
| `AS-1296` | You can request for new OTP after 30 seconds timestamp %s | Unclassified |
| `AS-1297` | This account is deactivated Please continue to reactivate abhaNumber %s | Cannot proceed |
| `AS-1298` | It appears that you are either not connected to the internet or experiencing a slow connection. please try ag… | Retry |
| `AS-1299` | UIDAI Error code : 953 : You have requested multiple OTPs in this transaction. Please try again in 30 minutes. | Retry |
| `AS-1300` | The mobile number you have entered has already been verified. Please provide an alternate mobile number. | Fix request |
| `AS-1301` | Old and New Passwords are same | Unclassified |
| `AS-1302` | This account is deactivated. Please reactivate it from ABHA portal. | Cannot proceed |
| `AS-1303` | No ABHA user registered with this Aadhaar number | Unclassified |
| `AS-1304` | UIDAI Error code : 400 :OTP validation failed | Unclassified |
| `AS-1305` | Please provide a photo featuring only one individual and not a group photo. | Unclassified |
| `AS-1306` | Invalid photo. Please upload a file with a human face. | Fix request |
| `AS-1307` | Your mobile number is not linked to the ABHA number. Please update your mobile number in ABHA or try using Aa… | Unclassified |
| `AS-1308` | You can request for new OTP after 30 seconds | Unclassified |
| `AS-1309` | As per NHA policy, your mobile number has reached the limit of 6 self-declared ABHA addresses. Please link yo… | Unclassified |
| `AS-1310` | User not found. Please verify and try again. | Retry |
| `AS-1311` | No password is set for this profile. Please log in using other login modes. | Unclassified |
| `AS-1312` | Mobile number is missing for this ABHA address. Please update your mobile number. | Fix request |
| `AS-1313` | The ABHA address entered is invalid. Please verify and try again. | Retry |
| `AS-1314` | Required header 'X-token' is not present. | Fix request |
| `AS-1315` | T-token expired | Cannot proceed |
| `AS-1316` | Doctor info not found for healthProfessionalId :'%s' | Fix request |
| `AS-1317` | An unexpected error has occurred. Please try again in some time. | Retry |
| `AS-1318` | Login via Password is not allowed | Unclassified |
| `AS-1319` | Invalid Password Request, Please enter valid ABHA Address or valid password | Fix request |
| `AS-1320` | Invalid OTP Value | Fix request |
| `AS-1321` | External service is temporarily unavailable | Retry |
| `AS-1322` | User not found. Please verify and try again. | Retry |
| `AS-1323` | User not found. Please verify and try again. | Retry |
| `AS-1324` | The mobile number you have entered does not match with any of the records. Please enter a different number | Fix request |
| `AS-1325` | Invalid Mobile Number | Fix request |
| `AS-1326` | UIDAI Error code : 400 : OTP validation failed | Unclassified |
| `AS-1327` | Mobile number is missing for this ABHA address. Please update your mobile number. | Fix request |
| `AS-1328` | Transaction is not found for UUID. | Fix request |
| `AS-1329` | You can request for new OTP after 30 seconds | Unclassified |
| `AS-1330` | T-token expired | Cannot proceed |
| `AS-1331` | The ABHA address entered is invalid. Please verify and try again. | Retry |
| `AS-1332` | Please enter a valid and registered provider Id. | Fix request |
| `AS-1333` | You can request for new OTP after 30 seconds | Unclassified |
| `AS-1334` | This account is deactivated. Please reactivate it from ABHA portal. | Cannot proceed |
| `AS-1335` | Login via Password is not allowed | Unclassified |
| `AS-1336` | No open order against ABHA. Please ensure a minimum of one open order | Unclassified |
| `AS-1337` | No CR Mapped with Abha Address | Unclassified |
| `AS-1338` | No pending care context found for this abha address | Unclassified |
| `AS-1339` | The provided gender does not match the gender in DigiLocker records | Unclassified |
| `AS-1340` | The provided DOB does not match the DOB in DigiLocker records | Unclassified |
| `AS-1341` | The provided name does not match the name in DigiLocker records | Unclassified |
| `AS-1342` | Invalid Face Auth PID | Fix request |
| `AS-1343` | No open order against ABHA. Please ensure a minimum of one open order | Unclassified |
| `AS-1344` | No registration found at %s. Contact counter support | Unclassified |
| `AS-1345` | Hospital services temporarily unavailable. Please try again after some time | Retry |
| `AS-1346` | Services disrupted, please try again. | Retry |
| `AS-1347` | Bank server not responding. Please try again later | Retry |
| `AS-1348` | Service details mismatch. Please ensure original service ID from HMIS | Fix request |
| `AS-1349` | The HIMS service is currently unavailable. Please try again after some time | Retry |
| `AS-1350` | Cannot process the request at the moment, please try later | Retry |
| `AS-1351` | No user profile found. | Unclassified |
| `AS-1352` | Cannot process the request at the moment, please try later. | Retry |
| `AS-1353` | Invalid OTP Request | Fix request |
| `AS-1354` | X-token expired | Cannot proceed |
| `AS-1355` | Invalid Mobile number. | Fix request |
| `AS-1356` | No pending care context found for this abha address | Unclassified |
| `AS-1357` | Invalid Password | Fix request |
| `AS-1358` | Invalid R-token | Fix request |
| `AS-1359` | Required header 'T-token' is not present. Please provide a valid T-token. | Fix request |
| `AS-1360` | Required header 'R-token' is not present. Please provide a valid R-token. | Fix request |
| `AS-1361` | Required header 'X-token' is not present. Please provide a valid X-token. | Fix request |
| `AS-1362` | Requested URL or resource is not available | Unclassified |
| `AS-1363` | Invalid X-token | Fix request |
| `AS-1364` | Invalid T-token | Fix request |
| `AS-1365` | The Scan and Pay functionality is not enabled at this facility. Kindly contact the hospital administration. | Unclassified |
| `AS-1366` | No CR Mapped with Abha Address | Unclassified |
| `AS-1367` | No care context is available for this patient. | Unclassified |
| `AS-1368` | No registration found at %s. Contact counter support | Unclassified |
| `AS-1369` | Invalid address line. It must be alphanumeric and can include the following special characters: ,.'/()- | Fix request |
| `AS-1370` | External service error | Unclassified |
| `AS-1371` | External service is temporarily unavailable | Retry |
| `AS-1372` | External Service Unavailable | Retry |
| `AS-1373` | Invalid Credentials. Make sure your API invocation call has a header: 'Authorization : Bearer ACCESS_TOKEN' o… | Fix request |
| `AS-1374` | Invalid Credentials. Make sure you have provided the correct security credentials | Fix request |
| `AS-1375` | Invalid Login Hint | Fix request |
| `AS-1376` | Invalid Scope | Fix request |
| `AS-1377` | Patient not found | Fix request |
| `AS-1378` | This account is deactivated. Please reactivate it from ABHA portal. | Cannot proceed |
| `AS-1379` | Digilocker account creation fail. | Unclassified |
| `AS-1380` | Too many request attempted in short period of time. This method is blocked for next 30 minutes | Cannot proceed |
| `AS-1381` | The email Id you have entered has already been verified. Please provide an alternate email Id | Fix request |
| `AS-1382` | Please avoid trying to generate the OTP multiple times within short time. | Unclassified |
| `AS-1383` | Sorry you have exceeded your feedback submission limit | Unclassified |
| `AS-1384` | Invalid KYC XML | Fix request |
| `AS-1385` | R-token expired | Cannot proceed |
| `AS-1386` | Invalid Email Id | Fix request |
| `AS-1387` | You have exceeded the maximum limit of failed attempts Please try to login using other modes or try again in … | Retry |
| `AS-1388` | Health Locker is Already Unsubscribed | Fix request |
| `AS-1389` | Beneficiary is not a covered member for requested policy. Please enroll beneficiary for the policy and try ag… | Retry |
| `AS-1390` | No Claim History with requested Details | Unclassified |
| `AS-1391` | External Service Unavailable | Retry |
| `AS-1392` | Duplicate Link token request | Unclassified |
| `AS-1393` | Digilocker Service Unavailable | Retry |
| `AS-1394` | You have exceeded the maximum limit of failed attempts Please try to login using other modes or try again in … | Retry |
| `AS-1395` | You have exceeded the maximum limit of failed attempts Please try to login using other modes or try again in … | Retry |
| `AS-1396` | Aadhaar number is incorrect.Please use correct Aadhaar. | Fix request |
| `AS-1397` | FileName can not be null or empty | Unclassified |
| `AS-1398` | You have exceeded the maximum limit of failed attempts. Please try to login using other modes or try again in… | Retry |
| `AS-1399` | Duplicate patient record share request. | Unclassified |
| `AS-1400` | Invalid HEALTHLOCKER Id or PHR Id. | Fix request |
| `AS-1401` | Invalid Service ID, it must be Alpha numeric and @, _ or - in middle. | Fix request |
| `AS-1402` | Care context cannot be null or empty. | Unclassified |
| `AS-1403` | Invalid data erase date. Date must be a future date. | Fix request |
| `AS-1404` | Data erase date cannot be null or empty. | Unclassified |
| `AS-1405` | Transaction Id is not matching with response. | Unclassified |
| `AS-1406` | Request Timed out. | Unclassified |
| `AS-1407` | expiry should be in future date. | Unclassified |
| `AS-1408` | Invalid API sequence flow, please follow logical flow. | Fix request |
| `AS-1409` | Invalid session status, Status should be TRANSFERRED, PARTIAL_TRANSFERRED or FAILED. | Fix request |
| `AS-1410` | Invalid health information status. | Fix request |
| `AS-1411` | endDate should be after startDate and before currentDate. | Unclassified |
| `AS-1412` | Invalid Mobile Number. | Fix request |
| `AS-1413` | LoginId is invalid. | Fix request |
| `AS-1414` | Invalid Transaction Id. | Fix request |
| `AS-1415` | Unable to fetch the file details. | Unclassified |
| `AS-1416` | Invalid PinCode, it must be only numbers and maximum length of 6. | Fix request |
| `AS-1417` | NHCX service is temporarily unavailable. | Retry |
| `AS-1418` | Maximum number of attempts for OTP match is exceeded or OTP is not generated. Please generate a fresh OTP and… | Unclassified |
| `AS-1419` | LoginId is invalid. | Fix request |
| `AS-1420` | Invalid Otp System. | Fix request |
| `AS-1421` | Invalid Auth Methods. | Fix request |
| `AS-1422` | This Aadhaar number is already linked to the ABHA Number %s. Please re-login and try using another Aadhaar Nu… | Fix request |

A code you meet that is not above is one the specifications do not carry yet. Read the code together with the message: a code can appear twice with different meanings.
