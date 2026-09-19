# Switch profile

`GET /abha/api/v3/phr/app/login/profile/switch-profile`

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/login/profile/switch-profile \
  --header 'X-token: Bearer <JWT TOKEN>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

## Headers

- `X-token` (string, required)
- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Responses

- `200`: OK
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "baeb429f-4ff0-42e3-abd6-fb55fa0f5bf1",
  "users": [
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    },
    {
      "abhaAddress": "<ABHA_ADDRESS>",
      "fullName": "John Doe",
      "status": "ACTIVE",
      "kycStatus": "PENDING"
    },
    "... 1 more of the same shape"
  ],
  "tokens": {
    "token": "<JWT TOKEN>",
    "expiresIn": 300,
    "refreshToken": null,
    "refreshExpiresIn": null
  }
}
```
