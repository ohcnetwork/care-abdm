# HIE-CM M3 debug

Diagnoses a failed M3 call. Every error below is an OODA loop: observe the error code and last request id, orient against the matched error atom below (list a second hypothesis if the match is not exact), decide the fix, act, and observe whether the *original* step now succeeds. Applying a fix is not the exit condition; the original step succeeding is.

Loop limit: 5 passes per error. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Errors

### ABDM-1040, your requester identity is not recognised (`hiecm.error.abdm-1040`)

**Observed as**

ABDM does not recognise the HIU id on this consent request.

Like the HIP version, this is a registration problem.

**Fix**

Confirm the entity is registered in the HIU role and that you are sending
the HIU id rather than the HIP id.

If you hold both ids, keep them in separate configuration values so they
cannot be swapped.

**Exit condition: the original call now succeeds**

The consent request is accepted and the on-init callback arrives with a consent request id.

### ABDM-1112, the consent you are fetching against is no longer usable (`hiecm.error.abdm-1112`)

**Observed as**

The consent artefact you presented is unknown, expired or revoked.

This is often not a bug. A patient is allowed to revoke consent, and a
consent window is allowed to end.

**Fix**

Check the artefact's expiry before fetching, and treat revocation as a
normal state your system handles rather than an error it reports.

If you need continued access, raise a new consent request. Do not retry
against the old artefact.

**Exit condition: the original call now succeeds**

A fetch against a currently granted artefact is accepted and the data callback arrives.

## Where the detail is

- Every operation in this milestone, with its body fields and responses: /docs/hiecm/v3/api/m3
- The flows as diagrams: /docs/hiecm/v3/milestones/m3
- Every error code across milestones: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary

## Every recorded code

### Codes

Code, message and error name are as published. The action column reads the message text by a documented rule, and says Unclassified where the rule could not classify one.

