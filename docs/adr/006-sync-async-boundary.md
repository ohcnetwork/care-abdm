# ADR-006 — Sync/async boundary and where ABDM traffic terminates

Status: Proposed
Date: 2026-09-09

## Context
- M1 answers arrive in the HTTP response; M2/M3 answers arrive later as POST
  callbacks to a registered public URL, correlated by `REQUEST-ID`
  (`/getting-started/sandbox` §3).
- Secrets (`clientSecret`) must never reach a browser (`/getting-started/sandbox` §2).
- Aadhaar/mobile/OTP must be RSA-encrypted *inside our own system*
  (`/milestones/m1` Journey 6 note, `/concepts/encryption`).
- Care exposes `/api/<plug>/` for each plug (`care/config/urls.py:111-112`)
  and has Celery in-process.

## Decision
1. The browser (MFE) talks **only to Care** (`/api/abdm/...`) via the host's
   authenticated request helper. It never calls ABDM hosts directly.
2. Care backend is the sole holder of `clientId/secret`, the gateway token
   cache, the RSA certificate, and per-transaction `X-token`s.
3. M1 flows are synchronous DRF endpoints that proxy one ABHA-service call
   each and return a Care-shaped response (raw ABDM response also stored for
   shape verification while the docs say shapes are unconfirmed).
4. M2/M3 outbound calls run in Celery tasks; every inbound callback is written
   to an `AbdmCallback` table (request-id, path, raw body, signature status,
   received_at) *before* any handler runs, then dispatched. Frontend reads
   state from Care and polls/uses query invalidation; nothing waits on ABDM in
   a request thread.
5. Callback signature verification per `/concepts/callback-authenticity`
   using gateway JWKS (`gateway-get-gateway-certs`), configurable to
   warn-only in sandbox until the docs' shape is confirmed by observation.

## Consequences
- Dev needs a public tunnel to Care's API for M2 (ADR-005).
- A callback log table makes docs gaps observable (we can diff documented vs
  actual payloads) — this is also the primary finding-generator for the
  documentation team.
