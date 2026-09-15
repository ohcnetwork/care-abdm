# verify and assign

`POST /family-management/verify-and-assign`

Verifies the OTP for a family link transaction and, in the same step, links the given ABHA address under the relationship type. May also unassign a previous address.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/family-management/verify-and-assign \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddressToLink": "<ABHA_ADDRESS_TO_LINK>",
  "txnId": "<TXN_ID>",
  "relationshipTypeId": 0,
  "abhaAddressToUnassign": "<ABHA_ADDRESS_TO_UNASSIGN>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `abhaAddressToLink` (string)
- `txnId` (string, required)
- `relationshipTypeId` (integer, required)
- `abhaAddressToUnassign` (string)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "<MESSAGE>",
  "success": false,
  "relationshipId": "<RELATIONSHIP_ID>"
}
```
