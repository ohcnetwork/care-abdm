# HIE-CM m1 build

Scaffolds an ABDM m1 integration one journey at a time. It covers ABHA creation, login and profile management.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

## Before the first journey, when the codebase already exists

Skip this section only for a system that does not exist yet. Otherwise it runs first, and its exit condition is a written plan, not a call.

### In plain words

Most ABDM integrations are not new systems. They are a hospital management
system, a laboratory system or a clinic application that already has patients,
visits, records, a login, an HTTP client and a way of keeping secrets. Every
ABDM journey has to land somewhere inside that, and a journey built before the
codebase has been read lands in the wrong place: a second HTTP client beside the
first, an ABHA column on the wrong table, a callback route the reverse proxy
never forwards.

So the first loop is not a journey. It is a survey of the system as it is, and
its exit condition is a written plan that names, for every ABDM touchpoint, the
file it will live in. The journeys then build against that plan rather than
against the specification's idea of a fresh codebase.

### Before you start

- The repository, checked out, with permission to read all of it. A survey of
  half a codebase produces a plan for half a system.
- The answers to the deployment interview. The
  code says what the system is. Only the integrator can say what the
  deployment is, and the two together decide which journeys are built at all.
- The practices that hold across every call, which
  the plan has to leave room for.

### What happens

This is one loop with a limit of eight passes over the codebase. Each pass
reads live state only, which here means the files themselves, never a README's
description of them and never an assumption carried from a similar system.

**Observe.** Inventory the system from its manifests and its tree, not from its
documentation. Record file paths for each of these, or record that none exists:

| Find | Where it usually shows | Why ABDM needs it |
|---|---|---|
| Languages and runtime versions | package manifests, lock files, toolchain files | Every generated call has to be idiomatic here |
| Build, run and test commands | manifests, CI configuration, a Makefile | Each journey's exit condition becomes a test that runs the same way |
| The frontend and backend split, and how they talk | the top level tree, an API client in the frontend, route definitions in the backend | The counter screens go in the frontend; every ABDM call goes through the backend |
| The outbound HTTP client the backend already uses | the dependency list, a shared client module | ABDM calls reuse it, or a second one appears and the two drift |
| How secrets and configuration reach the process | environment loading, a vault client, a config file | The client id, the secret and the gateway token travel the same way |
| The patient model, and the identifier fields it already carries | the schema, the ORM models, the migrations | The ABHA number and address become columns beside the existing identifiers, not a new table |
| The visit, encounter or record model | the same places | A care context maps to one of these, and the plan has to say which |
| Where inbound HTTP is routed and authenticated, and whether the deployment has a public URL | the router, the middleware, the reverse proxy configuration, the deployment manifests | ABDM calls back, and a callback route that nothing forwards is silence nobody notices |
| Existing cryptography helpers | a security or crypto module, the dependency list | The RSA encryption of identifiers reuses them |
| Where errors are shown to a user, and where they are logged | the frontend's error surface, the logging setup | A refused call has to land on the screen the person is looking at, and never log a token |

**Orient.** Map each ABDM touchpoint onto that inventory. Where the map is
exact, write the file path. Where it is not, write two candidates and say what
would decide between them. The common ambiguities: two places that could hold
the patient identifier, an HTTP client in the frontend and none in the backend,
a monorepo with several services and no obvious owner for callbacks.

Then read the interview answers against the inventory. A government integrator
gets the demographic route; a facility with no public URL gets no callback
driven journey until it has one; a desk with a fingerprint reader gets the
biometric method. The route set is the intersection of what the deployment
allows and what the code can host.

**Decide.** Order the journeys. The session token comes first because every
other call needs it. Then the journey whose exit condition can be observed with
the least new code, usually a profile read for a patient who already holds an
ABHA. Creation and linking come after, because each depends on state the earlier
ones produce. For each journey, name the files it will touch and the test that
proves its exit condition.

**Act.** Write the plan. It is a file in the repository, at the path the
integrator names or at the root as `abdm-integration-plan.md`, and it is the
only output of this loop. Then return to observe once, reading the plan against
the tree, to confirm every path in it exists or is marked as new.

