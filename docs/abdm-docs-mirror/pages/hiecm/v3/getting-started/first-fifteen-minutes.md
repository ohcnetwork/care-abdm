# Quickstart

You create a test [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) here, with your own sandbox credentials, in four calls that run live from this page: create a session, encrypt the Aadhaar number, request an OTP, create the account.

## Before you start

Have your `clientId` and `clientSecret` ([get them](/docs/hiecm/v3/getting-started/sandbox)) and a sandbox test identity: an Aadhaar number issued to you for sandbox use, with access to the mobile number registered against it, because that is where the OTP goes.

1.
2.
3.
4.

### Create a gateway session

Exchange your sandbox client id and secret for the access token every later call carries.

Client IDClient secret sensitiveHeld in this page only while the tab is open. It is never written to storage and never put in a URL.

### Encrypt the Aadhaar number

Fetch NHA's public certificate, then encrypt the number here in your browser. NHA never accepts a raw Aadhaar number.

What you type is encrypted in this browser with NHA's public key and posted only to NHA's sandbox host. This site has no server of its own and stores nothing you type. Use a sandbox test identity, not a real person's Aadhaar number. NHA does not publish a test Aadhaar number, so bring one issued to you for sandbox use.

Aadhaar number sensitiveMasked as you type, kept in this page's memory only, cleared when you close the tab.

### Request the OTP

NHA sends a one time password to the mobile number registered against that Aadhaar, and hands you a transaction id.

### Create the ABHA

Send the OTP with the transaction id. This call creates a real account on the sandbox, so send it once.

OTP sensitiveEncrypted with the same certificate before it is sent.Mobile numberThe number to attach to the new account. The specification requires it on this call and its example shows it unencrypted.

## How this fits your product

The registration desk is where most of this lands. Your intake screen either finds the patient's existing ABHA or creates one on the spot, which is the flow you just ran. The token from step 1 is not specific to ABHA creation: it is the token every later ABDM call carries, so whatever your system does next starts by getting one. Once the patient has an ABHA, records attach to it, and that is a different module.

- **Session, step 1.** Every call in every module carries this token. Mint it once, watch `expiresIn`, refresh it before it lapses.
- **Identity, [M1](/docs/hiecm/v3/milestones/m1).** Creating and verifying an ABHA at intake, which is the runner above.
- **Linking, [M2](/docs/hiecm/v3/milestones/m2).** Telling ABDM that you hold records for that ABHA, and sending them when they are asked for.
- **Reading, [M3](/docs/hiecm/v3/milestones/m3).** Requesting consent and fetching records held by somebody else.

[Your integration path](/docs/hiecm/v3/milestones) sets out which of these you need and in what order.

## If a call fails

Under the four steps you get the request each call sent and the response it got back, including the error body. A 401 on the session call means the request was not authorised, so see [Everything returns 401](/docs/hiecm/v3/troubleshooting/everything-returns-401).

A rejected `loginId` may be the encryption rather than the number. The runner encrypts with the padding the certificate declares rather than one you pick, and the certificate's own response is in the log below, so you can read which one it asked for. [Encryption](/docs/hiecm/v3/concepts/encryption) sets out what is confirmed and what is not.

## Next

[Your integration path](/docs/hiecm/v3/milestones).
