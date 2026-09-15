# Set Up Subscription for Aarogya Setu

`POST /api/consent-management/subscription/setup`

Sets up the PHR application's own subscription, so it is notified when the person links new care contexts.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/subscription/setup \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
