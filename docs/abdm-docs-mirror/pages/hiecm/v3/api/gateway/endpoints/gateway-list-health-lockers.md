# List health-locker-enabled providers

`GET /api/hiecm/gateway/v3/health-lockers`

List providers with health locker functionality enabled, optionally
filtered by name.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/health-lockers \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` returned by `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. It is how you and the gateway correlate a call with its callback and with a support ticket, so log it. Reusing one across requests makes both impossible.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. Sending the wrong one against the right host is a common first-day failure and reads as an authorisation error.

## Query parameters

- `name` (string): Filter by locker name.

## Responses

- `200`: Health-locker-enabled providers.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "identifier": "<IDENTIFIER>",
    "facilityType": [
      "HIP"
    ],
    "isHip": false,
    "isGovtEntity": false,
    "endpoints": {
      "healthLockerEndpoints": [
        "<HEALTH_LOCKER_ENDPOINTS>"
      ]
    }
  }
]
```
