# Integrate Subscriptions

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://dev.abdm.gov.in` ABDM gateway, sandbox
- `https://apis.abdm.gov.in` ABDM gateway, production
## Endpoints

17 operations, grouped by the journey they belong to.

### Other operations

| Method | Path | What it does |
| --- | --- | --- |
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
| `POST` | `/api/hiecm/subscription-requests/v3/hiu/care-context/on-notify` | Respond to /api/v3/hiu/subscription/notify. |
| `POST` | `/api/hiecm/subscription-requests/v3/hiu/on-notify` | Respond to /subscription-requests/hiu/notify. |
| `POST` | `/api/hiecm/subscription-requests/v3/init` | Initiate subscription request. |
| `POST` | `/api/v3/hiu/hiecm/subscription-requests/on-init` | This is a callback API for /api/hiecm/subscription-requests/v3/init. |
| `POST` | `/api/v3/hiu/subscription-requests/hiu/notify` | This is a callback API when a subscription request is approved or denied. |
| `POST` | `/api/v3/hiu/subscription/notify` | This is a callback API to notify the subscribed HIU when a care context is link… |
## Headers

| Header | What it is |
| --- | --- |
| `REQUEST-ID` | Unique UUID for track the end to end request transaction |
| `TIMESTAMP` | Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, follow… |
| `X-CM-ID` | Suffix of the consent manager to which the request was intended |
| `X-HIU-ID` | Identifier of the health information user to which the request was intended |
## A request, in full

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/.well-known/openid-configuration \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```
