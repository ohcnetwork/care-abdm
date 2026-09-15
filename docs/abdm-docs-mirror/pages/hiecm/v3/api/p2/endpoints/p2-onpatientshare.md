# onpatientshare

`POST /api/hiecm/patient-share/v3/on-share`

Callback the gateway sends after a profile share at a facility, acknowledging the share request.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/hiecm/patient-share/v3/on-share \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "SUCCESS",
    "abhaAddress": "<ABHA_ADDRESS>",
    "profile": {
      "context": "5",
      "tokenNumber": "<TOKENNUMBER>",
      "expiry": "1800"
    }
  },
  "response": {
    "requestId": "<TXN_ID>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `acknowledgement` (object, required)
- `acknowledgement.status` (string, required)
- `acknowledgement.abhaAddress` (string, required)
- `acknowledgement.profile` (object, required)
- `acknowledgement.profile.context` (string, required)
- `acknowledgement.profile.tokenNumber` (string, required)
- `acknowledgement.profile.expiry` (string, required)
- `response` (object, required)
- `response.requestId` (string, required)

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
