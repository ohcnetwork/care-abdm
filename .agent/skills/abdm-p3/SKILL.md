---
name: abdm-p3
description: Use when building, debugging or testing ABDM P3, the patient side of Milestone 3: subscriptions, auto approval policies, granting and revoking consent, and fetching the records a grant covers. Carries the endpoints, the notification rules, every recorded error code and the consent rules.
---

# ABDM P3, PHR consent and notifications

Generated from the ABDM Developer Portal on 2026-09-15, catalogue version 2026.08.24. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-p3/SKILL.md when it is older than the work you are doing.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What you can do with P3

- Manage consents from inside a PHR application, including auto approval policies.

What it cannot do yet matters as much. Read **Before anything else** below before assuming a capability is one endpoint away.

## What is in this folder

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends on an observed result rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 46 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix. No error code is recorded for this module yet. [references/debug.md](references/debug.md)
- **Test.** 0 test cases, each with the call it makes and what to see when it passes. [references/test.md](references/test.md)

This file is the map. Each line above is a file beside it, opened one at a time rather than read through.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- P3 is the other side of M3. M3 is a requester asking for records; P3 is the patient deciding, and being told each time.
- A PHR application implements the HIU role as well, because fetching a user's own records is an HIU flow.
- Build for revocation from the start. A consent that worked yesterday can be withdrawn today, and that is the system working correctly.
- A subscription is how the application hears about changes to a user's ABHA address. Set one up at address creation and at first login on a new install.
- An auto approval policy stops the user approving a request every time a hospital adds a record, and the user must be able to disable a policy at any time.

## Practices that hold across every call

- Read the body, not only the status. A refusal often names the field in its body while the status says nothing useful, and a bad clock can arrive as a 404.
- When ABDM publishes a value, read it rather than hard coding what it currently says. That covers a parameter, such as the encryption algorithm the certificate endpoints return beside the key, and it covers an enumeration: councils, courses, states, districts, purposes and HI types all have master data calls, and a table typed into your source is a table that goes stale silently. Refuse to act on a published value you do not recognise rather than falling back to a default.
- Read every field in a response, not the one you came for. The M1 certificate call returns the padding next to the key, and a catalogue that recorded only the key cost an integrator a day rediscovering it.
- Prove an assumption against a call that is able to disagree with you. An endpoint that refuses every input with one message cannot tell you which input was right, and testing against it turns a correct answer into a ruled out one.
- Suspect the transport before the data. When a call refuses a value you believe in, check the encryption, the headers and the clock before you doubt the number. Those failures are reported as if the value were wrong.
- Do not carry an encryption path from one module to another. The padding, the certificate and the key size belong to the registry you are calling, and a path that works in one module produces a value another cannot read.
- Never log a sensitive value before you encrypt it, and never send one to a remote service to be encrypted. Both move the leak rather than removing it.
- Generate a fresh REQUEST-ID for every call and log it before sending. Once a call has failed it is the only handle on it.
- Check the host on any sample before you copy it. Published samples mix production and sandbox hosts while describing sandbox behaviour, so a request copied whole can be correct in every respect except where it is pointed. This costs an afternoon because the failure looks like credentials.
- Do not validate an identifier more strictly than the platform does. A schema that types a field as a UUID is not a promise that the values are UUIDs, and ABDM ships examples that are not. Refusing a value ABDM would have accepted turns your own client into the thing that broke, and the rejection never reaches a log anyone is reading.
- Read a plural response as plural. A verification returns an accounts array, a consent request produces more than one artefact, and taking the first element is the bug that assigns a visit to the wrong record or drops half a fetch. Store the collection and decide from its length; length one is a case, not the normal case.
- A documented callback path is not a documented callback payload. Several ABDM callbacks name a route and record no body anywhere, so a handler written against an assumed shape fails on the first real delivery, asynchronously, where nobody is watching. Log the whole body on arrival before you parse it.
- Decode a token before you use it. A call that hands you a token has not necessarily handed you the token the next call wants: an M1 login returns one whose JWT payload reads `"typ": "Transfer"`, and every profile call refuses it while blaming its age. The claims are base64 and need no library, and reading them turns a confusing refusal into an obvious one.
- When a journey carries the same parameter through two calls, check whether it is the same value in both. An array like `scope` is a combination the operation validates as a whole, and the combination can legitimately change between opening a transaction and confirming it. Reusing the opening value is refused as though the parameter itself were wrong.
- Do not infer which path an identifier belongs to from where that identifier is most discussed. Aadhaar fills ABDM's enrolment documentation and is also a login identifier, so wiring it to enrolment quietly creates a second account for everyone who already holds one. Send every identifier to the lookup first and let the answer pick the path.
- Do not match an error code with string equality. ABDM returns codes carrying trailing punctuation and whitespace, observed as `"code": "ABDM-9999: "`. Trim and compare on the prefix, or the branch you wrote for that code never runs.
- A failure does not always carry a body. An HTTP 401 with zero bytes was observed on a PHR profile call with no user token. Handle the empty body before you parse, or your client throws on the simplest failure there is.
- On a `HIS-` response from the registries, read `details[0].code` before the top level `code`. The outer code and the HTTP status describe the wrong thing: a 422 saying the data was wrong carried `HIS-403`, not permitted, one level down. Acting on the outer code sends you hunting through a payload that is fine.
- Repeated bad credentials lock the client. Eight consecutive failed session calls locked a sandbox client for about eight minutes, and every attempt in that window returned `Invalid user credentials`, which reads as a wrong secret rather than a temporary lock. Back off on an auth failure rather than retrying, and never loop a credential check.
- Send TIMESTAMP in UTC with milliseconds and a trailing Z. Local time is refused, sometimes as a 404.
- Cache a public certificate with a validity window rather than forever. A rotation fails every encrypted call at once, and a cache with no expiry cannot recover on its own.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/p3
- The flows as diagrams: /docs/hiecm/v3/milestones/p3
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Sandbox test data: /docs/hiecm/v3/reference/data-dictionary
- Terms: /docs/hiecm/v3/getting-started/glossary
