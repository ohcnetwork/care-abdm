---
name: abdm-p2
description: Use when building, debugging or testing ABDM P2, the patient side of Milestone 2: discovering records held elsewhere, linking care contexts to an ABHA address, and pulling those records into a PHR application. Carries the endpoints, the timing rules the network enforces, every recorded error code and the discovery rules.
---

# ABDM P2, PHR linking and records

Generated from the ABDM Developer Portal on 2026-09-14, catalogue version 2026.08.24. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-p2/SKILL.md when it is older than the work you are doing.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What this skill covers

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends on an observed result rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 60 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix. No error code is recorded for this module yet. [references/debug.md](references/debug.md)
- **Test.** 0 test cases, each with the call it makes and what to see when it passes. [references/test.md](references/test.md)

Open one when the work calls for it. This file is the map, not the material.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- P2 is the mirror of M2. M2 is a provider publishing a record; P2 is the patient discovering it and linking it to their own ABHA address.
- Discovery is for facilities the user visited without giving an ABHA address, and for older records.
- A HIP is expected to answer a discovery request within 10 seconds.
- Never show a care context that is already linked.
- Send the data transfer request within 5 minutes of the user asking for their records.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/p2
- The flows as diagrams: /docs/hiecm/v3/milestones/p2
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Sandbox test data: /docs/hiecm/v3/reference/data-dictionary
- Terms: /docs/hiecm/v3/getting-started/glossary
