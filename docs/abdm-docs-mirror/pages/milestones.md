# Milestones

Four milestones. You certify them one at a time, in order, and together they
spell CARE.

## In short

M4 certifies last but blocks M2. Sharing a record needs a valid facility ID and
registration in the HIP role, and that facility ID comes from M4. Plan the
registry work early.

## One patient, four milestones

Meera arrives at your clinic. Each card below is one thing your system has to
be able to do for her, and one milestone that gives you it.

## The same story from Meera's own app

If you are building the patient's app rather than the clinic's system, you are
building a [PHR](/docs/hiecm/v3/getting-started/glossary#phr) application. The
work splits into three, and each part mirrors a milestone on the provider side.

## Which milestones you need

Each row below is the entity you build for. HIP and HIU are roles that entity
takes, not kinds of software: whoever holds a record and publishes it is the
HIP, and whoever asks to read records they did not create is the HIU.

| Who you build for | M1 | M2 | M3 | M4 |
| --- | --- | --- | --- | --- |
| A facility | Required | The bulk of your build | Where it also reads records it did not create | Required |
| An insurer, a referral service or an analytics service | Required | Not needed | The bulk of your build | [Confirm at onboarding](/docs/hiecm/v3/concepts/participants/insurer#confirm-at-onboarding) |
| A citizen | [P1](/docs/hiecm/v3/milestones/p1), the patient side | [P2](/docs/hiecm/v3/milestones/p2), the patient side | [P3](/docs/hiecm/v3/milestones/p3), the patient side | Not needed |

## What each milestone gets you

| Milestone | What you get | Who needs it |
| --- | --- | --- |
| [M1 Create](/docs/hiecm/v3/milestones/m1) | Identity and the session token | Everyone |
| [M2 Attach](/docs/hiecm/v3/milestones/m2) | Linking and sharing records | A facility publishing records, and a citizen pushing their own |
| [M3 Retrieve](/docs/hiecm/v3/milestones/m3) | Consent and record fetching | Anyone reading records they did not create, and every PHR app |
| [M4 Enrol](/docs/hiecm/v3/milestones/m4) | A facility ID and professional registration | Anyone going live as a facility |

These pages give the steps, the order to build them in and the failure modes.
Every request URL, header and body sits on the [API
reference](/docs/hiecm/v3/api) pages, one page per call.

## Next

Start with [M1 Create](/docs/hiecm/v3/milestones/m1), or read [Go
live](/docs/hiecm/v3/getting-started/going-live) for what happens after the
fourth certificate.
