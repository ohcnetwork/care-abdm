# Revoke Consent

`POST /api/consent-management/consents/revoke`

Revokes the consent artefacts given, so the HIUs holding them can no longer fetch under them.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consents/revoke \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "consents": [
    "<TXN_ID>"
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `consents` (string[], required)

## Responses

- `200`: Example values, scrubbed.
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "<MESSAGE>",
  "error": {
    "code": "<CODE>",
    "message": "<MESSAGE>"
  }
}
```
