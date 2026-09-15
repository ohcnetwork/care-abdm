# Get HIP IDs

`GET /api/care-context-link/get-hip-ids`

Lists the HIPs whose records have been transferred for the person, with the base URL to download from.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/get-hip-ids \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "downloadBaseUrl": "https://abhasbx.abdm.gov.in/fetchFile/disk4/phrpullrecord/",
  "transferredHipIds": [
    {
      "id": "DigiLocker_NEGD",
      "name": "<NAME>"
    }
  ],
  "lockerView": "PHR"
}
```