If the limit is reached with questions still open, escalate: name what was
found, name the two candidates that could not be separated, point at this
atom, and ask one question.

### How you know it worked

The plan exists and answers every row of the inventory table with a file path,
or with the words none, add at, followed by a path. No row is blank and no row
says to be decided.

Every ABDM touchpoint in the plan names one file, or names two candidates and
the observation that would choose between them. Every journey in the plan names
the test that proves its exit condition and the command that runs it.

Open the plan beside the tree. Every path it names resolves, or is marked as
new. That is the observation that ends this loop, and the first journey does
not start until it has been made.

### When it goes wrong

- **The plan puts the HTTP client in the frontend.** The survey found the
  frontend's API client and stopped. Every ABDM call carries a secret, so it
  goes through the backend, and the plan has to say which backend module.
- **Two patient tables, and the plan picked one.** Orient produced one
  hypothesis where it needed two. Name both, and name the query that shows
  which one the visit model points at.
- **The plan has a callback route and the deployment has no public URL.** The
  inventory row on inbound routing was answered from the router rather than
  from the deployment. Mark every callback driven journey as blocked on a URL,
  and build the ones that are not.
- **The survey read the README and not the tree.** A README describes the
  system somebody meant to build. The plan is for the one that exists.
- **Eight passes and the plan is still incomplete.** Escalate with the rows
  that are answered, the rows that are not, this atom, and one question about
  the row that blocks the most journeys.

From `shared.concept.survey-an-existing-codebase`.

## Journeys

### Session, tokens and certificate (`m1-session`)

**Act: the calls in this journey, in order**

#### 1. Request a token for accessing a user’s ABHA (`m1_get_v3_profile_account_request_token`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/token \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'R-token: Bearer {{R-jwtToken}}' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8'
```

#### 2. Generate Keycloak token/access token (`gateway_post_gateway_v3_sessions`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "SBX_0000",
  "clientSecret": "0******-***-***-***-a****",
  "grantType": "client_credentials"
}'
```

#### 3. Fetch public key (`m1_get_v3_profile_public_certificate`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/public/certificate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "publicKey": "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9Nwgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1AayfZp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7irDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkNergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXuiwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAlsIzQpnSVDUVEzv17grVAw078CAwEAAQ==",
  "encryptionAlgorithm": "RSA/ECB/OAEPWithSHA-1AndMGF1Padding"
}
```

### ABHA creation, Aadhaar OTP (`m1-create-aadhaar-otp`)

**Act: the calls in this journey, in order**

#### 1. Generate Keycloak token/access token (`gateway_post_gateway_v3_sessions`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "SBX_0000",
  "clientSecret": "0******-***-***-***-a****",
  "grantType": "client_credentials"
}'
```

#### 2. Fetch public key (`m1_get_v3_profile_public_certificate`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/public/certificate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8'
```

#### 3. Request enrolment OTP (`m1_post_v3_enrollment_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "scope": [
    "abha-enrol"
  ],
  "loginHint": "aadhaar",
  "loginId": "{{encrypted aadhaar number}}",
  "otpSystem": "aadhaar"
}'
```

#### 4. Enrol by Aadhaar (`m1_post_v3_enrollment_enrol_byaadhaar`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp}}",
      "mobile": "{{mobile number}}"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

#### 5. Request enrolment OTP (`m1_post_v3_enrollment_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "{{encrypted mobileNumber}}",
  "otpSystem": "abdm"
}'
```

#### 6. Verify- mobile OTP (`m1_post_v3_enrollment_auth_byabdm`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp}}"
    }
  }
}'
```

#### 7. Get the ABHA address suggestion (`m1_get_v3_enrollment_enrol_suggestion`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TRANSACTION_ID: {{txnId}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 8. Create ABHA address (`m1_post_v3_enrollment_enrol_abha_address`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "abhaAddress": "{{ABHA Address}}",
  "preferred": 1
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "23acf181-339d-4771-b532-5c5df4a28d19",
  "healthIdNumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>"
}
```

### ABHA creation, face authentication (`m1-create-face`)

**Act: the calls in this journey, in order**

#### 1. Generate Keycloak token/access token (`gateway_post_gateway_v3_sessions`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "SBX_0000",
  "clientSecret": "0******-***-***-***-a****",
  "grantType": "client_credentials"
}'
```

