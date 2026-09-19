# Integrate P1, PHR registration and login

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://abhasbx.abdm.gov.in` ABHA service, sandbox
- `https://dev.abdm.gov.in` ABDM gateway, sandbox
- `https://apis.abdm.gov.in` ABDM gateway, production
## Endpoints

22 operations, grouped by the journey they belong to.

### Other operations

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/abha/api/v3/phr/app/enrollment/enrol` | 3 flows: Enrol ABHA Address |
| `GET` | `/abha/api/v3/phr/app/enrollment/isExists` | 3 flows: isExists API, isExists API Copy |
| `POST` | `/abha/api/v3/phr/app/enrollment/request/otp` | 3 flows: OTP Request - Mobile, OTP Request - ABHA OTP, OTP Request - AADHAR OTP |
| `POST` | `/abha/api/v3/phr/app/enrollment/suggestion` | 3 flows: Suggestion API |
| `POST` | `/abha/api/v3/phr/app/enrollment/verify` | 3 flows: OTP Verify - Mobile, OTP Verify - ABHA OTP, OTP Verify - AADHAR OTP |
| `GET` | `/abha/api/v3/phr/app/login/public/certificate` | PHR Certificate |
| `POST` | `/abha/api/v3/phr/app/login/request/otp` | 7 flows: OTP Request - Mobile, OTP Request - Email, OTP Request - ABHAADDRES Mo… |
| `POST` | `/abha/api/v3/phr/app/login/search` | Search Auth Methods - ABHAAddress |
| `POST` | `/abha/api/v3/phr/app/login/verify` | 8 flows: Login OTP Verify - Mobile, Login OTP Verify - Email, Login OTP Verify … |
| `POST` | `/abha/api/v3/phr/app/login/verify/user` | 6 flows: Verify User, Verify - User |
| `POST` | `/abha/api/v3/profile/account/request/emailVerificationLink` | Email Verification Link |
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
| `REQUEST-ID` | Unique UUID for each request. |
| `TIMESTAMP` | Request timestamp in UTC, ISO-8601 with Z. |
| `T-token` |  |
| `X-token` |  |
| `X-CM-ID` | Suffix of the consent manager to which the request was intended |
## A request, in full

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
