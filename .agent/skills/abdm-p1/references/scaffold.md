# HIE-CM p1 build

Scaffolds an ABDM p1 integration one journey at a time. It covers creating an ABHA address in a PHR app and logging in to it.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

## Journeys

### Create ABHA number, Aadhaar OTP (`p1-create-abha-number-aadhaar-otp`)

**Act: the calls in this journey, in order**

#### 1. Request enrolment OTP (`m1_post_v3_enrollment_request_otp`)

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

#### 2. Enrol by Aadhaar (`m1_post_v3_enrollment_enrol_byaadhaar`)

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
    "abha-enrol",
    "mobile-verify"
  ],
  "loginHint": "mobile",
  "loginId": "{{encrypted mobileNumber}}",
  "otpSystem": "abdm"
}'
```

#### 4. Verify- mobile OTP (`m1_post_v3_enrollment_auth_byabdm`)

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

#### 5. Submit the email verification link (`p1_post_v3_profile_account_request_emailverificationlink`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/emailVerificationLink \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-token: Bearer <JWT TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "email-link-verify"
  ],
  "loginHint": "email",
  "loginId": "{{encrypted email}}",
  "otpSystem": "abdm"
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

#### 8. Get user profile details (`m1_get_v3_profile_account`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 9. Retrieve ABHA card image (`m1_get_v3_profile_account_abha_card`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha-card \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'X-token: Bearer {{X-token}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Create ABHA address, mobile number (`p1-create-abha-address-mobile`)

**Act: the calls in this journey, in order**

#### 1. Request enrolment OTP (`p1_post_v3_phr_app_enrollment_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/request/otp \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-enroll",
    "mobile-verify"
  ],
  "loginHint": "mobile-number",
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

#### 2. Verify the enrolment OTP (`p1_post_v3_phr_app_enrollment_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/verify \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-enroll",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

#### 3. Suggest an ABHA address (`p1_post_v3_phr_app_enrollment_suggestion`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/suggestion \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "ee10d1c7-e25f-40e0-a3a1-df4c1dda02211",
  "firstName": "John",
  "lastName": "Doe",
  "dayOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "yearOfBirth": "<DOB>",
  "email": ""
}'
```

#### 4. Check whether the ABHA address exists (`p1_get_v3_phr_app_enrollment_isexists`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/isExists \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 5. Enrol ABHA address (`p1_post_v3_phr_app_enrollment_enrol`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/enrol \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "27d444b7-2a3d-46d8-bf67-e5590b6c46b6",
  "phrDetails": {
    "mobile": "<BASE64_PHOTO>",
    "firstName": "John",
    "middleName": "",
    "lastName": "Doe",
    "yearOfBirth": "<DOB>",
    "dayOfBirth": "",
    "monthOfBirth": "<DOB>",
    "gender": "M",
    "email": "",
    "profilePhoto": "",
    "address": "<ADDRESS>",
    "stateName": "Maharashtra",
    "stateCode": "27",
    "districtName": "<ADDRESS>",
    "districtCode": "123",
    "pinCode": "<PINCODE>",
    "abhaAddress": "<ABHA_ADDRESS>",
    "password": "<BASE64_PHOTO>"
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "6907ebb5-ff71-47f9-8052-6dd5554df5df",
  "message": "ABHA Address Created Successfully",
  "phrDetails": {
    "firstName": "John",
    "middleName": "",
    "lastName": "Doe",
    "fullName": "John Doe",
    "dayOfBirth": "<DOB>",
    "monthOfBirth": "<DOB>",
    "yearOfBirth": "<DOB>",
    "dateOfBirth": "<DOB>",
    "gender": "M",
    "email": "<EMAIL>",
    "mobile": "******1234",
    "address": "<ADDRESS>",
    "stateName": "Maharashtra",
    "districtName": "<ADDRESS>",
    "pinCode": "<PINCODE>",
    "abhaAddress": [
      "<ABHA_ADDRESS>",
      "<ABHA_ADDRESS>",
      "<ABHA_ADDRESS>"
    ],
    "stateCode": "27",
    "districtCode": "123"
  },
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<JWT TOKEN>",
    "refreshExpiresIn": 1296000
  }
}
```

