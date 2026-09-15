# On Search

`POST /v1/on_search`

Callback carrying the PM-JAY empanelled facilities that matched a search.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/v1/on_search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "messageId": "<MESSAGE_ID>",
    "transactionId": "<TRANSACTION_ID>",
    "consumerId": "<CONSUMER_ID>",
    "consumerUri": "<CONSUMER_URI>",
    "action": "on_search"
  },
  "message": {
    "catalog": {
      "providers": [
        {
          "id": "string",
          "descriptor": {
            "name": "<NAME>"
          },
          "locations": [],
          "items": [],
          "fulfillments": []
        }
      ]
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `context` (object, required)
- `context.messageId` (string, required)
- `context.transactionId` (string, required)
- `context.consumerId` (string, required)
- `context.consumerUri` (string, required)
- `context.action` (string, required)
- `message` (object, required)
- `message.catalog` (object, required)
- `message.catalog.providers` (object[], required)
- `message.catalog.providers.id` (string, required)
- `message.catalog.providers.descriptor` (object, required)
- `message.catalog.providers.locations` (object[], required)
- `message.catalog.providers.items` (object[], required)
- `message.catalog.providers.fulfillments` (object[], required)

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
