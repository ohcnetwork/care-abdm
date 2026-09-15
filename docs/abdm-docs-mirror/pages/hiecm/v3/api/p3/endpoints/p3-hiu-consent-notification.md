# HIU Consent Notification

`POST /api/consent-management/consent/request/notify`

Notification the gateway sends a HIU when a consent request is granted, denied, revoked or expires.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consent/request/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "consentRequestId": "<TXN_ID>",
    "status": "DENIED",
    "consentArtefacts": [
      {
        "id": "<TXN_ID>"
      }
    ]
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `notification` (object, required)
- `notification.consentRequestId` (string, required)
- `notification.status` (string, required)
- `notification.consentArtefacts` (object[], required)
- `notification.consentArtefacts.id` (string, required)

## Responses

- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