#### 2. Fetch public key (`m1_get_v3_profile_public_certificate`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/public/certificate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8'
```

#### 3. Enrol auth init (`m1_post_v3_enrollment_enrol_auth_init`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/auth/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "face-auth"
  ]
}'
```

#### 4. Check the status of the transaction ID (`m1_post_v3_enrollment_enrol_capturepid`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/capturePID \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "face-verify"
  ],
  "txnId": "ea1dc7aa-d7c3-40ab-bee8-84c6f1eb90fa"
}'
```

#### 5. Enrol by Aadhaar (`m1_post_v3_enrollment_enrol_byaadhaar`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "face_auth"
    ],
    "face": {
      "txnId": "881f2bf5-7377-4067-b50e-1e6ff100b3cc",
      "aadhaar": "{{encrypted aadhaar number}}",
      "mobile": "{{mobile number}}"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

#### 6. Request enrolment OTP (`m1_post_v3_enrollment_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "{{encrypted mobileNumber}}",
  "otpSystem": "abdm"
}'
```

#### 7. Verify- mobile OTP (`m1_post_v3_enrollment_auth_byabdm`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp}}"
    }
  }
}'
```

#### 8. Get the ABHA address suggestion (`m1_get_v3_enrollment_enrol_suggestion`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TRANSACTION_ID: {{txnId}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 9. Create ABHA address (`m1_post_v3_enrollment_enrol_abha_address`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "abhaAddress": "{{ABHA Address}}",
  "preferred": 1
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "23acf181-339d-4771-b532-5c5df4a28d19",
  "healthIdNumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>"
}
```

### ABHA creation, fingerprint (`m1-create-fingerprint`)

**Act: the calls in this journey, in order**

#### 1. Generate Keycloak token/access token (`gateway_post_gateway_v3_sessions`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "SBX_0000",
  "clientSecret": "0******-***-***-***-a****",
  "grantType": "client_credentials"
}'
```

#### 2. Fetch public key (`m1_get_v3_profile_public_certificate`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/public/certificate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8'
```

#### 3. Enrol by Aadhaar (`m1_post_v3_enrollment_enrol_byaadhaar`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "bio"
    ],
    "bio": {
      "aadhaar": "{{encrypted aadhaar number}}",
      "fingerPrintAuthPid": "{{fingerPrintAuthPid}}",
      "mobile": "{{mobile number}}"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

#### 4. Request enrolment OTP (`m1_post_v3_enrollment_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "{{encrypted mobileNumber}}",
  "otpSystem": "abdm"
}'
```

#### 5. Verify- mobile OTP (`m1_post_v3_enrollment_auth_byabdm`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp}}"
    }
  }
}'
```

#### 6. Get the ABHA address suggestion (`m1_get_v3_enrollment_enrol_suggestion`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TRANSACTION_ID: {{txnId}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 7. Create ABHA address (`m1_post_v3_enrollment_enrol_abha_address`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "abhaAddress": "{{ABHA Address}}",
  "preferred": 1
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "23acf181-339d-4771-b532-5c5df4a28d19",
  "healthIdNumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>"
}
```

### ABHA creation, iris (`m1-create-iris`)

**Act: the calls in this journey, in order**

#### 1. Generate Keycloak token/access token (`gateway_post_gateway_v3_sessions`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "SBX_0000",
  "clientSecret": "0******-***-***-***-a****",
  "grantType": "client_credentials"
}'
```

#### 2. Fetch public key (`m1_get_v3_profile_public_certificate`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/public/certificate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8'
```

#### 3. Enrol by Aadhaar (`m1_post_v3_enrollment_enrol_byaadhaar`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "iris"
    ],
    "iris": {
      "aadhaar": "{{encrypted aadhaar number}}",
      "pid": "{{PID}}",
      "mobile": "{{mobile number}}"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

#### 4. Request enrolment OTP (`m1_post_v3_enrollment_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "{{encrypted mobileNumber}}",
  "otpSystem": "abdm"
}'
```

#### 5. Verify- mobile OTP (`m1_post_v3_enrollment_auth_byabdm`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp}}"
    }
  }
}'
```

