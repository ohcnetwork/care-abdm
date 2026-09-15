# PHR - Get File Metadata

`GET /api/care-context-link/phr/file/details`

Returns a record file's name, size and chunk size, so it can be downloaded in parts.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/phr/file/details \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "fileName": "nithishjanithi@sbx/DigiLocker_NEGD/25ac532f-178d-5885-9bcb-b82052f345eb_20260604192056317009/<TXN_ID>.json",
  "fileSize": 27636,
  "chunkSize": 5242880
}
```
