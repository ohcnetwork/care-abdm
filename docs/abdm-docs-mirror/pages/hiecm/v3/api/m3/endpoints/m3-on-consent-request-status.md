# The consent manager reports the state of a consent request you asked about.

`POST /api/v3/hiu/consent/request/on-status`

The consent manager reports the state of a consent request you asked about.

GRANTED is absent from `status`'s enum here on purpose: a grant is communicated
through the notify callback with `consentArtefacts`, not through this status
callback.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/api/v3/hiu/consent/request/on-status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "consentRequest": {
    "id": "77969467-5a92-44bb-9d6c-4caf24907ea5",
    "status": "REQUESTED"
  },
  "error": null,
  "response": {
    "requestId": "68b099de-f7ba-4a92-9bd5-97de2e397f31"
  },
  "resp": null
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Body

- `consentRequest` (object, required)
- `consentRequest.id` (string, required)
- `consentRequest.status` (string, required): GRANTED is not one of these values; see the operation description for why. One of: REQUESTED, DENIED, EXPIRED, REVOKED.
- `error` (null, required)
- `response` (object, required)
- `response.requestId` (string, required)
- `resp` (null, required)

## Responses

- `200`: OK. Acknowledge quickly, then process asynchronously.
