# search

`POST /nhcx/search`

Searches a payer's records for a member's policy through the National Health Claims Exchange. The result arrives at `on_submit`.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/nhcx/search \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "memberId": "PZ2Q9UZHM",
  "payerId": "1518@hcx",
  "productId": "100155",
  "productName": "PMJAY/HP/S/G",
  "processingId": "1518@hcx"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `memberId` (string, required)
- `payerId` (string, required)
- `productId` (string, required)
- `productName` (string, required)
- `processingId` (string, required)

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
  "timestamp": "12/06/2026 20:59:22",
  "api_call_id": "<TXN_ID>",
  "correlation_id": "<TXN_ID>",
  "result": {
    "sender_code": "NAS_001@hcx",
    "recipient_code": "1518@hcx",
    "entity_type": "preauth",
    "protocol_status": "request.queued"
  },
  "error": null
}
```
