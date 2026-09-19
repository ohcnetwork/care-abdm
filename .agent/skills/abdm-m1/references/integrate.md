# Integrate M1, ABHA identity

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://abhasbx.abdm.gov.in` ABHA service, sandbox
- `https://dev.abdm.gov.in` ABDM gateway, sandbox
- `https://apis.abdm.gov.in` ABDM gateway, production
## Endpoints

41 operations, grouped by the journey they belong to.

### Other operations

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/abha/api/v3/enrollment/auth/byAbdm` | UseCase: Verify- Mobile OTP |
| `POST` | `/abha/api/v3/enrollment/enrol/abha-address` | UseCase: Create ABHA address |
| `POST` | `/abha/api/v3/enrollment/enrol/auth/init` | UseCase: It will generate the Transaction ID. This Transaction ID will be used … |
| `POST` | `/abha/api/v3/enrollment/enrol/byAadhaar` | UseCase: Create ABHA number Via Aadhaar by verifying Aadhaar OTP, using Biometr… |
| `POST` | `/abha/api/v3/enrollment/enrol/capturePID` | UseCase: This API is used to check the status of the transaction ID. |
| `GET` | `/abha/api/v3/enrollment/enrol/suggestion` | UseCase: ABHA address suggestion |
| `GET` | `/abha/api/v3/enrollment/profile/children` | UseCase: Get Child ABHA address |
| `POST` | `/abha/api/v3/enrollment/request/otp` | Use Case: ABHA enrolment - Send OTP using Aadhaar number Mobile number, ABHA nu… |
| `POST` | `/abha/api/v3/phr/web/login/abha/request/otp` | Use Case: Sends an OTP to the Mobile Number, Aadhaar Number, Request Biometric … |
| `POST` | `/abha/api/v3/phr/web/login/abha/search` | Use Case: Search ABHA Profile using ABHA address |
| `POST` | `/abha/api/v3/phr/web/login/abha/verify` | Use Case: Verify OTP - Aadhaar Number, Mobile Number, Verify via Biometric |
| `GET` | `/abha/api/v3/phr/web/login/profile/abha-profile` | Use Case: Retrieves the user’s ABHA Profile |
| `GET` | `/abha/api/v3/phr/web/login/profile/abha/phr-card` | Use Case: Generate a PHR Card Profile |
| `GET` | `/abha/api/v3/phr/web/login/profile/abha/qr-code` | Use Case: Generate QR Code By Passing X-token to share user ABHA address Profil… |
| `GET` | `/abha/api/v3/profile/account` | Use Case: Get User Profile Details |
| `PATCH` | `/abha/api/v3/profile/account` | Use Case: Update the user ABHA Profile Photo, Update the Child ABHA Profile |
| `GET` | `/abha/api/v3/profile/account/abha-card` | Use Case: Retrieve ABHA Card image |
| `POST` | `/abha/api/v3/profile/account/abha/search` | Use Case: Search ABHA Profile |
| `GET` | `/abha/api/v3/profile/account/qrCode` | Use Case: Generate QR Code for an ABHA Profile |
| `POST` | `/abha/api/v3/profile/account/request/otp` | Use Case: Send OTP - ReKyc, Update Mobile, Child ABHA KYC Request OTP |
| `GET` | `/abha/api/v3/profile/account/request/token` | Use Case: Request a token for accessing a user’s ABHA |
| `POST` | `/abha/api/v3/profile/account/verify` | Use Case: Verify OTP - ReKyc, Update Mobile, CHILD ABHA KYC |
| `GET` | `/abha/api/v3/profile/benefit/abha/{abhanumber}` | Use Case: Retrieve the benefit details associated with a specific ABHA number |
| `POST` | `/abha/api/v3/profile/benefit/linkAndDelink` | Usecase: Benefit LINK or DELINK |
| `POST` | `/abha/api/v3/profile/benefit/search` | Use Case: Search for benefits associated with a user’s profile |
| `POST` | `/abha/api/v3/profile/login/request/otp` | Use Case: ABHA Login - Send OTP using Aadhaar number, ABHA number, Mobile numbe… |
| `POST` | `/abha/api/v3/profile/login/search` | Use Case: Search ABHA Account Existence |
| `POST` | `/abha/api/v3/profile/login/verify` | Use Case: ABHA Login - Verify OTP using Aadhaar number, ABHA number, Mobile num… |
| `POST` | `/abha/api/v3/profile/login/verify/user` | Use Case: This API is used to verify and confirm the selected ABHA user during … |
| `GET` | `/abha/api/v3/profile/public/certificate` | Use Case: Used to Fetch Public Key |
| `GET` | `/api/hiecm/gateway/v3/.well-known/openid-configuration` | Get the open ID configuration. |
| `PUT` | `/api/hiecm/gateway/v3/bridge-service` | v3/gateway/bridge-service |
| `GET` | `/api/hiecm/gateway/v3/bridge-service/serviceId/{service-id}` | Fetch the details of a service ID. |
| `GET` | `/api/hiecm/gateway/v3/bridge-services` | Fetch the service ids registered against a bridge. |
| `PATCH` | `/api/hiecm/gateway/v3/bridge/url` | Update the bridge URL. |
| `GET` | `/api/hiecm/gateway/v3/certs` | Get the certificate information. |
| `GET` | `/api/hiecm/gateway/v3/govt-programs` | Fetch the list of govt programmes. |
| `GET` | `/api/hiecm/gateway/v3/health-lockers` | Fetch the record with health locker enabled provider details. |
| `GET` | `/api/hiecm/gateway/v3/providers` | Fetch the list of providers filtered by name. |
| `GET` | `/api/hiecm/gateway/v3/providers/{provider-id}` | Fetch the record for provider details for requested provider ID. |
| `POST` | `/api/hiecm/gateway/v3/sessions` | Generate Keycloak token/access token. |
## Headers

| Header | What it is |
| --- | --- |
| `REQUEST-ID` |  |
| `TIMESTAMP` |  |
| `BENEFIT_NAME` | **Applicable for user who is enrolling via Benefit Program.** |
| `X-token` | **Applicable for child abha creation. X-token of Parent user, user can get X-token after login to the system** |
| `TRANSACTION_ID` |  |
| `Content-Type` |  |
| `R-token` |  |
| `T-token` |  |
| `X-CM-ID` | Suffix of the consent manager to which the request was intended |
## A request, in full

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
