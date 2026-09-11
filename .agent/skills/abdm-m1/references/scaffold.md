# HIE-CM M1 build

Scaffolds an ABDM M1 integration one flow at a time. M1 covers ABHA creation, login and profile management.

## How this skill runs

Every flow below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the flow step matched below, decide the cheapest next action, act, and return to observe. A flow step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per flow step. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Flows

### Create an ABHA using an Aadhaar OTP (`hiecm.flow.m1-create-abha-aadhaar-otp`)

**Before you start**

- A client id and secret, and a working session token. See
  registration and credentials (shared.sandbox.registration-and-credentials).
- The person's Aadhaar number, encrypted against NHA's public key. See
  why identifiers are encrypted (hiecm.concept.encrypted-identifiers).
- The person present, because they must read an OTP from their phone.
- Their explicit consent to create an ABHA, which you send in the
  enrolment call.

**Act: the calls in this flow, in order**

#### Send an OTP to begin or continue an enrolment (`hiecm.endpoint.m1-enrolment-request-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-enrol"
  ],
  "loginHint": "aadhaar",
  "loginId": "_encrypted_12_digit_aadhaar_no_",
  "otpSystem": "aadhaar"
}'
```

#### Create an ABHA from a verified Aadhaar OTP (`hiecm.endpoint.m1-enrolment-by-aadhaar`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'BENEFIT_NAME: <BENEFIT_SCHEME_NAME>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>",
      "mobile": "<MOBILE>"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

#### Verify an OTP that ABDM sent, during enrolment (`hiecm.endpoint.m1-enrolment-verify-abdm-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>"
    }
  }
}'
```

#### Get suggested ABHA addresses for a new account (`hiecm.endpoint.m1-enrolment-address-suggestions`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'TRANSACTION_ID: <TXN_ID_FROM_ENROLMENT>'
```

#### Claim a chosen ABHA address (`hiecm.endpoint.m1-enrolment-claim-abha-address`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "txnId": "<TXN_ID>",
  "abhaAddress": "<ABHA_ADDRESS>",
  "preferred": 1
}'
```

**Exit condition (Observe until this is true)**

The person has an ABHA number, and an address they chose rather than the
digits-based default.

Confirm it by reading the profile back and checking that the address you
claimed is present and marked preferred. Do not treat the enrolment
response alone as the end of the flow: an account with only the default
address is a half finished job the person will not recognise later.

**If it goes wrong**

The OTP never arrives. The mobile registered against Aadhaar is not
necessarily the one the person is holding, and only the Aadhaar mobile
receives this OTP.

The enrolment call fails after the OTP was accepted. Do not retry it
blindly, because a retry that succeeds may enrol the person twice. Start
a fresh transaction instead.

The chosen address is refused. NHA's policy requires at least four
characters, no leading digit, and no leading or trailing dot. Validate
before submitting so the person is not guessing.

Every call fails with a header error. Check
ABDM-2402 (hiecm.error.abdm-2402) and
ABDM-2404 (hiecm.error.abdm-2404) before assuming the flow is wrong.

### Create an ABHA from an identity document (`hiecm.flow.m1-create-abha-by-document`)

**Before you start**

- A working session token.
- The person's mobile number, and the person present to read an OTP.
- The document details.

**Act: the calls in this flow, in order**

#### Send an OTP to begin or continue an enrolment (`hiecm.endpoint.m1-enrolment-request-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-enrol"
  ],
  "loginHint": "aadhaar",
  "loginId": "_encrypted_12_digit_aadhaar_no_",
  "otpSystem": "aadhaar"
}'
```

#### Verify an OTP that ABDM sent, during enrolment (`hiecm.endpoint.m1-enrolment-verify-abdm-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>"
    }
  }
}'
```

#### Create an ABHA from an identity document (`hiecm.endpoint.m1-enrolment-by-document`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byDocument' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "txnId": "<TXN_ID>",
  "documentType": "DRIVING_LICENCE",
  "documentId": "DL0820****858",
  "firstName": "<FIRST_NAME>",
  "middleName": "<MIDDLE_NAME>",
  "lastName": "<LAST_NAME>",
  "dob": "<DATE_OF_BIRTH>",
  "gender": "M",
  "frontSidePhoto": "<ENCRYPTED_VALUE>",
  "backSidePhoto": "<ENCRYPTED_VALUE>",
  "address": "<ADDRESS>",
  "state": "<STATE>",
  "district": "<DISTRICT>",
  "pinCode": "<PIN_CODE>",
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

#### Read the signed in person's ABHA profile (`hiecm.endpoint.m1-profile-get-account`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/account' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>'
```