### Create ABHA address, ABHA number with ABHA OTP (`p1-create-abha-address-abha-number-abha-otp`)

**Act: the calls in this journey, in order**

#### 1. Request enrolment OTP (`p1_post_v3_phr_app_enrollment_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/request/otp \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

#### 2. Verify the enrolment OTP (`p1_post_v3_phr_app_enrollment_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/verify \
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
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

#### 3. Verify User, verify user (`p1_post_v3_phr_app_login_verify_user`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'T-token: Bearer <JWT TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa"
}'
```

#### 4. Suggest an ABHA address (`p1_post_v3_phr_app_enrollment_suggestion`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/suggestion \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
  "firstName": "John",
  "lastName": "Doe",
  "dayOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "yearOfBirth": "<DOB>",
  "email": ""
}'
```

#### 5. Check whether the ABHA address exists (`p1_get_v3_phr_app_enrollment_isexists`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/isExists \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 6. Enrol ABHA address (`p1_post_v3_phr_app_enrollment_enrol`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/enrol \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
  "phrDetails": {
    "firstName": "John",
    "middleName": "",
    "lastName": "Doe",
    "dayOfBirth": "<DOB>",
    "monthOfBirth": "<DOB>",
    "yearOfBirth": "<DOB>",
    "gender": "M",
    "email": "",
    "mobile": "<BASE64_PHOTO>",
    "address": "<ADDRESS>",
    "stateName": "Maharashtra",
    "stateCode": "27",
    "districtName": "<ADDRESS>",
    "districtCode": "123",
    "pinCode": "<PINCODE>",
    "abhaAddress": "<ABHA_ADDRESS>",
    "password": "<BASE64_PHOTO>"
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "6907ebb5-ff71-47f9-8052-6dd5554df5df",
  "message": "ABHA Address Created Successfully",
  "phrDetails": {
    "firstName": "John",
    "middleName": "",
    "lastName": "Doe",
    "fullName": "John Doe",
    "dayOfBirth": "<DOB>",
    "monthOfBirth": "<DOB>",
    "yearOfBirth": "<DOB>",
    "dateOfBirth": "<DOB>",
    "gender": "M",
    "email": "<EMAIL>",
    "mobile": "******1234",
    "address": "<ADDRESS>",
    "stateName": "Maharashtra",
    "districtName": "<ADDRESS>",
    "pinCode": "<PINCODE>",
    "abhaAddress": [
      "<ABHA_ADDRESS>",
      "<ABHA_ADDRESS>",
      "<ABHA_ADDRESS>"
    ],
    "stateCode": "27",
    "districtCode": "123"
  },
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<JWT TOKEN>",
    "refreshExpiresIn": 1296000
  }
}
```

### Create ABHA address, ABHA number with Aadhaar OTP (`p1-create-abha-address-abha-number-aadhaar-otp`)

**Act: the calls in this journey, in order**

#### 1. Request enrolment OTP (`p1_post_v3_phr_app_enrollment_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/request/otp \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encryptedData}}",
  "otpSystem": "aadhaar"
}'
```

#### 2. Verify the enrolment OTP (`p1_post_v3_phr_app_enrollment_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/verify \
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
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

