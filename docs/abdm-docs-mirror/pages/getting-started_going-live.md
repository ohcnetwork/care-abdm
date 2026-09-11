# Go live

Working in the sandbox is not the same as being live. One exit process sits between the
two, and you run it once, at the end.

## In short

- There is no per milestone submission. The exit process covers your whole integration, once.
- It has four steps, in a fixed order, and it opens with a demonstration.
- You demonstrate twice, to two different audiences.
- The [security audit](/docs/hiecm/v3/getting-started/security-audit) is separate from functional testing, and both feed the exit form.
- Production credentials are issued at the end. They are not your sandbox values.

## Prerequisites

Every milestone your integration needs works end to end.
[Your integration path](/docs/hiecm/v3/milestones) says which ones apply to a
citizen using a [PHR](/docs/hiecm/v3/getting-started/glossary#phr) application,
and which to a facility publishing as the
[HIP](/docs/hiecm/v3/getting-started/glossary#hip) or fetching as the
[HIU](/docs/hiecm/v3/getting-started/glossary#hiu).

Start the exit process once all of them are complete, not milestone by milestone.

## 1. Demonstrate what you built

You demonstrate the [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) functionality you
built to the integration team. This is the first of two demonstrations, and it opens the
process rather than closing it.

## 2. Complete functional testing and the security audit

Empanelled agencies run both, after the demonstration. They are separate exercises with
separate outputs: functional testing produces a report and a certificate, and the security
audit produces the
[Safe to Host certificate](/docs/hiecm/v3/getting-started/glossary#safe-to-host-certificate).
[Security audit](/docs/hiecm/v3/getting-started/security-audit) covers who may audit you,
which URL they audit, and how many audits your platforms need.

## 3. Submit the exit form

Upload the exit form on the sandbox with four things:

| What you upload | Comes from |
| --- | --- |
| The functional testing report and certificate | Your empanelled testing agency |
| The security audit report | Your CERT-In empanelled auditor |
| A signed undertaking | You |
| Any other supporting document requested | The integration team |

Confirm the format of the report and the undertaking with the integration team before you
assemble them.

## 4. Demonstrate to the Health Tech Committee

Once the earlier steps are complete, a demonstration is scheduled for the
[Health Tech Committee](/docs/hiecm/v3/getting-started/glossary#health-tech-committee).
Different audience, different demonstration. The committee records its decision in four
review stages, each carrying its own reviewer and date, so the outcome arrives as a
sequence rather than a single answer.

## 5. Switch to the production base URLs

Production credentials are issued once the exit process completes.

| What you call | Sandbox | Production |
| --- | --- | --- |
| The gateway | `https://dev.abdm.gov.in`, `X-CM-ID: sbx` | `https://apis.abdm.gov.in`, `X-CM-ID: abdm` |
| The [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) service | `https://abhasbx.abdm.gov.in/abha/api/v3/` | `https://abha.abdm.gov.in/api/abha/v3/` |

A production client id against a sandbox host, or the reverse, fails.

## What you see when it works

You hold a production client id and client secret, and a call that worked in the sandbox
returns the same result against the production host.

## When it goes wrong

If a call that worked in the sandbox fails in production, check the base URL and the
`X-CM-ID` header first. See
[Everything returns 401](/docs/hiecm/v3/troubleshooting/everything-returns-401).

Questions about the exit process itself, including where to submit the form or what counts
as a valid supporting document, go to [Support](/docs/support).

## Next steps

- Get the audit that feeds step 2: [Security audit](/docs/hiecm/v3/getting-started/security-audit).
- Hand your integration to an agent: [Build with AI](/docs/hiecm/v3/getting-started/build-with-ai).
