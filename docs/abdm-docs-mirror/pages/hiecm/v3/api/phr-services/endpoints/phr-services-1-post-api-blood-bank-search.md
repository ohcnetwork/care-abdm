# 1. POST /api/blood-bank/search

`POST /api/blood-bank/search`

Searches for blood banks and blood availability. Beckn `search` action; results arrive at `on_search`.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/blood-bank/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85110",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "0.9.1",
    "consumer_id": "aarogya.setu",
    "consumer_uri": "<BASE_URL>",
    "transaction_id": "<TRANSACTION_ID>",
    "message_id": "<MESSAGE_ID>",
    "timestamp": "<TIMESTAMP>",
    "ttl": "PT30S"
  },
  "message": {
    "intent": {
      "item": {
        "descriptor": {
          "name": "<NAME>"
        },
        "category_id": "BLOOD_GROUP"
      },
      "fulfillment": {
        "type": "BLOOD_BANK"
      },
      "location": {
        "gps": "28.6139,77.2090",
        "radius": {
          "type": "CIRCULAR",
          "value": "10",
          "unit": "km"
        },
        "city": {
          "name": "<NAME>",
          "code": "std:011"
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
- `context.transaction_id` (string, required)
- `context.message_id` (string, required)
- `context.timestamp` (string, required)
- `context.ttl` (string, required)
- `message` (object, required)
- `message.intent` (object, required)
- `message.intent.item` (object, required)
- `message.intent.item.descriptor` (object, required)
- `message.intent.item.category_id` (string, required)
- `message.intent.fulfillment` (object, required)
- `message.intent.fulfillment.type` (string, required)
- `message.intent.location` (object, required)
- `message.intent.location.gps` (string, required)
- `message.intent.location.radius` (object, required)
- `message.intent.location.city` (object, required)

## Responses

- `200`: No response body is documented for this request.
