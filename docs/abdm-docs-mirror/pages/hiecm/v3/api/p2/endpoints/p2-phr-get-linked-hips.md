# PHR - Get Linked HIPs

`GET /api/care-context-link/phr/fetch/hips`

Lists the HIPs whose records have been transferred for the person, with the base URL to download from.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/phr/fetch/hips \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.

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
