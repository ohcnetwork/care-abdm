# Integrate M1, ABHA identity

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://abhasbx.abdm.gov.in/abha/api` ABHA Server, Sandbox (primary)
- `https://dev.abdm.gov.in/api/hiecm` ABDM Gateway, Dev
- `https://dev.abdm.gov.in` Sandbox. Pair it with the `X-CM-ID: sbx` header.
- `https://apis.abdm.gov.in` Production. Pair it with the `X-CM-ID: abdm` header.
## Endpoints

55 operations, grouped by the journey they belong to.

### ABHA creation, Aadhaar biometric

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v3/enrollment/enrol/auth/init` | Start face or biometric authentication and get a transaction id |
| `POST` | `/v3/enrollment/enrol/capturePID` | Submit a captured biometric or face authentication block |

### ABHA creation, Aadhaar OTP

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v3/enrollment/auth/byAbdm` | Verify an OTP that ABDM sent, during enrolment |
| `POST` | `/v3/enrollment/enrol/abha-address` | Claim a chosen ABHA address |
| `POST` | `/v3/enrollment/enrol/byAadhaar` | Create an ABHA from a verified Aadhaar OTP |
| `GET` | `/v3/enrollment/enrol/suggestion` | Get suggested ABHA addresses for a new account |
| `POST` | `/v3/enrollment/request/otp` | Send an OTP to begin or continue an enrolment |

### ABHA creation, demographic authentication

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/v3/enrollment/profile/children` | List the child ABHA accounts linked to this account |

### ABHA creation, driving licence or PAN

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v3/enrollment/enrol/byDocument` | Create an ABHA from an identity document |

### ABHA Profile

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/profile/account/request/emailVerificationLink` | Send Email Verification Link |

### ABHA QR code

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/v3/profile/account/abha-card` | Get the ABHA card |
| `GET` | `/v3/profile/account/download-abha-card` | Download the ABHA card as a file |
| `GET` | `/v3/profile/account/qrCode` | Get the ABHA QR code |

### ABHA verification, Aadhaar OTP

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v3.1/profile/login/request/otp` | Send a login OTP, v3.1 |
| `POST` | `/v3.1/profile/login/verify` | Verify a login OTP, v3.1 |

### ABHA verification, mobile OTP

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v3/profile/login/request/otp` | Send a login OTP |
| `POST` | `/v3/profile/login/verify` | Verify a login OTP and get a user token |
| `POST` | `/v3/profile/login/verify/user` | Choose which ABHA to sign in to |

### Authentication

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/profile/public/certificate` | Get RSA Public Certificate |

### bridge

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v4/int/v1/bridges/MutipleHRPAddUpdateServices` | Register / Update Bridge Services (HIU) |

### Fetch ABHA by Aadhaar number

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/v3/profile/benefit/abha/{abhaNumber}` | Get the benefit record for an ABHA number |
| `GET` | `/v3/profile/benefit/abha/search/insurance/{abhaNumber}` | Find insurance cover recorded against an ABHA number |
| `GET` | `/v3/profile/benefit/abha/statedistrict/{abhaNumber}` | Get the state and district recorded against an ABHA number |
| `POST` | `/v3/profile/benefit/linkAndDelink` | Link or unlink a benefit record from an ABHA |
| `POST` | `/v3/profile/benefit/search` | Search benefit records for a person |
| `GET` | `/v3/profile/benefit/search/aadhaarByAbha` | Find the Aadhaar number behind an ABHA number |
| `GET` | `/v3/profile/benefit/search/abhaByAadhaar` | Find an ABHA number from an Aadhaar number |

### Fetch ABHA by mobile number

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v3/profile/account/abha/search` | Find an ABHA for somebody who does not know theirs |

