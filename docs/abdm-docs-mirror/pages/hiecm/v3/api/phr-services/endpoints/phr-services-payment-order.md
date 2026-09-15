# payment-order

`POST /scan-pay/payment-order`

Creates the payment order for the procedures selected and returns the UPI intent to pay with.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/scan-pay/payment-order \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "intent": "PAYMENT_ORDER",
  "openOrderRequestId": "<TXN_ID>",
  "procedures": [
    {
      "category": "OPD consultation",
      "services": [
        {
          "serviceId": "Resistance 1",
          "name": "<NAME>",
          "description": "Consult with a hematology specialist to assess for Protein C resistance, a condition that increases the risk of abnormal blood clotting. Ideal for patients with a history of deep vein thrombosis or unexplained clotting events.",
          "amount": 629
        },
        {
          "serviceId": "Resistance 2",
          "name": "<NAME>",
          "description": "989261250000094 1; date:06-May-2025",
          "amount": 610
        },
        {
          "serviceId": "Resistance 3",
          "name": "<NAME>",
          "description": "989261250000094 2; date:06-May-2025",
          "amount": 611
        }
      ]
    },
    {
      "category": "Laboratory and Diagnostics",
      "services": [
        {
          "serviceId": "Flowcytometric 1",
          "name": "<NAME>",
          "description": "A specialized test using flow cytometry to accurately count CD34+ hematopoietic stem cells in blood or bone marrow. Essential for evaluating stem cell mobilization before transplantation or therapy planning.",
          "amount": 62
        },
        {
          "serviceId": "Flowcytometric 2",
          "name": "<NAME>",
          "description": "989261250000094 2; date:06-May-2025",
          "amount": 629
        }
      ]
    },
    {
      "category": "Pharmacy",
      "services": [
        {
          "serviceId": "Tomography 1",
          "name": "<NAME>",
          "description": "A high-resolution 3D imaging scan used primarily for dental, ENT, and maxillofacial evaluations. CBCT provides detailed views of bones, teeth, and soft tissues, aiding in accurate diagnosis and treatment planning with minimal radiation exposure",
          "amount": 629
        },
        {
          "serviceId": "Tomography 2",
          "name": "<NAME>",
          "description": "Pharmacy Details",
          "amount": 610
        }
      ]
    },
    {
      "category": "Miscellaneous/Other",
      "services": [
        {
          "serviceId": "Computerized 1",
          "name": "<NAME>",
          "description": "A high-resolution 3D imaging scan used primarily for dental, ENT, and maxillofacial evaluations. CBCT provides detailed views of bones, teeth, and soft tissues, aiding in accurate diagnosis and treatment planning with minimal radiation exposure",
          "amount": 629
        },
        {
          "serviceId": "Computerized 2",
          "name": "<NAME>",
          "description": null,
          "amount": 129
        }
      ]
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `intent` (string, required)
- `openOrderRequestId` (string, required)
- `procedures` (object[], required)
- `procedures.category` (string, required)
- `procedures.services` (object[], required)
- `procedures.services.serviceId` (string, required)
- `procedures.services.name` (string, required)
- `procedures.services.description` (null,string, required)
- `procedures.services.amount` (number, required)

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
