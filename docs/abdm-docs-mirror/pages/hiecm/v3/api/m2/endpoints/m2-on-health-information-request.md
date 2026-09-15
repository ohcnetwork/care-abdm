# A request for the records a consent covers

`POST /api/v3/hip/health-information/request`

Inbound to the HIP, carrying the consent id, the date range, the data push URL and the encryption parameters. You have 20 minutes from this request to the data push.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/api/v3/hip/health-information/request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`. M2 also uses per flow tokens, a link token for linking and an authorisation token for patient scoped calls. Their header names are not yet published.

## Responses

- `202`: Your bridge accepted the callback. The gateway validates the body you send back, so a 202 carrying the wrong body is still a failure.
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
