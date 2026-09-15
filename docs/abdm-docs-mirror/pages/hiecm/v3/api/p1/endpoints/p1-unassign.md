# unassign

`PUT /api/family-management/unassign`

Ends the family relationship with the related ABHA address given, on the signed-in person's side.

```bash
curl --request PUT \
  --url https://phrsbx.abdm.gov.in/api/family-management/unassign \
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
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Relationship unassigned successfully",
  "success": true
}
```
