# NHA

The National Health Authority runs [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm), operates its gateways, and publishes this portal.

## Who NHA is in ABDM

The National Health Authority is the government body that runs the network. It publishes the specifications, and it operates both the [sandbox](/docs/hiecm/v3/getting-started/glossary#sandbox) and the production gateways.

It is not an integrator. There is no NHA system you exchange records with, and no role you take opposite it. It issues the identifiers you carry, routes your calls, and holds the permission that lets a record move.

## What NHA does

| What it runs                                             | What it gives you                                                                                           |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [ABHA](/docs/hiecm/v3/registries/abha)                   | A patient's 14 digit ABHA number and their ABHA address                                                     |
| [HPR](/docs/hiecm/v3/registries/nhpr/hpr)                | An [HPID](/docs/hiecm/v3/getting-started/glossary#hpid) for a doctor, nurse, pharmacist or facility manager |
| [HFR](/docs/hiecm/v3/registries/nhpr/hfr)                | A facility ID for a hospital, clinic, laboratory, imaging centre or pharmacy                                |
| [The gateway](/docs/hiecm/v3/concepts/gateway)           | Your session token, header validation, and routing to every other participant                               |
| [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) | Care context links, consent requests and consent artefacts                                                  |
| The sandbox                                              | Client credentials, test identities, and the milestone certification you submit                             |

One limit is deliberate. The HIE-CM is data blind. It holds identifiers, metadata about where records live, and consent artefacts. It never holds the record. Once consent exists, the record goes straight from the system that holds it to the system that asked, encrypted.

The National Health Authority runs two further gateways alongside the HIE-CM, each with its own specification. [UHI](/docs/hiecm/v3/getting-started/glossary#uhi) carries services such as appointments, and [NHCX](/docs/nhcx/v1) carries insurance claims.

## Why it is worth it

Because one authority runs the middle, you do not have to negotiate with every other participant. One identity works at every facility in the country. One consent model governs every transfer, so you implement it once. One certification path covers going live.

And because the HIE-CM is data blind, joining the network does not mean handing your patients' records to NHA. They stay where they were created, in your system, and they move only to a system the patient has allowed.

## Next

[How the pieces fit](/docs/hiecm/v3/concepts/how-it-fits) puts the registries, the gateway and your role in one page.
