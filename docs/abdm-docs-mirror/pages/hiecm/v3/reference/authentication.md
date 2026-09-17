# Authentication

Generated from the specifications. Every scheme and header below is declared in one of them.

## Gateway session

**gatewaySession**, `http` `bearer`. The `accessToken` returned by `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

**bearerAuth**, `http` `bearer`. JWT Bearer token from `POST /api/hiecm/gateway/v3/sessions`. Header: `Authorization: Bearer {accessToken}`

| Header       | Required | What it is                                                                                                                                                                                                                         |
| ------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `REQUEST-ID` | yes      | A fresh UUID that you generate for this request. It is how you and the gateway correlate a call with its callback and with a support ticket, so log it. Reusing one across requests makes both impossible.                         |
| `TIMESTAMP`  | yes      | The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one. |
| `X-CM-ID`    | yes      | Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. Sending the wrong one against the right host is a common first-day failure and reads as an authorisation error.                           |

## M1 ABHA identity

**gatewaySession**, `http` `bearer`. The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

**bearerAuth**, `http` `bearer`. JWT Bearer token from `POST /api/hiecm/gateway/v3/sessions`. Header: `Authorization: Bearer {accessToken}`

**xToken**, `apiKey`. Short-lived session token returned in login/verify responses. Required for all `/profile/account/*` operations. Header: `X-Token: {token}`

| Header           | Required | What it is                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `REQUEST-ID`     | yes      | Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `TIMESTAMP`      | yes      | ISO 8601 UTC timestamp of the request.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `X-token`        | no       | The user scoped token returned when a person logs in or verifies an OTP. Profile calls act on one account, so they need this in addition to the gateway token. Required on the calls that read or change a specific person's account. Send the bare token. Unlike the Authorization header this one carries no `Bearer `prefix, and adding one is refused as `ABDM-1094` with the message `X-token expired`. That message names the wrong thing: a token rejected one second after it was issued has not expired, it was malformed. Check the prefix before the lifetime.                                                                         |
| `BENEFIT_NAME`   | no       | The benefit scheme an enrolment belongs to. Send `healthid api` on the enrol and search calls, and `healthid` on the login OTP and verify calls under Find ABHA. On the enrolment OTP request the header is present but explicitly disabled, so it is not sent there. A login OTP request sent with `healthid api` rather than `healthid` was accepted on the sandbox on 2026-09-11, so the login calls may take either. NHA's files spell this header four different ways and use scheme values beyond healthid. Which spelling each endpoint accepts is not confirmed against the sandbox. The Conventions page for this module lists all four. |
| `T-token`        | no       | The transaction token that carries state between the two halves of a login. Returned by the verify call and sent back on the account selection call. Like X-token, the value carries a `Bearer `prefix in every one of the recorded requests.                                                                                                                                                                                                                                                                                                                                                                                                     |
| `R-token`        | no       | The refresh token, sent when asking for a new user token without making the person log in again. Like X-token, the value carries a `Bearer `prefix.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `aadhaarNumber`  | yes      | The person's Aadhaar number, RSA encrypted against the ABDM public key and sent as a header rather than in a body. The recorded value is an encrypted blob, never the raw number: encrypt it the same way as an enrolment `loginId`. See the input encryption concept atom for the padding rules.                                                                                                                                                                                                                                                                                                                                                 |
| `healthIdNumber` | yes      | The 14 digit ABHA number, sent plain in the recorded request, in the dashed `91-XXXX-XXXX-XXXX` form.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `KEY_TYPE`       | no       | Which ABDM public key the encryption helper should use.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `TRANSACTION_ID` | no       | The enrolment transaction this call belongs to, when the transaction is not carried in the body.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

## M2 Linking and sharing

**gatewaySession**, `http` `bearer`. The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`. M2 also uses per flow tokens, a link token for linking and an authorisation token for patient scoped calls. Their header names are not yet published.

**bearerAuth**, `http` `bearer`. Bearer token obtained from POST /hiecm/gateway/v3/sessions

| Header         | Required | What it is                                                                                                                                                                                                                                                          |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `REQUEST-ID`   | yes      | A fresh UUID that you generate for this request. The callback that answers it carries the same value, so this is how you match an asynchronous reply to the call that caused it. Store it before you send the request, not after.                                   |
| `TIMESTAMP`    | yes      | The current time in ISO 8601, UTC, with milliseconds and a `Z` suffix, from a synchronised clock. The sandbox rejects IST and accepts UTC.                                                                                                                          |
| `X-CM-ID`      | yes      | Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. A dedicated error code exists for an invalid value here, which tells you how often it is wrong.                                                                            |
| `X-Link-Token` | yes      | Short-lived link token generated via POST /hiecm/v3/token/generate-token                                                                                                                                                                                            |
| `X-HIP-ID`     | yes      | Identifier of the Health Information Provider the request or callback belongs to. This is per facility, and it is what a callback arriving at your one bridge URL is routed on. The bridge URL and your credentials belong to the integration, not to the facility. |
| `X-HIU-ID`     | yes      | Identifier of the Health Information User the request or callback belongs to. This is per facility, and it is what a callback arriving at your one bridge URL is routed on.                                                                                         |

## M3 Consent and fetching

**gatewaySession**, `http` `bearer`. The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

**bearerAuth**, `http` `bearer`. Bearer token obtained from POST /hiecm/gateway/v3/sessions

| Header       | Required | What it is                                                                                                                                                                                                                                                           |
| ------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `REQUEST-ID` | yes      | A fresh UUID that you generate for this request. The callback that answers it carries the same value. In M3 a single consent can produce several callbacks, so keep the mapping from request id to consent request id rather than relying on ordering.               |
| `TIMESTAMP`  | yes      | The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.                                   |
| `X-CM-ID`    | yes      | Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production.                                                                                                                                                                             |
| `X-HIU-ID`   | yes      | Identifier of the health information user the request or callback is intended for. This is per facility, and it is what a callback arriving at your one bridge URL is routed on. The bridge URL and your credentials belong to the integration, not to the facility. |

## M4 HPR and HFR

**gatewaySession**, `http` `bearer`. The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## P1 PHR identity and profile

**gatewaySession**, `http` `bearer`. The access token from `POST /api/hiecm/gateway/v3/sessions`.

## P2 PHR linking and records

**gatewaySession**, `http` `bearer`. The access token from `POST /api/hiecm/gateway/v3/sessions`.

## P3 PHR consent and notifications

**gatewaySession**, `http` `bearer`. The access token from `POST /api/hiecm/gateway/v3/sessions`.

## PHR application services

**gatewaySession**, `http` `bearer`. The access token from `POST /api/hiecm/gateway/v3/sessions`.
