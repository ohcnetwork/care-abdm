# Initiate Subscription Request

`POST /api/consent-management/subscription-requests/init`

Raises a subscription request as a HIU: asks to be notified when the patient links new care contexts at the HIPs and categories named, for a period.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/subscription-requests/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiu": {
    "id": "<hiu-id>"
  },
  "patient": {
    "id": "<abha-address>@abdm"
  },
  "purpose": {
    "text": "Care Management",
    "code": "CAREMGT",
    "refUri": "www.abdm.gov.in"
  },
  "hips": [
    {
      "id": "<hip-id>"
    }
  ],
  "categories": [
    "LINK",
    "DATA"
  ],
  "period": {
    "from": "2021-01-01T00:00:00.000Z",
    "to": "2023-12-31T23:59:59.999Z"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `hiu` (object, required)
- `hiu.id` (string, required)
- `patient` (object, required)
- `patient.id` (string, required)
- `purpose` (object, required)
- `purpose.text` (string, required)
- `purpose.code` (string, required)
- `purpose.refUri` (string, required)
- `hips` (object[], required)
- `hips.id` (string, required)
- `categories` (string[], required)
- `period` (object, required)
- `period.from` (string, required)
- `period.to` (string, required)

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
