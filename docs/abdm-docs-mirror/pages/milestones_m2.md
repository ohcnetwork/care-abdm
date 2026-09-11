# M2 Attach: linking and sharing

Milestone 2 attaches the health records you hold to a person's [ABHA
address](/docs/hiecm/v3/getting-started/glossary#abha-address). After it you
can group records into [care
contexts](/docs/hiecm/v3/getting-started/glossary#care-context), link them,
answer [discovery](/docs/hiecm/v3/getting-started/glossary#discovery) requests
from [PHR](/docs/hiecm/v3/getting-started/glossary#phr) apps, and push
encrypted records when a consented request arrives.

## In short

- Your facility is the [HIP](/docs/hiecm/v3/getting-started/glossary#hip) when
  it publishes a record, and your software is how it publishes. A valid facility
  ID and registration in the HIP role come first, from [M4 Enrol](./m4).
- M2 is keyed to an ABHA address, so [M1 Create](./m1) has to work before M2
  can.
- Hold a [link token](/docs/hiecm/v3/getting-started/glossary#link-token) per
  patient. Its validity is six months.
- Records go out as [FHIR](/docs/hiecm/v3/getting-started/glossary#fhir) R4
  against the ABDM profiles.
- Four callbacks name a path and carry no documented payload. Do not assume a
  body.

## What M2 gives you

| Capability | What your system can do |
|---|---|
| Care contexts | Group each visit or admission into a named unit that can be linked to an ABHA address |
| HIP initiated linking | Link a care context yourself, when the patient gave you their ABHA address at registration |
| Notification to mobile | Make a record findable when you hold only a mobile number, a name, an age and a gender |
| Discovery | Answer a patient's search for their records at your facility, and let them link what you return |
| Data request and transfer | Receive a consented request, package the records, encrypt them, and push them to the requester |

Requesting records from other facilities is [M3 Retrieve](./m3).

## Who needs it

Hospitals, laboratories, pharmacies and imaging centres, through the software
they record care in. A citizen pushing their own records from a PHR app builds
[P2 Linking and records](./p2), the patient side of M2.

## Prerequisites

1. A valid facility ID and registration in the HIP role. That authorises your
   facility to create health records and share them with whoever asks to read
   them as the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu). It comes from
   [M4 Enrol](./m4).
2. A working [M1 Create](./m1) integration. Linking is keyed to an ABHA
   address.
3. A link token per patient, stored when the patient registers. Validate it
   before use. If you hold no valid one, regenerate it using demographic
   authentication.
4. FHIR R4 output conforming to the ABDM profiles at
   [nrces.in](https://nrces.in/ndhm/fhir/r4/index.html).

:::note[Callback payloads]
Four callbacks name a path and carry no documented payload: discovery, link
init, link confirm, and consent notify. Do not assume a body for them. The data
notification callback is documented in full.
:::

## Record types you can link

Each type can be a simple bundle wrapping a PDF or image attachment, or a
structured bundle with coded clinical data.

| Record type | What it holds |
|---|---|
| Diagnostic Report Record | Radiology and laboratory reports |
| Discharge Summary Record | The discharge summary for the ABDM health data set |
| Health Document Record | Unstructured historical records, usually uploaded through a health locker |
| Immunization Record | Immunisations, vaccine certificates and next dose recommendations |
| OP Consult Record | Outpatient notes: examinations, procedures, medications and advice |
| Prescription Record | Medication advice, following Pharmacy Council of India guidelines |
| Wellness Record | Vitals, physical examination and general health data captured in PHR apps |
| Invoice Record | Pharmacy invoices, consultation invoices and other billing records |

An [HMIS](/docs/hiecm/v3/getting-started/glossary#hmis) must implement every
[HI type](/docs/hiecm/v3/getting-started/glossary#hi-type).

## Build it with an agent

Hand M2 to the agent you already use, as one file it loads once. Install it, or open it there in one click.

## Certification

M2 has no certification step of its own. One exit process covers the whole
integration, run once, after every milestone your role needs works end to end.
See [Going live](/docs/hiecm/v3/getting-started/going-live) for the four steps
and what each one asks of you.

Test data is in the [data
dictionary](/docs/hiecm/v3/reference/data-dictionary). [Support](/docs/support)
lists the channels. The cases you are certified against are in [M2 testing use
cases](/docs/hiecm/v3/resources/testing/m2).

## The journey, one diagram per flow

Milestone 2 (M2) of [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) has four flows. This page draws each one, so you can see the round trips before you read the detail.

"Your system" is the [HMIS](/docs/hiecm/v3/getting-started/glossary#hmis) or [LMIS](/docs/hiecm/v3/getting-started/glossary#lmis) your facility publishes through. "HIE-CM" is the [Health Information Exchange and Consent Manager](/docs/hiecm/v3/getting-started/glossary#hie-cm) gateway.

## Journey 1: HIP initiated linking

The patient gave you their [ABHA address](/docs/hiecm/v3/getting-started/glossary#abha-address) at registration. Link the [care context](/docs/hiecm/v3/getting-started/glossary#care-context) as soon as the record is ready: linking is what makes it reachable from [PHR](/docs/hiecm/v3/getting-started/glossary#phr) apps.

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant S as Your system
    participant CM as HIE-CM
    participant A as Patient's PHR apps
    P->>S: Registers, gives ABHA address
    S->>CM: Request link token
    CM-->>S: Link token, valid six months
    Note over S: Store the token against the patient
    S->>S: New health record created
    S->>S: Assign the record to a care context
    S->>CM: Link the care context, carrying the link token
    CM-->>S: Link acknowledged
    CM->>A: Notify every PHR app subscribed to that ABHA address
```

- **No valid [link token](/docs/hiecm/v3/getting-started/glossary#link-token).** Validate the stored token before use, with a tool such as JWT.io. If it is expired or missing, regenerate it through demographic authentication.
- **An existing care context gains new records.** The step 8 notification fires for that too, not only for a new context.

## Journey 2: Notification to mobile

You hold a mobile number, a name, an age and a gender, but no ABHA address. You cannot link, so you ask the HIE-CM to tell the patient a record is waiting.

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant S as Your system
    participant CM as HIE-CM
    participant A as PHR app
    P->>S: Registers with mobile, name, age, gender
    S->>S: New health record created
    S->>CM: Notify that a record is ready to share
    CM->>P: SMS with a secure deep link
    P->>A: Opens the link, installs a PHR app if needed
    P->>A: Creates an ABHA address if they do not have one
    Note over A,S: The patient now runs journey 3 to find and link the record
```

## Journey 3: Discovery and link

The patient starts [discovery](/docs/hiecm/v3/getting-started/glossary#discovery) from a PHR app and picks the facility they visited. Your system matches them on the identifiers the gateway passes you and answers with care contexts.

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant A as Patient's PHR app
    participant CM as HIE-CM
    participant S as Your system
    P->>A: Selects the facility they visited
    A->>CM: Discovery request
    CM->>S: Discovery request with verified and unverified identifiers
    S->>S: Match against your patient records
    S-->>CM: List of care contexts, metadata only
    CM-->>A: Care contexts to review
    P->>A: Selects the care contexts to link
    A->>CM: Link the selected care contexts
    CM->>S: Link request for those care contexts
    S-->>CM: Link confirmed
    CM-->>A: Records now linked to the ABHA address
```

Step 3 hands you two groups of identifiers.

- **Verified.** ABHA address, mobile number, name, gender, year of birth. Weight these higher.
- **Unverified, user declared.** Facility issued identifiers such as a medical registration number or patient ID.

Step 5 has a hard rule: care context metadata only. No diagnosis, no test result, no report content.

Steps 8 to 11 are drawn in words. The error codes name them init, confirm, on-init and on-confirm, so the shape is a gateway request and a callback from you. Their fields are not yet published.

## Journey 4: Health record request and data transfer

Another facility, an insurer or a citizen's PHR app asks for records under a [consent artefact](/docs/hiecm/v3/getting-started/glossary#consent-artefact) the patient granted. Whoever asks is the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu).

```mermaid
sequenceDiagram
    autonumber
    participant U as HIU
    participant CM as HIE-CM
    participant S as Your system
    U->>CM: Health information request
    Note over U,CM: Consent ID, data push URL, date range, public key and nonce
    CM->>CM: Generate a transaction ID
    CM-->>U: Transaction ID
    CM->>S: Forward the request with the transaction ID
    S->>S: Check the consent is valid and active
    S->>S: Check the date range sits inside the consent
    S->>S: Check the encryption parameters
    S->>S: Build the FHIR bundle, encrypt it, sign it
    S->>U: Push encrypted data to the data push URL
    S->>CM: Call health-information/notify, transfer complete
    U->>CM: Notify the outcome, success or failure
```

Four constraints apply to step 9, the push.

- The HIU supplies the data push URL. It can differ from its registered gateway URL, which keeps the requester harder to identify.
- The push has a 20 minute window from the start of the request. Past that, expect failure or timeout.
- Large datasets such as CT or MRI images may be split across multiple parts.
- Stream very large files rather than sending one whole payload.

Encryption uses [ECDH](/docs/hiecm/v3/getting-started/glossary#ecdh), Elliptic Curve Diffie Hellman, over Curve25519. Mechanics: [use cases](/reference/hiecm-m2). Call order: [API reference](/reference/hiecm-m2).

## Next

- The four flows as diagrams: [the journey below](#the-journey-one-diagram-per-flow).
- The calls, callbacks and error codes: [M2 API
  reference](/docs/hiecm/v3/api/m2).
- The next milestone: [M3 Retrieve](./m3).