#### 6. Get the ABHA address suggestion (`m1_get_v3_enrollment_enrol_suggestion`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TRANSACTION_ID: {{txnId}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 7. Create ABHA address (`m1_post_v3_enrollment_enrol_abha_address`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "abhaAddress": "{{ABHA Address}}",
  "preferred": 1
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "23acf181-339d-4771-b532-5c5df4a28d19",
  "healthIdNumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>"
}
```

### ABHA creation, demographic authentication (`m1-create-demographic`)

**Act: the calls in this journey, in order**

#### 1. Generate Keycloak token/access token (`gateway_post_gateway_v3_sessions`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "SBX_0000",
  "clientSecret": "0******-***-***-***-a****",
  "grantType": "client_credentials"
}'
```

#### 2. Fetch public key (`m1_get_v3_profile_public_certificate`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/public/certificate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8'
```

#### 3. Enrol by Aadhaar (`m1_post_v3_enrollment_enrol_byaadhaar`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "demo_auth"
    ],
    "demo_auth": {
      "aadhaarNumber": "{{encrypted aadhaar number}}",
      "districtCode": "{{District code}}",
      "stateCode": "{{State code}}",
      "dateOfBirth": "{{DOB}}",
      "gender": "{{Gender}}",
      "name": "{{Full name}}",
      "mobile": "{{Mobile number}}",
      "profilePhoto": "{{Base64 plain String}}",
      "pinCode": "<PINCODE>",
      "address": "<ADDRESS>"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "message": "This account already exist",
  "txnId": "b89ec10d-71fa-4280-83b3-1fedad66b5f5",
  "tokens": {
    "token": "<TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<TOKEN>",
    "refreshExpiresIn": 1296000
  },
  "ABHAProfile": {
    "firstName": "Username",
    "middleName": "<NAME>",
    "lastName": "<NAME>",
    "dob": "<DOB>",
    "gender": "M",
    "photo": "<BASE64_PHOTO>",
    "mobile": "******0903",
    "phrAddress": [
      "<ABHA_ADDRESS>"
    ],
    "address": "<ADDRESS>",
    "districtCode": "478",
    "stateCode": "27",
    "pinCode": "<PINCODE>",
    "abhaType": "STANDARD",
    "stateName": "MAHARASHTRA",
    "districtName": "<ADDRESS>",
    "ABHANumber": "<ABHA_NUMBER>",
    "abhaStatus": "ACTIVE"
  },
  "isNew": false
}
```

### ABHA creation, child ABHA (`m1-create-child`)

**Act: the calls in this journey, in order**

#### 1. Enrol by Aadhaar (`m1_post_v3_enrollment_enrol_byaadhaar`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "child"
    ],
    "child": {
      "dayOfBirth": "{{day Of Birth}}",
      "monthOfBirth": "{{month Of Birth}}",
      "yearOfBirth": "{{year Of Birth}}",
      "gender": "{{Gender}}",
      "password": "",
      "name": "{{Name}}",
      "profilePhoto": "",
      "parentConsent": "true"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

#### 2. Get child ABHA address (`m1_get_v3_enrollment_profile_children`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/profile/children \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'Content-Type: application/json' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}'
```

#### 3. Update the user ABHA profile Photo, update the child ABHA profile (`m1_patch_v3_profile_account`)

```bash
curl --request PATCH \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: <X_TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": "<ABHA_NUMBER>",
  "dob": "<DOB>",
  "name": "<NAME>",
  "gender": "F"
}'
```

#### 4. Send OTP ReKyc, update Mobile, child ABHA KYC request OTP (`m1_post_v3_profile_account_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "re-kyc"
  ],
  "loginHint": "aadhaar",
  "loginId": "{{encrypted aadhaar number}}",
  "otpSystem": "aadhaar"
}'
```

#### 5. Verify OTP ReKyc, update Mobile, CHILD ABHA KYC (`m1_post_v3_profile_account_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "re-kyc"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp value}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "6e3c1761-8e4c-44a3-929e-32b2c16083d5",
  "authResult": "success",
  "message": "Password updated successfully",
  "accounts": [
    {
      "ABHANumber": "<ABHA_NUMBER>"
    }
  ]
}
```

### ABHA login, mobile number (`m1-login-mobile`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "{{encrypted mobile number}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted OTP}}"
    }
  }
}'
```

