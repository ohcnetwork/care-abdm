# M1 APIs

Every Milestone 1 ([M1](/docs/hiecm/v3/api/m1)) endpoint of [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) has its own page, carrying its method, path, headers, body fields, responses and a curl sample. This page carries what those pages cannot: the rules that hold across all of them. The detail comes from [NHA](/docs/hiecm/v3/getting-started/glossary#nha)'s M1 [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) Postman collection, the only M1 source with real request text.

## Base URLs

The session call lives on the gateway host. Every other M1 call lives on the ABHA service. A few login routes sit on v3.1 instead of v3, at `https://abhasbx.abdm.gov.in/abha/api/v3.1/`, and their own pages say so.

## The scope array picks the job

About twenty paths cover the whole M1 surface. Most are reused for several jobs, and the `scope` array picks which. The same `POST enrollment/request/otp` sends the Aadhaar [OTP](/docs/hiecm/v3/getting-started/glossary#otp), the mobile OTP and the email OTP. `POST profile/account/request/otp` covers mobile update, email update, password change, re-[KYC](/docs/hiecm/v3/getting-started/glossary#kyc), delete and deactivate. Read the `scope` values on an endpoint page before you assume the path does one thing.

## Sensitive fields travel encrypted

Aadhaar numbers, mobile numbers, email addresses, OTP values and passwords are RSA encrypted with the ABDM public certificate before they go in the body. Placeholders are named for it, for example `<RSA_ENCRYPTED_AADHAAR_NUMBER>`.

Encrypt locally. The [encrypt endpoint](/docs/hiecm/v3/api/m1/endpoints/m1-encrypt-value) does it for you. That helps when you are trying a flow by hand, and it is wrong in production, because it sends the raw value to a remote host.

M1 names a `public/certificate` API for fetching the public key. Its URL, headers and response body are not yet published.

## Two tokens, not interchangeable

The gateway access token from the [session call](/docs/hiecm/v3/api/gateway/endpoints/gateway-sessions-create) goes in `Authorization`. It says your system may call. The user token from an enrolment or a login goes in `X-token`. It says whose account to act on.

Profile endpoints need both. That is every path under `profile/account`, including the card, the quick response (QR) code and logout. The refresh token is a third value with its own header: it goes in `R-token` on the token refresh call only, never in `X-token` and never in the body.

## The benefit endpoints are government only

The benefit programme APIs under `profile/benefit/` are government integrator only. A private integrator calling them receives `ABDM-1094`. See [errors](/docs/hiecm/v3/api/m1/errors). Child ABHA creation is restricted further, to specific government integrators on leadership approval.

## The BENEFIT_NAME header is spelled four ways

NHA's own files write this header four different ways across requests:
`BENEFIT_NAME` on most, `Benefit-Name` on demographic authentication and the
child ABHA calls, `BENEFIT-NAME` on child update and state district search, and
`Benefit_Name` once. An underscore and a hyphen are different header names on
the wire, so these are not the same header, and which spelling each endpoint
actually accepts has not been confirmed against the sandbox.

Send the spelling the endpoint's own page shows, and if a call is rejected for
a reason you cannot place, try the other spellings before looking elsewhere.

The value is usually `healthid api` or `healthid`, but benefit programme calls
use others: `COVIN` on an IRIS enrolment and a profile photo update, and a
`PAN` value that is present but disabled.

## Every endpoint has its own page

Each M1 endpoint is listed in the sidebar under its group, with its request fields, its recorded responses, and a request you can send from the page. Start at [the endpoint index](/docs/hiecm/v3/api), or read [the call order](/reference/hiecm-m1) first if you have not built the flow yet.
