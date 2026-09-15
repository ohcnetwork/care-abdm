# Create

`POST /health/service/bookmark/create`

Saves a place as a bookmark for the signed-in ABHA address, with a title, address and coordinates.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/health/service/bookmark/create \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "title": "House_05",
  "address": "<ADDRESS>",
  "latitude": 40.7128,
  "longitude": -74.006
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `title` (string, required)
- `address` (string, required)
- `latitude` (number, required)
- `longitude` (number, required)

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
  "id": 244,
  "abhaAddress": "<ABHA_ADDRESS>",
  "title": "House_05",
  "address": "<ADDRESS>",
  "latitude": 40.7128,
  "longitude": -74.006,
  "isDeleted": false,
  "createdTime": "2026-05-29T15:36:43.437326935",
  "updatedTime": "2026-05-29T15:36:43.437335006"
}
```
