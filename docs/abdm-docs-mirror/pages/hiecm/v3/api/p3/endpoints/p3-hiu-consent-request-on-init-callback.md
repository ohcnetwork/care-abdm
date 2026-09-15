# HIU Consent Request On-Init (Callback)

`POST /api/consent-management/consent/request/on-init`

Callback the gateway sends after a consent request is raised: the request id to track it by, or the error that stopped it.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consent/request/on-init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "requestId": "<GENERATED>",
  "timestamp": "<ISO_8601_TIMESTAMP>",
  "consentRequest": {
    "id": "<TXN_ID>"
  },
  "resp": {
    "requestId": "<TXN_ID>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `requestId` (string, required)
- `timestamp` (string, required)
- `consentRequest` (object, required)
- `consentRequest.id` (string, required)
- `resp` (object, required)
- `resp.requestId` (string, required)

## Responses

- `200`: No response body is documented for this request.
