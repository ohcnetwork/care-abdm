---
name: abdm-p1
description: Use when building, debugging or testing ABDM P1, the patient side of Milestone 1: registration in a PHR application, the four login routes, profile management, the ABHA card, and the family members a user manages. Carries the endpoints, the required headers, every recorded error code and the account rules.
---

# ABDM P1, PHR identity and profile

Generated from the ABDM Developer Portal on 2026-09-07, catalogue version 2026.08.24. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-p1/SKILL.md when it is older than the work you are doing.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What this skill covers

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends on an observed result rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 74 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix, and 422 recorded error codes. [references/debug.md](references/debug.md)
- **Test.** 0 test cases, each with the call it makes and what to see when it passes. [references/test.md](references/test.md)

Open one when the work calls for it. This file is the map, not the material.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- P1 is the patient side of M1. M1 is how a hospital system creates an ABHA; P1 is how the person's own application does it and maintains the account afterwards.
- Every user needs an ABHA address, `username@abdm`. Consent, notifications and record sharing all hang off it.
- Build both creation paths: by mobile number, and by an existing 14 digit ABHA number.
- All four login routes are mandatory.
- A user can hold several ABHA addresses but only one ABHA number.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/p1
- The flows as diagrams: /docs/hiecm/v3/milestones/p1
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Sandbox test data: /docs/hiecm/v3/reference/data-dictionary
- Terms: /docs/hiecm/v3/getting-started/glossary
