# Get All HIU Subscription Requests

`GET /api/consent-management/subscription-requests`

Lists the subscription requests HIUs have raised against the signed-in ABHA address, with paging.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/consent-management/subscription-requests \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "size": 5,
  "limit": 5,
  "offset": 0,
  "requests": [
    {
      "requestId": "<TXN_ID>",
      "createdAt": "2026-05-29T09:18:26.944Z",
      "lastUpdated": "2026-05-29T09:20:41.769Z",
      "purpose": {
        "text": "Self Requested",
        "code": "PATRQT",
        "refUri": "www.abdm.gov.in"
      },
      "patient": {
        "id": "nithishjanithi@sbx"
      },
      "hiu": {
        "id": "Priyanka_Health_Locker",
        "name": "<NAME>",
        "type": "HEALTH LOCKER"
      },
      "hips": [],
      "categories": [
        "DATA",
        "LINK"
      ],
      "period": {
        "from": "2026-05-29T09:19:26.699Z",
        "to": "2126-05-29T09:18:26.699Z"
      },
      "status": "UNSUBSCRIBED",
      "requesterType": "HEALTH_LOCKER"
    },
    {
      "requestId": "<TXN_ID>",
      "createdAt": "2025-06-15T14:53:24.437Z",
      "lastUpdated": "2026-05-29T09:20:41.769Z",
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "www.abdm.gov.in"
      },
      "patient": {
        "id": "nithishjanithi@sbx"
      },
      "hiu": {
        "id": "Priyanka_Health_Locker",
        "name": "<NAME>",
        "type": "HEALTH LOCKER"
      },
      "hips": [],
      "categories": [
        "LINK",
        "DATA"
      ],
      "period": {
        "from": "2024-01-01T09:00:00.000Z",
        "to": "2124-12-31T09:00:00.000Z"
      },
      "status": "UNSUBSCRIBED",
      "requesterType": "HEALTH_LOCKER",
      "subscriptionId": "<TXN_ID>"
    },
    "... 2 more of the same shape"
  ]
}
```
