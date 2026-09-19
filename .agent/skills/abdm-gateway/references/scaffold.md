# HIE-CM gateway build

Scaffolds an ABDM gateway integration one journey at a time. It covers the gateway session and bridge registry.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

## Journeys

### Gateway (`gateway-abdm-gateway`)

**Act: the calls in this journey, in order**

#### 1. Fetch the service ids registered against a bridge (`gateway_get_gateway_v3_bridge_services`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge-services \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

#### 2. Fetch the details of a service ID (`gateway_get_gateway_v3_bridge_service_serviceid_service_id`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge-service/serviceId/{service-id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

#### 3. Update the bridge URL (`gateway_patch_gateway_v3_bridge_url`)

```bash
curl --request PATCH \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge/url \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "url": "<YOUR_CALLBACK_URL>"
}'
```

#### 4. Update the bridge service (`gateway_put_gateway_v3_bridge_service`)

```bash
curl --request PUT \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge-service \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "bridgeId": "{{bridgeId}}",
  "serviceId": "{{serviceId}}",
  "name": "TEST Gateway",
  "isHip": true,
  "isHiu": true,
  "isHealthLocker": null,
  "isPhr": false,
  "endpoints": {},
  "attributes": null,
  "active": true
}'
```

#### 5. Fetch the list of providers filtered by name (`gateway_get_gateway_v3_providers`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/providers \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

#### 6. Fetch the record for provider details for requested provider ID (`gateway_get_gateway_v3_providers_provider_id`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/providers/{provider-id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

#### 7. Fetch the list of govt programmes (`gateway_get_gateway_v3_govt_programs`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/govt-programs \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

#### 8. Fetch the record with health locker enabled provider details (`gateway_get_gateway_v3_health_lockers`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/health-lockers \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
[
  {
    "identifier": {
      "name": "AB - PMJAY",
      "id": "PMJAY"
    },
    "facilityType": [
      "HIP"
    ],
    "isHip": true,
    "isGovtEntity": false,
    "endpoints": {
      "healthLockerEndpoints": [
        {
          "use": "registration",
          "connectionType": "HTTPS",
          "address": "https://abc.com/register"
        }
      ]
    }
  }
]
```

### Sessions (`gateway-abdm-sessions`)

**Act: the calls in this journey, in order**

#### 1. Generate Keycloak token/access token (`gateway_post_gateway_v3_sessions`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "SBX_0000",
  "clientSecret": "0******-***-***-***-a****",
  "grantType": "client_credentials"
}'
```

#### 2. Get the open ID configuration (`gateway_get_gateway_v3_well_known_openid_configuration`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/.well-known/openid-configuration \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

#### 3. Get the certificate information (`gateway_get_gateway_v3_certs`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/certs \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

**Exit condition (Observe until this is true)**

A 200 whose body matches:

```json
{
  "keys": [
    {
      "e": "AQAB",
      "kid": "AlRb5WCm8Tm9EJ_IfO9z06j9oCv51pKK",
      "kty": "RSA",
      "n": "mgmW7W5ZGF_G5cJevwYi8HiPcI-6qS_psnZxa4v3bkwAkyOoOd8-6ketrOI-ZA2PbRbGnxFfZHiI94rdFXJ4Q9ampscsz9NocTIPMPmWydJ8A50pZaYWyikYDSJiDltq7i3WspPKSOuQHr",
      "use": "sig",
      "x5c": [
        "MIICrzCCAZcCBgFy/3WZBjANBgkqhkiG9w0BAQsFADAbMRkwFwYDVQQDDBBjZW50cmFsLXJlZ2lzdHJ5MB4XDTIwMDYyOTA5NDEzNloXDTMwMDYyOTA5NDMxNlowGzEZMBcGA1UEAwwQY2VudHJhbC1yZWdpc3RyeTCCASIwDQYJK"
      ],
      "x5t": "EaMhYGUIvMkp8tvS",
      "x5t2": "vGer6Pt8AhZn8RlbHhAFksOCcGf3u1UWU7Qq",
      "alg": "RS256"
    }
  ]
}
```

## Where the detail is

- Every operation, with its body fields and responses: /docs/hiecm/v3/api/gateway
