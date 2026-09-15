# The consent request was accepted, with its request id

`POST /api/v3/hiu/consent/request/on-init`

Carries the consent request and the request id. Store the request id: it is how a later notification is tied back to the request you made.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/api/v3/hiu/consent/request/on-init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "consentRequest": {
    "id": "77969467-5a92-44bb-9d6c-4caf24907ea5"
  },
  "error": null,
  "response": {
    "requestId": "6cb80f71-49fa-4f8c-93d5-de9916a708e8"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Body

- `consentRequest` (object, required)
- `consentRequest.id` (string, required)
- `error` (null, required)
- `response` (object, required)
- `response.requestId` (string, required)

## Responses

- `200`: Your bridge acknowledged the callback with 200 OK. The gateway validates the body you send back, so a 200 carrying the wrong body is still a failure.
