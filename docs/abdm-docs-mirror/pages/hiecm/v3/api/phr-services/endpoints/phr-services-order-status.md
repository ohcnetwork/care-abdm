# order-status

`POST /scan-pay/order-status`

Returns the status of a scan and pay order by its order number.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/scan-pay/order-status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "orderNumber": "ORD-ABDM-123456",
  "openOrderRequestId": "<TXN_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `orderNumber` (string, required)
- `openOrderRequestId` (string, required)

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
