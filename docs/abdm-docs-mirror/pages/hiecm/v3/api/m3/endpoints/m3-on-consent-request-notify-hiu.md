# The patient's decision, sent to the requester

`POST /api/v3/hiu/consent/request/notify`

On a grant, carries every consent artefact id created against the request, with the request id. On a denial, carries the denial, with `reason` set if the gateway supplied one.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/api/v3/hiu/consent/request/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "consentRequestId": "77969467-5a92-44bb-9d6c-4caf24907ea5",
    "status": "GRANTED",
    "reason": null,
    "consentArtefacts": [
      {
        "id": "28ef6ae8-ad03-488d-b26e-940e27154cc0"
      }
    ]
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Body

- `notification` (object, required)
- `notification.consentRequestId` (string, required)
- `notification.status` (string, required)
- `notification.reason` (string,null, required): Set when the request was denied; null otherwise.
- `notification.consentArtefacts` (object[], required)
- `notification.consentArtefacts.id` (string, required)

## Responses

- `200`: Your bridge acknowledged the callback with 200 OK. The gateway validates the body you send back, so a 200 carrying the wrong body is still a failure.
