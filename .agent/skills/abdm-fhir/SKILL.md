---
name: abdm-fhir
description: Use when producing or checking FHIR for ABDM: building NRCES compliant document bundle generation into a codebase, or auditing the bundles an existing FHIR store already emits. Covers the resource profiles ABDM requires, the Composition rules, and the validator to check against.
---

# ABDM FHIR

Generated from the ABDM Developer Portal on 2026-09-07, catalogue version 2026.08.24.

This file is a snapshot. Re-download it from https://abdm-docs.dev.eka.care/skills/abdm-fhir/SKILL.md when it is older than the work you are doing.

## What this skill covers

- **Generate.** Build NRCES compliant bundle generation into a codebase. [references/generate.md](references/generate.md)
- **Audit.** Check an existing FHIR store's output against the same profiles. [references/audit.md](references/audit.md)

Open one when the work calls for it. This file is the map, not the material.

## Before anything else

- Nothing here has been run against the ABDM sandbox. Treat request and response shapes as unconfirmed, and check a response before you rely on its shape.
- A bundle that validates is not a bundle ABDM accepts. The NRCES profiles are the floor, and the milestone the bundle travels under adds its own rules.
