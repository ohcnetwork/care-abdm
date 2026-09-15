# Get Health Information by Transaction ID

`GET /api/care-context-link/get/health-information/{transactionId}`

Returns the health information received for a transfer, by its transaction id.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/get/health-information/{transactionId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `transactionId` (string, required): Passed as a path segment.

## Responses

- `200`: No response body is documented for this request.
