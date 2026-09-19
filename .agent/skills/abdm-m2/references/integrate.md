# Integrate M2, linking and sharing

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://dev.abdm.gov.in` ABDM gateway, sandbox
- `https://apis.abdm.gov.in` ABDM gateway, production
## Endpoints

32 operations, grouped by the journey they belong to.

### Other operations

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/hiecm/consent/v3/request/hip/on-notify` | Acknowledge the notification sent when a consent request is approved/revoked/ex… |
| `POST` | `/api/hiecm/data-flow/v3/health-information/hip/on-request` | Health information data request acknowledgement from HIP. |
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
| `POST` | `/api/hiecm/hip/v3/link/carecontext` | Perform HIP initiated linking. |
| `POST` | `/api/hiecm/hip/v3/link/context/notify` | Notify CM about any update on the already linked care context for a patient. |
| `POST` | `/api/hiecm/hip/v3/link/patient/links/sms/notify2` | Send SMS notification to patient that a care context is linked. |
| `POST` | `/api/hiecm/patient-share/v3/on-share` | Sharing the response of HIECM's /api/hiecm/patient-share/v3/on-share API |
| `POST` | `/api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm` | Sharing the response of /api/hiecm/user-initiated-linking/v3/link/care-context/… |
| `POST` | `/api/hiecm/user-initiated-linking/v3/link/care-context/on-init` | As a result of the initialization, HIP has to generate a unique reference-numbe… |
| `POST` | `/api/hiecm/user-initiated-linking/v3/patient/care-context/on-discover` | HMIS/LIMS/HIP has to ensure that only unlinked records of the patient has to be… |
| `POST` | `/api/hiecm/v3/token/generate-token` | Generate link token to link the health records |
| `POST` | `/api/v3/consent/request/hip/notify` | This is a callback API to notify HIP when consent is APPROVED or REVOKED. |
| `POST` | `/api/v3/hip/health-information/request` | Health information data request to HIP. |
| `POST` | `/api/v3/hip/link/care-context/confirm` | Confirm the linking of care contexts for a patient. It allows healthcare inform… |
| `POST` | `/api/v3/hip/link/care-context/init` | Initiate the linking of care contexts for a patient. It allows healthcare infor… |
| `POST` | `/api/v3/hip/patient/care-context/discover` | Discover care contexts associated with a patient. It allows healthcare informat… |
| `POST` | `/api/v3/hip/patient/share` | This API will be invoked to the HIP for sharing the response of HIECM's /api/hi… |
| `POST` | `/api/v3/hip/token/on-generate-token` | This is a call back API of [/api/hiecm/v3/token/generate-token]. |
| `POST` | `/api/v3/link/on_carecontext` | Is a callback API that will be called by HIE-CM. The response will be received … |
| `POST` | `/api/v3/links/context/on-notify` | This API endpoint is a call back API for /api/hiecm/hip/v3/link/context/notify … |
| `POST` | `/api/v3/patients/sms/on-notify` | This API endpoint is a call back API for /api/hiecm/hip/v3/link/patient/links/s… |
| `POST` | `/health-information/transfer` | health information transfer API |
## Headers

| Header | What it is |
| --- | --- |
| `REQUEST-ID` | Unique UUID for track the end to end request transaction |
| `TIMESTAMP` | Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, follow… |
| `X-CM-ID` | Suffix of the consent manager to which the request was intended |
| `X-HIP-ID` | Identifier of the health information provider to which the request was intended |
| `X-LINK-TOKEN` | JWT Authentication token which was issued by ABDM after successful validation of username and password |
## A request, in full

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/hip/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "OK",
    "consentId": "e3c74829-3f82-4f94-959e-e10f57bcd57b"
  },
  "error": {
    "code": "ABDM-1001",
    "message": "unable to connect database"
  },
  "response": {
    "requestId": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"
  }
}'
```
