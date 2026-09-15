# Get Subscription Details by Request ID

`GET /api/consent-management/subscription-requests/request/{subscriptionRequestId}`

Returns one subscription request with its status and details, by the request id.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/consent-management/subscription-requests/request/{subscriptionRequestId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `subscriptionRequestId` (string, required): Passed as a path segment.

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
  "requestId": "<TXN_ID>",
  "patientId": "<PATIENT_ID>",
  "requesterType": "HEALTH_LOCKER",
  "status": "UNSUBSCRIBED",
  "details": {
    "subscriptionRequestId": "<TXN_ID>",
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
    }
  },
  "dateCreated": "2026-05-29T09:18:26.944Z",
  "dateModified": "2026-05-29T09:20:41.769Z",
  "healthIdNumber": "<ABHA_NUMBER>"
}
```
