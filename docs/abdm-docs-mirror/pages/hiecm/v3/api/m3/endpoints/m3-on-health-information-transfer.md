# The encrypted health data itself, pushed to the URL you supplied

`POST /health-information/transfer`

The actual encrypted FHIR bundle. The HIP Data Bridge posts this directly to
the `dataPushUrl` you supplied in the health information request; it is not
routed through the Gateway, and this literal path is illustrative rather than
fixed, because `dataPushUrl` is a URL you host and register yourself.

Decrypt `entries[].content` with the ECDH shared secret derived from your
private key and `keyMaterial`. `entries[].checksum` is the MD5 of the content
before encryption, so verify it after decrypting. Large payloads arrive across
several calls, paginated by `pageNumber` and `pageCount`.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/health-information/transfer \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "pageNumber": 1,
  "pageCount": 1,
  "transactionId": "8376a2b0-3fc9-4bb5-8af5-54a49a3910f4",
  "entries": [
    {
      "content": "encrypted-fhir-bundle-content",
      "media": "application/fhir+json",
      "checksum": "d41d8cd98f00b204e9800998ecf8427e",
      "careContextReference": "manishk@abdm-02"
    }
  ],
  "keyMaterial": {
    "cryptoAlg": "ECDH",
    "curve": "Curve25519",
    "dhPublicKey": {
      "expiry": "2024-12-31T00:00:00.000Z",
      "parameters": "Curve25519/32byte",
      "keyValue": "base64-encoded-hip-ecdh-public-key"
    },
    "nonce": "base64-encoded-random-nonce-32bytes"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Body

- `pageNumber` (integer, required): Current page number, for a multi-page transfer.
- `pageCount` (integer, required): Total number of pages in this transfer.
- `transactionId` (string, required): The transaction id issued when the health information was requested.
- `entries` (object[], required)
- `entries.content` (string, required): Encrypted FHIR bundle content.
- `entries.media` (string, required) One of: application/fhir+json.
- `entries.checksum` (string, required): MD5 checksum of the content, taken before encryption.
- `entries.careContextReference` (string, required): The care context this entry's data belongs to.
- `keyMaterial` (object, required): ECDH key material for end-to-end encryption of health data
- `keyMaterial.cryptoAlg` (string, required) One of: ECDH.
- `keyMaterial.curve` (string, required) One of: Curve25519.
- `keyMaterial.dhPublicKey` (object, required)
- `keyMaterial.dhPublicKey.expiry` (string, required): Key expiry time
- `keyMaterial.dhPublicKey.parameters` (string, required)
- `keyMaterial.dhPublicKey.keyValue` (string, required): Base64-encoded ECDH public key (32 bytes for Curve25519)
- `keyMaterial.nonce` (string, required): Base64-encoded random nonce (32 bytes), unique per request

## Responses

- `202`: Accepted. Verify the checksum after decrypting before treating the transfer as complete.
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
