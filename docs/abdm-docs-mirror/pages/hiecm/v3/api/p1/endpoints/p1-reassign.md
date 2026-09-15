# reassign

`PUT /api/family-management/reassign`

Moves an existing family link to a different relationship type without delinking and assigning again.

```bash
curl --request PUT \
  --url https://phrsbx.abdm.gov.in/api/family-management/reassign \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Relationship type changed successfully",
  "success": true
}
```
