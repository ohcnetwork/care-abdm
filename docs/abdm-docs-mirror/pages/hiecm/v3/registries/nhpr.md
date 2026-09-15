# NHPR, the provider registries

NHPR is the provider half of [Registries](/docs/hiecm/v3/registries), and the name covers the pair underneath it: the [HPR](/docs/hiecm/v3/getting-started/glossary#hpr) for people and the [HFR](/docs/hiecm/v3/getting-started/glossary#hfr) for places. This page carries what they share and forks to each.

They are separate because a doctor holds one identity for a career across many facilities, while a facility sees many professionals pass through. Keeping them apart lets each change without rewriting the other, and lets [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) answer two questions: who wrote this, and where was it written.

## Which one you need, and when

| You need                                                           | When                                                                                                                                                                                                             |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| An [HPID](/docs/hiecm/v3/getting-started/glossary#hpid) on the HPR | Before anything else in NHPR. The HFR create call carries an HPR token in the header, generated from an HPR ID and password                                                                                      |
| A facility ID on the HFR                                           | Before the facility goes live as a [HIP](/docs/hiecm/v3/getting-started/glossary#hip) or an [HIU](/docs/hiecm/v3/getting-started/glossary#hiu). A valid facility ID is a prerequisite for sharing records at all |
| A bridge linked to the facility                                    | Last. It is what makes your software resolvable as that facility on the network                                                                                                                                  |

## Base URLs

Both registries share one set:

```text
Sandbox     https://apihspsbx.abdm.gov.in/v4/int/Production  https://apinhpr.abdm.gov.in/v4/int/
```

The session token that authorises them comes from the HIE-CM gateway, not from NHPR. [M4](/docs/hiecm/v3/api/m4) is the only milestone in [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) that writes to NHPR, and its endpoints, parameter tables and error codes are on [M4 operations and fields](/docs/hiecm/v3/api/m4/undocumented).

## Next

- [HPR](/docs/hiecm/v3/registries/nhpr/hpr): the HPID and the registration journey.
- [HFR](/docs/hiecm/v3/registries/nhpr/hfr): the facility record, the five call onboarding sequence, bridge linkage.
- [ABHA](/docs/hiecm/v3/registries/abha), the patient side.
- [M4 API reference](/reference/hiecm-m4).
