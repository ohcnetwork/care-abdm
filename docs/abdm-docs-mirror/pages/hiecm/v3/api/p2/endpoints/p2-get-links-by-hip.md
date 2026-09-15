# Get Links by HIP

`POST /api/care-context-link/link/get-links`

Lists the person's linked care contexts grouped by HIP.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/link/get-links \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "patient": {
      "id": "nithishjanithi@sbx",
      "links": [
        {
          "id": 496112,
          "smartData": {
            "dataProcessed": true,
            "status": "APPROVED",
            "documentId": "<TXN_ID>",
            "enabledForProcessing": true,
            "isAarogyaSetuProcessed": true
          },
          "hip": {
            "id": "DigiLocker_NEGD",
            "name": "<NAME>",
            "type": "HIP"
          },
          "referenceNumber": "nithishjanithi@sbx",
          "careContexts": [
            {
              "referenceNumber": "25ac532f-178d-5885-9bcb-b82052f345eb_20260604192056317009",
              "patientReference": "nithishjanithi@sbx",
              "hiTypes": [
                "OPConsultation"
              ]
            }
          ],
          "dateCreated": "2026-06-04 19:00:00.0",
          "isBookmarked": false
        },
        {
          "id": 481118,
          "smartData": {
            "dataProcessed": false,
            "enabledForProcessing": true,
            "isAarogyaSetuProcessed": false
          },
          "hip": {
            "id": "DigiLocker_NEGD",
            "name": "<NAME>",
            "type": "HIP"
          },
          "referenceNumber": "nithishjanithi@sbx",
          "careContexts": [
            {
              "referenceNumber": "25ac532f-178d-5885-9bcb-b82052f345eb_20260523161917547707",
              "patientReference": "nithishjanithi@sbx",
              "hiTypes": [
                "OPConsultation"
              ]
            }
          ],
          "dateCreated": "2026-05-23 16:06:14.614",
          "isBookmarked": false
        },
        "... 8 more of the same shape"
      ]
    }
  }
]
```
