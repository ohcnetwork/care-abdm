---
name: abdm-m1
description: Use when building, debugging or testing ABDM Milestone 1: creating an ABHA number or address, ABHA login, profile management, or the gateway session token. Carries the endpoints, the required headers, the two token rule, the encryption rule and the error codes its specification's examples return. Also carries the scaffolding loop that builds it flow by flow and the loop from a failed call to a named fix, in references/.
---

# ABDM M1, ABHA identity

Generated from the ABDM Developer Portal on 2026-09-16, catalogue version 2026.09.16. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download the whole folder from https://abdm-docs.dev.eka.care/skills/abdm-m1/ when it is older than the work you are doing: this router and every file under references/ that it links to. Fetching this file alone leaves those links pointing at files you do not have.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What you can do with M1

- Create an ABHA for somebody who has none: by Aadhaar, by mobile, by an identity document, by face or fingerprint, or under a parent for a child.
- Log in somebody who already has one, by Aadhaar, mobile, ABHA number or ABHA address.
- Read their profile, which carries the whole registration form: names, date of birth, gender, mobile, address with its codes, and a photograph.
- Find an ABHA somebody has forgotten, and pick the right account when one mobile holds several.
- Show the ABHA card and QR code, and take a profile a patient shares by QR at your counter.
- Update a profile, change a mobile, and upgrade a mobile made address to KYC verified.

What it cannot do yet matters as much. Read **Before anything else** below before assuming a capability is one endpoint away.

## What is in this folder

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends when the step's exit condition holds rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 41 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix, and 14 error codes from the specification's examples. [references/debug.md](references/debug.md)

This file is the map. Each line above is a file beside it, opened one at a time rather than read through.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- Get an access token first, from the gateway session endpoint. Every other call needs it in `Authorization: Bearer <token>`.
- Two tokens exist and they are not interchangeable. The gateway access token goes in `Authorization`. The user token from an enrolment or a login goes in `X-token`. Profile endpoints need both.
- Sensitive fields travel encrypted. Aadhaar numbers, mobile numbers, email addresses, OTP values and passwords are encrypted before they go in the body, then base64 encoded.
- The certificate response tells you the padding. `GET /v3/profile/public/certificate` returns `{"publicKey", "encryptionAlgorithm"}`. Read that field and translate it for your language. Do not hard code a padding: a constant is right until it is not, and the failure then looks like a bad value rather than a stale constant.
- One path serves several jobs. The `scope` array in the body picks which one, so read it before assuming an endpoint does one thing.
- Holds regardless of the design: the reason a front desk adopts ABHA is that the receptionist stops typing. `GET /v3/profile/account` returns the whole registration form: names, day, month and year of birth, gender, mobile, email, the full address with LGD codes and a photograph. So the ABHA step comes BEFORE the registration form and fills it. A journey that registers the patient first and offers ABHA afterwards has already spent the keystrokes it existed to save.
- Two ways the profile reaches the desk. The patient scans a QR carrying your facility id and a counter id, consents in their own app, and ABDM posts the profile to your callback, so nobody at the desk types or asks anything. Or the desk runs the identifier journey, which ends in a token that reads the profile. Build whichever the deployment can reach, but the form is the destination either way.
- Present the filled form for confirmation rather than saving it unseen. The profile is what ABDM holds, not what the clinician sees: names may be transliterated, addresses age, and a shared mobile may belong to a relative.
- ABDM publishes operations, not a user experience. The journey is the integrator's to design, and a product that knows its own counter will often beat any default. Offer the suggested shape below, say it is a suggestion, and build what the user asks for instead when they have a view.
- Suggested shape: one entry rather than a menu. Take one identifier, send one OTP, and branch on what comes back, because asking a person at a desk whether they want to log in or register puts a question to them they often cannot answer. A chooser is better where the desk genuinely knows, such as a counter that only registers new patients.
- Holds regardless of the design: send every identifier to the login path first, Aadhaar included. Wiring Aadhaar to enrolment because that is where Aadhaar is most discussed sends everyone who already holds an ABHA to create a second.
- The accounts array on a login verification already carries ABHANumber, preferredAbhaAddress, name, gender, dob, profilePhoto and kycVerified, so a registration form can fill the moment the OTP verifies and before any profile call.
- Holds regardless of the design: read the accounts on the verification response before creating. Creating when an account already exists leaves the patient holding two ABHA numbers and no M1 operation merges them. This is the one failure worth designing around first.
- Holds regardless of the design: decide deliberately whether a journey can complete without an ABHA. A patient record keyed by the hospital's own number does not need one, and a journey that cannot complete without one blocks care for anyone who has none.
- An identifier and an auth method are two different questions, and listing them together is what makes M1 look like five choices. ABDM accepts four identifiers: Aadhaar, mobile, ABHA number, ABHA address.
- How the person proves the identifier is theirs is `authMethods`, whose values include otp, bio, face, iris, child and demo_auth. Offer auth methods underneath the identifier, and only where there is more than one.
- The surface is more than a registration form. Finding a forgotten ABHA, upgrading a mobile-made address to KYC, showing the card and QR, sharing a profile by QR at a counter, and updating a mobile number are each placements the operations support. List them for the integrator so their own design can account for them rather than meeting them later.

