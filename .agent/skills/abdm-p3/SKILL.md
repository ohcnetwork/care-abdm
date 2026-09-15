---
name: abdm-p3
description: Use when building, debugging or testing ABDM P3, the patient side of Milestone 3: subscriptions, auto approval policies, granting and revoking consent, and fetching the records a grant covers. Carries the endpoints, the notification rules, every recorded error code and the consent rules.
---

# ABDM P3, PHR consent and notifications

Generated from the ABDM Developer Portal on 2026-09-14, catalogue version 2026.08.24. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-p3/SKILL.md when it is older than the work you are doing.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What this skill covers

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends on an observed result rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 46 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix. No error code is recorded for this module yet. [references/debug.md](references/debug.md)
- **Test.** 0 test cases, each with the call it makes and what to see when it passes. [references/test.md](references/test.md)

Open one when the work calls for it. This file is the map, not the material.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- P3 is the other side of M3. M3 is a requester asking for records; P3 is the patient deciding, and being told each time.
- A PHR application implements the HIU role as well, because fetching a user's own records is an HIU flow.
- Build for revocation from the start. A consent that worked yesterday can be withdrawn today, and that is the system working correctly.
- A subscription is how the application hears about changes to a user's ABHA address. Set one up at address creation and at first login on a new install.
- An auto approval policy stops the user approving a request every time a hospital adds a record, and the user must be able to disable a policy at any time.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/p3
- The flows as diagrams: /docs/hiecm/v3/milestones/p3
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Sandbox test data: /docs/hiecm/v3/reference/data-dictionary
- Terms: /docs/hiecm/v3/getting-started/glossary
