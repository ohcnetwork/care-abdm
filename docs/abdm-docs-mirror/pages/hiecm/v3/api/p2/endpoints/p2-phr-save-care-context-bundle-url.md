# PHR - Save Care Context Bundle URL

`POST /api/care-context-link/phr/care-context/bundle-url`

Records where the FHIR bundle for a care context was stored, with its fetch status.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/phr/care-context/bundle-url \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "careContextLinkId": 12345,
  "bundleUrl": "https://example.com/bundle/url",
  "status": "RECEIVED"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `careContextLinkId` (integer, required)
- `bundleUrl` (string, required)
- `status` (string, required)

## Responses

- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
