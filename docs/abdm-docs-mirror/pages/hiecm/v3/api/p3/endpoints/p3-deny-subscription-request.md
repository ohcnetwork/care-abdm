# Deny Subscription Request

`POST /api/consent-management/subscription-requests/{subscriptionRequestId}/deny`

Denies a subscription request, so the HIU is not notified of the person's new care contexts.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/subscription-requests/{subscriptionRequestId}/deny \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `subscriptionRequestId` (string, required): Passed as a path segment.

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
