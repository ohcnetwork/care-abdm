# Verify the OTP for a profile change

`POST /v3/profile/account/verify`

Completes the change the OTP was raised for. Send the same `scope` you
used when requesting it, along with the `txnId` and the encrypted OTP.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/verify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-profile",
    "mobile-verify"
  ],
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `X-token` (string, required): The user scoped token returned when a person logs in or verifies an OTP. Required on this operation. See the shared `XToken` parameter, and note that this header takes the bare token with no prefix.

## Body

- `scope` (string[], required)
- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `authData.otp` (object)
- `authData.otp.txnId` (string, required)
- `authData.otp.otpValue` (string, required)
- `authData.password` (object)
- `authData.password.newPassword` (string, required)
- `authData.password.oldPassword` (string, required)
- `reasons` (string[])

## Responses

- `200`: Whether the OTP verified, the transaction id, and the ABHA accounts the person may pick from.
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized, missing, invalid, or expired Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `422`: Unprocessable, the request parsed but failed validation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "<TXN_ID>",
  "authResult": "<AUTH_RESULT>",
  "message": "<MESSAGE>",
  "accounts": [
    "<ACCOUNTS>"
  ]
}
```
