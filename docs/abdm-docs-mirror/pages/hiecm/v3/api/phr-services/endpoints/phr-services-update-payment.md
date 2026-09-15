# update payment

`PUT /scan-pay/update/payment/{id}`

Records the outcome of a scan and pay payment: the amount, the transaction id and the receipt.

```bash
curl --request PUT \
  --url https://phrsbx.abdm.gov.in/scan-pay/update/payment/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "paymentName": "Kidney Function Test(Kft)Panel(Urea+Creat)",
  "orderNumber": "ORD-ABDM-123456",
  "transactionId": "",
  "counterCode": "IN0810000177",
  "paymentUrl": "https://payit.cc/I4321024287",
  "amount": "60.00"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `id` (string, required): Passed as a path segment.

## Body

- `paymentName` (string, required)
- `orderNumber` (string, required)
- `transactionId` (string, required)
- `counterCode` (string, required)
- `paymentUrl` (string, required)
- `amount` (string, required)

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
