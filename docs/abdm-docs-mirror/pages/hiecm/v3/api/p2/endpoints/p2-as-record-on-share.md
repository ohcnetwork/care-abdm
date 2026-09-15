# AS - Record On Share

`POST /scan-share/record-share/on-share`

Callback the gateway sends with the outcome of a record share request.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/scan-share/record-share/on-share \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiRequest": {
    "transactionId": "<TXN_ID>",
    "dataPushUrl": "https://webhook.site/<TXN_ID>/health-information/transfer",
    "keyMaterial": {
      "cryptoAlg": "ECDH.",
      "curve": "curve25519",
      "dhPublicKey": {
        "expiry": "2026-12-28T13:18:20.742Z",
        "parameters": "Ephemeral public key.",
        "keyValue": "<KEYVALUE>"
      },
      "nonce": "H5EG5X61tTJ2ctjs3ByenbMvUezrf1VCRHZukspooaY="
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

- `hiRequest` (object, required)
- `hiRequest.transactionId` (string, required)
- `hiRequest.dataPushUrl` (string, required)
- `hiRequest.keyMaterial` (object, required)
- `hiRequest.keyMaterial.cryptoAlg` (string, required)
- `hiRequest.keyMaterial.curve` (string, required)
- `hiRequest.keyMaterial.dhPublicKey` (object, required)
- `hiRequest.keyMaterial.dhPublicKey.expiry` (string, required)
- `hiRequest.keyMaterial.dhPublicKey.parameters` (string, required)
- `hiRequest.keyMaterial.dhPublicKey.keyValue` (string, required)
- `hiRequest.keyMaterial.nonce` (string, required)
- `response` (object, required)
- `response.requestId` (string, required)

## Responses

- `200`: No response body is documented for this request.
