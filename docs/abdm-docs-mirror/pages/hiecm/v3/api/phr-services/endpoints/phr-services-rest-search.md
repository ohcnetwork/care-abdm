# Rest Search

`POST /v1/rest/search`

Searches PM-JAY empanelled facilities and returns the results in the same call, without a callback.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/v1/rest/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85112",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "0.7.1",
    "consumer_id": "aarogyaSetu.eua",
    "consumer_uri": "https://aarogyasetu.abdm.gov.in/aarogyasetu/api/v3/app/api/hem",
    "message_id": "<GENERATED>",
    "timestamp": "<ISO_8601_TIMESTAMP>",
    "transaction_id": "<GENERATED>"
  },
  "message": {
    "intent": {
      "fulfillment": {
        "start": {
          "time": {
            "timestamp": "2022-07-22T13:21:41"
          }
        },
        "end": {
          "time": {
            "timestamp": "2022-07-22T23:59:59"
          }
        },
        "type": "PMJAYHEM"
      },
      "item": {
        "descriptor": {
          "code": "PMJAY",
          "name": "<NAME>",
          "flag": false
        }
      },
      "location": {
        "state": {
          "name": "<NAME>",
          "code": "27"
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
- `message.intent.fulfillment` (object, required)
- `message.intent.fulfillment.start` (object, required)
- `message.intent.fulfillment.end` (object, required)
- `message.intent.fulfillment.type` (string, required)
- `message.intent.item` (object, required)
- `message.intent.item.descriptor` (object, required)
- `message.intent.location` (object, required)
- `message.intent.location.state` (object, required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "context": {
    "domain": "string",
    "country": "string",
    "city": "string",
    "action": "string",
    "timestamp": "string",
    "core_version": "string",
    "consumer_id": "string",
    "consumer_uri": "string",
    "provider_id": "string",
    "provider_uri": "string",
    "transaction_id": "string",
    "message_id": "string"
  },
  "message": {
    "catalog": {
      "descriptor": {
        "name": "string",
        "images": "string",
        "flag": "boolean",
        "short_desc": "string",
        "long_desc": "string"
      },
      "providers": "array"
    }
  }
}
```
