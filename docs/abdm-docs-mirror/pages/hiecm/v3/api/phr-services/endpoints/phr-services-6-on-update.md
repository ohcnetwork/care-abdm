# 6. On_update

`POST /teleconsulting/update`

Updates a teleconsultation order, for example to reschedule. Beckn `update` action; the reply arrives at `on_update`.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/teleconsulting/update \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "context": {
    "domain": "nic2004:85111",
    "country": "IND",
    "city": "std:011",
    "action": "on_update",
    "core_version": "0.7.1",
    "consumer_id": "phr.euapid.bb",
    "consumer_uri": "https://d2xk0g5obixbh6.cloudfront.net/aarogyasetu/api/v3/app/api/teleconsulting",
    "message_id": "<TXN_ID>",
    "timestamp": "2022-07-05T15:24:35.481906",
    "provider_id": "hspa-nha",
    "provider_uri": "http://hspasbx.abdm.gov.in/api/v1",
    "transaction_id": "<TXN_ID>"
  },
  "message": {
    "order": {
      "id": "8441-696786-1042",
      "state": "DOCTOR_NO_SHOW",
      "item": {
        "id": "1",
        "descriptor": {
          "code": "Consultation",
          "name": "<NAME>"
        }
      },
      "fulfillment": {
        "id": "<TXN_ID>",
        "type": "Online",
        "agent": {
          "id": "<EMAIL>",
          "name": "<NAME>",
          "gender": "F",
          "tags": {
            "@abdm/gov.in/education": "MBBS,MS",
            "@abdm/gov.in/experience": "15.0",
            "@abdm/gov.in/languages": "English, Hindi, Marathi",
            "@abdm/gov.in/hpr_id": "<ABHA_NUMBER>,",
            "@abdm/gov.in/hfr_id": "<ABHA_NUMBER>"
          }
        },
        "start": {
          "time": {
            "timestamp": "2022-09-15T15:00:00"
          }
        },
        "end": {
          "time": {
            "timestamp": "2022-09-15T15:15:00"
          }
        },
        "tags": {
          "@abdm/gov.in/teleconsultation/uri": "www.callmyhspa.com/tele"
        }
      },
      "terms": [
        {
          "type": "Commercial",
          "descriptor": {
            "name": "<NAME>",
            "short_desc": "Short description of commercial terms",
            "long_desc": "Long descripiton of commercial terms"
          },
          "reasonRequired": false,
          "timePeriod": "2024-11-12T09:00:00",
          "reason": "",
          "termsState": "AGREED"
        },
        {
          "type": "Settlement",
          "descriptor": {
            "name": "<NAME>",
            "short_desc": "Short description of settlement terms",
            "long_desc": "Long descripiton of settlement terms"
          },
          "reasonRequired": false,
          "timePeriod": "2024-11-12T09:00:00",
          "reason": "",
          "termsState": "AGREED"
        },
        {
          "type": "Cancellation",
          "descriptor": {
            "name": "<NAME>",
            "short_desc": "Short description of cancellation terms",
            "long_desc": "Long descripiton of cancellation terms"
          },
          "reasonRequired": false,
          "timePeriod": "2024-11-12T09:00:00",
          "reason": "",
          "termsState": "AGREED"
        },
        {
          "type": "Refund",
          "descriptor": {
            "name": "<NAME>",
            "short_desc": "Short description of refund terms",
            "long_desc": "Long descripiton of refund terms"
          },
          "reasonRequired": false,
          "timePeriod": "2024-11-12T09:00:00",
          "reason": "",
          "termsState": "AGREED"
        },
        {
          "type": "Payment",
          "descriptor": {
            "name": "<NAME>",
            "short_desc": "Short description of payment terms",
            "long_desc": "Long descripiton of payment terms"
          },
          "reasonRequired": false,
          "timePeriod": "2024-11-12T09:00:00",
          "reason": "",
          "termsState": "AGREED"
        }
      ],
      "billing": {
        "name": "<NAME>",
        "address": {
          "door": "",
          "name": "<NAME>",
          "locality": "",
          "city": "Pune",
          "state": "Maharashtra",
          "country": "INDIA",
          "area_code": "412115"
        },
        "email": "<EMAIL>",
        "phone": "<MOBILE>"
      },
      "payment": {
        "uri": "https://api.bpp.com/pay?amt=1500&txn_id=ksh87yriuro34iyr3p4&mode=upi&vpa=sana.bhatt@upi",
        "type": "PRE-ORDER",
        "status": "PAID",
        "tl_method": "http/get",
        "params": {
          "transaction_id": "1",
          "amount": "1000",
          "mode": "UPI",
          "vpa": "xyz@ghh",
          "redirect_url": "https://uhieuasandbox.abdm.gov.in/on_paymentStatus? transaction_id=1&payment_status=success"
        }
      },
      "quote": {
        "price": {
          "currency": "INR",
          "value": "1000"
        },
        "breakup": [
          {
            "title": "Consultation",
            "price": {
              "currency": "INR",
              "value": "1000"
            }
          },
          {
            "title": "CGST @ 5%",
            "price": {
              "currency": "INR",
              "value": "0"
            }
          },
          {
            "title": "SGST @ 5%",
            "price": {
              "currency": "INR",
              "value": "0"
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
        "person": {
          "gender": "M",
          "dob": "<DATE_OF_BIRTH>",
          "dayOfBirth": 21,
          "monthOfBirth": 11,
          "yearOfBirth": 2022
        },
        "id": "satishc661994@sbx"
      },
      "provider": {
        "id": "1"
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
- `message.order` (object, required)
- `message.order.id` (string, required)
- `message.order.state` (string, required)
- `message.order.item` (object, required)
- `message.order.item.id` (string, required)
- `message.order.item.descriptor` (object, required)
- `message.order.fulfillment` (object, required)
- `message.order.fulfillment.id` (string, required)
- `message.order.fulfillment.type` (string, required)
- `message.order.fulfillment.agent` (object, required)
- `message.order.fulfillment.start` (object, required)
- `message.order.fulfillment.end` (object, required)
- `message.order.fulfillment.tags` (object, required)
- `message.order.terms` (object[], required)
- `message.order.terms.type` (string, required)
- `message.order.terms.descriptor` (object, required)
- `message.order.terms.reasonRequired` (boolean, required)
- `message.order.terms.timePeriod` (string, required)
- `message.order.terms.reason` (string, required)
- `message.order.terms.termsState` (string, required)
- `message.order.billing` (object, required)
- `message.order.billing.name` (string, required)
- `message.order.billing.address` (object, required)
- `message.order.billing.email` (string, required)
- `message.order.billing.phone` (string, required)
- `message.order.payment` (object, required)
- `message.order.payment.uri` (string, required)
- `message.order.payment.type` (string, required)
- `message.order.payment.status` (string, required)
- `message.order.payment.tl_method` (string, required)
- `message.order.payment.params` (object, required)
- `message.order.quote` (object, required)
- `message.order.quote.price` (object, required)
- `message.order.quote.breakup` (object[], required)
- `message.order.customer` (object, required)
- `message.order.customer.person` (object, required)
- `message.order.customer.id` (string, required)
- `message.order.provider` (object, required)
- `message.order.provider.id` (string, required)

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
