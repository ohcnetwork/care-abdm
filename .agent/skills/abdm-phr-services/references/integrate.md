# Integrate PHR application services

The calls themselves: where they live, what they need in their headers, and one request written out in full.

## Hosts

- `https://phrsbx.abdm.gov.in` Sandbox host, not yet confirmed.
- `https://phr.abdm.gov.in` Production.
- `https://dev.abdm.gov.in` Sandbox. Pair it with the `X-CM-ID: sbx` header.
- `https://apis.abdm.gov.in` Production. Pair it with the `X-CM-ID: abdm` header.
## Endpoints

72 operations, grouped by the journey they belong to.

### ambulance

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/ambulance-booking/init` | STEP 3 - init |
| `POST` | `/ambulance-booking/on_init` | STEP 4 - on_init |
| `POST` | `/ambulance-booking/on_search` | STEP 2 - on_search |
| `POST` | `/ambulance-booking/search` | STEP 1 - search |

### blood_bank

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/blood-bank/on_search` | 2. POST /api/blood-bank/on_search |
| `POST` | `/api/blood-bank/search` | 1. POST /api/blood-bank/search |

### bridge

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/v4/int/v1/bridges/MutipleHRPAddUpdateServices` | Register / Update Bridge Services (HIU) |

### Gateway & Bridge

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/.well-known/openid-configuration` | Get OIDC Discovery Document |
| `GET` | `/api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId}` | Find Bridge Service by Service ID |
| `GET` | `/api/hiecm/gateway/v3/bridge-services` | List All Bridge Services |
| `PATCH` | `/api/hiecm/gateway/v3/bridge/url` | Update HIP/HIU Bridge Callback URL |
| `GET` | `/api/hiecm/gateway/v3/certs` | Get Gateway JWKS Certificates |

### nearby_health_search

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/health/service/facility/geo-location/search-within-radius` | Search Facilities Within Radius |
| `POST` | `/health/service/bookmark/create` | Create |
| `DELETE` | `/health/service/bookmark/delete/{id}` | Delete |
| `GET` | `/health/service/bookmark/getByAbhaAddress` | getByAbhaAddress |
| `GET` | `/health/service/bookmark/summary` | get/summary |
| `PUT` | `/health/service/bookmark/update/{id}` | Update |
| `POST` | `/health/service/doctor/geo-location/search-within-radius` | {{aarogya-setu-sandbox-url}}api/health/service/doctor/geo-location/search-withi… |
| `GET` | `/health/service/doctor/master/languages` | Get Languanges |
| `GET` | `/health/service/doctor/master/system-of-medicine` | {{aarogya-setu-sandbox-url}}api/health/service/doctor/master/system-of-medicine |
| `GET` | `/health/service/doctor/search/{abhaNumber}` | search-doctor-by-id |
| `GET` | `/health/service/facility/categories/distinct` | Get Distinct Category List |
| `GET` | `/health/service/facility/categories/list` | Get Category List |
| `GET` | `/health/service/facility/categories/specialities` | Get Specialists Category List |
| `GET` | `/health/service/facility/doctors/{searchId}` | Get Doctor Details |
| `POST` | `/health/service/facility/geo-location/search-within-radius` | Search Facilities Within Radius |
| `GET` | `/health/service/facility/master/system-of-medicine` | Get System of Medicine List |
| `GET` | `/health/service/facility/search/IN3310027864` | Get Facility Details By Search ID |
| `GET` | `/v4/hfr/facility/search/searchFacility/IN2710002401` | Get HFR Facility Details By Search ID |

### nhcx

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/nhcx/get-coverage-eligibility` | get-coverage-eligibility |
| `POST` | `/nhcx/get-policies` | get-policies |
| `POST` | `/nhcx/search` | search |
| `POST` | `/nhcx/v1/coverageeligibility/on_check` | on_check |
| `POST` | `/nhcx/v1/hcx/notification/on_subscribe` | nhcx-onsubscribe |
| `POST` | `/nhcx/v1/notification/subscribe` | subscribe |
| `POST` | `/nhcx/v1/search/on_submit` | on_submit |