#### 3. Login verify user (`m1_post_v3_profile_login_verify_user`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'T-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "ABHANumber": "{{abha-number}}",
  "txnId": "{{txnId}}"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "token": "<TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000
}
```

### ABHA login, Aadhaar number (`m1-login-aadhaar`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify"
  ],
  "loginHint": "aadhaar",
  "loginId": "{{encrypted aadhaar-number}}",
  "otpSystem": "aadhaar"
}'
```

#### 2. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted OTP}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### ABHA login, ABHA number with Aadhaar OTP (`m1-login-abha-number-aadhaar-otp`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}",
  "otpSystem": "aadhaar"
}'
```

#### 2. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted OTP}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### ABHA login, ABHA number with mobile OTP (`m1-login-abha-number-mobile-otp`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted OTP}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### ABHA login, face authentication (`m1-login-face`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-face-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-face-verify"
  ],
  "authData": {
    "authMethods": [
      "face"
    ],
    "face": {
      "txnId": "{{txnId}}",
      "faceAuthPid": "{{PID}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### ABHA login, fingerprint (`m1-login-fingerprint`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-bio-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-bio-verify"
  ],
  "authData": {
    "authMethods": [
      "bio"
    ],
    "bio": {
      "txnId": "{{txnId}}",
      "fingerPrintAuthPid": "{{PID}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### ABHA login, iris (`m1-login-iris`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-iris-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-iris-verify"
  ],
  "authData": {
    "authMethods": [
      "iris"
    ],
    "iris": {
      "txnId": "{{txnId}}",
      "irisAuthPid": "{{PID}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### ABHA login, ABHA address with mobile OTP (`m1-login-abha-address-mobile-otp`)

**Act: the calls in this journey, in order**

#### 1. Search ABHA profile using ABHA address (`m1_post_v3_phr_web_login_abha_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/search \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

#### 2. Login request OTP (`m1_post_v3_phr_web_login_abha_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "mobile-verify"
  ],
  "loginHint": "abha-address",
  "loginId": "{{encryptedAbhaAddress}}",
  "otpSystem": "abdm"
}'
```

#### 3. Verify OTP Aadhaar Number, mobile Number, verify via biometric (`m1_post_v3_phr_web_login_abha_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "41e59beb-6ee7-421e-a844-3652b2482038",
      "otpValue": "{{encryptedOtpValue}}"
    }
  }
}'
```

#### 4. Retrieve the user’s ABHA profile (`m1_get_v3_phr_web_login_profile_abha_profile`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha-profile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 5. Generate a PHR card profile (`m1_get_v3_phr_web_login_profile_abha_phr_card`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha/phr-card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

**Exit condition (Observe until this is true)**

A 202 response. The specification gives no body for it, so read what comes back.

### ABHA login, ABHA address with Aadhaar OTP (`m1-login-abha-address-aadhaar-otp`)

**Act: the calls in this journey, in order**

#### 1. Search ABHA profile using ABHA address (`m1_post_v3_phr_web_login_abha_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/search \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

