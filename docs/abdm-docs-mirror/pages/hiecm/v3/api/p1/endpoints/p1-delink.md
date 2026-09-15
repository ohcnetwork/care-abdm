# delink

`PUT /api/family-management/delink`

Removes the family link between the signed-in person's ABHA address and the related address given.

```bash
curl --request PUT \
  --url https://phrsbx.abdm.gov.in/api/family-management/delink \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "relatedAbhaAddress": "nithishnov@sbx"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `relatedAbhaAddress` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Relationship delinked successfully",
  "success": true,
  "relationshipId": null
}
```
