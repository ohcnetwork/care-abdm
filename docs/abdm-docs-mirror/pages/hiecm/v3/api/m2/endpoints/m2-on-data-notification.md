# The provider pushes encrypted health information to the URL named in the request.

`POST /api-hiu/data/notification`

The provider pushes encrypted health information to the URL named in the request.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/api-hiu/data/notification \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`. M2 also uses per flow tokens, a link token for linking and an authorisation token for patient scoped calls. Their header names are not yet published.

## Responses

- `202`: Accepted. Acknowledge quickly, then process asynchronously.
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
