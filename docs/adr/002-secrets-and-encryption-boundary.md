# ADR-002 — Secrets and encryption boundary

Status: Accepted
Date: 2026-09-10

## Context
The sandbox docs say the client secret is a credential.
They say to keep it server side, never in a browser build.
Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/api/gateway/endpoints/gateway-sessions-create/index.md.

The M1 docs say Aadhaar, mobile, OTP, and password values travel RSA encrypted.
Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m1/index.md.

The encryption docs say to encrypt inside our own system.
They say a remote helper is not a production path.
Source: https://abdm-docs.dev.eka.care/docs/hiecm/v3/concepts/encryption/index.md.

The rendered encryption page still does not name the padding.
Our sandbox note records OAEP with SHA-1 as the only observed valid padding.
Source: `docs/findings.md:37-42`.

## Decision
1. Keep `clientId` and `clientSecret` only in the backend settings boundary.
   Code: `backend/src/abdm/settings.py:22-32`.
2. Keep the gateway token in the backend cache.
   Return only a token prefix from the status endpoint.
   Code: `backend/src/abdm/gateway/session.py:82-93`, `backend/src/abdm/urls.py:16-22`.
3. Encrypt Aadhaar, mobile, and OTP values in the backend.
   Use RSA-OAEP with SHA-1 and the ABDM public key.
   Code: `backend/src/abdm/abha/crypto.py:31-58`.
4. Store X-token, T-token, and R-token state only in `AbhaTransaction`.
   Strip tokens before data reaches a view response.
   Code: `backend/src/abdm/models.py:35-39`, `backend/src/abdm/abha/service.py:18-20`, `backend/src/abdm/abha/service.py:38-63`.
5. Let the frontend send Aadhaar and OTP only to Care.
   The browser uses the Care API URL and `/api/abdm/...` routes.
   Production traffic must use HTTPS.
   Code: `frontend/src/lib/request.ts:99-129`, `frontend/src/lib/careApi.ts:179-227`.
6. Do not persist Aadhaar numbers or OTP values.
   Do not log request bodies that can contain them.
   Code: `backend/src/abdm/models.py:1-40`, `backend/src/abdm/abha/client.py:67-81`.

## Consequences
- The MFE never holds ABDM credentials or ABDM tokens.
- Browser logs can contain form values before submit.
  Operators must treat the browser as the Care trust boundary.
- Unit tests can inject an RSA public key into `crypto.encrypt`.
  Runtime callers use the fetched ABDM key.
