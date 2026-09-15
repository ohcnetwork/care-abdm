# get-coverage-eligibility

`POST /nhcx/get-coverage-eligibility`

Checks whether a person's insurance policy covers them, through the National Health Claims Exchange. The result arrives at `on_check`.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/nhcx/get-coverage-eligibility \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "sno": "200012950",
  "abhanumber": "<ABHA_NUMBER>",
  "mobilenumber": "<MOBILE>",
  "memberid": "PM3T2HSBX",
  "payerid": "1518@hcx",
  "productid": "100155",
  "productname": "PMJAY/HP/S/G",
  "processingid": "1518@hcx"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `sno` (string, required)
- `abhanumber` (string, required)
- `mobilenumber` (string, required)
- `memberid` (string, required)
- `payerid` (string, required)
- `productid` (string, required)
- `productname` (string, required)
- `processingid` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "timestamp": "<TIMESTAMP>",
  "api_call_id": "<API_CALL_ID>",
  "correlation_id": "<CORRELATION_ID>",
  "result": {
    "sender_code": "<SENDER_CODE>",
    "recipient_code": "<RECIPIENT_CODE>",
    "entity_type": "<ENTITY_TYPE>",
    "protocol_status": "<PROTOCOL_STATUS>"
  },
  "error": "<ERROR>"
}
```
