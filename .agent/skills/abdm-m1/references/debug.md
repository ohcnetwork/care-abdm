# HIE-CM M1 debug

Diagnoses a failed M1 call. Every error below is an OODA loop: observe the error code and last request id, orient against the matched error atom below (list a second hypothesis if the match is not exact), decide the fix, act, and observe whether the *original* step now succeeds. Applying a fix is not the exit condition; the original step succeeding is.

Loop limit: 5 passes per error. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Errors

### 900900, the ABHA service rejected the call without saying why (`hiecm.error.900900`)

**Observed as**

A code from the ABHA service rather than from the gateway, observed in
NHA's own saved responses. The accompanying description names the API
path that was refused.

It means authentication failed and the service is not saying which part.

**Fix**

Check both tokens. Confirm `Authorization` carries a current session
token, and that `X-token` carries the token for the person whose account
you are reading.

If both look right, confirm the route is one your credentials are
entitled to call. Gateway subscription state produces refusals that look
like credential problems.

**Exit condition: the original call now succeeds**

The call returns the account or result you expected rather than an error envelope.

### 900901, the ABHA service rejected the credentials outright (`hiecm.error.900901`)

**Observed as**

A second ABHA service code observed in NHA's saved responses, paired with
the message "Invalid Credentials".

Unlike the unclassified failure, this one is definite: what you sent was
wrong, not merely unacceptable.

**Fix**

Re-check the client id and secret against the ones issued for this
environment, then get a fresh session token.

Sandbox credentials do not work against production. That is the most
common cause of a definite rather than an expired credential failure.

**Exit condition: the original call now succeeds**

The call returns its normal response. Verify by making the session call fresh and using its token immediately.

### ABDM-1013, the fourteen digit number is wrong or wrongly formatted (`hiecm.error.abdm-1013`)

**Observed as**

The ABHA number you sent is not one ABDM recognises.

Most often this is formatting rather than a wrong person.

**Fix**

Send the number in NHA's hyphenated form, and confirm you are sending a
number rather than an address.

If both look right, the account may not exist in this environment. A
sandbox account does not exist in production.

**Exit condition: the original call now succeeds**

The call returns the account you expected, and the number in the response matches the one you sent.

### ABDM-1016, your timestamp format is wrong (`hiecm.error.abdm-1016`)

**Observed as**

Your `TIMESTAMP` header is in a format the service does not accept, so
the request was refused before anything else was looked at.

This is a formatting problem, not a clock problem. Its sibling,
ABDM-2402 (hiecm.error.abdm-2402), is the clock drift case: the value is well
formed but too far from the gateway's own time. If your value parses as
ISO 8601 UTC with milliseconds and still fails, read that atom instead.

**Fix**

Format the header as ISO 8601 UTC with milliseconds and the `Z` suffix,
for example `2026-08-25T15:51:15.339Z`. That exact change is what turned
the observed failure into a success. Generate it from your language's
date library, for example `Instant.now().toString()` in Java or
`new Date().toISOString()` in JavaScript. Do not format the value by
hand.

If a well formed UTC value still fails, your clock has probably
drifted, which is ABDM-2402 (hiecm.error.abdm-2402)'s territory.

If you are matching error codes and never see `ABDM-1016`, check that
your parser is not doing an exact match on the `code` field. The
observed value carried a trailing colon and space.

**Exit condition: the original call now succeeds**

The call you were making returns its normal response rather than this
code. In the observed session, resending the identical request with the
`TIMESTAMP` reformatted to UTC succeeded immediately, so no wait or
retry backoff is involved.

### ABDM-1094, access to this feature is restricted (`hiecm.error.abdm-1094`)

**Observed as**

ABDM-1094 is an entitlement failure, HTTP 401. Your client id is not
allowed to do what it just tried. It carries two documented messages:
"Access to this feature is restricted. Please contact NHA to enable it"
means the endpoint itself is off limits for your client; "Invalid
Benefit Name" means the BENEFIT_NAME header you sent does not match a
benefit programme registered against your client.