#### 3. Suggest an ABHA address (`p1_post_v3_phr_app_enrollment_suggestion`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/suggestion \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "7f45052a-ac63-48de-92db-c5d8d3d0c92a",
  "firstName": "John",
  "lastName": "Doe",
  "dayOfBirth": "<DOB>",
  "monthOfBirth": "<DOB>",
  "yearOfBirth": "<DOB>",
  "email": ""
}'
```

#### 4. Check whether the ABHA address exists (`p1_get_v3_phr_app_enrollment_isexists`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/isExists \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

#### 5. Enrol ABHA address (`p1_post_v3_phr_app_enrollment_enrol`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/enrol \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
  "phrDetails": {
    "firstName": "John",
    "middleName": "",
    "lastName": "Doe",
    "dayOfBirth": "<DOB>",
    "monthOfBirth": "<DOB>",
    "yearOfBirth": "<DOB>",
    "gender": "M",
    "email": "",
    "mobile": "<BASE64_PHOTO>",
    "address": "<ADDRESS>",
    "stateName": "Maharashtra",
    "stateCode": "27",
    "districtName": "<ADDRESS>",
    "districtCode": "123",
    "pinCode": "<PINCODE>",
    "abhaAddress": "<ABHA_ADDRESS>",
    "password": "<BASE64_PHOTO>"
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "6907ebb5-ff71-47f9-8052-6dd5554df5df",
  "message": "ABHA Address Created Successfully",
  "phrDetails": {
    "firstName": "John",
    "middleName": "",
    "lastName": "Doe",
    "fullName": "John Doe",
    "dayOfBirth": "<DOB>",
    "monthOfBirth": "<DOB>",
    "yearOfBirth": "<DOB>",
    "dateOfBirth": "<DOB>",
    "gender": "M",
    "email": "<EMAIL>",
    "mobile": "******1234",
    "address": "<ADDRESS>",
    "stateName": "Maharashtra",
    "districtName": "<ADDRESS>",
    "pinCode": "<PINCODE>",
    "abhaAddress": [
      "<ABHA_ADDRESS>",
      "<ABHA_ADDRESS>",
      "<ABHA_ADDRESS>"
    ],
    "stateCode": "27",
    "districtCode": "123"
  },
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": "<JWT TOKEN>",
    "refreshExpiresIn": 1296000
  }
}
```

### PHR login, mobile number (`p1-login-mobile`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`p1_post_v3_phr_app_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "mobile-verify"
  ],
  "loginHint": "mobile-number",
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login PHR verify (`p1_post_v3_phr_app_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
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
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

#### 3. Verify User, verify user (`p1_post_v3_phr_app_login_verify_user`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'T-token: Bearer <JWT TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "txnId": "48bc0a00-1127-459c-b040-8147f4ccc11a"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "token": "<JWT TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<JWT TOKEN>",
  "refreshExpiresIn": 1296000
}
```

### PHR login, email (`p1-login-email`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`p1_post_v3_phr_app_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "email-verify"
  ],
  "loginHint": "email",
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login PHR verify (`p1_post_v3_phr_app_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "email-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

#### 3. Verify User, verify user (`p1_post_v3_phr_app_login_verify_user`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'T-token: Bearer <JWT TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "token": "<JWT TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<JWT TOKEN>",
  "refreshExpiresIn": 1296000
}
```

### PHR login, ABHA address with mobile OTP (`p1-login-abha-address-mobile-otp`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`p1_post_v3_phr_app_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp \
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
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login PHR verify (`p1_post_v3_phr_app_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
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
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "b81a963d-4b97-48b4-9f9f-acf9f13afab7",
  "message": "OTP verified successfully",
  "authResult": "success",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "VERIFIED"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    }
  ],
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": null,
    "refreshExpiresIn": null
  }
}
```

### PHR login, ABHA number with Aadhaar OTP (`p1-login-abha-number-aadhaar-otp`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`p1_post_v3_phr_app_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp \
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
  "loginId": "{{encryptedData}}",
  "otpSystem": "aadhaar"
}'
```

#### 2. Login PHR verify (`p1_post_v3_phr_app_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
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
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

#### 3. Verify User, verify user (`p1_post_v3_phr_app_login_verify_user`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'T-token: Bearer <JWT TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "token": "<JWT TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<JWT TOKEN>",
  "refreshExpiresIn": 1296000
}
```

### PHR login, ABHA number with ABHA OTP (`p1-login-abha-number-abha-otp`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`p1_post_v3_phr_app_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp \
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
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login PHR verify (`p1_post_v3_phr_app_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
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
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

#### 3. Verify User, verify user (`p1_post_v3_phr_app_login_verify_user`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'T-token: Bearer <JWT TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "token": "<JWT TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<JWT TOKEN>",
  "refreshExpiresIn": 1296000
}
```

### PHR login, ABHA address with password (`p1-login-abha-address-password`)

**Act: the calls in this journey, in order**

#### 1. Search auth methods ABHAAddress (`p1_post_v3_phr_app_login_search`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/search \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

#### 2. Login PHR verify (`p1_post_v3_phr_app_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "password-verify"
  ],
  "authData": {
    "authMethods": [
      "password"
    ],
    "password": {
      "abhaAddress": "<ABHA_ADDRESS>",
      "password": "<BASE64_PHOTO>"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "b81a963d-4b97-48b4-9f9f-acf9f13afab7",
  "message": "OTP verified successfully",
  "authResult": "success",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "VERIFIED"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    }
  ],
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": null,
    "refreshExpiresIn": null
  }
}
```

### PHR login, ABHA address with email OTP (`p1-login-abha-address-email-otp`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`p1_post_v3_phr_app_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "email-verify"
  ],
  "loginHint": "abha-address",
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

