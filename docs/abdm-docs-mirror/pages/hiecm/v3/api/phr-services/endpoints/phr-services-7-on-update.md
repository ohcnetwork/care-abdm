# 7.on_update

`POST /teleconsulting/on_update`

Callback carrying the provider's reply to a teleconsultation update.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/teleconsulting/on_update \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85111",
    "country": "IND",
    "city": "std:011",
    "action": "on_update",
    "timestamp": "2025-10-15T06:31:05.168137Z",
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
      "id": "1481-367013-4819",
      "provider": {
        "id": "1",
        "descriptor": {
          "name": "<NAME>",
          "flag": false,
          "short_desc": "Expertise in every field with renowned staff.",
          "long_desc": "We are Test hospital. We have established a very profound name in the healthcare industry by providing expert services in every healthcare fields that we have."
        },
        "categories": [
          {
            "id": "201",
            "parent_category_id": "101",
            "descriptor": {
              "name": "<NAME>",
              "code": "CARDIOLOGY",
              "flag": false
            }
          },
          {
            "id": "101",
            "parent_category_id": "",
            "descriptor": {
              "name": "<NAME>",
              "code": "ALLOPATHY",
              "flag": false
            }
          }
        ],
        "location": {
          "id": "1",
          "descriptor": {
            "name": "<NAME>",
            "flag": false,
            "short_desc": "Expertise in every field with renowned staff.",
            "long_desc": "We are Test hospital. We have established a very profound name in the healthcare industry by providing expert services in every healthcare fields that we have."
          },
          "city": {
            "name": "<NAME>",
            "code": "011"
          },
          "country": {
            "name": "<NAME>",
            "code": "+91"
          },
          "gps": "18.5246036,73.792927",
          "address": "<ADDRESS>"
        }
      },
      "state": "COMPLETED",
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
        "type": "Physical",
        "agent": {
          "id": "<EMAIL>",
          "name": "<NAME>",
          "image": "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",
          "gender": "M",
          "tags": {
            "@abdm/gov.in/experience": "5.0",
            "@abdm/gov.in/languages": "English, Hindi",
            "@abdm/gov.in/education": "MBBS",
            "@abdm/gov.in/hpr_id": "<ABHA_NUMBER>"
          }
        },
        "start": {
          "time": {
            "timestamp": "2025-10-15T17:50:00"
          }
        },
        "end": {
          "time": {
            "timestamp": "2025-10-15T18:10:00"
          }
        },
        "tags": {
          "@abdm/gov.in/slot_id": "<TXN_ID>",
          "@abdm/gov.in/doctors_key": "<@ABDM/GOV.IN/DOCTORS_KEY>"
        }
      },
      "billing": {
        "name": "<NAME>",
        "address": {
          "name": "<NAME>",
          "locality": "bhadgaon road, near new watar tank, sapthshrungi nagar, Chalisgaon, Chalisgaon, Jalgaon, Maharashtra",
          "city": "JALGAON",
          "state": "MAHARASHTRA",
          "country": "INDIA",
          "area_code": "424101"
        },
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
        "id": "ganesh2305@sbx",
        "person": {
          "gender": "M",
          "dayOfBirth": 23,
          "monthOfBirth": 5,
          "yearOfBirth": 1992,
          "dob": "<DATE_OF_BIRTH>"
        }
      },
      "payment": {
        "uri": "",
        "type": "ON-ORDER",
        "status": "FREE",
        "params": {
          "transaction_id": "",
          "amount": "0.0",
          "mode": "",
          "vpa": "",
          "redirect_url": ""
        }
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
          "timePeriod": "2025-10-15T17:50:00",
          "reason": "",
          "termsState": "AGREED"
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
          "timePeriod": "2025-10-15T17:50:00",
          "reason": "",
          "termsState": "AGREED"
        },
        {
          "type": "Cancellation",
          "descriptor": {
            "name": "<NAME>",
            "flag": false,
            "short_desc": "Short description of Cancellation terms",
            "long_desc": "Cancellation: Full refund if cancelled 48 hrs before consultation time. n Rescheduling: No charges for rescheduling 48 hrs prior to consultation time"
          },
          "reasonRequired": false,
          "timePeriod": "2025-10-15T17:50:00",
          "reason": "",
          "termsState": "AGREED"
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
          "timePeriod": "2025-10-15T17:50:00",
          "reason": "",
          "termsState": "AGREED"
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
          "timePeriod": "2025-10-15T17:50:00",
          "reason": "",
          "termsState": "AGREED"
        }
      ],
      "authorization": {
        "type": "PIN",
        "token": "<TOKEN>",
        "valid_from": "2025-10-15T00:00:00",
        "valid_to": "2025-10-15T23:59:00",
        "status": "GENERATED"
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
- `message.order.provider.descriptor` (object, required)
- `message.order.provider.categories` (object[], required)
- `message.order.provider.location` (object, required)
- `message.order.state` (string, required)
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
- `message.order.billing.phone` (string, required)
- `message.order.quote` (object, required)
- `message.order.quote.price` (object, required)
- `message.order.quote.breakup` (object[], required)
- `message.order.customer` (object, required)
- `message.order.customer.id` (string, required)
- `message.order.customer.person` (object, required)
- `message.order.payment` (object, required)
- `message.order.payment.uri` (string, required)
- `message.order.payment.type` (string, required)
- `message.order.payment.status` (string, required)
- `message.order.payment.params` (object, required)
- `message.order.terms` (object[], required)
- `message.order.terms.type` (string, required)
- `message.order.terms.descriptor` (object, required)
- `message.order.terms.reasonRequired` (boolean, required)
- `message.order.terms.timePeriod` (string, required)
- `message.order.terms.reason` (string, required)
- `message.order.terms.termsState` (string, required)
- `message.order.authorization` (object, required)
- `message.order.authorization.type` (string, required)
- `message.order.authorization.token` (string, required)
- `message.order.authorization.valid_from` (string, required)
- `message.order.authorization.valid_to` (string, required)
- `message.order.authorization.status` (string, required)

## Responses

- `200`: No response body is documented for this request.
