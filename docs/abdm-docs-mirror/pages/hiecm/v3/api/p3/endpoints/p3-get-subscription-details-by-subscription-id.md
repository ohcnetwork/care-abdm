# Get Subscription Details by Subscription ID

`GET /api/consent-management/subscription-requests/{subscriptionId}`

Returns one subscription with its details, by the subscription id.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/consent-management/subscription-requests/{subscriptionId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `subscriptionId` (string, required): Passed as a path segment.

## Responses

- `200`: No response body is documented for this request.
