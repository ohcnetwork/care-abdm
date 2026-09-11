# Integrate P1, PHR identity and profile

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://dev.abdm.gov.in` Sandbox. Pair it with the `X-CM-ID: sbx` header.
- `https://apis.abdm.gov.in` Production. Pair it with the `X-CM-ID: abdm` header.
- `https://phrsbx.abdm.gov.in` Sandbox host, not yet confirmed.
- `https://phr.abdm.gov.in` Production.
## Endpoints

74 operations, grouped by the journey they belong to.

### bridge

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v4/int/v1/bridges/MutipleHRPAddUpdateServices` | Register / Update Bridge Services (HIU) |

### digilocker_apis

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/digi-locker/account` | 02 - Get DigiLocker Account [GET] |
| `GET` | `/digi-locker/getCode` | 03 - Get Access Token / OAuth Callback [GET] |
| `GET` | `/digi-locker/hip/pull/records` | 10 - Get HIP Refresh Records [GET] |
| `POST` | `/digi-locker/incoming/records` | 08 - Fetch Incoming Records Bundle [POST] |
| `POST` | `/digi-locker/incoming/records/list` | 07 - Fetch Incoming Records List [POST] |
| `POST` | `/digi-locker/pull/records` | 09 - Pull / Refresh Records [POST] |
| `GET` | `/digi-locker/records/list` | 01 - Get Health Records List [GET] |
| `GET` | `/digi-locker/records/read` | 06 - Read Uploaded Record [GET] |
| `GET` | `/digi-locker/status` | 04 - Get Account Status [GET] |
| `POST` | `/digi-locker/upload` | 05 - Upload Record [POST] |

### family_management

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/family-management/assign` | assign |
| `PUT` | `/api/family-management/delink` | delink |
| `GET` | `/api/family-management/get-relationship-types` | Get Relationship Types |
| `GET` | `/api/family-management/linked-by-me` | linked-by-me |
| `GET` | `/api/family-management/linked-to-me` | linked-to-me |
| `PUT` | `/api/family-management/reassign` | reassign |
| `PUT` | `/api/family-management/unassign` | unassign |
| `POST` | `/family-management/verify-and-assign` | verify and assign |

### Gateway & Bridge

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/.well-known/openid-configuration` | Get OIDC Discovery Document |
| `GET` | `/api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId}` | Find Bridge Service by Service ID |
| `GET` | `/api/hiecm/gateway/v3/bridge-services` | List All Bridge Services |
| `PATCH` | `/api/hiecm/gateway/v3/bridge/url` | Update HIP/HIU Bridge Callback URL |
| `GET` | `/api/hiecm/gateway/v3/certs` | Get Gateway JWKS Certificates |

### global_collection

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/global/get/session` | Session-Token |
| `GET` | `/api/global/phr/public-certificate` | Certificate |
| `GET` | `/global/lgd/district` | Get District with stateCode |
| `GET` | `/global/lgd/search` | Get lgd with pincode |
| `GET` | `/global/lgd/state` | Get States |
| `GET` | `/global/providers/000` | getProvidersByID |

### login

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/abha/api/v3/phr/app/enrollment/encrypt` | ENCRYPTION |
| `POST` | `/abha/api/v3/phr/app/login/profile/abha/verify` | Update mobile verify OTP |
| `POST` | `/api/hiecm/gateway/v3/sessions` | Session API |
| `POST` | `/login/phr/isKycVerified` | IsKycVerified |
| `POST` | `/login/phr/request/otp` | OTP Request - AADHAR OTP |
| `POST` | `/login/phr/search` | Search Auth Methods - ABHAAddress |
| `POST` | `/login/phr/verify` | Login OTP Verify - AADHAR |
| `POST` | `/login/phr/verify/user` | Verify - User |
| `POST` | `/profile/abha/request/otp` | Update mobile request OTP |

### profile

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/login/profile/request/otp` | Send ABHA Otp - Link-DeLink |
| `POST` | `/login/profile/abha/de-link` | De-Link Request |
| `POST` | `/login/profile/request/otp` | Send AADHAAR Otp - Link-DeLink |
| `POST` | `/login/profile/verify` | Verify AADHAAR Otp - Link-DeLink |
| `GET` | `/notification/get-notification` | Get notifications |
| `GET` | `/profile/phr` | Get Profile |
| `GET` | `/profile/phr/card` | Get PHR Card |
| `POST` | `/profile/phr/link` | Link Request |
| `GET` | `/profile/phr/qr-code` | Get QR Code |
| `GET` | `/profile/phr/request/logout` | Logout |
| `POST` | `/profile/phr/request/otp` | Send ABHA OTP |
| `GET` | `/profile/phr/request/token` | Refresh Token |
| `POST` | `/profile/phr/set-preferred/abha-address` | Set the preferred ABHA address |
| `GET` | `/profile/phr/switch-profile` | Switch Profile |
| `POST` | `/profile/phr/update` | Update Profile |
| `POST` | `/profile/phr/verify` | Verify ABHA OTP |
| `POST` | `/profile/phr/verify/switch-profile/user` | Verify User Switch Profile |

### Provider directory

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/govt-programs` | List government programs |
| `GET` | `/api/hiecm/gateway/v3/health-lockers` | List health-locker-enabled providers |
| `GET` | `/api/hiecm/gateway/v3/providers` | List providers by name |
| `GET` | `/api/hiecm/gateway/v3/providers/{provider-id}` | Get a provider by id |

### registration

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/registration/abha/custom/phr/create` | 4. Create Custom PHR Address |
| `POST` | `/api/registration/abha/request/otp` | 1. Request OTP for an ABHA registration |
| `GET` | `/api/registration/abha/suggestion` | 5. Get PHR Suggestions |
| `POST` | `/api/registration/abha/verify/aadhaar` | 2. Verify Aadhaar |
| `POST` | `/api/registration/abha/verify/auth` | 3. Verify Auth |
| `GET` | `/api/registration/phr/exists` | 4. Check PHR Address Existence |
| `GET` | `/api/registration/phr/lgd/district` | 2. Get Districts by State Code |
| `GET` | `/api/registration/phr/lgd/search` | 3. Search LGD by Pin Code |
| `GET` | `/api/registration/phr/lgd/state` | 1. Get All States |
| `POST` | `/api/registration/phr/register/details` | 5. Register Details |
| `POST` | `/api/registration/phr/request/otp` | 1. Request OTP for a PHR registration |
| `POST` | `/api/registration/phr/suggestion` | 3. PHR Address Suggestion |
| `POST` | `/api/registration/phr/verify/otp` | 2. Verify OTP |

### Session and tokens

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/hiecm/gateway/v3/sessions` | Create a session and get an access token |
## Headers

| Header | What it is |
| --- | --- |
| `REQUEST-ID` | A fresh UUID that you generate for this request. It is how you and the gateway correlate a call with its call… |
| `TIMESTAMP` | The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose t… |
| `X-CM-ID` | Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. Sending the wrong on… |
## A request, in full

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/v4/int/v1/bridges/MutipleHRPAddUpdateServices \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "IN07100XXXXX",
  "facilityName": "City Health HIU",
  "HRP": [
    {
      "bridgeId": "BRIDGE_HIU_001",
      "hipName": "City Health HIU",
      "type": "HIU",
      "active": true
    }
  ]
}'
```
