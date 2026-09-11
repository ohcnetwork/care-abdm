# Get your sandbox credentials

Every [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) call carries a token, and every token
starts with a client id and a client secret. Here is how you get them.

## Before you start

You need an organisation to register, and a URL we can post callbacks to. Step 3 says what that
URL has to do.

## 1. Register on the sandbox

Create an account on the sandbox application and register your organisation.

<SandboxAction action="register">Register on the sandbox</SandboxAction>

## 2. Get your client id and client secret

Sign in to the sandbox application. Your `clientId` and `clientSecret` are issued there.

Store the secret the way you store any other production credential. Never commit it, and never
send it to a browser.

<SandboxAction action="credentials">Open the sandbox</SandboxAction>

## 3. Register your callback URL

In [M1](/docs/hiecm/v3/api/m1) the answer comes back in the response to your call. In
[M2](/docs/hiecm/v3/api/m2) and [M3](/docs/hiecm/v3/api/m3) it does not. The response only
acknowledges your request, and the answer arrives afterwards as a POST to a URL you registered.

Register one base URL. We post to paths under it, and every callback carries the `REQUEST-ID`
you sent on the original call, so you can match the answer to the question. Each path is named on
the page of the call it belongs to, in the [API reference](/docs/hiecm/v3/api).

<SandboxAction action="callbackUrl">Open the sandbox</SandboxAction>

Two things about that URL decide whether your integration works:

- **It has to be reachable from the public internet.** If it is not, the flow appears to hang
  and nothing tells you why. From our side the call succeeded and the callback was sent.
- **It has to be listening whether or not you are ready.** We post when the answer is ready, not
  when you ask for it. In development that usually means a tunnel, and a tunnel gives you a new
  URL every restart. Register the new one each time.

## 4. Note the base URLs

| What you call | Sandbox |
| --- | --- |
| The gateway, including the session call | `https://dev.abdm.gov.in`, with the header `X-CM-ID: sbx` |
| The [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) service | `https://abhasbx.abdm.gov.in/abha/api/v3/` |

More than one sandbox host appears across our published documents.
[The ABDM gateway](/docs/hiecm/v3/concepts/gateway) lists every host and where each one is
written down.

## What you see when it works

You hold three things: a `clientId`, a `clientSecret`, and a callback URL registered against
them. Nothing has been called yet.

## Next

[Make your first call](/docs/hiecm/v3/getting-started/first-fifteen-minutes).
