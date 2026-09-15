# Insurer

You sit on two gateways, and they share no API surface. Clinical records move on the [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm). Claims move on [NHCX](/docs/hiecm/v3/getting-started/glossary#nhcx).

## Who you are in ABDM

On the HIE-CM you take the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) role, health information user. That is a direction, not a category of company. Your organisation is the HIU whenever it asks to read records it did not create, and your software is how it asks.

On NHCX you are a payer, which covers an insurer or a third party administrator acting for one. You onboard as a participant, in sandbox first and then in production.

## Confirm at onboarding

- **Which registry entry your organisation holds on the HIE-CM.** The [HFR](/docs/hiecm/v3/getting-started/glossary#hfr) lists hospitals, clinics, laboratories, imaging centres, pharmacies and blood banks, and does not list insurers. Do not scope your build around a facility ID. [M4](/docs/hiecm/v3/api/m4) is required for an HIU, so ask which entry you register against before you plan that work. Build M1 and M3 meanwhile.

## What you can do

On the HIE-CM you build [M1](/docs/hiecm/v3/api/m1) for identity and [M3](/docs/hiecm/v3/api/m3) for consent and fetching.

- Raise a consent request naming the patient's [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) address, the purpose, the record types and the date range.
- Use the purpose code `HPAYMT`, Healthcare Payment, where payment is the reason you are asking. The patient reads that code.
- Wait. The patient decides, and may narrow the request before granting it, so read the artefact rather than assuming you got what you asked for.
- Fetch under the granted artefact and decrypt.
- Handle revocation. A consent that was live when you sent the request can be dead when the record holder validates it.

## Why it is worth it

You receive structured records from the system that created them, as [FHIR](/docs/hiecm/v3/getting-started/glossary#fhir) bundles, instead of scans collected from the member. The permission behind each one is explicit, scoped and time boxed, and both sides report the transfer.

What this does not give you is claim settlement. That is NHCX work, and a separate integration.

## Next

[Consent](/docs/hiecm/v3/concepts/consent) covers what you may ask for, and [NHCX](/docs/nhcx/v1) covers the claims gateway.
