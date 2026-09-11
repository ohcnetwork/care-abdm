# Integrate M2, linking and sharing

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://dev.abdm.gov.in` Sandbox. Pair it with the `X-CM-ID: sbx` header.
- `https://apis.abdm.gov.in` Production. Pair it with the `X-CM-ID: abdm` header.
- `https://dev.abdm.gov.in/api` ABDM Gateway (Dev / Sandbox)
- `https://apihspsbx.abdm.gov.in` HSP Registry (Sandbox)
## Endpoints

31 operations, grouped by the journey they belong to.

### bridge

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v4/int/v1/bridges/MutipleHRPAddUpdateServices` | Register / Update Bridge Services (HIU) |

### data-transfer

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/hiecm/consent/v3/request/hip/on-notify` | Acknowledge a consent notification, as the HIP |
| `POST` | `/hiecm/data-flow/v3/health-information/hip/on-request` | Acknowledge a health information data request |
| `POST` | `/hiecm/data-flow/v3/health-information/notify` | Notify the gateway that a data transfer finished |

### deep-linking

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/hiecm/hip/v3/link/patient/links/sms/notify2` | Send an SMS with a deep link to the ABHA App |

### Gateway & Bridge

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/.well-known/openid-configuration` | Get OIDC Discovery Document |
| `GET` | `/api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId}` | Find Bridge Service by Service ID |
| `GET` | `/api/hiecm/gateway/v3/bridge-services` | List All Bridge Services |
| `PATCH` | `/api/hiecm/gateway/v3/bridge/url` | Update HIP/HIU Bridge Callback URL |
| `GET` | `/api/hiecm/gateway/v3/certs` | Get Gateway JWKS Certificates |

### hip-linking

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/hiecm/hip/v3/link/carecontext` | Link care contexts to an ABHA address |
| `POST` | `/hiecm/hip/v3/link/context/notify` | Link Care Context Notify |
| `POST` | `/hiecm/v3/token/generate-token` | Generate Link Token |

### Provider directory

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/govt-programs` | List government programs |
| `GET` | `/api/hiecm/gateway/v3/health-lockers` | List health-locker-enabled providers |
| `GET` | `/api/hiecm/gateway/v3/providers` | List providers by name |
| `GET` | `/api/hiecm/gateway/v3/providers/{provider-id}` | Get a provider by id |

### Session and tokens

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/hiecm/gateway/v3/sessions` | Create a session and get an access token |

### user-linking

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/hiecm/user-initiated-linking/v3/link/care-context/on-confirm` | Link On-Confirm, HIP confirms linked care contexts |
| `POST` | `/hiecm/user-initiated-linking/v3/link/care-context/on-init` | Link On-Init, HIP responds with OTP communication details |
| `POST` | `/hiecm/user-initiated-linking/v3/patient/care-context/on-discover` | On Discovery, HIP responds with found care contexts |

### webhooks

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api-hiu/data/notification` | The provider pushes encrypted health information to the URL named in the reques… |
| `POST` | `/api/v3/hip/health-information/request` | A request for the records a consent covers |
| `POST` | `/api/v3/hip/link/care-context/confirm` | Confirmation of a link, carrying the token the patient approved |
| `POST` | `/api/v3/hip/link/care-context/init` | A request to start linking a care context |
| `POST` | `/api/v3/hip/patient/care-context/discover` | A discovery request for a patient you may hold records for |
| `POST` | `/v0.5/consents/hiu/notify` | A consent notification to an HIU bridge |
| `POST` | `/v3/hip/token/on-generate-token` | The link token m2_generate_link_token generated, or why it failed |
| `POST` | `/v3/link/on_carecontext` | The outcome of a care context linking call you made |
| `POST` | `/v3/links/context/on-notify` | The outcome of a care context notify call you made |
| `POST` | `/v3/patients/sms/on-notify` | The outcome of an SMS deep link notify call you made |
## Headers

| Header | What it is |
| --- | --- |
| `REQUEST-ID` | A fresh UUID that you generate for this request. The callback that answers it carries the same value, so this… |
| `TIMESTAMP` | The current time in ISO 8601, UTC, with milliseconds and a `Z` suffix, from a synchronised clock. The sandbox… |
| `X-CM-ID` | Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. A dedicated error co… |
| `X-HIP-ID` | Identifier of the Health Information Provider the request or callback belongs to. |
| `X-Link-Token` | Short-lived link token generated via POST /hiecm/v3/token/generate-token |
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