## Practices that hold across every call

- Read the body, not only the status. A refusal often names the field in its body while the status says nothing useful.
- When ABDM publishes a value, read it rather than hard coding what it currently says. That covers a parameter, such as the encryption algorithm the certificate endpoints return beside the key, and it covers an enumeration: councils, courses, states, districts, purposes and HI types all have master data calls, and a table typed into your source goes stale silently. Refuse to act on a published value you do not recognise rather than falling back to a default.
- Read every field in a response, not the one you came for. The M1 certificate call returns the encryption algorithm next to the key.
- Prove an assumption against a call that is able to disagree with you. A call that refuses every input with one message cannot tell you which input was right.
- Suspect the transport before the data. When a call refuses a value you believe in, check the encryption, the headers and the clock before you doubt the value.
- Do not carry an encryption path from one module to another. Read the certificate and the algorithm from the registry you are calling.
- Never log a sensitive value before you encrypt it, and never send one to a remote service to be encrypted. Both move the leak rather than removing it.
- Generate a fresh REQUEST-ID for every call and log it before sending. Once a call has failed it is the only handle on it.
- Check the host on any sample before you copy it. A request copied whole can be correct in every respect except where it is pointed, and that failure looks like credentials.
- Do not validate an identifier more strictly than the platform does. A schema that types a field as a UUID is not a promise that every value is one. Refusing a value ABDM would have accepted turns your own client into the thing that broke.
- Read a plural response as plural. A verification returns an accounts array and a consent request can produce more than one artefact. Store the collection and decide from its length.
- A documented callback path is not a documented callback payload. Log the whole body on arrival before you parse it, so a handler written against an assumed shape fails where you can see it.
- Decode a token before you use it. A call that hands you a token has not necessarily handed you the token the next call wants, and the claims are base64 that need no library to read.
- When a journey carries the same parameter through two calls, check what each call's specification asks for rather than carrying the first value forward.
- Do not infer which path an identifier belongs to from where that identifier is most discussed. Send every identifier to the lookup first and let the answer pick the path, so nobody who already holds an account is sent to create a second.
- Do not match an error code with string equality. A code may come back bare, as `ABDM-1001`, or with a trailing `: ` separator, as `ABDM-1001: `. Match on the code itself and tolerate the separator.
- Handle a failure that carries no body. Check for an empty body before you parse, or your client throws on the simplest failure there is.
- Back off on an authentication failure rather than retrying, and never loop a credential check.
- Send TIMESTAMP in UTC, ISO-8601 with milliseconds and a trailing Z, as in `2022-10-06T15:10:00.587Z`.
- Cache a public certificate with a validity window rather than forever. A rotation fails every encrypted call at once, and a cache with no expiry cannot recover on its own.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/m1
- The flows as diagrams: /docs/hiecm/v3/milestones/m1
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary
