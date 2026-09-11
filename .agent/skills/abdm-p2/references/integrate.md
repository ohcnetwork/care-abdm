# Integrate P2, PHR linking and records

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://dev.abdm.gov.in` Sandbox. Pair it with the `X-CM-ID: sbx` header.
- `https://apis.abdm.gov.in` Production. Pair it with the `X-CM-ID: abdm` header.
- `https://phrsbx.abdm.gov.in` Sandbox host, not yet confirmed.
- `https://phr.abdm.gov.in` Production.
## Endpoints

60 operations, grouped by the journey they belong to.

### bridge

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v4/int/v1/bridges/MutipleHRPAddUpdateServices` | Register / Update Bridge Services (HIU) |

### care_context_link

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/care-context-link/bookmark/{careContextLinkId}` | Bookmark Care Context |
| `GET` | `/api/care-context-link/care-context-link/fetch` | Get Care Context Links |
| `GET` | `/api/care-context-link/care-context/bundle-url/{careContextLinkId}` | Fetch Care Context Bundle URL |
| `GET` | `/api/care-context-link/fetch/hips` | Get Linked HIPs |
| `GET` | `/api/care-context-link/file/details` | Get File Metadata |
| `GET` | `/api/care-context-link/file/download` | Download File Chunk |
| `GET` | `/api/care-context-link/get-hip-ids` | Get HIP IDs |
| `GET` | `/api/care-context-link/get/data-flow-part/{transactionId}` | Get Data Flow Part Status |
| `GET` | `/api/care-context-link/get/health-information/{transactionId}` | Get Health Information by Transaction ID |
| `POST` | `/api/care-context-link/health-information/on-request` | Health Information On-Request Callback |
| `POST` | `/api/care-context-link/link/get-links` | Get Links by HIP |
| `GET` | `/api/care-context-link/link/patient/links` | Get All Linked Care Contexts |
| `POST` | `/api/care-context-link/my-record/bookmark` | Add My Record Bookmark |
| `DELETE` | `/api/care-context-link/my-record/bookmark` | Delete My Record Bookmark |
| `POST` | `/api/care-context-link/my-records/fetch/all` | Get All Care Context Links for ABHA Address |
| `POST` | `/api/care-context-link/patient/consent-request` | Post Patient Consent Request |
| `POST` | `/api/care-context-link/patient/health-information/fetch` | Fetch Patient Health Information |
| `POST` | `/api/care-context-link/patient/health-information/pull` | Pull Patient Health Information |
| `POST` | `/api/care-context-link/patient/health-information/refresh` | Refresh Patient Health Information |
| `POST` | `/api/care-context-link/patient/health-information/status` | Fetch Health Information Status |
| `POST` | `/api/care-context-link/patient/transaction-ids` | Get Patient Transaction IDs by HIPs |
| `GET` | `/api/care-context-link/phr/care-context-link/fetch/all` | PHR - Get All Care Context Links |
| `POST` | `/api/care-context-link/phr/care-context/bundle-url` | PHR - Save Care Context Bundle URL |
| `GET` | `/api/care-context-link/phr/care-context/bundle-url/{careContextLinkId}` | PHR - Fetch Care Context Bundle URL |
| `GET` | `/api/care-context-link/phr/fetch` | PHR - Get Care Context Links |
| `GET` | `/api/care-context-link/phr/fetch/hips` | PHR - Get Linked HIPs |
| `GET` | `/api/care-context-link/phr/file/details` | PHR - Get File Metadata |
| `GET` | `/api/care-context-link/phr/file/download` | PHR - Download File Chunk |
| `POST` | `/api/care-context-link/phr/patient/health-information/pull` | PHR - Pull Health Information for Care Context |
| `POST` | `/api/care-context-link/phr/patient/health-information/refresh` | PHR - Refresh Patient Health Information |
| `DELETE` | `/api/care-context-link/read/link/patient/links/{hipId}` | Mark Linked Facility as Read |
| `POST` | `/api/care-context-link/save` | Save Care Context Link |
| `GET` | `/api/care-context-link/search/care-context-link` | Search Care Context Links |
| `POST` | `/api/care-context-link/v0.5/health-information/transfer` | Health Information Data Transfer (HIP to HIU) |

### Gateway & Bridge

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/.well-known/openid-configuration` | Get OIDC Discovery Document |
| `GET` | `/api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId}` | Find Bridge Service by Service ID |
| `GET` | `/api/hiecm/gateway/v3/bridge-services` | List All Bridge Services |
| `PATCH` | `/api/hiecm/gateway/v3/bridge/url` | Update HIP/HIU Bridge Callback URL |
| `GET` | `/api/hiecm/gateway/v3/certs` | Get Gateway JWKS Certificates |

### health_locker

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/health-locker/lockers/unsubscribe` | Public-Health-Lockers-Unsubscribe |
| `POST` | `/health-locker/lockers/subscribe` | Public-Health-Lockers-Subscribe |
| `GET` | `/health-locker/subscription-requests/patients/lockers` | Public -Get-Subscribed-Lockers-By-PatientId |

### Provider directory

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/govt-programs` | List government programs |
| `GET` | `/api/hiecm/gateway/v3/health-lockers` | List health-locker-enabled providers |
| `GET` | `/api/hiecm/gateway/v3/providers` | List providers by name |
| `GET` | `/api/hiecm/gateway/v3/providers/{provider-id}` | Get a provider by id |

### scan_and_share

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/hiecm/patient-share/v3/on-share` | onpatientshare |
| `POST` | `/scan-share/profile/share` | profile share |
| `POST` | `/scan-share/record-share/on-notify` | AS - RecordShare on-notify |
| `POST` | `/scan-share/record-share/on-share` | AS - Record On Share |
| `POST` | `/scan-share/record-share/share` | AS - RecordShare |
| `GET` | `/scan-share/share-record/audit-history` | AS - RecordShare History |

### Session and tokens

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/hiecm/gateway/v3/sessions` | Create a session and get an access token |

### user_initiated_linking

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm` | call-back link-on-confirm |
| `POST` | `/api/hiecm/user-initiated-linking/v3/link/care-context/on-init` | call-back on-init |
| `POST` | `/user-initiated-linking/link/confirm` | 03 link-confirm |
| `POST` | `/user-initiated-linking/link/discover` | 01 discovery |
| `POST` | `/user-initiated-linking/link/init` | 02 link-init |
| `POST` | `/user-initiated-linking/link/on-discover` | call-back on-discovery |
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
