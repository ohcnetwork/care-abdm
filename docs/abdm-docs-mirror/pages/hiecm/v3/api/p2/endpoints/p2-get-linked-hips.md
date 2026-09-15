# Get Linked HIPs

`GET /api/care-context-link/fetch/hips`

Lists the HIPs linked to the person whose records have not yet been transferred, with the base URL to download from.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/fetch/hips \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "downloadBaseUrl": "https://abhasbx.abdm.gov.in/abha/api/v3/fetchFile/phrpullrecord/",
  "unTransferredHipIds": [
    {
      "id": "LTIM_HIP_1",
      "name": "<NAME>"
    },
    {
      "id": "LTIM_HIP",
      "name": "<NAME>"
    },
    "... 1 more of the same shape"
  ]
}
```