#### 2. Login request OTP (`m1_post_v3_phr_web_login_abha_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "aadhaar-verify"
  ],
  "loginHint": "abha-address",
  "loginId": "{{encryptedAbhaAddress}}",
  "otpSystem": "aadhaar"
}'
```

#### 3. Verify OTP Aadhaar Number, mobile Number, verify via biometric (`m1_post_v3_phr_web_login_abha_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "aadhaar-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "41e59beb-6ee7-421e-a844-3652b2482038",
      "otpValue": "{{encryptedOtpValue}}"
    }
  }
}'
```

#### 4. Retrieve the user’s ABHA profile (`m1_get_v3_phr_web_login_profile_abha_profile`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha-profile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 5. Generate a PHR card profile (`m1_get_v3_phr_web_login_profile_abha_phr_card`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha/phr-card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

**Exit condition (Observe until this is true)**

A 202 response. The specification gives no body for it, so read what comes back.

### ABHA login, ABHA address with fingerprint (`m1-login-abha-address-fingerprint`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_phr_web_login_abha_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-bio-verify"
  ],
  "loginHint": "abha-address",
  "loginId": "{{encryptedAbhaAddress}}",
  "otpSystem": "aadhaar"
}'
```

#### 2. Verify OTP Aadhaar Number, mobile Number, verify via biometric (`m1_post_v3_phr_web_login_abha_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-bio-verify"
  ],
  "authData": {
    "authMethods": [
      "bio"
    ],
    "bio": {
      "txnId": "41e59beb-6ee7-421e-a844-3652b2482038",
      "fingerPrintAuthPid": "{{fingerPrintAuthPid}}"
    }
  }
}'
```

#### 3. Retrieve the user’s ABHA profile (`m1_get_v3_phr_web_login_profile_abha_profile`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha-profile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 4. Generate a PHR card profile (`m1_get_v3_phr_web_login_profile_abha_phr_card`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha/phr-card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 5. Login profile QR code (`m1_get_v3_phr_web_login_profile_abha_qr_code`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha/qr-code \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### ABHA login, ABHA address with face authentication (`m1-login-abha-address-face`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_phr_web_login_abha_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-face-verify"
  ],
  "loginHint": "abha-address",
  "loginId": "{{encryptedAbhaAddress}}",
  "otpSystem": "aadhaar"
}'
```

#### 2. Verify OTP Aadhaar Number, mobile Number, verify via biometric (`m1_post_v3_phr_web_login_abha_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-face-verify"
  ],
  "authData": {
    "authMethods": [
      "face"
    ],
    "face": {
      "txnId": "41e59beb-6ee7-421e-a844-3652b2482038",
      "faceAuthPid": "{{faceAuthPid}}"
    }
  }
}'
```

#### 3. Retrieve the user’s ABHA profile (`m1_get_v3_phr_web_login_profile_abha_profile`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha-profile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 4. Generate a PHR card profile (`m1_get_v3_phr_web_login_profile_abha_phr_card`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha/phr-card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 5. Login profile QR code (`m1_get_v3_phr_web_login_profile_abha_qr_code`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha/qr-code \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### ABHA login, ABHA address with iris (`m1-login-abha-address-iris`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`m1_post_v3_phr_web_login_abha_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-iris-verify"
  ],
  "loginHint": "abha-address",
  "loginId": "{{encryptedAbhaAddress}}",
  "otpSystem": "aadhaar"
}'
```

#### 2. Verify OTP Aadhaar Number, mobile Number, verify via biometric (`m1_post_v3_phr_web_login_abha_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-iris-verify"
  ],
  "authData": {
    "authMethods": [
      "iris"
    ],
    "iris": {
      "txnId": "41e59beb-6ee7-421e-a844-3652b2482038",
      "irisAuthPid": "{{irisAuthPid}}"
    }
  }
}'
```

#### 3. Retrieve the user’s ABHA profile (`m1_get_v3_phr_web_login_profile_abha_profile`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha-profile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 4. Generate a PHR card profile (`m1_get_v3_phr_web_login_profile_abha_phr_card`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha/phr-card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{jwtToken}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 5. Login profile QR code (`m1_get_v3_phr_web_login_profile_abha_qr_code`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/profile/abha/qr-code \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Find ABHA, mobile OTP (`m1-find-mobile-otp`)

**Act: the calls in this journey, in order**

#### 1. Search ABHA profile (`m1_post_v3_profile_account_abha_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search-abha"
  ],
  "mobile": "{{rsaMobileEncryptionOutput}}"
}'
```

#### 2. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "search-abha",
    "mobile-verify"
  ],
  "loginHint": "index",
  "loginId": "{{rsaIndexEncryptionOutput}}",
  "otpSystem": "abdm",
  "txnId": "{{searchTxnId}}"
}'
```

