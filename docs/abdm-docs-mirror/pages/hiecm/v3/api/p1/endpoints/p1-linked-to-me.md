# linked-to-me

`GET /api/family-management/linked-to-me`

Lists the ABHA addresses that have linked the signed-in person's address as a family member.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/family-management/linked-to-me \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `202`: Example values, scrubbed.
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 202 response, generated from the schema. The values are placeholders, not a captured response:

```json
"array"
```
