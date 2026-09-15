# Create a session and get an access token

`POST /api/hiecm/gateway/v3/sessions`

Send the client id and client secret from your ABDM sandbox
registration. The response carries a bearer token that every module
API accepts in the `Authorization` header.

This is the one call that does not itself need a bearer token, which
is why `security` is empty here.

The token is short lived. Read `expiresIn` from the response rather
than assuming a duration, and refresh before it runs out instead of
waiting for a 401.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "<CLIENT_ID>",
  "clientSecret": "<CLIENT_SECRET>",
  "grantType": "client_credentials"
}'
```

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. It is how you and the gateway correlate a call with its callback and with a support ticket, so log it. Reusing one across requests makes both impossible.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. Sending the wrong one against the right host is a common first-day failure and reads as an authorisation error.

## Body

- `clientId` (string, required): The client id issued when you registered on the ABDM sandbox.
- `clientSecret` (string, required): The client secret issued alongside the client id. It is a credential. Keep it server side, never in a mobile or browser build.
- `grantType` (string, required): The only accepted value is `client_credentials`.

## Responses

- `200`: A session was created and a bearer token was issued.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "accessToken": "<ACCESS_TOKEN>",
  "expiresIn": 0,
  "refreshExpiresIn": 0,
  "refreshToken": "<REFRESH_TOKEN>",
  "tokenType": "bearer"
}
```