| Code | Message | What to do |
| --- | --- | --- |
| `ABDM-1000` | Unable to connect the database | Retry |
| `ABDM-1001` | Subscription source update returned empty | Unclassified |
| `ABDM-1002` | Invalid frequency unit, it must be in HOUR, WEEK, DAY, MONTH, YEAR | Fix request |
| `ABDM-1003` | Email Gateway is unavailable | Retry |
| `ABDM-1004` | SMS Gateway is unavailable | Retry |
| `ABDM-1005` | Invalid receiver | Fix request |
| `ABDM-1006` | Invalid HIType, it must be in Prescription,DiagnosticReport,OPConsultation,DischargeSummary,ImmunizationRecor… | Fix request |
| `ABDM-1007` | Connection failed due to timeout | Retry |
| `ABDM-1008` | SMS service currently disabled | Unclassified |
| `ABDM-1009` | Email service currently disabled | Unclassified |
| `ABDM-1010` | No pending care context found for this abha address | Unclassified |
| `ABDM-1011` | Gateway database unavailable | Retry |
| `ABDM-1012` | No records found against the ABHA Address | Unclassified |
| `ABDM-1013` | Invalid ABHA Number | Fix request |
| `ABDM-1014` | Invalid Mobile Email | Fix request |
| `ABDM-1015` | Invalid Response | Fix request |
| `ABDM-1016` | Invalid Timestamp | Fix request |
| `ABDM-1017` | Invalid Transaction Id | Fix request |
| `ABDM-1018` | Share Profile database unavailable | Retry |
| `ABDM-1019` | Dependent Service Unavailable | Retry |
| `ABDM-1020` | Unknown database | Unclassified |
| `ABDM-1021` | Lack of required priviledges | Fix request |
| `ABDM-1022` | Too many requests | Retry |
| `ABDM-1023` | Invalid User | Fix request |
| `ABDM-1024` | Dependent service unavailable | Retry |
| `ABDM-1025` | Invalid ServiceId | Fix request |
| `ABDM-1026` | Bridge Id not found | Fix request |
| `ABDM-1027` | You are blocked. Please try again after 24 hours. | Cannot proceed |
| `ABDM-1028` | HIP is unavailable | Retry |
| `ABDM-1029` | Redis server is unavailable | Retry |
| `ABDM-1030` | Request id not found | Fix request |
| `ABDM-1031` | Invalid reason. Reason should not be null or empty and should contains only alphabets, dot(.) and comma(,) | Fix request |
| `ABDM-1032` | Invalid header | Fix request |
| `ABDM-1033` | HIU is unavailable | Retry |
| `ABDM-1034` | Notification service unavailable | Retry |
| `ABDM-1035` | OTP does not matched | Unclassified |
| `ABDM-1039` | Invalid Consent request id | Cannot proceed |
| `ABDM-1040` | Invalid Locker ID | Fix request |
| `ABDM-1041` | Invalid Acknowledgement | Fix request |
| `ABDM-1046` | Invalid Purpose | Fix request |
| `ABDM-1047` | Purpose does not exist | Fix request |
| `ABDM-1048` | Timeout | Retry |
| `ABDM-1051` | Invalid ABHA Number or ABHA Address | Fix request |
| `ABDM-1054` | Invalid Subscription Request Id | Fix request |
| `ABDM-1057` | Invalid Care Contexts | Fix request |
| `ABDM-1058` | Invalid HI Types | Fix request |
| `ABDM-1060` | Invalid Patient Reference Number | Fix request |
| `ABDM-1061` | Consent artefact expired | Cannot proceed |
| `ABDM-1062` | ABHA number mismatch with Link token), | Fix request |
| `ABDM-1063` | HIP Id mismatch with Link token | Fix request |
| `ABDM-1064` | request with this request id already exists | Fix request |
| `ABDM-1065` | Health facility does not exist | Fix request |
| `ABDM-1070` | Duplicate consent request | Cannot proceed |
| `ABDM-1071` | User doesn't belongs to same organisation | Unclassified |
| `ABDM-1072` | Included source size must be at least 1 | Unclassified |
| `ABDM-1074` | HIP object cannot be null in excluded sources | Fix request |
| `ABDM-1075` | HIP object cannot be null in included sources | Fix request |
| `ABDM-1077` | Auto approval policy id doesn't exist. | Unclassified |
| `ABDM-1078` | Failed to upload documents | Unclassified |
| `ABDM-1079` | Auto approval id is already disabled | Fix request |
| `ABDM-1080` | Subscription request may be already approved or denied | Fix request |
| `ABDM-1081` | Please upload registration certificate of your organisation | Unclassified |
| `ABDM-1082` | Please upload authority letter from your organisation | Unclassified |
| `ABDM-1083` | User doesn't belongs to same organisation | Unclassified |
| `ABDM-1084` | The Details fetched from Aadhaar is not matching with our database. Please select the correct details to proc… | Unclassified |
| `ABDM-1085` | ABHA number mismatch with X Auth token | Fix request |
| `ABDM-1099` | Invalid event Id, it cannot be null | Fix request |
| `ABDM-1100` | You have requested multiple OTPs Or Exceeded maximum number of attempts for OTP match in this transaction. Pl… | Retry |
| `ABDM-1112` | The provided gender does not match the gender in DigiLocker records | Unclassified |
| `ABDM-1113` | Duplicate health information provider data flow response data flow resoponse | Fix request |
| `ABDM-1116` | generate_and_save_link_token : 'NoneType' object has no attribute 'get' | Unclassified |
| `ABDM-1117` | Auto approval id is already active | Fix request |
| `ABDM-1118` | Login via ABHA Number OTP is not allowed | Fix request |
| `ABDM-1119` | Login via Aadhaar OTP is not allowed | Fix request |
| `ABDM-1120` | No care context is available for this patient. | Unclassified |
| `ABDM-1144` | Incorrect facility ID or password. | Fix request |
| `ABDM-1145` | Subscription is already disabled | Fix request |
| `ABDM-1146` | Subscription is not in revoked state | Unclassified |
| `ABDM-1147` | Subscription is not in granted state | Unclassified |
| `ABDM-1148` | Subscription id does not belong to the patient | Unclassified |
| `ABDM-1151` | Health locker is already setup for the user | Fix request |
| `ABDM-1152` | Subscription not found for the locker | Fix request |
| `ABDM-1153` | Unable to create Consent Auto Approval for the health locker | Cannot proceed |
| `ABDM-1154` | Unable to save user health locker | Unclassified |
| `ABDM-1170` | Invalid ABHA address | Fix request |
| `ABDM-1401` | Your mobile number is not linked to the ABHA number. Please update your mobile number in ABHA or try to regis… | Unclassified |
| `ABDM-1402` | Transaction Id is not matching with response | Unclassified |
| `ABDM-1403` | As per NHA policy, you have exceeded ABHA address creation limit, please link your ABHA address to ABHA numbe… | Unclassified |
| `ABDM-1404` | Patient record share detail not found | Fix request |
| `ABDM-1405` | Invalid health information status | Fix request |
| `ABDM-1406` | Invalid session status, Status should be TRANSFERRED, PARTIAL_TRANSFERRED or FAILED | Fix request |
| `ABDM-1407` | The ABHA Number associated with this ABHA Address is currently deactivated. Please reactivate it. | Cannot proceed |
| `ABDM-1408` | Invalid API sequence flow, please follow logical flow | Fix request |
| `ABDM-8877` | HIP did not acknowledge the HIP consent notify. Please try again after some time | Cannot proceed |
| `ABDM-9999` | Invalid purpose text, it must be in Care Management, Break the Glass, Public Health, Healthcare Payment, Dise… | Fix request |

A code you meet that is not above is one the specifications do not carry yet. Read the code together with the message: a code can appear twice with different meanings.
