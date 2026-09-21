# ADR-015 — M4 Enrol: the NHPR from CARE (HFR facility identity, HPR professional identity)

Status: Accepted (Rithvik, 2026-09-19: "Everything, A to D")
Date: 2026-09-19
Depends on: ADR-007 (facility setup page), ADR-011 (the gateway as the source of truth; 1 table per
ABDM object), ADR-012 (1 failure shape), ADR-014 (M3; the consent `requester`).
Amended by: ADR-016 (2026-09-19): `AbdmHfrOnboarding` is removed; the onboarding state and the registry
record live in `Facility.extensions["abdm"]`; `hfr-card.tsx` is replaced by `registry-card.tsx`; the
setup `PUT` takes `hip_name` and `counters` only.

## Context

The 2026-09-16 republication turned M4 from 2 published endpoints into 100 operations on 4 journeys
(`milestones/m4`): HPID creation through an Aadhaar page of the registry, professional registration,
facility onboarding to the HFR, and bridge linkage. The sanctioned route for a facility is still the
NHPR portal by hand; the API route is what an HMIS offers its own customers.

Facts that shape the design:

| Fact | Source |
|---|---|
| Every NHPR call takes the integration bearer token. The HFR create and submit calls also take a **person's** HPR token in `x-hprid-auth`; "both come from a person, not from your application". Role 2 or 3 (facility manager) is needed to register a facility. | `registries/nhpr/hfr` §The link to the HPR token; `registries/nhpr/hpr` §Who can enrol |
| Credential scope: client id, secret, bridge URL and the management-token username and password are "your integration, one"; the facility id and `hipName` are per facility; the HPR token is per person. | `concepts/how-it-fits` §one bridge, many facilities; `registries/nhpr/hpr` §What your system has to hold |
| Codes, not names: every coded field comes from a master call; the registry rejects display values. | `registries/nhpr/hfr` §Codes, not names |
| The HFR onboarding is 5 calls in a fixed order; a record not submitted stays a draft and "goes nowhere". The basic step returns the `trackingId` every later step carries. | `registries/nhpr/hfr` §The onboarding journey |
| Facility search by `facilityId` or by name and LGD state answers the registered name and status. | `m4-search/02` |
| HPID creation: the person completes Aadhaar on the URL the registry returns; the system never handles the Aadhaar number or OTP. Mobile match first; OTP only when it is false. The mobile number, the OTP and the password are RSA/ECB/PKCS1 encrypted with the NHPR certificate, a different cipher and certificate from M1. | `milestones/m4` journey 1; `registries/nhpr/hpr` |
| The linkage call takes 1 HRP entry per link type, `HIP` or `HIU`; `hipName` is 15 characters, no special characters, unique per bridge. | `m4-multiple-hrp-api/01`; `registries/nhpr/hfr` §Bridge linkage |

Rithvik holds a sandbox HPR ID with the facility-manager role and its password, and no management-token
credentials.

## Decisions (Rithvik, 2026-09-19)

1. **Scope: all 4 tiers.** A, facility lookup, search, link and linkage as HIP + HIU; B, an HPR ID on the
   Care user, used as the M3 `requester.identifier`; C, the HFR onboarding wizard; D, HPID creation and
   the **full** register-professional form.
2. **Bearer.** Every NHPR call carries the gateway session token, which the HRP linkage has used since
   2026-09-14. No management-token credential is configured; the plug reads what the sandbox answers
   (findings N1).
3. **Seams.** Facility side: the ABDM setup page gets an HFR card (lookup by ID, search by name and
   state, link, programme OTP) and a link to the wizard page `/facility/:facilityId/abdm/hfr/register`.
   Professional side: "My HPR ID" from the user menu (`userNavItems`), which the host routes to
   `/facility/:facilityId/users/:username/abdm-hpr`. Care facility creation stays in core.
4. **Who logs in.** The HPR token is a per-user secret held server-side (`AbdmHprProfile.token`),
   obtained by password or by Aadhaar OTP (`auth/init` → `confirmWithAadhaarOtp`). Mobile OTP is not
   offered: the registry publishes a send call and no verify call (N5). Search and linkage need no HPR
   token; HFR writes and the person's own profile calls do.
5. **One HPR ID per Care account.** A second identity is refused until the first is unlinked. An
   existing HPID found during creation (`checkHpIdAccountExist`) is linked, not duplicated.
6. **Retention.** The Aadhaar photo lives on the creation row only until the HPID exists; account
   information is stored without photos; certificate bytes are relayed and never stored; the plug
   keeps photo names of the HFR basic step, not the bytes.

## Design

**Backend `abdm/nhpr/`**: `rules.py` (pure: formats, every body, every parser, masters normaliser),
`crypto.py` (RSA/ECB/PKCS1 with the NHPR certificate; PEM, DER, X.509 and JSON-wrapped shapes),
`client.py` (1 wrapper per call on `ABDM_HSP_URL/v4/int`; `x-hprid-auth` and the HPR bearer where the
pages name them; the certificate cached 6 h; 27 master kinds cached 24 h), `facility.py` (lookup,
search, link, programme OTP, the 5-step onboarding with the `IN` id found by a name search after
submission), `professional.py` (login, profile, HPID creation, register, documents, info; the M3
requester identifier), `views.py`.

3 tables: `AbdmHprProfile` (user ↔ HPR ID, the token), `AbdmHprLogin` (an OTP login in progress),
`AbdmHpidTransaction` (the creation wizard). The per-facility wizard state was a 4th table,
`AbdmHfrOnboarding`, until ADR-016 moved it into `Facility.extensions["abdm"]["hfr_onboarding"]`. Migration
`0004`. `outbound.send(role="none")` sends no facility header to the NHPR. The linkage body names `HIP`
and `HIU`.

**Routes.** Facility: `GET .../abdm/hfr/lookup?facility_id=`, `GET .../hfr/search?name=&state=`,
`POST .../hfr/link`, `GET/POST .../hfr/onboarding` (`{step, payload}`), `POST .../hfr/otp`. User:
`GET users/me/abdm/hpr`, `GET .../verify-id`, `POST .../login`, `.../login/verify`,
`.../session/logout|unlink`, `.../create/<action>`, `.../register[/update]`, `GET/POST .../documents`,
`GET .../professional-info`. Masters: `GET nhpr/masters/<kind>`.

**Frontend.** `hfr-card.tsx` (replaced by `registry-card.tsx`, ADR-016), `hfr-onboarding-wizard.tsx` (route), `hpr-page.tsx` (route),
`hpr-login-dialog.tsx`, `hpid-create-wizard.tsx` (polls `isAuthenticated` every 5 s while the link is
live), `hpr-register-form.tsx` (the 5 blocks, dynamic registrations and qualifications, certificates as
base64), `master-select.tsx`. Fields the docs type as a code with no master call (salutation, category,
work status) are free text with the example value as the hint (N6).

## Consequences

- 3 tables (4 before ADR-016), 16 routes, 27 master kinds, no callback: every NHPR answer is synchronous.
- The Aadhaar photo and the person's HPR token are the 2 sensitive values the plug holds; both have a
  documented end (creation; logout or expiry).
- Nothing has met the sandbox. The first run must confirm the bearer for the HPID calls (N1), the
  `generateLink` URL field (N2), the `auth/cert` response shape (N4), the `IN` id after submission (N7)
  and the master type names (N8). `03-roadmap.md` Phase 5 lists the proofs.
