# Certificate

`GET /api/global/phr/public-certificate`

Returns the ABDM public key and the encryption algorithm to apply with it. Fetch it before encrypting any value for the PHR application services.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/global/phr/public-certificate \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "publicKey": "<PUBLICKEY>",
  "encryptionAlgorithm": "RSA/ECB/OAEPWithSHA-1AndMGF1Padding",
  "abhaPublicKey": "<ABHAPUBLICKEY>"
}
```
