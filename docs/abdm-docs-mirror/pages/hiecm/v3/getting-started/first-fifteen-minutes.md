# Quickstart

You create a test [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) here, with your own sandbox credentials, in four calls that run live from this page: create a session, encrypt the Aadhaar number, request an OTP, create the account.

## Before you start

Have your `clientId` and `clientSecret` ([get them](/docs/hiecm/v3/getting-started/sandbox)) and a sandbox test identity: an Aadhaar number issued to you for sandbox use, with access to the mobile number registered against it, because that is where the OTP goes.

### Create a gateway session

Exchange your sandbox client id and secret for the access token every later call carries.

clientIdclientSecret sensitiveHeld in this page only while the tab is open. It is never written to storage and never put in a URL.

### Encrypt the Aadhaar number

Fetch NHA's public certificate, then encrypt the number here in your browser. NHA never accepts a raw Aadhaar number.

Create a session first. Fetching the certificate needs the access token.

### Request the OTP

NHA sends a one time password to the mobile number registered against that Aadhaar, and hands you a transaction id.

Encrypt the Aadhaar number first. This call takes the encrypted value, never the raw one.

### Create the ABHA

Send the OTP with the transaction id. This call creates a real account on the sandbox, so send it once.

Request an OTP first. This call needs the transaction id that came back with it.

## How this fits your product

The registration desk is where most of this lands. Your intake screen either finds the patient's existing ABHA or creates one on the spot, which is the flow you just ran. The token from step 1 is not specific to ABHA creation: it is the token every later ABDM call carries, so whatever your system does next starts by getting one. Once the patient has an ABHA, records attach to it, and that is a different module.

- **Session, step 1.** Every call in every module carries this token. Mint it once, watch `expiresIn`, refresh it before it lapses.
- **Identity, [M1](/docs/hiecm/v3/milestones/m1).** Creating and verifying an ABHA at intake, which is the runner above.
- **Linking, [M2](/docs/hiecm/v3/milestones/m2).** Telling ABDM that you hold records for that ABHA, and sending them when they are asked for.
- **Reading, [M3](/docs/hiecm/v3/milestones/m3).** Requesting consent and fetching records held by somebody else.

[Your integration path](/docs/hiecm/v3/milestones) sets out which of these you need and in what order.

## If a call fails

Under the four steps you get the request each call sent and the response it got back, including the error body. A 401 on the session call usually means the credentials or the `X-CM-ID` header, so see [Everything returns 401](/docs/hiecm/v3/troubleshooting/everything-returns-401).

A rejected `loginId` may be the encryption rather than the number. The runner uses RSA-OAEP, which is the only RSA encryption a browser offers, and leaves the digest as a control you can change. [Encryption](/docs/hiecm/v3/concepts/encryption) sets out what is confirmed and what is not.

## Next

[Your integration path](/docs/hiecm/v3/milestones).
