---
name: abdm-m2
description: Use when building, debugging or testing ABDM Milestone 2: care contexts, HIP initiated linking, discovery, and pushing encrypted health records to a requester. Carries the endpoints and the encryption parameters. Also carries the scaffolding loop that builds it flow by flow and the loop from a failed call to a named fix, in references/.
---

# ABDM M2, linking and sharing

Generated from the ABDM Developer Portal on 2026-09-16, catalogue version 2026.09.16. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download the whole folder from https://abdm-docs.dev.eka.care/skills/abdm-m2/ when it is older than the work you are doing: this router and every file under references/ that it links to. Fetching this file alone leaves those links pointing at files you do not have.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What you can do with M2

- Tell ABDM a patient had a visit with you, so their records can be found later.
- Answer a discovery request when somebody looks for that patient.
- Send records out encrypted when a consent says you must.
- Get the link token the linking calls need.

What it cannot do yet matters as much. Read **Before anything else** below before assuming a capability is one endpoint away.

## What is in this folder

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends when the step's exit condition holds rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 32 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The specification's examples return no error code for this module. [references/debug.md](references/debug.md)

This file is the map. Each line above is a file beside it, opened one at a time rather than read through.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- You act as the HIP.
- M2 is keyed to an ABHA address, so a working M1 integration comes first.
- You are the side that encrypts, and the parameters arrive from the requester rather than from you. The health information request carries `keyMaterial` with `cryptoAlg`, `curve: Curve25519`, the requester's `dhPublicKey` and a `nonce`. Generate your own Curve25519 pair and your own nonce, and send your public key and nonce back with the data so the requester can derive the same secret.
- The key derivation and the symmetric cipher applied over that shared secret are not yet published. Confirm both at onboarding before you ship, rather than inferring them from a sample.

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

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/m2
- The flows as diagrams: /docs/hiecm/v3/milestones/m2
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary
