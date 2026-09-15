# How the pieces fit

[ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) has three moving parts: registries that issue identifiers, the [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) gateway that routes requests and holds consent, and the two roles a record moves between.

## In short

- Two identities come first: the care seeker's ABHA, and the care provider's HPR and HFR.
- There are two integrator roles, IMS or PHR. HIP and HIU are not roles, they are the two ends of one record moving.
- Two configuration levels: your integration is one bridge, and every facility it serves links to that bridge. Neither is set inside the other.
- Records never move to a centre. A pointer and a consent move, then the record goes point to point.

## Two identities come first

Every call carries an identifier issued by a registry, and there are two kinds of entity to identify: the care seeker, and the care provider giving them care. Creating those entries comes before anything else.

| Identity      | Registry                                  | Who it identifies                               | Identifier                                 | Written by                  |
| ------------- | ----------------------------------------- | ----------------------------------------------- | ------------------------------------------ | --------------------------- |
| Care seeker   | [ABHA](/docs/hiecm/v3/registries/abha)    | A patient                                       | 14 digit ABHA number, plus an ABHA address | [M1](/docs/hiecm/v3/api/m1) |
| Care provider | [HPR](/docs/hiecm/v3/registries/nhpr/hpr) | A doctor, nurse, pharmacist or facility manager | HPR ID                                     | [M4](/docs/hiecm/v3/api/m4) |
| Care provider | [HFR](/docs/hiecm/v3/registries/nhpr/hfr) | A hospital, clinic, lab or pharmacy             | Facility ID                                | [M4](/docs/hiecm/v3/api/m4) |

[ABHA](/docs/hiecm/v3/getting-started/glossary#abha) is the care seeker's. [HPR](/docs/hiecm/v3/getting-started/glossary#hpr) and [HFR](/docs/hiecm/v3/getting-started/glossary#hfr) sit together under NHPR and are the care provider's: one for the professional, one for the place. [Registries](/docs/hiecm/v3/registries) has what each one holds.

## The gateway sits in the middle

Your system never calls another participant directly. You call the gateway, it forwards the request, and the answer arrives at your callback URL as a separate inbound call. That is why every flow here is drawn as a sequence.

HIE-CM is data blind. It holds identifiers, metadata about where records live, and consent artefacts, never the record itself. It does not access or store health record content.

[The ABDM gateway](/docs/hiecm/v3/concepts/gateway) covers the gateway and the session token every call carries.

## Your role is IMS or PHR

There are two integrator roles on HIE-CM, and your product is one of them for its whole life. What decides it is which entity your software acts for.

| Role                                               | It acts for                                                                                             | What you build                                                           |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| [IMS](/docs/hiecm/v3/getting-started/glossary#ims) | A care provider. An HMIS in a hospital, an EMR in a clinic, a LIMS in a laboratory, a PMS in a pharmacy | [M1](/docs/hiecm/v3/milestones/m1) to [M4](/docs/hiecm/v3/milestones/m4) |
| [PHR](/docs/hiecm/v3/getting-started/glossary#phr) | A care seeker, who holds their own records and gives consent                                            | [P1](/docs/hiecm/v3/milestones/p1) to [P3](/docs/hiecm/v3/milestones/p3) |

[HIP](/docs/hiecm/v3/getting-started/glossary#hip) and [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) are not a third and a fourth role, and they are not something you register as. They are the two ends of one record moving: whoever publishes it is the HIP for that exchange, and whoever asks to read one they did not create is the HIU.

Both roles are both, and it changes call by call:

- A hospital is the HIP when it shares a discharge summary, and the HIU when it pulls an earlier prescription, through the same IMS.
- A citizen is the HIP when they push a record from their PHR application, and the HIU when they fetch one.

Neither is a thing you can build once and be. See [HIP and HIU](/docs/hiecm/v3/concepts/hip-hiu).

## One bridge, many facilities

Two levels of configuration exist and they are easy to confuse. Your integration registers once, as a bridge. The facilities it serves register separately and are linked to that bridge. One bridge serves every facility linked to it, whether that is one facility or a hundred.

Decide which level a setting belongs to before you build a settings screen for it. Nothing about your integration is configured per facility, and nothing about a facility is configured in your integration's own credentials.

| Setting                       | Level                                      | Where it is set                                                                                 |
| ----------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| Client id and client secret   | Your integration, one of each              | [Sandbox registration](/docs/hiecm/v3/getting-started/sandbox)                                  |
| Bridge callback URL           | Your integration, one                      | [Sandbox registration](/docs/hiecm/v3/getting-started/sandbox#3-register-your-callback-url)     |
| Facility ID                   | Each facility                              | [HFR onboarding](/docs/hiecm/v3/milestones/m4#journey-3-a-facility-onboards-to-the-hfr)         |
| `hipId`, `hipName`, `hipType` | Each facility, once per bridge it links to | [The bridge linkage call](/docs/hiecm/v3/milestones/m4#journey-4-linking-bridges-to-a-facility) |

Every callback for every facility arrives at the one bridge URL. The header says which facility it belongs to: `X-HIP-ID` in [M2](/docs/hiecm/v3/api/m2), and `X-HIU-ID` in M2 and [M3](/docs/hiecm/v3/api/m3). That header is what your handler routes a callback on, and the facility ID is what your records key to.

A callback URL kept in a facility's settings is a design error, and so is a client secret. Either survives the first facility and fails on the next. See [the headers](/docs/hiecm/v3/reference/authentication) for what travels on each call.

## Records stay where they were created

ABDM has no central store. A record stays in the system that created it. What moves is smaller:

- A **care context** is a pointer, not content: a reference number and a display name. Putting a diagnosis or a result in that name is not allowed. See [linking](/docs/hiecm/v3/concepts/linking).
- A **consent artefact** is the patient's permission, scoped by purpose, record type and date range. See [consent](/docs/hiecm/v3/concepts/consent).
- The **record** goes point to point, encrypted, from the HIP that holds it to the HIU that asked, once a consent artefact exists. It is packaged as a [FHIR](/docs/hiecm/v3/getting-started/glossary#fhir) R4 bundle. See [data flow](/docs/hiecm/v3/concepts/data-flow) and [FHIR](/docs/hiecm/v3/concepts/fhir).

## One path end to end

1. The patient has an ABHA identity.
2. The facility is listed in the HFR and gets a Facility ID.
3. The facility links its software as a bridge, which makes your system resolvable as that facility.
4. Records created there become care contexts, linked to the patient's ABHA address through HIE-CM, and the patient sees them in a PHR app.
5. Another system asks for those records, and the patient decides whether to allow it.

The doctor's HPR ID sits alongside. It identifies the professional inside a record and authorises facility registration.

## Next

[Your integration path](/docs/hiecm/v3/milestones) for what each role has to build.
