# ADR-001 — Scope: build CARE as an HIP first (M1 → M4 → M2); defer M3

Status: Proposed (awaiting Rithvik)
Date: 2026-09-09

## Context
The docs classify integrators by the entity they build for
(`/docs/hiecm/v3/milestones`, "Which milestones you need"). CARE is facility
software (HMIS). For a facility the docs say: M1 required, M2 "the bulk of
your build", M3 only "where it also reads records it did not create", M4
required and it *blocks* M2 because linking needs a facility ID in the HIP role.

The docs also say M1–M4 have one combined exit process, not per-milestone
certification (`/milestones/m1` §Certification).

## Decision
Build order: Phase 1 gateway session → Phase 2 M1 → Phase 3 M4 (facility ID +
bridge URL) → Phase 4 M2. M3 (HIU) is a separate later phase, only if wanted.

Within M1, implement only what the docs mark Mandatory for private
integrators (`/concepts/hip-hiu` capability table): Aadhaar-OTP creation,
four login routes, profile/card, session/refresh. Face/biometric/demographic
auth, benefits, re-KYC are out.

## Consequences
- The plug is useful after Phase 2 alone (ABHA capture at registration).
- M2 cannot be verified end-to-end until a sandbox facility ID exists (M4).
- P1–P3 (PHR app side) and UHI/NHCX are out of scope entirely.
