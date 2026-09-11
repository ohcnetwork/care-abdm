---
name: abdm-phr-services
description: Use when building services a PHR application offers on top of ABDM: teleconsultation, nearby facility search, ambulance booking, blood bank search, scan and pay, PMJAY facility discovery and NHCX coverage lookups. None of it is required to certify as a PHR application.
---

# ABDM PHR application services

Generated from the ABDM Developer Portal on 2026-09-07, catalogue version 2026.08.24. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-phr-services/SKILL.md when it is older than the work you are doing.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What this skill covers

- **Integrate.** 72 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix. No error code is recorded for this module yet. [references/debug.md](references/debug.md)
- **Test.** 0 test cases, each with the call it makes and what to see when it passes. [references/test.md](references/test.md)

Open one when the work calls for it. This file is the map, not the material.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- None of this is a certification milestone. Nothing here is required to certify as a PHR application, and building none of it is a valid choice.
- These operations sit apart from P1 to P3 so that nothing here implies a PHR application must build them.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/phr-services
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Sandbox test data: /docs/hiecm/v3/reference/data-dictionary
- Terms: /docs/hiecm/v3/getting-started/glossary
