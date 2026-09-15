# 5. Status

`POST /teleconsulting/status`

Asks for the current status of a teleconsultation order. Beckn `status` action; the reply arrives at `on_status`.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/teleconsulting/status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85111",
    "country": "IND",
    "city": "std:011",
    "action": "status",
    "core_version": "0.7.1",
    "consumer_id": "phr.euapid.bb",
    "consumer_uri": "https://d2xk0g5obixbh6.cloudfront.net/aarogyasetu/api/v3/app/api/teleconsulting",
    "message_id": "<TXN_ID>",
    "timestamp": "2022-07-05T15:24:35",
    "provider_id": "hspa-nha",
    "provider_uri": "http://hspasbx.abdm.gov.in/api/v1",
    "transaction_id": "<TXN_ID>"
  },
  "message": {
    "order": {
      "id": "8441-696786-1042"
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
- `context.core_version` (string, required)
- `context.consumer_id` (string, required)
- `context.consumer_uri` (string, required)
- `context.message_id` (string, required)
- `context.timestamp` (string, required)
- `context.provider_id` (string, required)
- `context.provider_uri` (string, required)
- `context.transaction_id` (string, required)
- `message` (object, required)
- `message.order` (object, required)
- `message.order.id` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": {
    "ack": {
      "status": "ACK"
    }
  }
}
```
