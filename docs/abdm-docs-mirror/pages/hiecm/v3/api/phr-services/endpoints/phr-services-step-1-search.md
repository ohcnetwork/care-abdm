# STEP 1 - search

`POST /ambulance-booking/search`

Searches for ambulance services. Beckn `search` action; results arrive at `on_search`.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/ambulance-booking/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2008:86909",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "0.7.1",
    "consumer_id": "aarogyaSetu.eua",
    "consumer_uri": "https://aarogyasetu-sandbox.abdm.gov.in/aarogyasetu/api/v3/app/api/ambulance-booking",
    "message_id": "<TXN_ID>",
    "timestamp": "2026-06-12T10:00:00",
    "transaction_id": "<TXN_ID>"
  },
  "message": {
    "intent": {
      "category": {
        "descriptor": {
          "code": "ALL",
          "name": "<NAME>"
        }
      },
      "fulfillment": {
        "type": "EMERGENCY",
        "start": {
          "time": {
            "timestamp": "2026-06-12T10:00:00"
          }
        },
        "end": {
          "time": {
            "timestamp": "2026-06-12T23:59:59"
          }
        }
      },
      "locations": [
        {
          "descriptor": {
            "code": "SOURCE",
            "name": "<NAME>"
          },
          "gps": "12.423423,77.325647",
          "address": "<ADDRESS>"
        }
      ],
      "item": {
        "descriptor": {
          "code": "AMBULANCE",
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
- `message.intent.fulfillment.type` (string, required)
- `message.intent.fulfillment.start` (object, required)
- `message.intent.fulfillment.end` (object, required)
- `message.intent.locations` (object[], required)
- `message.intent.locations.descriptor` (object, required)
- `message.intent.locations.gps` (string, required)
- `message.intent.locations.address` (string, required)
- `message.intent.item` (object, required)
- `message.intent.item.descriptor` (object, required)

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
