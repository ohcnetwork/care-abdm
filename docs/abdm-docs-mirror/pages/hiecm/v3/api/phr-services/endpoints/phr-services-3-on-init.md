# 3. on_init

`POST /teleconsulting/on_init`

Callback carrying the provider's reply to a teleconsultation `init`: the quote and the terms to confirm.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/teleconsulting/on_init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85111",
    "country": "IND",
    "city": "std:011",
    "action": "on_init",
    "timestamp": "2025-09-10T08:06:14.327Z",
    "core_version": "0.7.1",
    "consumer_id": "aarogyaSetu.eua",
    "consumer_uri": "https://aarogyasetu-sandbox.abdm.gov.in/aarogyasetu/api/v3/app/api/teleconsulting",
    "provider_id": "hspa-nha",
    "provider_uri": "https://hspasbx.abdm.gov.in/api/v1",
    "transaction_id": "<TXN_ID>",
    "message_id": "<TXN_ID>"
  },
  "message": {
    "order": {
      "id": "1944-731810-6639",
      "provider": {
        "id": "1"
      },
      "item": {
        "id": "0",
        "descriptor": {
          "name": "<NAME>",
          "code": "CONSULTATION",
          "flag": false
        },
        "price": {
          "currency": "INR",
          "value": "0.0"
        },
        "fulfillment_id": "<TXN_ID>"
      },
      "fulfillment": {
        "id": "<TXN_ID>",
        "type": "Online",
        "agent": {
          "id": "<EMAIL>",
          "name": "<NAME>",
          "gender": "M",
          "tags": {
            "@abdm/gov.in/education": "MBBS",
            "@abdm/gov.in/experience": "5.0",
            "@abdm/gov.in/hpr_id": "<EMAIL>",
            "@abdm/gov.in/languages": "Eng, Hin"
          }
        },
        "start": {
          "time": {
            "timestamp": "2025-09-11T12:00:00"
          }
        },
        "end": {
          "time": {
            "timestamp": "2025-09-11T12:15:00"
          }
        },
        "tags": {
          "@abdm/gov.in/slot_id": "<TXN_ID>"
        }
      },
      "billing": {
        "name": "<NAME>",
        "address": {
          "door": "54",
          "name": "<NAME>",
          "locality": "Nethaji subhash chandra bose street, GNT road, Gummidipoondi, Thiruvallur",
          "state": "Tamil Nadu",
          "country": "INDIA",
          "area_code": "601201"
        },
        "email": "<EMAIL>",
        "phone": "<MOBILE>"
      },
      "quote": {
        "price": {
          "currency": "INR",
          "value": "0.0"
        },
        "breakup": [
          {
            "title": "Consultation",
            "price": {
              "currency": "INR",
              "value": "0.0"
            }
          },
          {
            "title": "CGST @ 5%",
            "price": {
              "currency": "INR",
              "value": "0.0"
            }
          },
          {
            "title": "SGST @ 5%",
            "price": {
              "currency": "INR",
              "value": "0.0"
            }
          },
          {
            "title": "Registration",
            "price": {
              "currency": "INR",
              "value": "0"
            }
          }
        ]
      },
      "customer": {
        "id": "nithishjaniti@sbx",
        "person": {
          "gender": "M",
          "dayOfBirth": 14,
          "monthOfBirth": 10,
          "yearOfBirth": 1999,
          "dob": "<DATE_OF_BIRTH>"
        }
      },
      "payment": {
        "type": "ON-ORDER",
        "status": "FREE"
      },
      "terms": [
        {
          "type": "Commercial",
          "descriptor": {
            "name": "<NAME>",
            "flag": false,
            "short_desc": "Short description of commercial terms",
            "long_desc": "Long description of commercial terms"
          },
          "reasonRequired": false,
          "timePeriod": "2025-09-11T12:00:00",
          "reason": "",
          "termsState": "INITIATED"
        },
        {
          "type": "Settlement",
          "descriptor": {
            "name": "<NAME>",
            "flag": false,
            "short_desc": "Short description of Settlement terms",
            "long_desc": "Long description of Settlement terms"
          },
          "reasonRequired": false,
          "timePeriod": "2025-09-11T12:00:00",
          "reason": "",
          "termsState": "INITIATED"
        },
        {
          "type": "Cancellation",
          "descriptor": {
            "name": "<NAME>",
            "flag": false,
            "short_desc": "Short description of Cancellation terms",
            "long_desc": "Cancellation: Full refund if cancelled 48 hrs before consultation time. \\n Rescheduling: No charges for rescheduling 48 hrs prior to consultation time"
          },
          "reasonRequired": false,
          "timePeriod": "2025-09-11T12:00:00",
          "reason": "",
          "termsState": "INITIATED"
        },
        {
          "type": "Refund",
          "descriptor": {
            "name": "<NAME>",
            "flag": false,
            "short_desc": "Short description of Refund terms",
            "long_desc": "No Show: If doctor does not show up - full refund. No refund if patient does not turn up for appointment"
          },
          "reasonRequired": false,
          "timePeriod": "2025-09-11T12:00:00",
          "reason": "",
          "termsState": "INITIATED"
        },
        {
          "type": "Payment",
          "descriptor": {
            "name": "<NAME>",
            "flag": false,
            "short_desc": "Short description of Payment terms",
            "long_desc": "Long description of Payment terms"
          },
          "reasonRequired": false,
          "timePeriod": "2025-09-11T12:00:00",
          "reason": "",
          "termsState": "INITIATED"
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
- `message.order.provider` (object, required)
- `message.order.provider.id` (string, required)
- `message.order.item` (object, required)
- `message.order.item.id` (string, required)
- `message.order.item.descriptor` (object, required)
- `message.order.item.price` (object, required)
- `message.order.item.fulfillment_id` (string, required)
- `message.order.fulfillment` (object, required)
- `message.order.fulfillment.id` (string, required)
- `message.order.fulfillment.type` (string, required)
- `message.order.fulfillment.agent` (object, required)
- `message.order.fulfillment.start` (object, required)
- `message.order.fulfillment.end` (object, required)
- `message.order.fulfillment.tags` (object, required)
- `message.order.billing` (object, required)
- `message.order.billing.name` (string, required)
- `message.order.billing.address` (object, required)
- `message.order.billing.email` (string, required)
- `message.order.billing.phone` (string, required)
- `message.order.quote` (object, required)
- `message.order.quote.price` (object, required)
- `message.order.quote.breakup` (object[], required)
- `message.order.customer` (object, required)
- `message.order.customer.id` (string, required)
- `message.order.customer.person` (object, required)
- `message.order.payment` (object, required)
- `message.order.payment.type` (string, required)
- `message.order.payment.status` (string, required)
- `message.order.terms` (object[], required)
- `message.order.terms.type` (string, required)
- `message.order.terms.descriptor` (object, required)
- `message.order.terms.reasonRequired` (boolean, required)
- `message.order.terms.timePeriod` (string, required)
- `message.order.terms.reason` (string, required)
- `message.order.terms.termsState` (string, required)

## Responses

- `200`: No response body is documented for this request.