**Fix**

Retrying does not help; entitlement is configuration, not a transient
state. Restricted message: stop calling the endpoint, or ask NHA to
enable the entitlement. Invalid benefit name: use the exact name NHA
gave you at onboarding.

**Exit condition: the original call now succeeds**

The original call returns a non 401 response. For the benefit name case,
NHA's own collection uses the exact registered name, such as
`healthid api`.

### ABDM-1107, invalid combinations of scopes (`hiecm.error.abdm-1107`)

**Observed as**

`scope` is an array, and the operations care about the combination rather than
about any one value in it. This code means the combination you sent is not one
this operation accepts, or is not the one the transaction was opened with.

```response
{"error": {"code": "ABDM-1107", "message": "Invalid combinations of scopes"}}
```

Observed on the sandbox on 2026-09-14: an enrolment OTP request sent
`["abha-enrol"]` and returned 200, and the verification that followed reused
`["abha-enrol"]` and was refused with this code.

**Fix**

- You reused one scope across a whole journey. Read the scope off the example
  for the operation you are calling, not off the one before it.
- You are on the enrolment path and meant to be on the login path. Aadhaar is a
  login identifier as well as an enrolment one, and the scope is the first
  place the two diverge. A patient who already holds an ABHA belongs on the
  login path, and sending them down enrolment creates a second ABHA number that
  nothing merges. See designing the ABHA journey.
- The transaction was opened for something else. `txnId` carries the scope it
  was created with, so a transaction cannot be reused across journeys.

**Exit condition: the original call now succeeds**

The call the refusal came from returns its own success body instead: a login
verification returns `authResult: "success"` with a token and an accounts
array, and an enrolment verification continues the enrolment.

### ABDM-1407, the person's account is switched off (`hiecm.error.abdm-1407`)

**Observed as**

The ABHA number exists but has been deactivated, so it cannot be used
until it is reactivated.

Nothing about your request is wrong.

**Fix**

There is no fix on your side. The person reactivates their own account,
which M1 exposes as a call.

What your system should do is say so plainly rather than presenting a
generic failure, because the person is the only one who can resolve it.

**Exit condition: the original call now succeeds**

The same call succeeds after the account is reactivated. There is nothing you can verify from your side while it is deactivated.

### ABDM-2401, the person scoped token is wrong or expired (`hiecm.error.abdm-2401`)

**Observed as**

This is not about your application's session token. It is about the token
that identifies one person, returned when they logged in and sent
afterwards as `X-token`.

The gateway accepted your application and rejected the person.

**Fix**

Have the person log in again, or refresh the token using the refresh
token rather than making them repeat the OTP.

If it persists, check you are not sending the application session token
in `X-token`. The two tokens are not interchangeable.

**Exit condition: the original call now succeeds**

The profile call returns the account you expected, and the identifiers in the response match the person who logged in.

## Where the detail is

- Every operation in this milestone, with its body fields and responses: /docs/hiecm/v3/api/m1
- The flows as diagrams: /docs/hiecm/v3/milestones/m1
- Every error code across milestones: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary

## Every recorded code

### Six error shapes, not one

Do not write a parser that expects a single shape. Four come from the ABHA
service and its gateway. The fifth is an empty body. The sixth comes from
the registries and hides its real code one level down.

### Shape 1: the wrapped ABDM error

```json
{
    "error": {
        "code": "ABDM-1204",
        "message": "UIDAI Error code : 300 : Biometric data did not match."
    }
}
```

The code lives at `error.code`. This comes from the ABHA service's own business logic.

Do not compare that code with string equality. It is not always a clean
token: a failed session call returned `{"error":{"code":"ABDM-9999: ",
"message":"Invalid user credentials"}}`, with a trailing colon and space
inside the code. Trim it and match on the `ABDM-nnnn` prefix, or the branch
you wrote for that code never runs.

### Shape 2: the flat ABDM error

```json
{
    "code": "ABDM-1094",
    "message": "Access to this feature is restricted. Please contact NHA to enable it.",
    "timestamp": "2024-10-25 15:02:34"
}
```

