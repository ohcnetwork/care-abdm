# Create an ABHA from a verified Aadhaar OTP

`POST /v3/enrollment/enrol/byAadhaar`

Exchanges the OTP you just received for a real ABHA number. Send the
`txnId` from the OTP request, the encrypted OTP value, and the consent
block recording that the person agreed.

This is the call that creates the account, so treat a success as a
permanent side effect. If you retry it blindly after a timeout you may be
enrolling somebody twice.

`BENEFIT_NAME` is sent on this call when the enrolment belongs to a
benefit scheme.

The demographic authentication variant reads the user token from a
different place: `token` at the top level, while the OTP, face and
fingerprint variants take `tokens.token`. Check which one you get
before parsing.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'BENEFIT_NAME: healthid api' \
  --header 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  --header 'Content-Type: application/json' \
  --data '{
  "authData": {
    "authMethods": [
      "otp"
    ],
    "otp": {
      "txnId": "<TXN_ID>",
      "otpValue": "<OTPVALUE>",
      "mobile": "<MOBILE>"
    }
  },
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `BENEFIT_NAME` (string): The benefit scheme an enrolment belongs to. Send `healthid api` on the enrol and search calls, and `healthid` on the login OTP and verify calls under Find ABHA. On the enrolment OTP request the header is present but explicitly disabled, so it is not sent there. A login OTP request sent with `healthid api` rather than `healthid` was accepted on the sandbox on 2026-09-11, so the login calls may take either. NHA's files spell this header four different ways and use scheme values beyond healthid. Which spelling each endpoint accepts is not confirmed against the sandbox. The Conventions page for this module lists all four.
- `X-token` (string): The user scoped token returned when a person logs in or verifies an OTP. Profile calls act on one account, so they need this in addition to the gateway token. Required on the calls that read or change a specific person's account. Send the bare token. Unlike the Authorization header this one carries no `Bearer ` prefix, and adding one is refused as `ABDM-1094` with the message `X-token expired`. That message names the wrong thing: a token rejected one second after it was issued has not expired, it was malformed. Check the prefix before the lifetime.

## Body

- `authData` (object, required)
- `authData.authMethods` (string[], required)
- `authData.otp` (object)
- `authData.otp.txnId` (string, required)
- `authData.otp.otpValue` (string)
- `authData.otp.mobile` (string, required)
- `authData.otp.fingerPrintAuthPid` (string)
- `authData.otp.timeStamp` (string)
- `authData.face` (object)
- `authData.face.txnId` (string, required)
- `authData.face.aadhaar` (string, required)
- `authData.iris` (object)
- `authData.iris.aadhaar` (string, required)
- `authData.iris.Pid` (string, required)
- `authData.iris.mobile` (string, required)
- `authData.bio` (object)
- `authData.bio.aadhaar` (string, required)
- `authData.bio.fingerPrintAuthPid` (string, required)
- `authData.bio.mobile` (string, required)
- `consent` (object, required)
- `consent.code` (string, required)
- `consent.version` (string, required)

## Responses

- `200`: The specification does not describe this body. Send the call with Try it to see what comes back.
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
