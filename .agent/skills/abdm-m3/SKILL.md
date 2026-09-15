---
name: abdm-m3
description: Use when building, debugging or testing ABDM Milestone 3: raising a consent request, tracking its status, reading consent artefacts, and fetching encrypted health records as an HIU. Carries the endpoints, the consent rules, every recorded error code and the M3 test matrix. Also carries the scaffolding loop that builds it flow by flow and the loop from a failed call to a named fix, in references/.
---

# ABDM M3, consent and fetching

Generated from the ABDM Developer Portal on 2026-09-14, catalogue version 2026.08.24. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-m3/SKILL.md when it is older than the work you are doing.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What this skill covers

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends on an observed result rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 25 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix, and 95 recorded error codes. [references/debug.md](references/debug.md)
- **Test.** 32 test cases, each with the call it makes and what to see when it passes. [references/test.md](references/test.md)

Open one when the work calls for it. This file is the map, not the material.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- You act as the HIU. The HIE-CM holds the consent and asks the patient on your behalf. No artefact, no records.
- The patient must be known to you by ABHA address before you can raise a request.
- One consent request can produce more than one artefact. Store the request id and every artefact id.
- Records arrive encrypted on your callback URL. Decrypt them, then acknowledge receipt to the gateway.
- NHA's schema declares `consentId` and `consentRequestId` as UUIDs while NHA's own examples give values that are not. Do not validate them as UUIDs. Recorded as correction C3 in catalogue/openapi/corrections.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/m3
- The flows as diagrams: /docs/hiecm/v3/milestones/m3
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Sandbox test data: /docs/hiecm/v3/reference/data-dictionary
- Terms: /docs/hiecm/v3/getting-started/glossary
