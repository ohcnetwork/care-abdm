# 02 link-init

`POST /user-initiated-linking/link/init`

Initiates linking of the care contexts discovered at a HIP. The HIP replies with how the person will authenticate.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/user-initiated-linking/link/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "<TXN_ID>",
  "patient": [
    {
      "referenceNumber": "<ABHA_ADDRESS>",
      "display": "Test",
      "careContexts": [
        {
          "referenceNumber": "Test 1",
          "display": "Sugar Test"
        }
      ],
      "hiType": "Invoice",
      "count": 1
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `transactionId` (string, required)
- `patient` (object[], required)
- `patient.referenceNumber` (string, required)
- `patient.display` (string, required)
- `patient.careContexts` (object[], required)
- `patient.careContexts.referenceNumber` (string, required)
- `patient.careContexts.display` (string, required)
- `patient.hiType` (string, required)
- `patient.count` (integer, required)

## Responses

- `200`: No response body is documented for this request.
