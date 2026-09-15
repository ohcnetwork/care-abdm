# Delete push notification

`DELETE /api/notification/schedule-push-notification/0eg`

Deletes a scheduled push notification by its id.

```bash
curl --request DELETE \
  --url https://phrsbx.abdm.gov.in/api/notification/schedule-push-notification/0eg \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: No response body is documented for this request.