### Gateway & Bridge

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/.well-known/openid-configuration` | Get OIDC Discovery Document |
| `GET` | `/api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId}` | Find Bridge Service by Service ID |
| `GET` | `/api/hiecm/gateway/v3/bridge-services` | List All Bridge Services |
| `PATCH` | `/api/hiecm/gateway/v3/bridge/url` | Update HIP/HIU Bridge Callback URL |
| `GET` | `/api/hiecm/gateway/v3/certs` | Get Gateway JWKS Certificates |
| `POST` | `/v1/bridges/MutipleHRPAddUpdateServices` | Register / Update HIP-HIU Services (Facility Registry) |

### Login & Verification

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/profile/login/search` | Search ABHA Profile (for Password Login) |

### PHR & ABHA Address

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/phr/web/login/abha/request/otp` | Send OTP for ABHA Address Login |
| `POST` | `/phr/web/login/abha/search` | Search ABHA Address, Get Auth Methods |
| `POST` | `/phr/web/login/abha/verify` | Verify OTP / Biometric for ABHA Address Login |
| `GET` | `/phr/web/login/profile/abha-profile` | Get PHR Profile |
| `GET` | `/phr/web/login/profile/abha/phr-card` | Download PHR Card |
| `GET` | `/phr/web/login/profile/abha/qr-code` | Download PHR QR Code |

### Profile update

| Method | Path | What it does |
| --- | --- | --- |
| `PATCH` | `/v3/profile/account` | Update fields on an ABHA profile |
| `POST` | `/v3/profile/account/request/otp` | Send an OTP to change something on the profile |
| `POST` | `/v3/profile/account/verify` | Verify the OTP for a profile change |

### Provider directory

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/govt-programs` | List government programs |
| `GET` | `/api/hiecm/gateway/v3/health-lockers` | List health-locker-enabled providers |
| `GET` | `/api/hiecm/gateway/v3/providers` | List providers by name |
| `GET` | `/api/hiecm/gateway/v3/providers/{provider-id}` | Get a provider by id |

### Scan & Share

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/patient-share/v3/on-share` | Send Share Acknowledgement (HIP → Gateway) |
| `POST` | `/patient-share/v3/share` | Receive a patient's shared profile |

### Session and tokens

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/hiecm/gateway/v3/sessions` | Create a session and get an access token |
| `POST` | `/v3/phr/app/enrollment/encrypt` | Encrypt a value with the ABDM public key |
| `GET` | `/v3/profile/account/request/logout` | Log the person out and invalidate their user token |
| `GET` | `/v3/profile/account/request/token` | Get a new user token from a refresh token |

### Share patient profile

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/v3/profile/account` | Read the signed in person's ABHA profile |
## Headers

| Header | What it is |
| --- | --- |
| `REQUEST-ID` | Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every cal… |
| `TIMESTAMP` | ISO 8601 UTC timestamp of the request. |
| `BENEFIT_NAME` | The benefit scheme an enrolment belongs to. Send `healthid api` on the enrol and search calls, and `healthid`… |
| `X-token` | The user scoped token returned when a person logs in or verifies an OTP. Profile calls act on one account, so… |
| `TRANSACTION_ID` | The enrolment transaction this call belongs to, when the transaction is not carried in the body. |
| `T-token` | The transaction token that carries state between the two halves of a login. Returned by the verify call and s… |
| `healthIdNumber` | The 14 digit ABHA number, sent plain in the recorded request, in the dashed `91-XXXX-XXXX-XXXX` form. |
| `aadhaarNumber` | The person's Aadhaar number, RSA encrypted against the ABDM public key and sent as a header rather than in a … |
| `X-CM-ID` | Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. Sending the wrong on… |
| `KEY_TYPE` | Which ABDM public key the encryption helper should use. |
| `R-token` | The refresh token, sent when asking for a new user token without making the person log in again. Required for… |
## A request, in full

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'BENEFIT_NAME: healthid api' \
  --header 'X-token: Bearer <X_TOKEN_FROM_LOGIN_VERIFY>' \
  --header 'Content-Type: application/json' \
  --data '{
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