#### 3. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted OTP}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### Find ABHA, Aadhaar OTP (`m1-find-aadhaar-otp`)

**Act: the calls in this journey, in order**

#### 1. Search ABHA profile (`m1_post_v3_profile_account_abha_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search-abha"
  ],
  "mobile": "{{rsaMobileEncryptionOutput}}"
}'
```

#### 2. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "search-abha",
    "aadhaar-verify"
  ],
  "loginHint": "index",
  "loginId": "{{rsaIndexEncryptionOutput}}",
  "otpSystem": "aadhaar",
  "txnId": "{{searchTxnId}}"
}'
```

#### 3. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted OTP}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### Find ABHA, fingerprint (`m1-find-fingerprint`)

**Act: the calls in this journey, in order**

#### 1. Search ABHA profile (`m1_post_v3_profile_account_abha_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search-abha"
  ],
  "mobile": "{{rsaMobileEncryptionOutput}}"
}'
```

#### 2. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "search-abha",
    "aadhaar-bio-verify"
  ],
  "loginHint": "index",
  "loginId": "{{rsaIndexEncryptionOutput}}",
  "otpSystem": "aadhaar",
  "txnId": "{{searchTxnId}}"
}'
```

#### 3. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-bio-verify"
  ],
  "authData": {
    "authMethods": [
      "bio"
    ],
    "bio": {
      "txnId": "{{txnId}}",
      "fingerPrintAuthPid": "{{PID}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### Find ABHA, face authentication (`m1-find-face`)

**Act: the calls in this journey, in order**

#### 1. Search ABHA profile (`m1_post_v3_profile_account_abha_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search-abha"
  ],
  "mobile": "{{rsaMobileEncryptionOutput}}"
}'
```

#### 2. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "search-abha",
    "aadhaar-face-verify"
  ],
  "loginHint": "index",
  "loginId": "{{rsaIndexEncryptionOutput}}",
  "otpSystem": "aadhaar",
  "txnId": "{{searchTxnId}}"
}'
```

