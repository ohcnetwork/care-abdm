# 2. POST /api/blood-bank/on_search

`POST /api/blood-bank/on_search`

Callback carrying the blood banks and stock that matched a search.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/blood-bank/on_search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85110",
    "country": "IND",
    "city": "std:011",
    "action": "on_search",
    "core_version": "0.9.1",
    "consumer_id": "aarogya.setu",
    "consumer_uri": "<BASE_URL>",
    "provider_id": "bloodbank.provider.in",
    "provider_uri": "https://bloodbank-provider.example.in/api",
    "transaction_id": "<TRANSACTION_ID>",
    "message_id": "<MESSAGE_ID>",
    "timestamp": "<TIMESTAMP>"
  },
  "message": {
    "catalog": {
      "descriptor": {
        "name": "<NAME>"
      },
      "providers": [
        {
          "id": "BB_AIIMS_001",
          "descriptor": {
            "name": "<NAME>",
            "short_desc": "All India Institute of Medical Sciences Blood Bank"
          },
          "location": {
            "id": "LOC001",
            "gps": "28.5672,77.2100",
            "address": "<ADDRESS>",
            "city": {
              "name": "<NAME>",
              "code": "std:011"
            },
            "state": {
              "name": "<NAME>"
            },
            "country": {
              "name": "<NAME>",
              "code": "IND"
            }
          },
          "contact": {
            "phone": "<MOBILE>",
            "email": "<EMAIL>"
          },
          "categories": [
            {
              "id": "BLOOD_GROUP",
              "descriptor": {
                "name": "<NAME>",
                "code": "BG"
              }
            }
          ],
          "items": [
            {
              "id": "ITEM_O_POS_001",
              "descriptor": {
                "name": "<NAME>",
                "code": "O_POSITIVE"
              },
              "category_id": "BLOOD_GROUP",
              "quantity": {
                "count": 15
              },
              "provider_id": "BB_AIIMS_001"
            },
            {
              "id": "ITEM_A_POS_001",
              "descriptor": {
                "name": "<NAME>",
                "code": "A_POSITIVE"
              },
              "category_id": "BLOOD_GROUP",
              "quantity": {
                "count": 8
              },
              "provider_id": "BB_AIIMS_001"
            }
          ],
          "fulfillments": [
            {
              "id": "FF001",
              "type": "BLOOD_BANK",
              "tracking": false
            }
          ]
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
- `context.domain` (string, required)
- `context.country` (string, required)
- `context.city` (string, required)
- `context.action` (string, required)
- `context.core_version` (string, required)
- `context.consumer_id` (string, required)
- `context.consumer_uri` (string, required)
- `context.provider_id` (string, required)
- `context.provider_uri` (string, required)
- `context.transaction_id` (string, required)
- `context.message_id` (string, required)
- `context.timestamp` (string, required)
- `message` (object, required)
- `message.catalog` (object, required)
- `message.catalog.descriptor` (object, required)
- `message.catalog.descriptor.name` (string, required)
- `message.catalog.providers` (object[], required)
- `message.catalog.providers.id` (string, required)
- `message.catalog.providers.descriptor` (object, required)
- `message.catalog.providers.location` (object, required)
- `message.catalog.providers.contact` (object, required)
- `message.catalog.providers.categories` (object[], required)
- `message.catalog.providers.items` (object[], required)
- `message.catalog.providers.fulfillments` (object[], required)

## Responses

- `200`: No response body is documented for this request.
