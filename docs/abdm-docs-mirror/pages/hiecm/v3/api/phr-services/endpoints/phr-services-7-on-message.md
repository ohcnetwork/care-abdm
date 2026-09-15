# 7 .On_message

`POST /teleconsulting/message`

Sends a message within a teleconsultation. Beckn `message` action.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/teleconsulting/message \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85111",
    "country": "IND",
    "city": "std:011",
    "action": "on_message",
    "core_version": "0.7.1",
    "consumer_id": "aarogyaSetu.eua",
    "consumer_uri": "https://aarogyasetu-sandbox.abdm.gov.in/aarogyasetu/api/v3/app/api/teleconsulting",
    "message_id": "<TXN_ID>",
    "timestamp": "2022-07-05T15:24:35.481906Z",
    "provider_id": "hspa-nha",
    "provider_uri": "http://hspasbx.abdm.gov.in/api/v1",
    "transaction_id": "<TXN_ID>"
  },
  "message": {
    "intent": {
      "chat": {
        "sender": {
          "person": {
            "name": "<NAME>",
            "gender": "M",
            "image": "image",
            "id": "santoshjagtap@sbx"
          }
        },
        "receiver": {
          "person": {
            "name": "<NAME>",
            "gender": "M",
            "image": "image hashed base64",
            "id": "<EMAIL>"
          }
        },
        "content": {
          "content_id": "<TXN_ID>",
          "content_value": "Base64 Encoded text",
          "content_type": "text"
        },
        "time": {
          "timestamp": "2022-10-03T11:32:01"
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
- `context.provider_id` (string, required)
- `context.provider_uri` (string, required)
- `context.transaction_id` (string, required)
- `message` (object, required)
- `message.intent` (object, required)
- `message.intent.chat` (object, required)
- `message.intent.chat.sender` (object, required)
- `message.intent.chat.receiver` (object, required)
- `message.intent.chat.content` (object, required)
- `message.intent.chat.time` (object, required)

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
