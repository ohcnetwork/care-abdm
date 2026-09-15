# 00 — Context

## What this is

An experiment, and a real deliverable. NHA (National Health Authority, India)
runs ABDM, the national health data network. A third-party team (eka.care,
which the user is part of) is writing an unofficial technical documentation
site and sandbox portal for ABDM: https://abdm-docs.dev.eka.care.

The question being tested: **can an AI agent, given only that documentation,
integrate ABDM into a real healthcare system?** The system is CARE
(ohcnetwork/care + ohcnetwork/care_fe). The output is a CARE plug — a backend
Django app and a frontend MFE remote — living in this repo.

Every gap we hit is a finding about the docs. Record gaps in
`docs/findings.md` (create on first finding) with the URL that should have
answered the question.

## Hard rules (from the user, non-negotiable)

1. **The only ABDM source is https://abdm-docs.dev.eka.care/docs/hiecm/v3**
   and the artefacts it publishes (its `llms.txt`, `.md` mirrors, skills at
   `/skills/`, MCP server at `https://abdm-docs-mcp.dev.eka.care/mcp`).
2. **Forbidden:** official NHA/ABDM documentation, sandbox.abdm.gov.in docs,
   any third-party ABDM writeup, and any existing ABDM code — specifically
   `~/ohc.network/care_abdm`, `~/ohc.network/care_abdm_fe`, `~/ohc.network/abdm-bruno`,
   `~/ohc.network/abdm_docs`, `~/ohc.network/abdm_stats`, `~/ohc.network/notify-when-abdm-is-up`.
   Do not open them. Do not grep them. Pre-existing knowledge of ABDM in the
   model is also out of bounds: if the docs don't say it, we don't know it.
3. **CARE host code is fair game and mandatory reading** — `~/ohc.network/care`,
   `~/ohc.network/care_fe`, and the reference plugs `care_token_display`,
   `care_token_display_fe`, `care_teleicu_devices`, `care_teleicu_devices_fe`.
4. Work happens in `~/ohc.network/care-abdm-sbx` only.

## Actors

- **Rithvik Nishad** — maintainer, OHC. Wants seam design discussed before
  implementation; wants real end-to-end verification against the sandbox, not
  mocks.
- **Kiran** — the agent (Hermes profile `kiran`), Care Plug Engineer.
- **ABDM sandbox** — the real thing our code will be tested against. Needs
  `clientId`/`clientSecret` and a publicly reachable callback URL
  (docs: `/getting-started/sandbox`). We do not have credentials yet.

## The shape of ABDM, as the docs describe it

Three gateways: HIE-CM (identity, care contexts, consent, records), UHI
(service discovery/booking), NHCX (insurance claims). Only HIE-CM is in scope.

HIE-CM work is four milestones spelling CARE
(`/docs/hiecm/v3/milestones`):

| | Name | What it gives a facility |
|---|---|---|
| M1 | Create | ABHA identity: create/verify a patient's ABHA, session token, profile, card |
| M2 | Attach | Link the facility's records (care contexts) to an ABHA address; answer discovery; push records on consented request |
| M3 | Retrieve | Act as HIU: request consent and fetch records held elsewhere |
| M4 | Enrol | Facility ID (HFR) and professional registration (HPR). Optional since 2026-09-15: a facility registered by hand on the NHPR portal needs no M4 build; M2 still needs the facility ID and a linked HIP bridge |

CARE is a multi-tenant HMIS: one instance holds many facilities, so every ABDM facility-scoped thing (HFR ID, HIP role, bridge) is per Care facility, and identity (ABHA) is per patient across the instance. The docs' facility row applies per tenant facility. The docs say M1 and M4 are required, M2 is
"the bulk of your build", M3 only if the facility also reads records it did
not create (`/docs/hiecm/v3/milestones`, table "Which milestones you need").

Key facts that shape the architecture (all from `/docs/hiecm/v3/milestones/m1`,
`/m2`, `/concepts/hip-hiu`, `/getting-started/sandbox`):

- Sandbox credentials are in `.env.local` (git-ignored; `.env.example` shows keys). Dev callback ingress = tunnel to local Care (ADR-005).
- Nothing runs until the gateway session call returns an access token.
- One bridge URL serves every facility of the integration; `X-HIP-ID` (= HFR facility ID) names the facility on each call and callback (docs update 2026-09-15).
- Two tokens: gateway token in `Authorization`, user (ABHA holder) token in
  `X-token`. Not interchangeable.
- Aadhaar numbers, mobile numbers, OTPs, passwords travel RSA-encrypted with
  NHA's public certificate — encrypted **inside our own system**, never via a
  remote helper.
- M1 answers are synchronous. M2/M3 answers are **asynchronous**: the call
  returns an ack, the answer arrives later as a POST to a callback URL we
  register, matched by `REQUEST-ID`. The callback URL must be publicly
  reachable and always listening.
- Per patient we store a **link token** (valid 6 months) at registration.
- Care context = one per OPD visit / one per IPD admission; HIE-CM holds only
  our reference ID and a non-clinical display name.
- Records go out as FHIR R4 bundles against NRCES profiles; eight record types,
  all mandatory for an HMIS.
- Data push has a 20-minute window; encryption is ECDH over Curve25519.
- The docs repeatedly warn: **nothing on the site has been run against the
  sandbox; response shapes are unconfirmed.** So we verify every shape against
  a real call before relying on it.
