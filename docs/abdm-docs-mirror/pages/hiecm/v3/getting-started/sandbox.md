# Get your sandbox credentials

Every [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) call carries a token, and every token starts with a client id and a client secret. Here is how you get them.

## How sandbox integration works

Complete the integration process in 6 stages. Use a single workspace to manage the integration from account creation to production review. The integrating entity and the National Health Authority review team can access the relevant submissions, supporting evidence, queries and decisions.

| Stage                                                | What happens                                                                                                                         | Where                                                    |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| 01. Send Request                                     | Submit a request to access the ABDM Sandbox APIs.                                                                                    | [Step 1](#1-send-a-request-for-sandbox-access)           |
| 02. Get Access                                       | Receive Sandbox access after approval by the [Health Tech Committee](/docs/hiecm/v3/getting-started/glossary#health-tech-committee). | [Step 2](#2-get-access-your-client-id-and-client-secret) |
| 03. Integrate APIs                                   | Integrate the applicable ABDM APIs with your software solution.                                                                      | [Milestones](/docs/hiecm/v3/milestones)                  |
| 04. Complete Functional Testing and Security Audit   | Test the integrated solution and complete the required security audit.                                                               | [Go live](/docs/hiecm/v3/getting-started/going-live)     |
| 05. Complete the Health Tech Committee Demonstration | Present the integrated solution to the Health Tech Committee and obtain approval for production access.                              | [Go live](/docs/hiecm/v3/getting-started/going-live)     |
| 06. Go Live                                          | Move the approved integration to the production environment and begin using ABDM services.                                           | [Go live](/docs/hiecm/v3/getting-started/going-live)     |

## Before you start

You need an organisation to register, and a URL we can post callbacks to. Step 3 says what that URL has to do.

## 1. Send a request for sandbox access

Submit a request to access the ABDM Sandbox APIs. Eligible entities may apply for access to the ABDM Sandbox to integrate and test their software with ABDM APIs. Provide the required organisation, product and contact details and select the applicable integration category while submitting the request.

[Apply for Sandbox Integration](https://sandbox.abdm.gov.in/sandbox/v3/sandbox-registration)

## 2. Get access: your client id and client secret

Sandbox access is granted after approval by the [Health Tech Committee](/docs/hiecm/v3/getting-started/glossary#health-tech-committee). Once approved, sign in to the sandbox application. Your `clientId` and `clientSecret` are issued there.

Store the secret the way you store any other production credential. Never commit it, and never send it to a browser.

[Open the sandbox](https://sandbox.abdm.gov.in/)

## 3. Register your callback URL

In [M1](/docs/hiecm/v3/api/m1) the answer comes back in the response to your call. In [M2](/docs/hiecm/v3/api/m2) and [M3](/docs/hiecm/v3/api/m3) it does not. The response only acknowledges your request, and the answer arrives afterwards as a POST to a URL you registered.

Register one base URL. We post to paths under it, and each callback that answers a call carries the `REQUEST-ID` you sent on it in `response.requestId`, so you can match the answer to the question. Each path is named on the page of the call it belongs to, in the [API reference](/docs/hiecm/v3/api).

One URL covers your whole integration, however many facilities it serves. It belongs to your bridge, never to a facility, and the callback names the facility it is for in its own header. See [one bridge, many facilities](/docs/hiecm/v3/concepts/how-it-fits#one-bridge-many-facilities).

[Open the sandbox](https://sandbox.abdm.gov.in/)

Two things about that URL decide whether your integration works:

- **It has to be reachable from the public internet.** If it is not, the flow appears to hang and nothing tells you why. From our side the call succeeded and the callback was sent.
- **It has to be listening whether or not you are ready.** We post when the answer is ready, not when you ask for it. In development that usually means a tunnel, and a tunnel gives you a new URL every restart. Register the new one each time.

## 4. Note the base URLs

| What you call                                                    | Sandbox                                                   |
| ---------------------------------------------------------------- | --------------------------------------------------------- |
| The gateway, including the session call                          | `https://dev.abdm.gov.in`, with the header `X-CM-ID: sbx` |
| The [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) service | `https://abhasbx.abdm.gov.in/abha/api/v3/`                |

More than one sandbox host appears across our published documents. [The ABDM gateway](/docs/hiecm/v3/concepts/gateway) lists every host and where each one is written down.

## What you see when it works

You hold three things: a `clientId`, a `clientSecret`, and a callback URL registered against them. Nothing has been called yet.

## Next

[Make your first call](/docs/hiecm/v3/getting-started/first-fifteen-minutes).
