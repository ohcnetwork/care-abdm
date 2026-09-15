# Acknowledge a consent notification, as the HIU

`POST /hiecm/consent/v3/request/hiu/on-notify`

Also known as: Consent HIU On-Notify.
**Async Callback:** After ABDM Gateway sends a consent grant/deny notification to the HIU
bridge URL (`{bridgeUrl}/v0.5/consents/hiu/notify`), the HIU calls this Gateway endpoint
to acknowledge receipt.

The Gateway sends this notification when:
- Patient grants the consent
- Patient denies the consent
- A previously granted consent is revoked

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/consent/v3/request/hiu/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": [
    {
      "status": "OK",
      "consentId": "consent-art-uuid-001"
    }
  ],
  "response": {
    "requestId": "req-uuid-from-hiu-notify"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): Bearer token obtained from POST /hiecm/gateway/v3/sessions

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value. In M3 a single consent can produce several callbacks, so keep the mapping from request id to consent request id rather than relying on ordering.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production.

## Body

- `acknowledgement` (object[], required)
- `acknowledgement.status` (string, required) One of: OK, ERROR.
- `acknowledgement.consentId` (string, required)
- `response` (object, required): Echo of the requestId from the original Gateway-to-HIU request
- `response.requestId` (string, required): requestId received in the original Gateway notification to HIU bridge

## Responses

- `202`: Acknowledgement accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad request, invalid parameters or missing fields
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized, missing or invalid Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
