# Milestones

Four milestones. You certify them one at a time, in order, and together they spell CARE.

## In short

[M1Create and verify the patient's ABHA, the identity every record hangs on.](/docs/hiecm/v3/milestones/m1)[M2Attach the records you hold to that identity: care contexts, linking, and sharing as a HIP.](/docs/hiecm/v3/milestones/m2)[M3Retrieve records held elsewhere, with the patient's consent, as an HIU.](/docs/hiecm/v3/milestones/m3)[M4Enrol your facility and your professionals in the registries, so you can go live.](/docs/hiecm/v3/milestones/m4)

M2 needs a facility ID and registration in the HIP role before it can share a record. That ID does not have to come from M4. A facility can be registered by hand on the NHPR portal, and many products do exactly that and never build M4. Build M4 when you want to register facilities or professionals from your own software instead. Either way, get the facility ID early, because M2 cannot be tested end to end without one.

## One patient, four milestones

Meera arrives at your clinic. Each card below is one thing your system has to be able to do for her, and one milestone that gives you it.

1. Milestone 1 · CreateRegister Meera's ABHA

   Meera walks in without a health ID. Create her ABHA so every record from today onwards links to one identity.

   [Build M1 Create](/docs/hiecm/v3/milestones/m1)

2. Milestone 2 · AttachAttach today's visit to her ABHA

   Her consultation note and her blood test are yours to hold. Group them into care contexts, link them to her ABHA address, and answer when her app comes looking.

   [Build M2 Attach](/docs/hiecm/v3/milestones/m2)

3. Milestone 3 · RetrieveRetrieve the scan from another hospital

   Meera mentions a scan done last year, somewhere else. Ask her for consent, wait for her answer, then fetch and decrypt what she granted.

   [Build M3 Retrieve](/docs/hiecm/v3/milestones/m3)

4. Milestone 4 · EnrolEnrol the clinic and its doctors

   None of the above leaves sandbox until the clinic is a registered facility and its doctors hold professional IDs. Enrol both, then link your software to the facility.

   [Build M4 Enrol](/docs/hiecm/v3/milestones/m4)

## The same story from Meera's own app

If you are building the patient's app rather than the clinic's system, you are building a [PHR](/docs/hiecm/v3/getting-started/glossary#phr) application. The work splits into three, and each part mirrors a milestone on the provider side.

1. PHR 1 · Identity and profileMeera signs up and holds her own profile

   She registers with a mobile number or an existing ABHA number, logs in four different ways, and manages her card, her QR code and her family members.

   [Build P1](/docs/hiecm/v3/milestones/p1)

2. PHR 2 · Linking and recordsShe finds records she never linked

   She searches for the hospital she visited last year, sees what it holds, verifies by one time password, and pulls those care contexts onto her ABHA address.

   [Build P2](/docs/hiecm/v3/milestones/p2)

3. PHR 3 · Consent and notificationsShe decides who sees what

   A clinic asks for her records. She reads the request, narrows it, grants or denies it, and revokes it later. Your app tells her each time.

   [Build P3](/docs/hiecm/v3/milestones/p3)

## Which milestones you need

Each row below is the entity you build for. HIP and HIU are roles that entity takes, not kinds of software: whoever holds a record and publishes it is the HIP, and whoever asks to read records they did not create is the HIU.

| Who you build for                                      | M1                                                   | M2                                                   | M3                                                   | M4                                                                                          |
| ------------------------------------------------------ | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| A facility                                             | Required                                             | The bulk of your build                               | Where it also reads records it did not create        | Required                                                                                    |
| An insurer, a referral service or an analytics service | Required                                             | Not needed                                           | The bulk of your build                               | [Confirm at onboarding](/docs/hiecm/v3/concepts/participants/insurer#confirm-at-onboarding) |
| A citizen                                              | [P1](/docs/hiecm/v3/milestones/p1), the patient side | [P2](/docs/hiecm/v3/milestones/p2), the patient side | [P3](/docs/hiecm/v3/milestones/p3), the patient side | Not needed                                                                                  |

## What each milestone gets you

| Milestone                                   | What you get                                | Who needs it                                                   |
| ------------------------------------------- | ------------------------------------------- | -------------------------------------------------------------- |
| [M1 Create](/docs/hiecm/v3/milestones/m1)   | Identity and the session token              | Everyone                                                       |
| [M2 Attach](/docs/hiecm/v3/milestones/m2)   | Linking and sharing records                 | A facility publishing records, and a citizen pushing their own |
| [M3 Retrieve](/docs/hiecm/v3/milestones/m3) | Consent and record fetching                 | Anyone reading records they did not create, and every PHR app  |
| [M4 Enrol](/docs/hiecm/v3/milestones/m4)    | A facility ID and professional registration | Anyone going live as a facility                                |

These pages give the steps, the order to build them in and the failure modes. Every request URL, header and body sits on the [API reference](/docs/hiecm/v3/api) pages, one page per call.

## Next

Start with [M1 Create](/docs/hiecm/v3/milestones/m1), or read [Go live](/docs/hiecm/v3/getting-started/going-live) for what happens after the fourth certificate.
