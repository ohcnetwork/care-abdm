# call-back link-on-confirm

`POST /api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm`

Callback the gateway sends after a link confirmation: the patient's linked care contexts, or the error that stopped it.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/hiecm/user-initiated-linking/v3/link/care-context/on-confirm \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "patient": [
    {
      "referenceNumber": "<ABHA_ADDRESS>",
      "display": "Test",
      "careContexts": [
        {
          "referenceNumber": "Test 4",
          "display": "Sugar Test"
        }
      ],
      "hiType": "Invoice",
      "count": 1
    }
  ],
  "response": {
    "requestId": "<TXN_ID>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `patient` (object[], required)
- `patient.referenceNumber` (string, required)
- `patient.display` (string, required)
- `patient.careContexts` (object[], required)
- `patient.careContexts.referenceNumber` (string, required)
- `patient.careContexts.display` (string, required)
- `patient.hiType` (string, required)
- `patient.count` (integer, required)
- `response` (object, required)
- `response.requestId` (string, required)

## Responses

- `200`: No response body is documented for this request.
