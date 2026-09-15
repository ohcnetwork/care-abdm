# Integrate M3, consent and fetching

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://dev.abdm.gov.in` Sandbox. Pair it with the `X-CM-ID: sbx` header.
- `https://apis.abdm.gov.in` Production. Pair it with the `X-CM-ID: abdm` header.
- `https://dev.abdm.gov.in/api` ABDM Gateway (Dev / Sandbox)
- `https://apis.abdm.gov.in/api` ABDM Gateway (Production)
- `https://apihspsbx.abdm.gov.in` HSP Registry (Sandbox)
## Endpoints

25 operations, grouped by the journey they belong to.

### bridge

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v4/int/v1/bridges/MutipleHRPAddUpdateServices` | Register / Update Bridge Services (HIU) |

### consent

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/hiecm/consent/v3/fetch` | Fetch the full consent artefact |
| `POST` | `/hiecm/consent/v3/request/hiu/on-notify` | Acknowledge a consent notification, as the HIU |
| `POST` | `/hiecm/consent/v3/request/init` | Initiate a consent request |
| `POST` | `/hiecm/consent/v3/request/status` | Check the status of a consent request |

### data-retrieval

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/hiecm/data-flow/v3/health-information/notify` | Notify the gateway that data was received |
| `POST` | `/hiecm/data-flow/v3/health-information/request` | Request a patient's health information |
| `GET` | `/hiecm/data-flow/v3/health-information/request/status/{transaction-id}` | Health Information Request Status |

### Gateway & Bridge

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/.well-known/openid-configuration` | Get OIDC Discovery Document |
| `GET` | `/api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId}` | Find Bridge Service by Service ID |
| `GET` | `/api/hiecm/gateway/v3/bridge-services` | List All Bridge Services |
| `PATCH` | `/api/hiecm/gateway/v3/bridge/url` | Update HIP/HIU Bridge Callback URL |
| `GET` | `/api/hiecm/gateway/v3/certs` | Get Gateway JWKS Certificates |

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

### webhooks

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/v3/consent/request/hip/notify` | The patient's decision, sent to the record holder |
| `POST` | `/api/v3/hiu/consent/on-fetch` | The consent artefact detail, fetched by artefact id |
| `POST` | `/api/v3/hiu/consent/request/notify` | The patient's decision, sent to the requester |
| `POST` | `/api/v3/hiu/consent/request/on-init` | The consent request was accepted, with its request id |
| `POST` | `/api/v3/hiu/consent/request/on-status` | The consent manager reports the state of a consent request you asked about. |
| `POST` | `/api/v3/hiu/health-information/on-request` | Acknowledgement of a health information request |
| `POST` | `/health-information/transfer` | The encrypted health data itself, pushed to the URL you supplied |
## Headers

| Header | What it is |
| --- | --- |
| `REQUEST-ID` | A fresh UUID that you generate for this request. The callback that answers it carries the same value. In M3 a… |
| `TIMESTAMP` | The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose t… |
| `X-CM-ID` | Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. |
| `X-HIU-ID` | Identifier of the health information user the request or callback is intended for. This is per facility, and … |
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
