# Get Gateway JWKS Certificates

`GET /api/hiecm/gateway/v3/certs`

Get the JSON Web Key Set (JWKS) to verify JWT signatures in gateway callbacks.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/certs \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z'
```

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. It is how you and the gateway correlate a call with its callback and with a support ticket, so log it. Reusing one across requests makes both impossible.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.

## Responses

- `200`: JWKS response

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "keys": [
    {
      "kid": "<KID>",
      "kty": "<KTY>",
      "alg": "<ALG>",
      "use": "<USE>",
      "n": "<N>",
      "e": "<E>",
      "x5c": [
        "<X5C>"
      ],
      "x5t": "<X5T>",
      "x5t2": "<X5T2>"
    }
  ]
}
```
