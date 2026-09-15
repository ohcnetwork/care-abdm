# notify status

`GET /scan-pay/notify/status/{id}`

Returns the payment status of one scan and pay request, with the receipt link once paid.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/scan-pay/notify/status/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `id` (string, required): Passed as a path segment.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "abhaAddress": "<ABHA_ADDRESS>",
  "scanPayRequestId": "<SCAN_PAY_REQUEST_ID>",
  "status": "<STATUS>",
  "orderNumber": "<ORDER_NUMBER>",
  "transactionId": "<TRANSACTION_ID>",
  "hipId": "<HIP_ID>",
  "paymentDate": "<PAYMENT_DATE>",
  "paymentReceiptLink": "<PAYMENT_RECEIPT_LINK>"
}
```
