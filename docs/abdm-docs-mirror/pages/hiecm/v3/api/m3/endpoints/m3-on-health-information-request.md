# Acknowledgement of a health information request

`POST /api/v3/hiu/health-information/on-request`

Carries the transaction id, the request id and the current status. This is an acknowledgement, not the records. The records arrive at the data push URL you supplied.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/api/v3/hiu/health-information/on-request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiRequest": {
    "transactionId": "8376a2b0-3fc9-4bb5-8af5-54a49a3910f4",
    "sessionStatus": "REQUESTED"
  },
  "error": null,
  "response": {
    "requestId": "e492d2b5-5f0a-4406-8a5d-5b4351e2ff2c"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Body

- `hiRequest` (object, required)
- `hiRequest.transactionId` (string, required)
- `hiRequest.sessionStatus` (string, required)
- `error` (null, required)
- `response` (object, required)
- `response.requestId` (string, required)

## Responses

- `200`: Your bridge acknowledged the callback with 200 OK. The gateway validates the body you send back, so a 200 carrying the wrong body is still a failure.
