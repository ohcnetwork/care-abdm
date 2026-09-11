# HIE-CM P1 build

Scaffolds an ABDM P1 integration one flow at a time. P1 covers registration in a PHR application, the four login routes, and the profile the person holds.

## How this skill runs

Every flow below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the flow step matched below, decide the cheapest next action, act, and return to observe. A flow step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per flow step. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Flows

### Create an ABHA address in a PHR application (`hiecm.flow.p1-create-abha-address`)

**Before you start**

Four things must already be true, each checkable:

- You hold a gateway session token. See
  the gateway session (hiecm.concept.gateway-session).
- You can send and verify an OTP (shared.glossary.otp), and
  your screens keep resend locked for 60 seconds in every flow.
- You can store a refresh token securely, because login follows
  immediately and the application holds the session from here on.
- You know which path the user is on. A mobile number produces a
  Self-Declared profile with no KYC (shared.glossary.kyc); an
  existing 14 digit ABHA number (shared.glossary.abha-number)
  produces a KYC Verified one.

**Act: the calls in this flow, in order**

#### Send the OTP that starts a registration (`hiecm.endpoint.p1-enrollment-request-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/request/otp' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "scope": [ "abha-address-enroll", "mobile-verify" ], "loginHint": "mobile-number", "loginId": "{{encrypted-mobile-number}}", "otpSystem": "abdm" }'
```

#### Verify the registration OTP (`hiecm.endpoint.p1-enrollment-verify-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/verify' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "scope": [ "abha-address-enroll", "mobile-verify" ], "authData": { "authMethods": [ "otp" ], "otp": { "txnId": "*{{transactionId}}*", "otpValue": "*{{encrypted OTP}}*" } } }'
```

#### Ask for address suggestions (`hiecm.endpoint.p1-enrollment-address-suggestion`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/suggestion' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "txnId": "*{{transactionId}}*", "firstName": "John", "lastName": "Doe", "dayOfBirth": "14", "monthOfBirth": "11", "yearOfBirth": "1998" }'
```

#### Check whether an address is taken (`hiecm.endpoint.p1-enrollment-address-exists`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/isExists' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Create the health address (`hiecm.endpoint.p1-enrollment-enrol`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/enrol' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "txnId": "22387064-45ea-42d4-b6c5-8b86dbec6fe5", "phrDetails": { "mobile": " *{{encrypted mobile-number }}*", "firstName": "John", "middleName": "", "lastName": "Doe", "yearOfBirth": "1998", "dayOfBirth": "14", "monthOfBirth": "11", "gender": "M", "email": "", "profilePhoto": "{{base-64-encoded-profile-photo}}", "stateCode": "9", "districtCode": "135", "pinCode": 232101, "address": "Street number 4, sector 12", "stateName": "Maharashtra", "districtName": "Nashik", "ABHANumber": "XX-XXXX-XXXX-1234", "abhaAddress": "johndoe@sbx", "password": "*{{encrypted password}}*" } }'
```

#### Encrypt data (Aadhaar/Mobile/OTP/Password) (`hiecm.endpoint.p1-encrypt-data-aadhaar-mobile-otp-password`)

```bash
curl -X GET 'https://dev.abdm.gov.inhttps://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/public/certificate' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Get User Profile (`hiecm.endpoint.p1-get-user-profile`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/profile' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

**Exit condition (Observe until this is true)**

The user holds an ABHA address in the form `username@abdm`, and the
profile screen shows it marked Self-Declared or KYC Verified according to
the path they took. The ABHA number is visible only on a KYC Verified
profile.

Listing the addresses linked to that mobile number or ABHA number now
returns the address the user ended with, which is what proves the
creation landed rather than the screen merely closing.

**If it goes wrong**

The failures these sources document, in rough order of frequency:

- A duplicate address, because step 3 was skipped and the user created a
  second one rather than picking the one they had.
- A mandatory demographic field missing on the mobile number path, which
  is rejected as validation. The mandatory set is narrower than it looks:
  day and month of birth are not in it.
- An expired OTP, where the user waited out the window. Resend is locked
  for 60 seconds by design, so the screen must say so rather than appear
  broken.

### Sign a user in to a PHR application (`hiecm.flow.p1-login`)

**Before you start**

Four things must already be true, each checkable:

- The person holds an ABHA address (shared.glossary.abha-address).
  See create an ABHA address.
- You hold a gateway session token. See
  the gateway session (hiecm.concept.gateway-session).
- You can store a refresh token securely, and you have a sign out that
  clears it.
- Your application supports more than one user profile per install, with
  sign in and sign out between them.

**Act: the calls in this flow, in order**

#### Send the OTP that starts a login (`hiecm.endpoint.p1-login-request-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "scope": [ "abha-address-login", "mobile-verify" ], "loginHint": "mobile-number", "loginId": "*{{encrypted mobile-number}}*", "otpSystem": "abdm" }'
```

#### Verify the login OTP (`hiecm.endpoint.p1-login-verify-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "scope": [ "abha-address-login", "mobile-verify" ], "authData": { "authMethods": [ "otp" ], "otp": { "txnId": "*{{ transactionId}}*", "otpValue": "*{{encrypted OTP}}*" } } }'
```

#### Say which address is signing in (`hiecm.endpoint.p1-login-verify-user`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify/user' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "abhaAddress":"johndoe@abdm", "txnId":"*{{transactionId}}*" }'
```

#### Login using Password Search user (`hiecm.endpoint.p1-login-using-password-search-user`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/search' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "abhaAddress": "johndoe@sbx" }'
```

#### Generate Refresh Token (`hiecm.endpoint.p1-generate-refresh-token`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/profile/request/token' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Logout User (`hiecm.endpoint.p1-logout-user`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/profile/request/logout' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

**Exit condition (Observe until this is true)**

The application holds a session for one named ABHA address, and the
profile screen shows that address rather than a chooser. Signing out and
back in returns the user to the same address without repeating the
choice, which is what proves the session was stored rather than held in
memory.

**If it goes wrong**

The failures these sources document, in rough order of frequency:

- The wrong auth mode offered for an address, so the user is asked for a
  password they never set. Read the modes rather than defaulting.
- A mobile number carrying several addresses and no chooser shown, which
  signs the person in as the wrong one of their own identities.
- An expired OTP where the screen offered resend before the 60 seconds
  were up, or did not say the wait was deliberate.

## Where the detail is

- Every operation in this milestone, with its body fields and responses: /docs/hiecm/v3/api/p1
- The flows as diagrams: /docs/hiecm/v3/milestones/p1
- Every error code across milestones: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary
