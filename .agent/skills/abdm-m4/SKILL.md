---
name: abdm-m4
description: Use when building, debugging or testing ABDM Milestone 4, the NHPR: creating an HPID, registering a healthcare professional on the HPR, onboarding a facility to the HFR, and linking that facility to its HIP or HIU bridges. Carries the operations NHA has published, the registration order, every recorded error code and the identifier formats.
---

# ABDM M4, facility and professional registries

Generated from the ABDM Developer Portal on 2026-09-07, catalogue version 2026.08.24. Every fact below comes from a page in that portal, which is the place to look when this file does not carry enough.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-m4/SKILL.md when it is older than the work you are doing.
If the abdm-docs MCP server is connected, trust its answers over this file: it serves the current catalogue and stamps every response with its catalogue_version, which you can compare against the version above.

## What this skill covers

- **Scaffold.** Build it flow by flow against the sandbox, as a loop that ends on an observed result rather than on a call returning 200. [references/scaffold.md](references/scaffold.md)
- **Integrate.** 13 operations, with their hosts and headers. [references/integrate.md](references/integrate.md)
- **Debug.** The loop from a failed call to a named fix, and 150 recorded error codes. [references/debug.md](references/debug.md)
- **Test.** 184 test cases, each with the call it makes and what to see when it passes. [references/test.md](references/test.md)

Open one when the work calls for it. This file is the map, not the material.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- Neither registry moves a health record. M4 establishes who the professional is and what the facility is, so every record flow has a verified provider behind it.
- M4 blocks M2 and M3 in production. Without a facility in the HFR and a bridge linked to it, you cannot share as a HIP or fetch as an HIU.
- The HPR comes first. Onboarding a facility needs an HPR token, which needs a person who already holds an HPID.
- Creating an HPID returns an `hprToken`. Keep it: the register professional call carries it in its payload.
- A facility ID is `IN` followed by 10 characters. An HPID is 14 digits.
- Facility onboarding is one search, three writes and a submit, all keyed to the `trackingId` the first write returns. Stop before submit and the facility stays in draft, invisible to ABDM.
- Register professional takes codes, not names. Fetch council, course, college, university, state, district and language from the master data APIs first.
- A facility ID alone does not make records flow. Link the facility to a bridge and mark each link HIP or HIU. The HIP name is what a patient sees in their PHR app: 15 characters or fewer, no special characters, and unique for every bridge on that facility.
- Send the mobile number encrypted. Fetch the public certificate from `/v4/int/api/v1/auth/cert` and encrypt with `RSA/ECB/PKCS1Padding`.
- Several published M4 samples show the production host while describing sandbox behaviour. Check the host before you copy a sample.

## Where the detail is

- Every endpoint, with its body fields and responses: /docs/hiecm/v3/api/m4
- The flows as diagrams: /docs/hiecm/v3/milestones/m4
- Every error code across modules: /docs/hiecm/v3/reference/error-codes
- Sandbox test data: /docs/hiecm/v3/reference/data-dictionary
- Terms: /docs/hiecm/v3/getting-started/glossary
