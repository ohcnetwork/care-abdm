# Doctor

You are a registered healthcare professional. Your identity in [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) is personal, it is separate from the facility you work in, and the facility cannot register without someone who holds one.

## Who you are in ABDM

You register on the [HPR](/docs/hiecm/v3/getting-started/glossary#hpr), the Healthcare Professionals Registry, and are issued an [HPID](/docs/hiecm/v3/getting-started/glossary#hpid). It is a 14 digit, Aadhaar authenticated identifier, written as both HPID and HPR ID.

| Form        | Sample              | Sent as                                     |
| ----------- | ------------------- | ------------------------------------------- |
| The number  | `71-2665-5777-XXXX` | `hpid` or `hprIdNumber`                     |
| The address | `name@hpr.abdm`     | `hprId`, with a `domainName` of `@hpr.abdm` |

Three categories can enrol today: doctor, nurse and pharmacist. You also declare a system of medicine. A role code says what you are on the registry: 1 for a healthcare professional, 2 for a facility manager, 3 for both.

Your HPR ID identifies you as a professional. It does not put your software on the network, and it is not the [HFR](/docs/hiecm/v3/getting-started/glossary#hfr) facility ID your hospital holds.

## What you can do

- Create your HPID through Aadhaar authentication, then register the full profile: personal details, communication address, council registration, qualification and current work.
- Upload your degree certificate and registration certificate. Both are mandatory.
- Get a fresh HPR token later, by password, by mobile [OTP](/docs/hiecm/v3/getting-started/glossary#otp) or by Aadhaar OTP.
- With role 2 or role 3, register your facility on the HFR. Both calls take `x-hprid-auth`, and submit also takes `x-hprid-auth-verifier`.

Records themselves carry a `Practitioner` resource inside the [FHIR](/docs/hiecm/v3/getting-started/glossary#fhir) bundle, so the professional behind a record is named in it.

## Why it is worth it

Your registration is a verified national identity, checked against Aadhaar and carrying your council registration and qualifications.

It is also the thing that unblocks your organisation. Nobody can register a facility, and therefore nobody can share or fetch records, until a person with facility manager rights exists. That person is you or a colleague.

No fee, payment or incentive for registering is documented here.

## Next

[HPR, the professional registry](/docs/hiecm/v3/registries/nhpr/hpr) has the call order, the profile blocks and the code lists.
