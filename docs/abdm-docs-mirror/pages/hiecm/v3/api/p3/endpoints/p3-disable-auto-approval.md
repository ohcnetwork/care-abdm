# Disable Auto Approval

`POST /api/consent-management/consents/auto-approval-policy/{autoApprovalId}/disable`

Turns off an auto-approval policy, so later consent requests it would have matched wait for the person again.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consents/auto-approval-policy/{autoApprovalId}/disable \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `autoApprovalId` (string, required): Passed as a path segment.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "error": {
    "code": "<CODE>",
    "message": "<MESSAGE>"
  },
  "message": "<MESSAGE>"
}
```
