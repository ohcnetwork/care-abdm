# HIE-CM m1 build

Scaffolds an ABDM m1 integration one journey at a time. It covers ABHA creation, login and profile management.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

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
