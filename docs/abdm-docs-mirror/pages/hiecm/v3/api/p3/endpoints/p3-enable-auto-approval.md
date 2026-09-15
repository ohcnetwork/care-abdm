# Enable Auto Approval

`POST /api/consent-management/consents/auto-approval-policy/{autoApprovalId}/enable`

Turns an auto-approval policy back on.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consents/auto-approval-policy/{autoApprovalId}/enable \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `autoApprovalId` (string, required): Passed as a path segment.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
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