Same family of codes, no `error` wrapper, plus a `timestamp`. The collection shows `ABDM-1094` in both shapes on different calls, so the wrapper is not tied to the code. Read `error.code` first and fall back to a top level `code`.

### Shape 3: field validation

```json
{
    "txnId": "Invalid Transaction Id",
    "timestamp": "2025-01-15 13:21:16"
}
```

No code at all. The key names the field you got wrong. Several bad fields produce several keys:

```json
{
    "scope": "Invalid Scope",
    "authData": "Invalid Auth Data",
    "timestamp": "2025-01-15 13:39:03"
}
```

Treat every key except `timestamp` as a field name. These always arrive as HTTP 400.

Two of these read almost the same. Only one of them tells you anything.

| Body | What it tells you |
|---|---|
| `{"loginId": "LoginId is invalid"}` | It decrypted. The plaintext failed a format rule |
| `{"loginId": "Invalid LoginId"}` | On the enrolment endpoint, nothing at all |

The first is the one that costs an afternoon, because the value really was
encrypted and really was the right number. An ABHA number keeps its dashes,
`NN-NNNN-NNNN-NNNN`.

The second carries no diagnostic value on `/v3/enrollment/request/otp`. That
endpoint returns it for plaintext, for an empty string, for base64 that is
not ciphertext, and for a correctly encrypted value alike. A padding matrix
run against it returns the same refusal for every row, the correct row
included, which is how a wrong padding survives a test that looks thorough.

Test encryption against `POST /v3/profile/login/request/otp` with
`loginHint: "mobile"` instead, and with a number that is registered against
an ABHA account. The 200 is the signal: a right padding returns it with a
`txnId`, a wrong one returns `Invalid Mobile Number`.

The number has to be a real one. A correctly encrypted `9999999999` returns
that same `Invalid Mobile Number`, because the value decrypted fine and
named nobody. With an unregistered number this endpoint is as uninformative
as the enrolment one.

The algorithm is published: read `encryptionAlgorithm` from the certificate
response. The plaintext shape for every encrypted field is in
[encryption](/docs/hiecm/v3/concepts/encryption).

### Shape 4: the API gateway error

```json
{
    "code": "900901",
    "message": "Invalid Credentials",
    "description": "Invalid JWT token. Make sure you have provided the correct security credentials"
}
```

A numeric code, not an `ABDM-` code, plus a `description` field the other shapes lack. This comes from the API gateway in front of the ABHA service, before your request reaches the business logic. It almost always means the `Authorization` header is wrong or expired.

`900901` is a bad token. `900902` is no token at all, observed on the NHPR
host. Match the family, not the single code.

### Shape 5: the empty body

An HTTP 401 with a zero length body and no JSON at all, observed on
`/v3/phr/web/login/profile/abha-profile` when no user token was sent. There
is nothing to parse and nothing to match. Code that assumes every failure
carries a body throws here, on a response that means something simple.

### Shape 6: the registry error, with the real code nested

```json
{
    "code": "HIS-422",
    "message": "Unable to process the current request due to some wrong data entered.",
    "details": [
        {"message": "You are not allowed to access this API", "code": "HIS-403", "attribute": null}
    ]
}
```

The registries return a `HIS-` family rather than `ABDM-`, and the top level
code is not the cause. `HIS-422` and its message say the data was wrong. The
real reason is in `details[0]`: `HIS-403`, not permitted. The HTTP status
disagrees with the nested code too, arriving as 422 for what is an
authorisation failure.

Read `details[0].code` before the top level one on any `HIS-` response, and
show `details[0].message` to whoever is debugging. Acting on the outer code
sends you to check your payload for a problem that is not there.

### Codes

Code, message and error name are as published. The action column reads the message text by a documented rule, and says Unclassified where the rule could not classify one.

