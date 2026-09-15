# assign

`POST /api/family-management/assign`

Links another ABHA address to the signed-in person's address under a relationship type, so the two profiles are managed as a family.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/family-management/assign \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "relatedAbhaAddress": "nithishnov@sbx",
  "relationshipTypeId": 2
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `relatedAbhaAddress` (string, required)
- `relationshipTypeId` (integer, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Relationship assigned successfully",
  "success": true,
  "relationshipId": null
}
```
