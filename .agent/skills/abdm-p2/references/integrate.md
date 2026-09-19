# Integrate P2, PHR management

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://abhasbx.abdm.gov.in` ABHA service, sandbox
- `https://dev.abdm.gov.in` ABDM gateway, sandbox
- `https://apis.abdm.gov.in` ABDM gateway, production
## Endpoints

43 operations, grouped by the journey they belong to.

### Other operations

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/abha/api/v3/phr/app/login/profile` | Get Profile |
| `POST` | `/abha/api/v3/phr/app/login/profile/link` | 2 flows: Link Request |
| `GET` | `/abha/api/v3/phr/app/login/profile/phrCard` | Get PHR Card |
| `GET` | `/abha/api/v3/phr/app/login/profile/qrCode` | Get QR Code |
| `GET` | `/abha/api/v3/phr/app/login/profile/request/logout` | Logout |
| `POST` | `/abha/api/v3/phr/app/login/profile/request/otp` | 4 flows: Send OTP - Update Email, Send OTP - Update Mobile, Send ABHA OTP - Lin… |
| `GET` | `/abha/api/v3/phr/app/login/profile/request/token` | Refresh Token |
| `GET` | `/abha/api/v3/phr/app/login/profile/switch-profile` | Switch Profile |
| `POST` | `/abha/api/v3/phr/app/login/profile/updateProfile` | Update Profile |
| `POST` | `/abha/api/v3/phr/app/login/profile/verify` | 5 flows: Verify OTP - Update Email, Verify OTP - Update Mobile, Verify Password… |
| `POST` | `/abha/api/v3/phr/app/login/profile/verify/switch-profile/user` | Verify User Switch Profile |
| `GET` | `/api/hiecm/consent/v3/artefact` | Fetch all the consent artefact details of a patient. |
| `GET` | `/api/hiecm/consent/v3/artefact/{artefact-id}` | Fetch the consent artefact details associated with the artefact-ID. |
| `GET` | `/api/hiecm/consent/v3/artefact/request/{request-id}` | Fetch all the consent artefact details associated with a consent request REQUES… |
| `POST` | `/api/hiecm/consent/v3/auto/approve` | Setup an auto-approval policy for given HIU. |
| `POST` | `/api/hiecm/consent/v3/auto/approve/{auto-approval-id}/disable` | Disable the auto-approval policy. |
| `POST` | `/api/hiecm/consent/v3/auto/approve/{auto-approval-id}/enable` | Enable the auto-approval policy. |
| `GET` | `/api/hiecm/consent/v3/request` | Fetch all the consent request details of a patient. |
| `GET` | `/api/hiecm/consent/v3/request/{request-id}` | Get the consent request details by REQUEST-ID. |
| `POST` | `/api/hiecm/consent/v3/request/{request-id}/approve` | Approve the consent request raised by HIU from PHR/mobile application. |
| `POST` | `/api/hiecm/consent/v3/request/{request-id}/deny` | Deny the consent request raised by HIU from PHR/mobile application. |
| `POST` | `/api/hiecm/consent/v3/revoke` | Revoke the granted consent from PHR/mobile application. |
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
| `GET` | `/api/hiecm/hip/v3/link/patient/links` | This is the PHR APP API, this API will used to fetch all link care-context for … |
| `GET` | `/api/hiecm/patient-share/v3/profile/getTokenDetails` | Get the historical token numbers of the patient |
| `POST` | `/api/hiecm/patient-share/v3/share` | Be invoked from the PHR-HIU application for sharing the patient/user profile wi… |
| `POST` | `/api/hiecm/user-initiated-linking/v3/link/care-context/confirm` | Confirm his/her health records. |
| `POST` | `/api/hiecm/user-initiated-linking/v3/link/care-context/init` | Link his/her health records. |
| `POST` | `/api/hiecm/user-initiated-linking/v3/patient/care-context/discover` | Discover his/her health records. |
| `POST` | `/api/v3/hiu/patient/care-context/on-confirm` | Receive confirmation of the linked care contexts for a patient. It provides det… |
| `POST` | `/api/v3/hiu/patient/care-context/on-discover` | Receive the discovered care contexts of a patient. It provides detailed informa… |
| `POST` | `/api/v3/hiu/patient/care-context/on-init` | Receive the initial linking of care contexts for a patient. It provides detaile… |
| `POST` | `/api/v3/hiu/patient/on-share` | This API will be invoked to the HIU for sharing the response of HIECM's /api/hi… |
## Headers

| Header | What it is |
| --- | --- |
| `X-token` |  |
| `REQUEST-ID` | Unique UUID for each request. |
| `TIMESTAMP` | Request timestamp in UTC, ISO-8601 with Z. |
| `R-token` |  |
| `T-token` |  |
| `X-CM-ID` | Suffix of the consent manager to which the request was intended |
| `X-AUTH-TOKEN` | JWT Authentication token which was issued by ABDM after successful validation of username and password |
| `X-HIU-ID` | Identifier of the health information user to which the request was intended |
## A request, in full

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/profile \
  --header 'X-token: Bearer <JWT TOKEN>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```
