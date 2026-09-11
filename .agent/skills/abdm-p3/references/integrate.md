# Integrate P3, PHR consent and notifications

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://dev.abdm.gov.in` Sandbox. Pair it with the `X-CM-ID: sbx` header.
- `https://apis.abdm.gov.in` Production. Pair it with the `X-CM-ID: abdm` header.
- `https://phrsbx.abdm.gov.in` Sandbox host, not yet confirmed.
- `https://phr.abdm.gov.in` Production.
## Endpoints

46 operations, grouped by the journey they belong to.

### bridge

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v4/int/v1/bridges/MutipleHRPAddUpdateServices` | Register / Update Bridge Services (HIU) |

### consent_management

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/consent-management/consent-artefacts` | Get All Consent Artefacts by ABHA Address |
| `GET` | `/api/consent-management/consent-requests` | Get Consent Request List |
| `GET` | `/api/consent-management/consent-requests/{consentRequestId}` | Get Consent Request by Request ID |
| `POST` | `/api/consent-management/consent-requests/{consentRequestId}/approve` | Approve Consent Request |
| `GET` | `/api/consent-management/consent-requests/{consentRequestId}/consent-artefacts` | Get All Consent Artefacts by Request ID |
| `POST` | `/api/consent-management/consent-requests/{consentRequestId}/deny` | Deny Consent Request |
| `POST` | `/api/consent-management/consent/on-fetch` | HIU On-Fetch (Consent Artefact Fetch Callback) |
| `POST` | `/api/consent-management/consent/request/init` | Init Consent Request |
| `POST` | `/api/consent-management/consent/request/notify` | HIU Consent Notification |
| `POST` | `/api/consent-management/consent/request/on-init` | HIU Consent Request On-Init (Callback) |
| `GET` | `/api/consent-management/consents/{consentArtefactId}` | Get Consent Artefact by Artefact ID |
| `POST` | `/api/consent-management/consents/auto-approval-policy/{autoApprovalId}/disable` | Disable Auto Approval |
| `POST` | `/api/consent-management/consents/auto-approval-policy/{autoApprovalId}/enable` | Enable Auto Approval |
| `POST` | `/api/consent-management/consents/auto-approve` | Consent Auto Approve |
| `POST` | `/api/consent-management/consents/revoke` | Revoke Consent |
| `POST` | `/api/consent-management/link/get-links` | Get Links |
| `PUT` | `/api/consent-management/patients/subscription-requests/{subscriptionId}` | Edit Subscription |
| `GET` | `/api/consent-management/subscription-requests` | Get All HIU Subscription Requests |
| `GET` | `/api/consent-management/subscription-requests/{subscriptionId}` | Get Subscription Details by Subscription ID |
| `POST` | `/api/consent-management/subscription-requests/{subscriptionRequestId}/approve` | Approve Subscription Request |
| `POST` | `/api/consent-management/subscription-requests/{subscriptionRequestId}/deny` | Deny Subscription Request |
| `POST` | `/api/consent-management/subscription-requests/init` | Initiate Subscription Request |
| `GET` | `/api/consent-management/subscription-requests/request/{subscriptionRequestId}` | Get Subscription Details by Request ID |
| `POST` | `/api/consent-management/subscription/setup` | Set Up Subscription for Aarogya Setu |

### Gateway & Bridge

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/.well-known/openid-configuration` | Get OIDC Discovery Document |
| `GET` | `/api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId}` | Find Bridge Service by Service ID |
| `GET` | `/api/hiecm/gateway/v3/bridge-services` | List All Bridge Services |
| `PATCH` | `/api/hiecm/gateway/v3/bridge/url` | Update HIP/HIU Bridge Callback URL |
| `GET` | `/api/hiecm/gateway/v3/certs` | Get Gateway JWKS Certificates |

### notification_collection

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/notification/app-push-notification/all` | Single/Multiple Notification read |
| `PATCH` | `/api/notification/app-push-notification/clear-notification` | Clear Notification |
| `POST` | `/api/notification/feedback` | Add Feedback |
| `GET` | `/api/notification/get-notification` | Get all notification details |
| `POST` | `/api/notification/new-app-push-notification` | Add new Notification |
| `GET` | `/api/notification/request/app-notification-token` | App Notification Token |
| `GET` | `/api/notification/schedule-push-notification` | GET-scheduled push Notifications |
| `POST` | `/api/notification/schedule-push-notification` | Schedule-push-notification - internal |
| `PUT` | `/api/notification/schedule-push-notification` | Update-scheduled push notification |
| `DELETE` | `/api/notification/schedule-push-notification/0eg` | Delete push notification |
| `POST` | `/notification/app-notification-token` | Post - add App Notification Token |

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
