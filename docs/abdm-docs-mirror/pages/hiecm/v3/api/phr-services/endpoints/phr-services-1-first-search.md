# 1. First Search

`POST /api/teleconsulting/search`

Searches for teleconsultation services by category. Beckn `search` action; results arrive at `on_search`.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/teleconsulting/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85111",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "0.7.1",
    "consumer_id": "aarogyaSetu.eua",
    "consumer_uri": "https://aarogyasetu-sandbox.abdm.gov.in/aarogyasetu/api/v3/app/api/teleconsulting",
    "message_id": "<TXN_ID>",
    "timestamp": "2022-07-05T15:24:35",
    "transaction_id": "<TXN_ID>"
  },
  "message": {
    "intent": {
      "category": {
        "descriptor": {
          "code": "CARDIOLOGY",
          "name": "<NAME>"
        }
      },
      "fulfillment": {
        "agent": {
          "name": "<NAME>"
        },
        "type": "Online",
        "start": {
          "time": {
            "timestamp": "2022-07-15T00:00:00"
          }
        },
        "end": {
          "time": {
            "timestamp": "2022-07-16T00:00:00"
          }
        }
      },
      "item": {
        "descriptor": {
          "code": "Consultation",
          "name": "<NAME>"
        }
      }
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
- `context.transaction_id` (string, required)
- `message` (object, required)
- `message.intent` (object, required)
- `message.intent.category` (object, required)
- `message.intent.category.descriptor` (object, required)
- `message.intent.fulfillment` (object, required)
- `message.intent.fulfillment.agent` (object, required)
- `message.intent.fulfillment.type` (string, required)
- `message.intent.fulfillment.start` (object, required)
- `message.intent.fulfillment.end` (object, required)
- `message.intent.item` (object, required)
- `message.intent.item.descriptor` (object, required)

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
