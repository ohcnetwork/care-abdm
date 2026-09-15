# STEP 4 - on_init

`POST /ambulance-booking/on_init`

Callback carrying the provider's reply to an ambulance booking `init`: the quote and the terms to confirm.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/ambulance-booking/on_init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2008:86909",
    "country": "IND",
    "city": "std:011",
    "action": "on_init",
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
      "id": "<O_R_D_E_R_I_D>",
      "state": "INITIALIZED"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `context` (object, required)
- `context.domain` (string, required)
- `context.country` (string, required)
- `context.city` (string, required)
- `context.action` (string, required)
- `context.timestamp` (string, required)
- `context.core_version` (string, required)
- `context.consumer_id` (string, required)
- `context.consumer_uri` (string, required)
- `context.provider_id` (string, required)
- `context.provider_uri` (string, required)
- `context.transaction_id` (string, required)
- `context.message_id` (string, required)
- `message` (object, required)
- `message.order` (object, required)
- `message.order.id` (string, required)
- `message.order.state` (string, required)

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