#### Get the ABHA QR code (`hiecm.endpoint.m1-profile-get-qr-code`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/qrCode' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>'
```

**Exit condition (Observe until this is true)**

The profile read returns an account, and the QR code call returns an
image.

Because the account is restricted, also confirm what it cannot yet do
before telling the person they are finished.

**If it goes wrong**

The person expects full functionality. A document based account is
restricted, and the limits appear later as unexplained refusals unless
you say so at creation.

The document is not accepted. NHA's collection only exercises a driving
licence, so treat other document types as unproven until you have run
them.

### Create an ABHA using Aadhaar face authentication (`hiecm.flow.m1-create-abha-face-auth`)

**Before you start**

- Everything the OTP route needs. See
  create an ABHA using an Aadhaar OTP.
- The ABHA app installed on the person's phone, and the Aadhaar RD
  service available to it.
- A way to show a QR code, because that is how the transaction moves from
  your screen to their phone.

**Act: the calls in this flow, in order**

#### Start face or biometric authentication and get a transaction id (`hiecm.endpoint.m1-enrolment-face-auth-init`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/auth/init' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>'
```

#### Submit a captured biometric or face authentication block (`hiecm.endpoint.m1-enrolment-capture-pid`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/capturePID' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-enrol",
    "face-verify"
  ],
  "txnId": "<TXN_ID>"
}'
```

#### Create an ABHA from a verified Aadhaar OTP (`hiecm.endpoint.m1-enrolment-by-aadhaar`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'BENEFIT_NAME: <BENEFIT_SCHEME_NAME>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>",
      "mobile": "<MOBILE>"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

#### Get suggested ABHA addresses for a new account (`hiecm.endpoint.m1-enrolment-address-suggestions`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'TRANSACTION_ID: <TXN_ID_FROM_ENROLMENT>'
```

#### Claim a chosen ABHA address (`hiecm.endpoint.m1-enrolment-claim-abha-address`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "txnId": "<TXN_ID>",
  "abhaAddress": "<ABHA_ADDRESS>",
  "preferred": 1
}'
```

**Exit condition (Observe until this is true)**

Same ending as the OTP route: the person has an ABHA number and an
address they chose, confirmed by reading the profile back.

The step specific to this route is the capture. You know it worked when
the capture call is accepted rather than when the app says the face
scan succeeded, because those are different events.

**If it goes wrong**

The person does not have the ABHA app. The flow cannot start, and the app
store redirect is part of the journey rather than an error.

The PID block is rejected as stale. Captures expire. Recapture rather
than retrying the same block.

The person completes face authentication and nothing happens in your
application. Nothing pushes that result to you, so you must continue the
flow yourself once they confirm.

### Find somebody's ABHA when they do not know it (`hiecm.flow.m1-find-abha`)

**Before you start**

- A working session token.
- The identifier the person remembers, encrypted.
- The person present to read an OTP.

**Act: the calls in this flow, in order**

#### Encrypt a value with NHA's public key (`hiecm.endpoint.m1-encrypt-value`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/encrypt' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <UTC_ISO_8601_WITH_MILLISECONDS_AND_Z>' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "<PLAINTEXT_TO_ENCRYPT>"
}'
```