#### 2. Login PHR verify (`p1_post_v3_phr_app_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-address-login",
    "email-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "37d8d312-35a0-41e7-a6e4-1074eb18a5fa",
      "otpValue": "{{encryptedData}}"
    }
  }
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "txnId": "b81a963d-4b97-48b4-9f9f-acf9f13afab7",
  "message": "OTP verified successfully",
  "authResult": "success",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "VERIFIED"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "abhaNumber": "<ABHA_NUMBER>",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    }
  ],
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 1800,
    "refreshToken": null,
    "refreshExpiresIn": null
  }
}
```

### PHR login, Aadhaar OTP (`p1-login-aadhaar-otp`)

**Act: the calls in this journey, in order**

#### 1. Login request OTP (`p1_post_v3_phr_app_login_request_otp`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/request/otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify",
    "aadhaar-otp-verify"
  ],
  "loginHint": "aadhaar",
  "loginId": "<BASE64_PHOTO>",
  "otpSystem": "aadhaar"
}'
```

#### 2. Login PHR verify (`p1_post_v3_phr_app_login_verify`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "aadhaar-verify",
    "aadhaar-otp-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "c51ad4d8-ae92-4509-8fb9-b91dea948492",
      "otpValue": "<BASE64_PHOTO>"
    }
  }
}'
```

#### 3. Verify User, verify user (`p1_post_v3_phr_app_login_verify_user`)

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/verify/user \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'T-token: Bearer <JWT TOKEN>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "txnId": "c51ad4d8-ae92-4509-8fb9-b91dea948492"
}'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "token": "<JWT TOKEN>",
  "expiresIn": 1800,
  "refreshToken": "<JWT TOKEN>",
  "refreshExpiresIn": 1296000
}
```

### PHR certificate and session token (`p1-certificate-and-session`)

**Act: the calls in this journey, in order**

#### 1. Get the PHR certificate (`p1_get_v3_phr_app_login_public_certificate`)

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/public/certificate \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
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

**Exit condition (Observe until this is true)**

A 202 whose body matches:

```json
{
  "accessToken": "<TOKEN>",
  "expiresIn": 1200,
  "refreshExpiresIn": 1800,
  "refreshToken": "<TOKEN>",
  "tokenType": "bearer"
}
```

## Where the detail is

- Every operation, with its body fields and responses: /docs/hiecm/v3/api/p1
- Error codes: /docs/hiecm/v3/api/p1/errors
