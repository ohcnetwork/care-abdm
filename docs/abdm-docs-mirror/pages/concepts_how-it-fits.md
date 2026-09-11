# How the pieces fit

[ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) has three moving parts: registries that
issue identifiers, the [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) gateway that
routes requests and holds consent, and the two roles a record moves between.

## Identity comes first

Every call carries an identifier issued by a registry. Creating that entry comes first.

| Registry | Identifies | Identifier | Written by |
| --- | --- | --- | --- |
| [ABHA](/docs/hiecm/v3/registries/abha) | A patient | 14 digit ABHA number, plus an ABHA address | [M1](/docs/hiecm/v3/api/m1) |
| [HPR](/docs/hiecm/v3/registries/nhpr/hpr) | A doctor, nurse, pharmacist or facility manager | HPR ID | [M4](/docs/hiecm/v3/api/m4) |
| [HFR](/docs/hiecm/v3/registries/nhpr/hfr) | A hospital, clinic, lab or pharmacy | Facility ID | [M4](/docs/hiecm/v3/api/m4) |

[ABHA](/docs/hiecm/v3/getting-started/glossary#abha) is the patient side.
[HPR](/docs/hiecm/v3/getting-started/glossary#hpr) and
[HFR](/docs/hiecm/v3/getting-started/glossary#hfr) sit together under NHPR, the provider side.
[Registries](/docs/hiecm/v3/registries) has what each one holds.

## The gateway sits in the middle

Your system never calls another participant directly. You call the gateway, it forwards the
request, and the answer arrives at your callback URL as a separate inbound call. That is why
every flow here is drawn as a sequence.

HIE-CM is data blind. It holds identifiers, metadata about where records live, and consent
artefacts, never the record itself. It does not access or store health record content.

[The ABDM gateway](/docs/hiecm/v3/concepts/gateway) covers the gateway and the session token
every call carries.

## Your role decides what you build

Whoever holds a record and publishes it is the [HIP](/docs/hiecm/v3/getting-started/glossary#hip).
Whoever asks to read records they did not create is the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu).
A hospital that shares discharge summaries and pulls earlier prescriptions is the HIP for the
first and the HIU for the second. See [HIP and HIU](/docs/hiecm/v3/concepts/hip-hiu).

| Role | Who takes it | What it does | Milestone |
| --- | --- | --- | --- |
| HIP | A facility, through its [HMIS](/docs/hiecm/v3/getting-started/glossary#hmis). A citizen, through their PHR app | Links records to a patient, sends them under a valid consent | [M2](/docs/hiecm/v3/api/m2) |
| HIU | Another facility, a citizen's PHR app, an insurer, a referral service, an analytics service | Raises a consent request, then fetches records held elsewhere | [M3](/docs/hiecm/v3/api/m3) |

A citizen's [PHR](/docs/hiecm/v3/getting-started/glossary#phr) app takes both. The citizen is the
HIP when they push a record from it, and the HIU when they fetch one.

## Records stay where they were created

ABDM has no central store. A record stays in the system that created it. What moves is smaller:

- A **care context** is a pointer, not content: a reference number and a display name. Putting a
  diagnosis or a result in that name is not allowed. See
  [linking](/docs/hiecm/v3/concepts/linking).
- A **consent artefact** is the patient's permission, scoped by purpose, record type and date
  range. See [consent](/docs/hiecm/v3/concepts/consent).
- The **record** goes point to point, encrypted, from the HIP that holds it to the HIU that
  asked, once a consent artefact exists. It is packaged as a
  [FHIR](/docs/hiecm/v3/getting-started/glossary#fhir) R4 bundle. See
  [data flow](/docs/hiecm/v3/concepts/data-flow) and [FHIR](/docs/hiecm/v3/concepts/fhir).

## One path end to end

1. The patient has an ABHA identity.
2. The facility is listed in the HFR and gets a Facility ID.
3. The facility links its software as a bridge, which makes your system resolvable as that
   facility.
4. Records created there become care contexts, linked to the patient's ABHA address through
   HIE-CM, and the patient sees them in a PHR app.
5. Another system asks for those records, and the patient decides whether to allow it.

The doctor's HPR ID sits alongside. It identifies the professional inside a record and
authorises facility registration.

## Next

[Your integration path](/docs/hiecm/v3/milestones) for what each role has to
build.