#### Find an ABHA for somebody who does not know theirs (`hiecm.endpoint.m1-find-abha-search`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'BENEFIT_NAME: <BENEFIT_SCHEME_NAME>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "search-abha"
  ],
  "mobile": "<MOBILE>"
}'
```

#### Send a login OTP (`hiecm.endpoint.m1-login-request-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'BENEFIT_NAME: <BENEFIT_SCHEME_NAME>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "<ENCRYPTED_MOBILE_NUMBER>",
  "otpSystem": "abdm"
}'
```

#### Verify a login OTP and get a user token (`hiecm.endpoint.m1-login-verify`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'BENEFIT_NAME: <BENEFIT_SCHEME_NAME>' \
  -H 'T-token: <T_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

You hold the person's ABHA account details and a token for it, and the
masked mobile shown during the search matched the phone they are holding.

If the person could not confirm the masked mobile, the flow has found
somebody else's account and must not continue.

**If it goes wrong**

The search finds nothing. The identifier may belong to no account, or to
an account in another environment. A sandbox account does not exist in
production.

The masked mobile is not theirs. Stop. This is the flow working
correctly, and continuing would disclose another person's account.

You are tempted to skip the OTP because search already returned the
account. Do not. Search plus verification is the flow; search alone is a
lookup of somebody else's identity.

### Log somebody in to their existing ABHA (`hiecm.flow.m1-login-by-mobile`)

**Before you start**

- A working session token.
- The person's mobile number, encrypted. See
  why identifiers are encrypted (hiecm.concept.encrypted-identifiers).
- The person present to read an OTP.

**Act: the calls in this flow, in order**

#### Send a login OTP (`hiecm.endpoint.m1-login-request-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'BENEFIT_NAME: <BENEFIT_SCHEME_NAME>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "<ENCRYPTED_MOBILE_NUMBER>",
  "otpSystem": "abdm"
}'
```

#### Verify a login OTP and get a user token (`hiecm.endpoint.m1-login-verify`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'BENEFIT_NAME: <BENEFIT_SCHEME_NAME>' \
  -H 'T-token: <T_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>"
    }
  }
}'
```

#### Choose which ABHA to sign in to (`hiecm.endpoint.m1-login-select-account`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify/user' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'T-token: <T_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "ABHANumber": "<ABHA_NUMBER>",
  "txnId": "<TXN_ID>"
}'
```

**Exit condition (Observe until this is true)**

You hold an `X-token`, and a profile read with it returns the account the
person expected.

The token read back is the check, not the presence of a token. A token
for the wrong account in a multi account household is the failure this
flow exists to prevent.

**If it goes wrong**

The verify call returns a list rather than a token. That is the multi
account branch, not an error.

The token is rejected on the next call. See
ABDM-2401 (hiecm.error.abdm-2401), and check you are not sending the
application session token in `X-token`.

Login fails with an authentication error and nothing more specific. See
900900 (hiecm.error.900900).

### Change the mobile number or email on an ABHA profile (`hiecm.flow.m1-update-mobile`)

**Before you start**

- The person logged in, so you hold their `X-token`. See
  log somebody in.
- The new value, encrypted.
- The person present, holding the new number, because the OTP goes there.

**Act: the calls in this flow, in order**

#### Send an OTP to change something on the profile (`hiecm.endpoint.m1-profile-request-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/otp' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-profile",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "<MOBILE_ENCRYPTION>",
  "otpSystem": "abdm"
}'
```

#### Verify the OTP for a profile change (`hiecm.endpoint.m1-profile-verify-otp`)

```bash
curl -X POST 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/verify' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "scope": [
    "abha-profile",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>"
    }
  }
}'
```

#### Read the signed in person's ABHA profile (`hiecm.endpoint.m1-profile-get-account`)

```bash
curl -X GET 'https://abhasbx.abdm.gov.in/abha/api/v3/profile/account' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>'
```

**Exit condition (Observe until this is true)**

Read the profile back and confirm the new value is present and marked
verified.

A successful verify response is not sufficient on its own. The profile
read is what proves the change persisted against the account you meant.

**If it goes wrong**

The OTP goes to the old number. It does not: it goes to the new one,
which is the point. If the person cannot receive it, the change cannot
proceed.

The scopes do not match between the two calls, and the verify is
refused. Send the array you sent on the request.

The person is not logged in and the call is refused. See
ABDM-2401 (hiecm.error.abdm-2401).

## Where the detail is

- Every operation in this milestone, with its body fields and responses: /docs/hiecm/v3/api/m1
- The flows as diagrams: /docs/hiecm/v3/milestones/m1
- Every error code across milestones: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary
