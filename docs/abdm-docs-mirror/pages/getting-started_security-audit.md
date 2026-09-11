# Security audit

Every application passes a security audit before it reaches production. The audit is
called a [WASA](/docs/hiecm/v3/getting-started/glossary#wasa), and it produces the
[Safe to Host certificate](/docs/hiecm/v3/getting-started/glossary#safe-to-host-certificate)
you upload with your exit form.

## In short

- The audit is separate from anything functional. Passing every milestone still leaves this to do.
- Your auditor comes from the CERT-In empanelled list. An audit by anyone else does not count.
- The audit runs on your staging URL, and the certificate then licenses the same application in production.
- Each platform you ship is audited on its own. A website, an Android app and an iOS app need three.
- A certificate that is in date covers a new module without re-auditing what it already covers.

## Prerequisites

Build the modules you intend to certify before you apply. An audit covering several
modules can only cover modules that exist.

## 1. Appoint an auditor

Choose an auditor from the
[CERT-In empanelled list](https://www.cert-in.org.in/PDF/Empanel_org_2021.pdf).

## 2. Point the auditor at staging

The audit is conducted on your staging URL. The certificate it produces then licenses
the same application in production. An auditor pointed at a live production URL is
working the wrong way round.

## 3. Cover every platform you ship

One audit covers one platform. An audit of a shared
[ABHA](/docs/hiecm/v3/getting-started/glossary#abha) base URL does not cover the mobile
applications that call it.

## What gets audited

Scope depends on what you have certified before.

| Your situation | What the auditor covers |
| --- | --- |
| Nothing audited before | The whole application |
| Adding a module to an application already certified | The new module alone, subtracting the part already certified |
| Website, Android application, iOS application | Three separate audits, one for each |
| A valid Safe to Host certificate already in hand | Nothing, until that certificate expires |

## When you audit again

A new audit is required when a change is major, and when a change touches your backend.
Minor changes do not trigger one. Your certificate also carries an expiry date, and an
expired certificate needs a fresh audit whatever has changed since.

## How you know it worked

You hold a Safe to Host certificate that is in date, names the application you are about
to run in production, and covers every platform you ship.

## When it goes wrong

The three that cost integrators the most time, in order:

- **One audit, several platforms.** Three platforms need three certificates. A single certificate naming one of them stops the exit form.
- **Auditing production instead of staging.** The audit belongs on staging, and the certificate carries into production from there.
- **Treating a backend change as minor.** Anything touching your backend needs a new audit, and the exit gate is an expensive place to discover that.

## Next steps

- Run the exit process this certificate feeds into: [Go live](/docs/hiecm/v3/getting-started/going-live).
- Ask about a certificate or an auditor: [Support](/docs/support).
