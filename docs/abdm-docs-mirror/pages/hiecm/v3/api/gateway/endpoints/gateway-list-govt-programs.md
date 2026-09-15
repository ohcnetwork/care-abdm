# List government programs

`GET /api/hiecm/gateway/v3/govt-programs`

List government programs registered with the gateway. The response
items share the same shape, field for field, as the provider-by-id
response. That shape has not been observed against the sandbox.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/govt-programs \
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

## Responses

- `200`: Government programs.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "identifier": "<IDENTIFIER>",
    "facilityType": [
      "HIP"
    ],
    "isHIP": false
  }
]
```
