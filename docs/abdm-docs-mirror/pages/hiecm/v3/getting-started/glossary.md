# Glossary

The following terms are defined in accordance with the official terminology used by the Ayushman Bharat Digital Mission (ABDM) and the National Health Authority (NHA). The other gateways carry their own terms: [UHI](/docs/uhi/v1/getting-started/glossary), [NHCX](/docs/nhcx/v1/getting-started/glossary).

## Across ABDM

These terms mean the same thing on every ABDM gateway.

### ABDM

The Ayushman Bharat Digital Mission (ABDM) is a Government of India initiative that aims to develop an integrated, citizen-centric digital health ecosystem. It establishes common standards and core digital building blocks to enable secure and interoperable exchange of health information among participating stakeholders.

### ABHA

Ayushman Bharat Health Account (ABHA) is the account used by an individual to participate in India’s digital health ecosystem. It includes an [ABHA Number](#abha-number) for unique identification and may be linked to an [ABHA Address](#abha-address) for consent-based access and sharing of digital health records.

### ABHA address

An ABHA Address is a unique, self-declared username that enables an individual to link, access and share health records digitally with appropriate consent.

### ABHA number

An ABHA Number is a unique 14-digit number that identifies an individual as a participant in India’s digital health ecosystem. It provides a trusted identity that may be used across participating healthcare providers and payers. Creation and use of an ABHA Number are voluntary.

### FHIR

Fast Healthcare Interoperability Resources (FHIR) is a standard developed by Health Level Seven International (HL7) for the electronic exchange of healthcare information. ABDM adopts applicable FHIR R4 profiles published by the National Resource Centre for EHR Standards (NRCeS) to support interoperable health-data exchange.

### Gateway

The ABDM Gateway enables secure routing and exchange of information among participating systems in the ABDM ecosystem. Integrators communicate through approved ABDM interfaces and implement the callback endpoints and authentication mechanisms specified in the applicable technical documentation.

### Health Tech Committee

The Health Technology Committee (HTC) reviews eligible integrations as part of the ABDM sandbox exit and production onboarding process. The review is undertaken after completion of the applicable functional, security and documentation requirements prescribed by [NHA](#nha). See [Go live](/docs/hiecm/v3/getting-started/going-live).

### HFR

The Health Facility Registry (HFR) is a comprehensive repository of public and private health facilities in India across different systems of medicine. Registered facilities receive a unique Facility ID and may access applicable digital services within the ABDM ecosystem. See [registries](/docs/hiecm/v3/registries).

### HIE-CM

The Health Information Exchange and Consent Manager (HIE-CM) is a gateway under ABDM that manages consent relating to an individual’s personal health data and supports the secure, consent-based exchange of interoperable health information among ecosystem participants. See [The ABDM gateway](/docs/hiecm/v3/concepts/gateway).

### HPID

Healthcare Professional ID (HPID) refers to the unique identifier assigned to an eligible healthcare professional upon successful registration and verification in the [Healthcare Professionals Registry](#hpr). See [M4](/docs/hiecm/v3/getting-started/glossary#m4).

### HPR

The Healthcare Professionals Registry (HPR) is the national registry of doctors, nurses and pharmacists. Registering a professional on the HPR results in the issuance of an [HPID](#hpid). The HPR Token can also be used to onboard a facility to the [HFR](#hfr).

### KYC

Know Your Customer: the identity check that must pass before an [ABHA number](#abha-number) is issued. The check runs against Aadhaar: by [OTP](#otp), by biometric authentication (face, fingerprint or iris), or, for government entities only, by demographic authentication.

### NHA

The National Health Authority (NHA), under the Ministry of Health and Family Welfare, Government of India, is responsible for the implementation of ABDM and PMJAY and the management of its foundational digital health building blocks, policies and standards.

### NHCX

The National Health Claims Exchange (NHCX) is a digital gateway under ABDM that supports standardised and interoperable exchange of health-insurance claims information among payers, providers and other authorised participants. See [NHCX](/docs/nhcx/v1).

### OTP

One Time Password: a short code sent to a mobile number or an email address to prove the person holds it. An ABHA OTP is valid for 10 minutes, and it is always verified together with the [txnId](#txnid) of the call that requested it.

### PHR

A Personal Health Record (PHR) application enables an individual to discover, link, view and manage personal health records and to provide or withdraw consent for sharing those records through the ABDM ecosystem. See [PHR applications](/docs/hiecm/v3/concepts/phr).

### Safe to Host certificate

The security documentation a [WASA](#wasa) supports. It is issued after the assessment by a CERT-In-empanelled auditor, and it is required for production onboarding under ABDM.

### Sandbox

The ABDM Sandbox is a controlled test environment that enables health-technology companies and other eligible entities to integrate their software with ABDM building blocks, test applicable use cases and demonstrate compliance before seeking production access.

### txnId

Transaction id. Most flows take two or three calls, and the first one returns a `txnId` that the calls after it send back, so ABDM knows which attempt they belong to. It is short lived and single purpose. It is not a session and it is not a token: holding a `txnId` does not authenticate you, and it stops working once the flow it belongs to finishes or expires.

### UHI

The Unified Health Interface (UHI) is an open network for digital health-service discovery and delivery. It enables participating applications and providers to interact through standard protocols for services such as appointment discovery and booking and other supported digital health use cases. See [UHI](/docs/uhi/v1).

### WASA

Web Application Security Assessment (WASA) is a security assessment performed by a CERT-In-empanelled auditor on the relevant application environment. The assessment supports issuance of the required security documentation for production onboarding under ABDM. See [Security audit](/docs/hiecm/v3/getting-started/security-audit).

## On HIE-CM

These terms describe the principal roles, consent objects and integration concepts used within the ABDM HIE-CM framework.

### Bridge

A bridge is the registered integration endpoint through which a participating system exchanges callback-based messages with the [ABDM Gateway](#gateway). The endpoint must be configured and secured in accordance with the applicable sandbox and API specifications.

### Care context

A care context is a logical grouping of an individual’s health records maintained by a [Health Information Provider](#hip). It is represented through a reference number and a display name and is linked to the individual’s [ABHA Address](#abha-address) with appropriate authentication or consent, as applicable.

### Consent artefact

A consent artefact is the machine-readable record of consent granted by an individual for access to specified health information. It contains the authorised purpose, health-information types, data range, frequency, expiry and participating entities, as applicable.

### Consent manager

A Consent Manager enables an individual to manage consent for the collection, use and sharing of personal health information. Within ABDM, the [HIE-CM](#hie-cm) framework supports consent management and consent-based exchange of health records among authorised participants.

### Discovery

Discovery is the process through which an individual’s [PHR application](#phr) requests a participating [Health Information Provider](#hip) to identify available [care contexts](#care-context) associated with that individual. The provider performs matching using the identifiers supplied through the prescribed workflow and returns eligible care-context metadata without disclosing clinical content.

### ECDH

Elliptic Curve Diffie-Hellman (ECDH) is a cryptographic key-agreement method used in the secure exchange of health information. Its implementation must conform to the encryption, key-management and payload specifications prescribed in the applicable ABDM technical documentation.

### EMR, EHR

An Electronic Medical Record (EMR) is a digital record of care maintained within a healthcare organisation, while an Electronic Health Record (EHR) is designed to support a broader, longitudinal view of an individual’s health information across care settings. ABDM enables interoperable, consent-based exchange of such records while the source records remain with the responsible data custodian. See [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu).

### HI type

Health Information (HI) Type denotes the category of health record covered by a consent or data-exchange request. Supported values are specified in the current ABDM API and FHIR implementation documentation and may include prescriptions, diagnostic reports, outpatient consultations, discharge summaries, immunisation records, health documents and wellness records.

### HIP

A Health Information Provider (HIP) is an entity that creates or holds an individual’s health information and makes it available for consent-based exchange through ABDM. A HIP supports discovery and linking of [care contexts](#care-context) and shares health information only in accordance with a valid [consent artefact](#consent-artefact) and the applicable technical requirements.

### HIU

A Health Information User (HIU) is an authorised entity that requests and uses an individual’s health information for a specified purpose. An HIU may access health information only after the individual grants valid consent and the request satisfies the applicable policy and technical requirements.

### HMIS, HIS, HIMS

Hospital Management Information System (HMIS), Hospital Information System (HIS) and Hospital Information Management System (HIMS) are terms commonly used for software that supports a healthcare facility’s administrative, operational and clinical workflows. Such systems may integrate with ABDM to perform applicable HIP, HIU, [ABHA](#abha) and registry-related functions. See [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu).

### HRP

A Health Repository Provider (HRP) is an entity responsible for storing or maintaining health information on behalf of a healthcare provider or another authorised participant. Where applicable, an HRP may also perform the HIP function for consent-based exchange of records.

### IMS

An Information Management System (IMS) is a digital solution used by a healthcare facility or service provider to manage relevant administrative, operational or clinical information. Depending on its use case, an IMS may integrate with ABDM building blocks and perform authorised HIP or HIU functions.

### LIMS, LMIS

A Laboratory Information Management System (LIMS), also referred to in some contexts as an LMIS, supports laboratory workflows such as test orders, specimen tracking, processing and reporting. An ABDM-enabled laboratory system may link and share diagnostic records as a HIP and may request authorised records as an HIU. See [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu).

### Link token

The token that authorises a [Health Information Provider](#hip) to link [care contexts](#care-context) to a patient's [ABHA Address](#abha-address). It is generated through the link token API and is valid for six months.

### M1

Milestone 1 (M1 Create), ABHA Creation and Verification, covers ABHA-related functions implemented within an integrated application, including creation of an [ABHA Number](#abha-number) through supported methods, creation of an [ABHA Address](#abha-address), verification during patient registration, download of the ABHA Card and other role-specific functions prescribed in the current test cases. See [M1 Create](/docs/hiecm/v3/milestones/m1).

### M2

Milestone 2 (M2 Attach), [Health Information Provider](#hip) Services, covers linking health records with an individual’s [ABHA Address](#abha-address). It includes discovery of eligible [care contexts](#care-context), authentication or consent for linking, linking of care contexts by the HIP and notification of newly linked records to the applicable [PHR application](#phr). See [M2 Attach](/docs/hiecm/v3/milestones/m2).

### M3

Milestone 3 (M3 Retrieve), [Health Information User](#hiu) Services, covers consent-based exchange of health information. It includes creation and management of consent requests by an HIU, receipt of the individual’s decision, retrieval of a valid [consent artefact](#consent-artefact) and secure exchange of the authorised health information between participating entities. See [M3 Retrieve](/docs/hiecm/v3/milestones/m3).

### M4

Milestone 4 (M4 Enrol), also referred to as National Healthcare Providers Registry (NHPR) native integration, covers integration of healthcare-professional and health-facility registration functions into eligible applications. The milestone is undertaken in accordance with the roles, sequencing and test requirements prescribed by [NHA](#nha). See [M4 Enrol](/docs/hiecm/v3/milestones/m4).

### PMS

A Pharmacy Management System (PMS) supports pharmacy operations such as prescription processing, dispensing, inventory and billing. Where integrated with ABDM, it may perform authorised HIP or HIU functions in accordance with the relevant use case, consent requirements and technical specifications. See [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu).

### Purpose of use

The reason an [HIU](#hiu) gives for asking for records; it travels in the consent request and the patient sees it. The codes are a subset of HL7's v3 PurposeOfUse value set: `CAREMGT` (care management), `BTG` (break the glass), `PUBHLTH` (public health), `HPAYMT` (healthcare payment), `DSRCH` (disease specific healthcare research) and `PATRQT` (self requested).