| Code | Message | What to do |
| --- | --- | --- |
| `ABDM-1001` | Subscription source update returned empty | Unclassified |
| `ABDM-1002` | Invalid frequency unit, it must be in HOUR, WEEK, DAY, MONTH, YEAR | Fix request |
| `ABDM-1006` | Invalid HIType, it must be in Prescription,DiagnosticReport,OPConsultation,DischargeSummary,ImmunizationRecor… | Fix request |
| `ABDM-1008` | SMS service currently disabled | Unclassified |
| `ABDM-1009` | Email service currently disabled | Unclassified |
| `ABDM-1010` | No pending care context found for this abha address | Unclassified |
| `ABDM-1013` | Invalid ABHA Number | Fix request |
| `ABDM-1016` | Invalid Timestamp | Fix request |
| `ABDM-1017` | Invalid Transaction Id | Fix request |
| `ABDM-1019` | Dependent Service Unavailable | Retry |
| `ABDM-1021` | Lack of required priviledges | Fix request |
| `ABDM-1022` | Too many requests | Retry |
| `ABDM-1029` | Redis server is unavailable | Retry |
| `ABDM-1030` | Request id not found | Fix request |
| `ABDM-1034` | Notification service unavailable | Retry |
| `ABDM-1045` | Database Access is restricted | Unclassified |
| `ABDM-1047` | Purpose does not exist | Fix request |
| `ABDM-1048` | Timeout | Retry |
| `ABDM-1065` | Health facility does not exist | Fix request |
| `ABDM-1066` | Please enter a valid Password | Unclassified |
| `ABDM-1094` | Access to this feature is restricted. Please contact NHA to enable it. | Fix auth |
| `ABDM-1094` | Invalid Benefit Name | Fix auth |
| `ABDM-1100` | You have requested multiple OTPs Or Exceeded maximum number of attempts for OTP match in this transaction. Pl… | Retry |
| `ABDM-1101` | This ABHA Address already exists. Please create with unique ABHA address | Fix request |
| `ABDM-1102` | Mobile number verification is pending. | Unclassified |
| `ABDM-1103` | Cannot link with CHILD ABHA Number | Unclassified |
| `ABDM-1104` | Cannot link with same ABHA Number | Unclassified |
| `ABDM-1105` | Invalid request for parent linking | Fix request |
| `ABDM-1107` | Invalid combinations of scopes | Fix request |
| `ABDM-1108` | Notification DB service unavailable | Retry |
| `ABDM-1109` | Invalid On discovery response | Fix request |
| `ABDM-1110` | Your new password must be different from your old password. Please enter a unique new password. | Unclassified |
| `ABDM-1111` | Invalid old password, please try with valid password. | Fix request |
| `ABDM-1112` | The provided gender does not match the gender in DigiLocker records | Unclassified |
| `ABDM-1113` | Duplicate health information provider data flow response data flow resoponse | Fix request |
| `ABDM-1114` | The provided name does not match the name in DigiLocker records | Unclassified |
| `ABDM-1115` | Invalid patient information. At least one patient information is required. | Fix request |
| `ABDM-1116` | generate_and_save_link_token : 'NoneType' object has no attribute 'get' | Unclassified |
| `ABDM-1117` | Auto approval id is already active | Fix request |
| `ABDM-1118` | Login via ABHA Number OTP is not allowed | Fix request |
| `ABDM-1119` | Login via Aadhaar OTP is not allowed | Fix request |
| `ABDM-1121` | Invalid Enrolment Number | Fix request |
| `ABDM-1122` | Request can not be processed | Unclassified |
| `ABDM-1124` | The mobile number provided by you is already linked to 6 ABHA Numbers. Please provide a different Mobile Numb… | Fix request |
| `ABDM-1126` | F-Token Expired | Fix request |
| `ABDM-1127` | Invalid F-Token | Fix request |
| `ABDM-1132` | Kindly enter valid linked ABHA Address | Unclassified |
| `ABDM-1133` | Please enter a valid captcha result. Entered captcha result is incorrect. | Fix request |
| `ABDM-1134` | Deactivated ABHA Account | Cannot proceed |
| `ABDM-1135` | The email address provided by you is already linked to 6 ABHA Numbers. Please provide a different email Id. | Fix request |
| `ABDM-1136` | message should not be null or empty. | Unclassified |
| `ABDM-1137` | Benefit Name Not Found | Fix request |
| `ABDM-1138` | The benefit record has already been de-linked | Treat as success |
| `ABDM-1139` | Benefit record not found | Fix request |
| `ABDM-1140` | The benefit record has already been linked | Treat as success |
| `ABDM-1141` | An existing ABHA number created using this Aadhaar number has been found. It is advisable to delete this acco… | Unclassified |
| `ABDM-1142` | Please enter a valid captcha. Entered captcha is expired. | Fix request |
| `ABDM-1143` | Captcha limit exceeded. | Unclassified |
| `ABDM-1144` | Incorrect facility ID or password. | Fix request |
| `ABDM-1155` | Parents must be 18 years of age or older to create a Child ABHA Account | Unclassified |
| `ABDM-1156` | Please ensure that the mobile number is mapped to the parent's ABHA number | Unclassified |
| `ABDM-1157` | Child ABHA’s account limit has been exceeded for the requested Abha ID number ‘(.*?) | Unclassified |
| `ABDM-1158` | Invalid X-Token | Fix request |
| `ABDM-1159` | Children’s ages should be below '(.*?)' years as of the current date | Unclassified |
| `ABDM-1160` | Non KYC CHILD ABHA is allowed to update their profile only once | Unclassified |
| `ABDM-1200` | LGD Gateway is unavailable | Retry |
| `ABDM-1201` | IDP Gateway is unavailable | Retry |
| `ABDM-1202` | Document Gateway is unavailable | Retry |
| `ABDM-1203` | TEST | Unclassified |
| `ABDM-1204` | A UIDAI failure passed through. The UIDAI code and text sit inside the message string | Fix request |
| `ABDM-1205` | Document DB Gateway is unavailable | Retry |
| `ABDM-1206` | Aadhaar Gateway is unavailable | Retry |
| `ABDM-1207` | The information you provided does not match the details on record with Aadhaar. Please verify and provide acc… | Fix request |
| `ABDM-1211` | Email Sending Limit Exceeded | Unclassified |
| `ABDM-1218` | Role for the user does not exist. | Fix request |
| `ABDM-1219` | Your ABHA is linked with govt benefit programme, so it can not be deleted- ABDM, National Health Authority. | Unclassified |
| `ABDM-1220` | Sorry, Unable to process your request at this time. Please try again later. | Retry |
| `ABDM-1224` | Login via Biometric is not allowed. | Fix auth |
| `ABDM-1226` | Vault service unavailable | Retry |
| `ABDM-1227` | This client ID has reached the maximum limit of 100 ABHA account creations. | Unclassified |
| `ABDM-1228` | Your ABHA is linked with govt benefit programme, so it can not be deactivated- ABDM, National Health Authorit… | Cannot proceed |
| `ABDM-9999` | Recorded as `ABDM-9999: ` with an `ABDM-1094` message stuck to the front of the text | Fix auth |

### Codes, untagged

The same collection, and the only source that recorded HTTP statuses.

| Code | HTTP | Message | What to do |
| --- | --- | --- | --- |
| `900901` | 401 | Invalid Credentials, invalid JWT token. From the API gateway in front of the ABHA service, before your reques… | Fix auth |
| `900900` | 500 | Unclassified authentication failure. The one saved example had a bad path and a bad token together, so read i… | Fix auth |
| `404` | 404 | No matching resource found for given API Request`. A wrong path, not a missing record | Fix request |

### Codes, uidai

Codes from the Unique Identification Authority of India, passed through inside the message of ABDM-1204. More codes pass through than are listed here, so parse the message.

| Code | Message | What to do |
| --- | --- | --- |
| `300` | Biometric mismatch |  |
| `561` | Request expired |  |
| `563` | Duplicate request |  |
| `810` | Missing biometric data |  |

A code you meet that is not above is one the specifications do not carry yet. Read the code together with the message: a code can appear twice with different meanings.