### pmjay_panel_facility_discovery

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hem/getSpecialists` | Get Specialists |
| `POST` | `/v1/on_search` | On Search |
| `POST` | `/v1/rest/search` | Rest Search |
| `POST` | `/v1/search` | Search |

### Provider directory

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/hiecm/gateway/v3/govt-programs` | List government programs |
| `GET` | `/api/hiecm/gateway/v3/health-lockers` | List health-locker-enabled providers |
| `GET` | `/api/hiecm/gateway/v3/providers` | List providers by name |
| `GET` | `/api/hiecm/gateway/v3/providers/{provider-id}` | Get a provider by id |

### scan_and_pay

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/scan-pay/get/details` | get details |
| `GET` | `/scan-pay/notify/status/{id}` | notify status |
| `POST` | `/scan-pay/open-order` | OPENORDER |
| `POST` | `/scan-pay/order-status` | order-status |
| `POST` | `/scan-pay/payment-order` | payment-order |
| `PUT` | `/scan-pay/update/payment/{id}` | update payment |

### Session and tokens

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/hiecm/gateway/v3/sessions` | Create a session and get an access token |

### teleconsulting

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/teleconsulting/getOrders/6254-172027-4007` | get Orders by id |
| `GET` | `/api/teleconsulting/getOrdersByAbhaId` | get Orders by ABHA id |
| `POST` | `/api/teleconsulting/on_search` | 1. on_search |
| `POST` | `/api/teleconsulting/search` | 1. First Search |
| `POST` | `/teleconsulting/confirm` | 4. Confirm |
| `GET` | `/teleconsulting/getCategories` | Get categories |
| `GET` | `/teleconsulting/getCategories/1` | Get categories by id |
| `GET` | `/teleconsulting/getOrdersByAbhaIdAndType/kushal.1122000@sbx` | Get Orders by Abha Id and Type |
| `GET` | `/teleconsulting/getOrdersByAbhaIdDesc` | Get Orders by ABHA id desc |
| `POST` | `/teleconsulting/init` | 3. Init |
| `POST` | `/teleconsulting/message` | 7 .On_message |
| `POST` | `/teleconsulting/on_cancel` | 6.on_cancel |
| `POST` | `/teleconsulting/on_confirm` | 4.on_confirm |
| `POST` | `/teleconsulting/on_init` | 3. on_init |
| `POST` | `/teleconsulting/on_search` | 2. on_search |
| `POST` | `/teleconsulting/on_status` | 5.On status |
| `POST` | `/teleconsulting/on_update` | 7.on_update |
| `POST` | `/teleconsulting/search` | 2. Second Search |
| `POST` | `/teleconsulting/status` | 5. Status |
| `POST` | `/teleconsulting/update` | 6. On_update |
## Headers

| Header | What it is |
| --- | --- |
| `REQUEST-ID` | A fresh UUID that you generate for this request. It is how you and the gateway correlate a call with its call… |
| `TIMESTAMP` | The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose t… |
| `X-CM-ID` | Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. Sending the wrong on… |
## A request, in full

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/ambulance-booking/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2008:86909",
    "country": "IND",
    "city": "std:011",
    "action": "init",
    "timestamp": "2026-06-12T10:00:00",
    "core_version": "0.7.1",
    "consumer_id": "aarogyaSetu.eua",
    "consumer_uri": "https://aarogyasetu-sandbox.abdm.gov.in/aarogyasetu/api/v3/app/api/ambulance-booking",
    "provider_id": "nha.hspa",
    "provider_uri": "https://hspasbx.abdm.gov.in/api/v1/hspa/ambulance",
    "transaction_id": "<TXN_ID>",
    "message_id": "<TXN_ID>"
  },
  "message": {
    "order": {
      "id": "<O_R_D_E_R_I_D>"
    }
  }
}'
```
