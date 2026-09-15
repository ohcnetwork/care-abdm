# Deny Consent Request

`POST /api/consent-management/consent-requests/{consentRequestId}/deny`

Denies a consent request, with the reason the person gave.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consent-requests/{consentRequestId}/deny \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "reason": "Not required"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `consentRequestId` (string, required): Passed as a path segment.

## Body

- `reason` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "status": "<STATUS>",
  "error": {
    "code": "<CODE>",
    "message": "<MESSAGE>"
  }
}
```
