# Update

`PUT /health/service/bookmark/update/{id}`

Updates the title or address of a saved place bookmark.

```bash
curl --request PUT \
  --url https://phrsbx.abdm.gov.in/health/service/bookmark/update/{id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "title": "Happy Family",
  "address": "<ADDRESS>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `id` (string, required): Passed as a path segment.

## Body

- `title` (string, required)
- `address` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "id": 245,
  "abhaAddress": "<ABHA_ADDRESS>",
  "title": "Happy Family",
  "address": "<ADDRESS>",
  "latitude": null,
  "longitude": null,
  "isDeleted": false,
  "createdTime": "2026-05-29T15:38:17.982575",
  "updatedTime": "2026-05-29T15:41:49.399205251"
}
```
