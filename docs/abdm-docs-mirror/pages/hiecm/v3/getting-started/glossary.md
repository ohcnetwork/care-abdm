# Glossary

Every term the HIE-CM documentation links to. Each row keeps its own anchor, so a link like `#hip` lands on the right row. The other gateways carry their own terms: [UHI](/docs/uhi/v1/getting-started/glossary), [NHCX](/docs/nhcx/v1/getting-started/glossary).

## Across ABDM

These terms mean the same thing on every ABDM gateway.

### ABDM

Ayushman Bharat Digital Mission, India's national programme for digital health, run by the [NHA](#nha). ABDM sets the identifiers, the registries and the exchange rules that let a health record move from the system that created it to the person it belongs to.

### ABHA

Ayushman Bharat Health Account. It comes in two forms people confuse: the 14 digit [ABHA number](#abha-number) and the readable [ABHA address](#abha-address). When a document says "the patient's ABHA", work out which of the two it means before you write code against it.

### ABHA address

A readable name on the [HIE-CM](#hie-cm), such as `name@abdm`, used to reach health records and share them with a provider. Every ABHA number is issued a default address made from the number itself: `14digit@sbx` in [sandbox](#sandbox), `14digit@abdm` in production. A person can also create an ABHA address without holding an ABHA number, using mobile number, name, age and gender.

### ABHA number

A 14 digit identifier issued to a person only after a [KYC](#kyc) check passes, and the identity anchor of ABDM: one person, one number. An ABHA number carries a check digit and validates under the Luhn algorithm. See [M1](/docs/hiecm/v3/getting-started/glossary#m1) for how one is created.

### FHIR

Fast Healthcare Interoperability Resources, the HL7 standard ABDM uses to carry health records. ABDM uses FHIR R4 with the profiles published by NRCES at [nrces.in/ndhm/fhir/r4](https://nrces.in/ndhm/fhir/r4/index.html). Every record you share travels as a FHIR bundle of type `document` whose first entry is a Composition.

### Gateway

The routing layer for ABDM: you do not call another participant directly, you call the gateway, it forwards your request, and the reply arrives at your [bridge](/docs/hiecm/v3/getting-started/glossary#bridge) as a separate inbound call. You get a session token first, by posting your client id and client secret to `/api/hiecm/gateway/v3/sessions`. Two sandbox hosts serve that path, `https://apissbx.abdm.gov.in` and `https://dev.abdm.gov.in`. Take the host from your onboarding documentation and keep it in configuration; see [Choose your gateway](/docs/hiecm/v3).

### Health Tech Committee

The committee that reviews your integration at the end of the sandbox exit process, referred to as the HTC. Once your functional testing, security audit and exit form are complete, it is scheduled its own demonstration, separate from the one you give the integration team earlier. Its decision is recorded in four review stages, each carrying its own reviewer, comment and date. See [Go live](/docs/hiecm/v3/getting-started/going-live).

### HFR

Health Facility Registry, the national directory of health facilities across modern and traditional systems of medicine, public and private, including hospitals, clinics, diagnostic laboratories, imaging centres and pharmacies. A facility enrols once and receives a facility ID that identifies it everywhere in ABDM. See [registries](/docs/hiecm/v3/registries).

### HIE-CM

Health Information Exchange and Consent Manager, the component that routes exchange requests and manages patient consent. It is data blind: it holds identifiers and metadata about [care contexts](/docs/hiecm/v3/getting-started/glossary#care-context), never the content of a record. See [The ABDM gateway](/docs/hiecm/v3/concepts/gateway).

### HPID

Healthcare Professional ID: a 14 digit number issued to a healthcare professional or a facility manager after Aadhaar authentication. It is the professional's digital identity across ABDM, and it is created on the [HPR](#hpr). See [M4](/docs/hiecm/v3/getting-started/glossary#m4).

### HPR

Healthcare Professionals Registry, the national registry of doctors, nurses, pharmacists and other healthcare professionals. Registering a professional there issues an [HPID](#hpid). The HPR token is also used when onboarding a facility to the [HFR](#hfr).

### KYC

Know Your Customer: the identity check that must pass before an [ABHA number](#abha-number) is issued. In ABDM the check runs against Aadhaar, by one of four methods: an [OTP](#otp) to the Aadhaar linked mobile number, face authentication, fingerprint or IRIS capture on a registered device, or a demographic match. Re-KYC repeats the check on an ABHA number that already exists.

### NHA

National Health Authority, the government body that runs ABDM, publishes its specifications, and operates both the [sandbox](#sandbox) and the production gateways.

### NHCX

National Health Claims Exchange, ABDM's network for insurance claims between providers and payers, with its own sandbox and its own document set at [hcxsbx.abdm.gov.in](https://hcxsbx.abdm.gov.in). See [NHCX](/docs/nhcx/v1).

### OTP

One Time Password: a short code sent to a mobile number or an email address to prove the person holds it. ABDM uses OTPs at many points: Aadhaar [KYC](#kyc), mobile number verification during ABHA creation, and login. An OTP is always paired with a transaction id from the call that requested it.

### PHR

Personal Health Record, a patient facing application: the person logs in with their [ABHA address](#abha-address), discovers records held by facilities they visited, links them, and reads them. PHR apps subscribe to a patient's ABHA address and are notified when a new [care context](/docs/hiecm/v3/getting-started/glossary#care-context) is linked. See [PHR applications](/docs/hiecm/v3/concepts/phr).

### Safe to Host certificate

The certificate a [WASA](#wasa) produces, issued by a CERT-In empanelled auditor, and required before you receive production credentials. It names the application it covers and carries an issue date and an expiry date. A certificate that is in date covers a new module without a fresh audit of the parts already certified. See [Security audit](/docs/hiecm/v3/getting-started/security-audit).

### Sandbox

The ABDM test environment, and where every integration starts: you register on the sandbox portal, declare your role and the milestones you plan to complete, and receive a client id and client secret. Sandbox hosts differ from production, so ABHA calls go to `abhasbx.abdm.gov.in` in sandbox and `abha.abdm.gov.in` in production. Everything in sandbox is test data; see [Get started](/docs/hiecm/v3/getting-started/sandbox).

### txnId

Transaction id. Most flows take two or three calls, and the first one returns a `txnId` that the calls after it send back, so ABDM knows which attempt they belong to. It is short lived and single purpose. It is not a session and it is not a token: holding a `txnId` does not authenticate you, and it stops working once the flow it belongs to finishes or expires.

### UHI

Unified Health Interface, an open protocol network for health services that are not record exchange: physical consultation booking, ambulance booking, blood bank discovery, Jan Aushadhi and pharmacy search. It has two roles, [EUA](/docs/uhi/v1/getting-started/glossary#eua) on the consumer side and [HSPA](/docs/uhi/v1/getting-started/glossary#hspa) on the provider side, and every call is signed with Ed25519. See [UHI](/docs/uhi/v1).

### WASA

The security audit of your application, conducted on your staging URL by an auditor from the CERT-In empanelled list. It produces the [Safe to Host certificate](#safe-to-host-certificate), and it is separate from functional testing: passing every milestone still leaves this to do. Each platform you ship is audited on its own. See [Security audit](/docs/hiecm/v3/getting-started/security-audit).

## On HIE-CM

These terms belong to HIE-CM: the roles, the consent objects and the four milestones.

### Bridge

The set of callback endpoints your system exposes to the [gateway](#gateway). A bridge is your integration, not a facility: one bridge URL is stored for each registered participant, every facility you link to that bridge shares it, and callbacks are posted underneath it. The paths are `POST {hiuBridgeUrl}/v0.5/consents/hiu/notify` for an [HIU](#hiu) and `POST {hipBridgeUrl}/v0.5/health-information/hip/request` for a [HIP](#hip). Registering your bridge URL is part of sandbox onboarding.

### Care context

A group of a patient's health records, defined by your system. It carries two fields and nothing else: a reference number, which is your own internal identifier, and a display name a person can read, which must not carry clinical detail such as a diagnosis or a test result because it is shown before consent. Use one care context per outpatient visit and one per inpatient admission.

### Consent artefact

The record of a consent the patient granted. It names the patient, the requesting [HIU](#hiu), the [HI types](#hi-type) covered, the [purpose of use](#purpose-of-use), the date range of records allowed and an expiry. An HIU quotes the consent artefact id when it asks for data, and the [HIP](#hip) checks that id, and its date range, before it sends anything.

### Consent manager

The component that holds consent on the patient's behalf. In ABDM that component is the [HIE-CM](#hie-cm). It receives consent requests, shows them to the patient, records the grant or the denial, and tells both the requester and the record holder what the patient decided.

### Discovery

The step where a patient's [PHR](#phr) app asks a facility whether it holds records for that patient. The [HIE-CM](#hie-cm) forwards the request to the [HIP](#hip) with verified identifiers (ABHA address, mobile number, name, gender, year of birth) and any unverified identifier the patient typed, such as a hospital patient ID. Your system matches those against your own patients and replies with a list of [care contexts](#care-context), carrying no clinical detail.

### ECDH

Elliptic Curve Diffie-Hellman key exchange, used so that only the [HIU](#hiu) that holds a valid consent can read the records a [HIP](#hip) sends. Both sides generate a short lived key pair and a random 32 byte nonce, exchange the public halves, and derive the same session key. The exchange uses Curve25519, and the encryption itself uses AES-GCM.

### EMR, EHR

Electronic Medical Record and Electronic Health Record: the clinical system a hospital or a clinic records consultations, prescriptions and results in. The distinction drawn is that an EMR holds one provider's record of what happened in their own building and an EHR follows the patient across providers, but vendors use the two words for the same product. A facility uses it to publish records as the [HIP](#hip), linking care contexts in [M2](#m2), and to fetch them as the [HIU](#hiu) in [M3](#m3). ABDM does not build an EHR as a database: the records stay with the facility that created them, and the [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) plus consent is what lets another provider assemble the picture. See [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu).

### HI type

Health Information type: the kind of record being asked for or shared, used in consent requests and in data requests. There are seven values: `Prescription`, `DiagnosticReport`, `OPConsultation`, `DischargeSummary`, `ImmunizationRecord`, `HealthDocumentRecord` and `WellnessRecord`. The M2 error message for an invalid HI type also lists `Invoice`.

### HIP

Health Information Provider: the role an entity takes when it publishes a health record. A hospital, laboratory or pharmacy takes it through its own software, and a citizen takes it through a [PHR](#phr) app. The HIP links [care contexts](#care-context) to a patient's [ABHA address](#abha-address), answers [discovery](#discovery), and sends encrypted records when a valid [consent artefact](#consent-artefact) exists. [M2](#m2) is the HIP milestone.

### HIU

Health Information User: whoever asks to read records they did not create is the HIU. A facility asks through a doctor's console or its [HMIS](#hmis), a citizen asks through a [PHR](#phr) app or a health locker, and an insurer, a referral tool or an analytics product asks while holding neither an [ABHA address](#abha-address) nor a facility ID. The HIU raises a consent request, waits for the patient's decision, and fetches data only under a granted [consent artefact](#consent-artefact). [M3](#m3) is the HIU milestone.

### HMIS, HIS, HIMS

The software a hospital runs day to day: registration, visits, orders, results and billing. Three names for it: HMIS is Hospital Management Information System, HIS is Hospital Information System, HIMS is Hospital Information Management System. A facility uses it to publish records as the [HIP](#hip) and to fetch them as the [HIU](#hiu), so the ABDM work is [M2](#m2) and [M3](#m3) either way, and it must implement every [HI type](#hi-type). Note that `HIS-` is also the prefix on every error code the HPR and the HFR return: those are [M4](#m4) registry errors and nothing to do with hospital software. See [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu).

### HRP

Health Repository Provider. HRP is whoever holds the records, which is custody rather than a direction of travel. That is the facility in most integrations, and its repository software is how the facility holds them. Where a facility's records sit with another organisation, that organisation is the HRP. HRP and HIP are written together as "HRP/HIP" because the entity holding the records is usually the entity publishing them. If you run an [HMIS](#hmis) or a [LIMS](#lims) for a facility integrating [M2](#m2), that facility is the HRP. One repository can hold the records of many facilities.

### IMS

Information Management System, the umbrella term for the software a health facility runs: an [HMIS](#hmis) in a hospital, an [EMR](#emr) in a clinic, a [LIMS](#lims) in a laboratory, a [PMS](#pms) in a pharmacy. IMS is one of the two integrator roles on HIE-CM, the other being [PHR](#phr), and it is fixed for the life of your product. Which of those systems you build does not change the integration: the facility is the [HIP](#hip) when it publishes and the [HIU](#hiu) when it fetches, so the work is [M2](#m2) and [M3](#m3) either way.

### LIMS, LMIS

Laboratory Information Management System, also written LMIS: the system a diagnostic lab uses to record orders, samples and results. A laboratory uses it to publish records as the [HIP](#hip), linking each report as a care context in [M2](#m2), which is most of what a lab does, and to fetch them as the [HIU](#hiu) on the rarer occasions it reads a patient's history. See [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu).

### Link token

The token that authorises your system to link a [care context](#care-context) to a patient's [ABHA address](#abha-address); your system obtains it when the patient registers and stores it against that patient. A link token is valid for six months. Validate it before use. If you do not hold a valid one, regenerate it through demographic authentication before you link.

### M1

Milestone 1, ABHA identity: creating an [ABHA number](#abha-number), logging a person in, reading and updating their profile, downloading the ABHA card, and the [gateway](#gateway) session and token calls that everything else depends on. Most of these APIs are mandatory for both private and government integrators, with Aadhaar demographic authentication the exception: mandatory for government integrators, not required for private ones. See [M1](/docs/hiecm/v3/api/m1).

### M2

Milestone 2, sharing records as a [HIP](#hip): turning your records into [FHIR](#fhir) bundles, grouping them into [care contexts](#care-context), linking those to a patient's [ABHA address](#abha-address), answering [discovery](#discovery), and encrypting and pushing data when consent allows. See [M2](/docs/hiecm/v3/api/m2).

### M3

Milestone 3, consent and reading records as an [HIU](#hiu): raising a consent request, tracking its status, handling the grant or denial callback, fetching the [consent artefact](#consent-artefact), requesting health information and decrypting what arrives. See [M3](/docs/hiecm/v3/api/m3).

### M4

Milestone 4, the registries: creating an [HPID](#hpid) on the [HPR](#hpr) and onboarding a facility to the [HFR](#hfr). This is also called NHPR. See [M4](/docs/hiecm/v3/api/m4).

### PMS

Pharmacy Management System: the software a pharmacy runs to dispense and to keep its stock. A pharmacy uses it to fetch the prescription it is dispensing against as the [HIU](#hiu), and to publish what it dispensed as the [HIP](#hip). See [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu).

### Purpose of use

The reason an [HIU](#hiu) gives for asking for records; it travels in the consent request and the patient sees it. The codes are a subset of HL7's v3 PurposeOfUse value set: `CAREMGT` (care management), `BTG` (break the glass), `PUBHLTH` (public health), `HPAYMT` (healthcare payment), `DSRCH` (disease specific healthcare research) and `PATRQT` (self requested).
