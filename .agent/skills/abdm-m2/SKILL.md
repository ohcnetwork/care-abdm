---
name: abdm-m2
description: Use when building, debugging or testing ABDM Milestone 2: care contexts, HIP initiated linking, discovery, and pushing encrypted health records to a requester. Carries the endpoints, the prerequisites, every recorded error code and the M2 test matrix. Also carries the scaffolding loop that builds it flow by flow and the loop from a failed call to a named fix, in references/.
---

# ABDM M2, linking and sharing

Generated from the ABDM Developer Portal on 2026-09-07, catalogue version 2026.08.24. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-m2/SKILL.md when it is older than the work you are doing.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What this skill covers

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends on an observed result rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 31 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix, and 120 recorded error codes. [references/debug.md](references/debug.md)
- **Test.** 46 test cases, each with the call it makes and what to see when it passes. [references/test.md](references/test.md)

Open one when the work calls for it. This file is the map, not the material.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- You act as the HIP. NHA requires a valid Facility ID and registration in the HIP role before you can create health records and share them.
- M2 is keyed to an ABHA address, so a working M1 integration comes first.
- Hold a link token per patient, stored at registration. NHA gives its validity as six months and says to validate it before use. If you hold no valid one, regenerate it using demographic authentication.
- Records go out as FHIR R4 conforming to the ABDM profiles at https://nrces.in/ndhm/fhir/r4/index.html.
- Four callbacks name a path and carry no payload in either of NHA sources: discovery, link init, link confirm and consent notify. Do not assume a body for those.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/m2
- The flows as diagrams: /docs/hiecm/v3/milestones/m2
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Sandbox test data: /docs/hiecm/v3/reference/data-dictionary
- Terms: /docs/hiecm/v3/getting-started/glossary
