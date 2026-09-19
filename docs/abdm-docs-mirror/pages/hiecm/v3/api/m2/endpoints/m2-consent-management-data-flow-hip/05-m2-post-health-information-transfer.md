# Receive the transferred health information

`POST /health-information/transfer`

<p><strong>NOTE:</strong> This API is actually the callback URL that is passed as <code>dataPushUrl</code> in the data request API - <code>/api/v3/hip/health-information/request</code>. This API is directly called by HIP Data Bridge and is not mediated via CM, and hence not routed through the Gateway.</p> <ul> <li>This API should be implemented at HIU side. It may be implemented by the Data Bridge representing the HIU.</li> <li>Entry elements may be content or link, although for version 1, entry content is preferred.</li> <li>Entry content (or even link reference content) must be encrypted by means of Elliptic-curve Diffie–Hellman Key Exchange, using the HIU key materials that are passed through the data request API - <code>/api/v3/hip/health-information/request</code>.</li> <li>Media contains the mimetype of content, and for v1, it is "application/fhir+json".</li> <li>Checksum is MD5 checksum of the data content, before encryption.</li> <li>Please refer to the ABDM Sandbox Documentation for the format of FHIR bundle that is passed through content.</li> </ul> <ol type="*"><li><strong>Authorisation token is mandatory for this API.</strong></li></ol>

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/health-information/transfer \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "pageNumber": 0,
  "pageCount": 1,
  "transactionId": "<TRANSACTION_ID>",
  "entries": [
    {
      "content": "Encrypted content of data packaged in FHIR bundle",
      "media": "application/fhir+json",
      "checksum": "string",
      "careContextReference": "1931-nd2"
    }
  ],
  "keyMaterial": {
    "cryptoAlg": "ECDH",
    "curve": "Curve25519",
    "dhPublicKey": {
      "expiry": "<EXPIRY>",
      "parameters": "Curve25519/32byte random key",
      "keyValue": "<KEY_VALUE>"
    },
    "nonce": "<NONCE>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Body

- `pageNumber` (integer, required): Current page number.
- `pageCount` (integer, required): Total number of pages.
- `transactionId` (string, required): Transaction Id issued when data requested.
- `entries` (object[], required)
- `entries.content` (string, required): Encrypted content
- `entries.media` (string, required) One of: application/fhir+json.
- `entries.checksum` (string, required): Md5 checksum of the content before encryption
- `entries.careContextReference` (string, required): care context reference number.
- `keyMaterial` (object, required): Encryption and decryption key details.
- `keyMaterial.cryptoAlg` (string, required) One of: ECDH.
- `keyMaterial.curve` (string, required) One of: Curve25519.
- `keyMaterial.dhPublicKey` (object, required)
- `keyMaterial.dhPublicKey.expiry` (string, required)
- `keyMaterial.dhPublicKey.parameters` (string, required): Parameters of the encryption and decryption key. One of: Curve25519/32byte random key.
- `keyMaterial.dhPublicKey.keyValue` (string, required)
- `keyMaterial.nonce` (string, required)

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized. The request carried no valid credentials, or the access token has expired. Obtain a fresh token from the session API and retry.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
