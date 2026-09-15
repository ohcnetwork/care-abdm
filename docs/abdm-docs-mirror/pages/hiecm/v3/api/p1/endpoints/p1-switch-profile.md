# Switch Profile

`GET /profile/phr/switch-profile`

Lists the other accounts the signed-in person can switch to and opens a transaction for the switch.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/profile/phr/switch-profile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "<TXN_ID>",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "manish",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "test",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    },
    "... 70 more of the same shape"
  ],
  "tokens": {
    "token": "<TOKEN>",
    "expiresIn": 300,
    "refreshToken": null,
    "refreshExpiresIn": null
  }
}
```
