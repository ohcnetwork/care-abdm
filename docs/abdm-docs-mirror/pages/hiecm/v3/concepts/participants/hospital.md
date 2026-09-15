# Hospital

You create health records and you want records created elsewhere. That puts you on both sides of every exchange in [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm).

## Who you are in ABDM

You enrol on the [HFR](/docs/hiecm/v3/getting-started/glossary#hfr), the Health Facility Registry, and a verified facility is issued a facility ID. Two formats are documented for it: `IN` followed by 10 characters on bridge linkage and search, and a 6 digit value on deduplicate search.

Registering the facility gives it an identity. Linking a [bridge](/docs/hiecm/v3/getting-started/glossary#bridge) makes your software resolvable as that facility, in the [HIP](/docs/hiecm/v3/getting-started/glossary#hip) or [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) direction.

| Role | When you are it                     | Milestone                   |
| ---- | ----------------------------------- | --------------------------- |
| HIP  | You hold the record and send it     | [M2](/docs/hiecm/v3/api/m2) |
| HIU  | You ask for a record held elsewhere | [M3](/docs/hiecm/v3/api/m3) |

Your clinicians hold their own [HPR](/docs/hiecm/v3/getting-started/glossary#hpr) IDs, and one of them needs facility manager rights before you can register at all.

## What you can do

- Identify the patient at registration by [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) address, or create an ABHA for someone who has none.
- Group each visit into a [care context](/docs/hiecm/v3/getting-started/glossary#care-context) and link it, so the patient can find it.
- Answer [discovery](/docs/hiecm/v3/getting-started/glossary#discovery) when a patient comes looking from their app. This is mandatory for every HIP.
- Validate the consent, then encrypt, sign and push the records inside the 20 minute window.
- Ask for a patient's history from another facility, under a consent they grant.

## Why it is worth it

Enrolling on the HFR gets your facility a trusted identity, a listing in national search results, less paperwork on licence renewals and insurance empanelment, and access to ABDM's digital services.

On the exchange itself, a record you link appears in the patient's own app without you posting anything. Earlier records from other facilities reach your clinicians with the patient's consent instead of arriving as a paper folder. Your records stay in your system throughout. There is no central store to hand them to.

## Next

[Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu) is the build guide for this role.