#### 3. Check the status of the transaction ID (`m1_post_v3_enrollment_enrol_capturepid`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/capturePID \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "face-verify"
  ],
  "txnId": "ea1dc7aa-d7c3-40ab-bee8-84c6f1eb90fa"
}'
```

#### 4. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-face-verify"
  ],
  "authData": {
    "authMethods": [
      "face"
    ],
    "face": {
      "txnId": "{{txnId}}",
      "faceAuthPid": "{{PID}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### Find ABHA, iris (`m1-find-iris`)

**Act: the calls in this journey, in order**

#### 1. Search ABHA profile (`m1_post_v3_profile_account_abha_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search-abha"
  ],
  "mobile": "{{rsaMobileEncryptionOutput}}"
}'
```

#### 2. Login request OTP (`m1_post_v3_profile_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "search-abha",
    "aadhaar-iris-verify"
  ],
  "loginHint": "index",
  "loginId": "{{rsaIndexEncryptionOutput}}",
  "otpSystem": "aadhaar",
  "txnId": "{{searchTxnId}}"
}'
```

#### 3. Login profile verify (`m1_post_v3_profile_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-iris-verify"
  ],
  "authData": {
    "authMethods": [
      "iris"
    ],
    "iris": {
      "txnId": "{{txnId}}",
      "irisAuthPid": "{{PID}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "authResult": "success",
  "message": "Password verified successfully",
  "token": "<TOKEN>",
  "expiresIn": 1296000,
  "refreshToken": "<TOKEN>",
  "refreshExpiresIn": 1296000,
  "accounts": []
}
```

### Profile management, profile and ABHA card (`m1-profile-and-card`)

**Act: the calls in this journey, in order**

#### 1. Generate QR code for an ABHA profile (`m1_get_v3_profile_account_qrcode`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/qrCode \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 2. Retrieve ABHA card image (`m1_get_v3_profile_account_abha_card`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha-card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 3. Get user profile details (`m1_get_v3_profile_account`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "ABHANumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>",
  "mobile": "******0903",
  "firstName": "Username",
  "middleName": "<NAME>",
  "lastName": "<NAME>",
  "name": "<NAME>",
  "yearOfBirth": "<DOB>",
  "dayOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "gender": "M",
  "profilePhoto": "<BASE64_PHOTO>",
  "status": "ACTIVE",
  "stateCode": "27",
  "districtCode": "478",
  "pincode": "<PINCODE>",
  "address": "<ADDRESS>",
  "kycPhoto": "<BASE64_PHOTO>",
  "stateName": "MAHARASHTRA",
  "districtName": "<ADDRESS>",
  "subdistrictName": "<ADDRESS>",
  "authMethods": [
    "MOBILE_OTP",
    "AADHAAR_BIO",
    "AADHAAR_OTP",
    "DEMOGRAPHICS",
    "PASSWORD"
  ],
  "tags": {},
  "kycVerified": true,
  "verificationStatus": "VERIFIED",
  "verificationType": "AADHAAR",
  "localizedDetails": {
    "name": "<NAME>",
    "stateName": "महाराष्ट्र",
    "districtName": "<ADDRESS>",
    "villageName": "<ADDRESS>",
    "townName": "<ADDRESS>",
    "gender": "पुरुष",
    "localizedLabels": {
      "name": "नाव",
      "abhaNumber": "आभा क्रमांक",
      "abhaAddress": "आभा पत्ता",
      "gender": "लिंग",
      "dob": "जन्मतारीख",
      "mobile": "मोबाईल"
    }
  },
  "createdDate": "07-05-2024"
}
```

### Profile management, mobile number update (`m1-update-mobile`)

**Act: the calls in this journey, in order**

#### 1. Send OTP ReKyc, update Mobile, child ABHA KYC request OTP (`m1_post_v3_profile_account_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "{{encrypted mobile number}}",
  "otpSystem": "abdm"
}'
```

#### 2. Verify OTP ReKyc, update Mobile, CHILD ABHA KYC (`m1_post_v3_profile_account_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "6e3c1761-8e4c-44a3-929e-32b2c16083d5",
  "authResult": "success",
  "message": "Password updated successfully",
  "accounts": [
    {
      "ABHANumber": "<ABHA_NUMBER>"
    }
  ]
}
```

### Profile management, re-KYC (`m1-re-kyc`)

**Act: the calls in this journey, in order**

#### 1. Send OTP ReKyc, update Mobile, child ABHA KYC request OTP (`m1_post_v3_profile_account_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "re-kyc"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}",
  "otpSystem": "aadhaar"
}'
```

#### 2. Verify OTP ReKyc, update Mobile, CHILD ABHA KYC (`m1_post_v3_profile_account_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "re-kyc"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "{{txnId}}",
      "otpValue": "{{encrypted otp}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "6e3c1761-8e4c-44a3-929e-32b2c16083d5",
  "authResult": "success",
  "message": "Password updated successfully",
  "accounts": [
    {
      "ABHANumber": "<ABHA_NUMBER>"
    }
  ]
}
```

### Benefit programmes (`m1-benefit`)

**Act: the calls in this journey, in order**

#### 1. Search for benefits associated with a user’s profile (`m1_post_v3_profile_benefit_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "search"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}"
}'
```

#### 2. Retrieve the benefit details associated with a specific ABHA number (`m1_get_v3_profile_benefit_abha_abhanumber`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/abha/{abhanumber} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 3. Submit the benefit LINK or DELINK (`m1_post_v3_profile_benefit_linkanddelink`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/linkAndDelink \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "link"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encrypted abha-number}}"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "benefitName": "Benefit Name",
  "healthId": "<ABHA_NUMBER>",
  "status": "Benefit record has been linked successfully"
}
```

## Where the detail is

- Every operation, with its body fields and responses: /docs/hiecm/v3/api/m1
- Error codes: /docs/hiecm/v3/api/m1/errors
