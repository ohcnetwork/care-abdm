# Encrypt a value with the ABDM public key

`POST /v3/phr/app/enrollment/encrypt`

Every `loginId` in M1 is encrypted rather than sent raw, and this is the
hosted helper for doing it. It is convenient for trying a flow by hand.

Do not put it in a production path. Sending an Aadhaar or mobile number to
a remote endpoint so that it can be encrypted defeats the point of
encrypting it. Encrypt locally against NHA's published public key
instead.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/encrypt \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'KEY_TYPE: <KEY_TYPE>' \
  --header 'Content-Type: application/json' \
  --data '{
  "data": "1"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `KEY_TYPE` (string): Which ABDM public key the encryption helper should use.

## Body

- `data` (string, required)

## Responses

- `200`: The specification does not describe this body. Send the call with Try it to see what comes back.
