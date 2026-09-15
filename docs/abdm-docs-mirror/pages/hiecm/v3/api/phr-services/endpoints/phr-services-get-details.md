# get details

`GET /scan-pay/get/details`

Lists the person's scan and pay requests with the status, order number and transaction id of each.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/scan-pay/get/details \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": 0,
    "abhaAddress": "<ABHA_ADDRESS>",
    "scanPayRequestId": "<SCAN_PAY_REQUEST_ID>",
    "status": "<STATUS>",
    "dateModified": "<DATE_MODIFIED>",
    "dateCreated": "<DATE_CREATED>",
    "orderNumber": "<ORDER_NUMBER>",
    "transactionId": "<TRANSACTION_ID>",
    "hipId": "<HIP_ID>",
    "paymentDate": "<PAYMENT_DATE>",
    "paymentUrl": "<PAYMENT_URL>",
    "paymentAmount": "<PAYMENT_AMOUNT>",
    "counterCode": "<COUNTER_CODE>",
    "facilityName": "<FACILITY_NAME>",
    "patientSelectRequestId": "<PATIENT_SELECT_REQUEST_ID>",
    "paymentDesc": [
      {
        "category": "<CATEGORY>",
        "services": [
          {
            "name": "<NAME>",
            "description": "<DESCRIPTION>",
            "amount": 0,
            "serviceId": "<SERVICE_ID>"
          }
        ]
      }
    ],
    "paymentReceiptLink": "<PAYMENT_RECEIPT_LINK>",
    "scanPayVersion": "<SCAN_PAY_VERSION>"
  }
]
```
