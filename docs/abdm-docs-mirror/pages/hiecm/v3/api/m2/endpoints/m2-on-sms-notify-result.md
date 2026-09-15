# The outcome of an SMS deep link notify call you made

`POST /v3/patients/sms/on-notify`

Hosted by your bridge, not by ABDM. The gateway calls this endpoint at the callback URL registered for your bridge, so the path above is relative to that URL. This is the result leg for `m2_sms_deep_link_notify`.

`response.requestId` echoes the REQUEST-ID you sent to m2_sms_deep_link_notify.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/patients/sms/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "SUCCESS"
  },
  "error": {
    "code": "<CODE>",
    "message": "<MESSAGE>"
  },
  "response": {
    "requestId": "<REQUEST_ID>"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`. M2 also uses per flow tokens, a link token for linking and an authorisation token for patient scoped calls. Their header names are not yet published.

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value, so this is how you match an asynchronous reply to the call that caused it. Store it before you send the request, not after.
- `TIMESTAMP` (string, required): The current time in ISO 8601, UTC, with milliseconds and a `Z` suffix, from a synchronised clock. The sandbox rejects IST and accepts UTC.
- `X-HIP-ID` (string, required): Identifier of the Health Information Provider the request or callback belongs to. This is per facility, and it is what a callback arriving at your one bridge URL is routed on. The bridge URL and your credentials belong to the integration, not to the facility.

## Body

- `acknowledgement` (object, required)
- `acknowledgement.status` (string, required) One of: SUCCESS, ERRORED.
- `error` (object): The error code and message on a failed callback delivery.
- `error.code` (string, required)
- `error.message` (string, required)
- `response` (object, required): Echo of the requestId from the original Gateway-to-HIP request
- `response.requestId` (string, required): requestId received in the original Gateway request to HIP bridge

## Responses

- `200`: Your bridge accepted the callback. The gateway validates the body you send back, so a 200 carrying the wrong body is still a failure.
