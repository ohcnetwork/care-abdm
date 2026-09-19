# Hospital, lab and pharmacy systems

A facility publishing a record through your software is the [HIP](/docs/hiecm/v3/getting-started/glossary#hip), the health information provider in [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm). Your job has two halves. Identify the patient by their [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) address at registration, which is [M1](/docs/hiecm/v3/api/m1). Make the records the facility creates discoverable and shareable, which is [M2](/docs/hiecm/v3/api/m2).

## Before you start

- **A valid facility ID, registered in the HIP role.** That authorises the facility to create health records and share them with whoever asks to read them as the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu). Registration lives in the [Health Facility Registry](/docs/hiecm/v3/registries).
- **A link to an [HRP](/docs/hiecm/v3/getting-started/glossary#hrp), a health repository provider**, so discovery reaches you. The facility is the HRP in most integrations, and the [HMIS](/docs/hiecm/v3/getting-started/glossary#hmis) or [LMIS](/docs/hiecm/v3/getting-started/glossary#lmis) you run is how it holds the records. Where a facility's records sit with another organisation, that organisation is the HRP.

| Purpose                          | Sandbox                                    | Production                 |
| -------------------------------- | ------------------------------------------ | -------------------------- |
| ABHA identity APIs (M1)          | `https://abhasbx.abdm.gov.in/abha/api/v3/` |                            |
| Gateway and record exchange (M2) | `https://dev.abdm.gov.in`                  | `https://apis.abdm.gov.in` |

## What you build in M1

M1 is the registration desk: create an ABHA for a patient who does not have one, or verify the one they do have. Each capability is mandatory or optional, differently for private and government integrators.

| Capability                                                        | Private integrators | Government integrators                             |
| ----------------------------------------------------------------- | ------------------- | -------------------------------------------------- |
| ABHA creation by Aadhaar OTP                                      | Mandatory           | Mandatory                                          |
| ABHA creation by Aadhaar face authentication                      | Optional            | Optional                                           |
| ABHA creation by Aadhaar biometrics, fingerprint or IRIS          | Optional            | Optional                                           |
| ABHA creation by Aadhaar demographic authentication               | Not required        | Mandatory                                          |
| Child ABHA                                                        | Not available       | Specific integrators, with NHA leadership approval |
| Login by mobile number, Aadhaar number, ABHA number, ABHA address | Mandatory           | Mandatory                                          |
| Fetch user profile                                                | Mandatory           | Mandatory                                          |
| Download ABHA card                                                | Mandatory           | Mandatory                                          |
| Mobile number management                                          | Optional            | Optional                                           |
| Re-KYC                                                            | Optional            | Optional                                           |
| Benefit programme search, link and delink                         | Not available       | Government only                                    |
| Session and refresh token APIs                                    | Mandatory           | Mandatory                                          |

Face authentication runs through the ABHA app and the Aadhaar RD service: your portal generates a QR code, the patient scans it in the ABHA app, and you poll for the result. Biometric creation needs an Aadhaar registered device, and UIDAI publishes the device list at <https://uidai.gov.in/en/ecosystem/authentication-devices-documents/biometric-devices.html>.

Implement two validation algorithms locally before you spend an API call: Luhn for an ABHA number, Verhoeff for an Aadhaar number.

## What you build in M2

Five things have to work.

1. **Health records in the right format.** A [FHIR](/docs/hiecm/v3/getting-started/glossary#fhir) R4 bundle following the NRCES profiles at <https://nrces.in/ndhm/fhir/r4/index.html>, either simple with a PDF or image attachment or structured with coded information. There are eight record types, all mandatory for an HMIS. See [FHIR and health record formats](/docs/hiecm/v3/concepts/fhir).
2. **Care contexts.** The unit that attaches to an ABHA address. The [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) is data blind and holds two fields per care context: your internal reference ID, and a display name with nothing clinical in it. Use one per outpatient visit and one per inpatient admission.
3. **Linking.** Two routes: HIP initiated with their ABHA address, and discovery when the patient comes looking from their [PHR](/docs/hiecm/v3/getting-started/glossary#phr) app. Linking needs a linking token, stored at registration, valid 6 months, regenerated with the generate link token call. See [Care contexts and linking](/docs/hiecm/v3/concepts/linking).
4. **Answering discovery.** Mandatory for every HIP. Match on the verified identifiers the gateway sends, weight them above the patient declared ones, and return reference ID and display name pairs. The response carries no clinical or sensitive information. Metadata only.
5. **Health information request and data transfer.** Validate the consent ID and the date range against the artefact, then retrieve, encrypt with the HIU's key material, sign with your long term private key, push to the data push URL and notify with `health-information/notify`. The timeout is 20 minutes from the start of the request; split large data such as CT or MRI images into parts, streaming rather than sending one payload. See [How a record travels](/docs/hiecm/v3/concepts/data-flow).

## How linking fits a clinical workflow

1. **Registration.** The patient gives an ABHA address, or scans your counter QR code and shares their profile, or gives only name, mobile, age and gender.
2. **Store the linking token** against that patient record. You need it for every visit for 6 months.
3. **Care happens.** Your system produces a prescription, a report, a discharge summary.
4. **Group the records.** One care context per OPD visit, one per IPD admission.
5. **Link when the record is ready to share**, not when the visit opens.
6. **Wait.** The HIE-CM notifies the patient's PHR app, the app raises a consent request, and when consent is granted a health information request arrives.
7. **Validate, encrypt, push, notify.** Inside 20 minutes.

Steps 1 and 2 are M1 work in your registration module. Steps 4 to 7 are M2 work, and most of it belongs in a background job, not the clinician's screen.

## Testing the loop in sandbox

There is a single end to end check:

1. Log in to a PHR app with a sandbox ABHA address.
2. Register a patient with that same ABHA address in your system.
3. Create a health record for that patient.
4. Link a care context for it using HIP initiated linking.
5. The PHR app requests the record with the appropriate consent.
6. Prepare, encrypt and transfer the record to the data push URL the app supplied.
7. The record appears in the PHR app.

Codes that cover its failures: `ABDM-1038` ABHA address and link token mismatch, `ABDM-1056` care context already linked.

## What you do not need to build

- **Consent screens.** Consent is collected in the patient's PHR app. You validate the artefact.
- **Record storage for other facilities.** You share your own records.
- **Fetching records as the HIU**, unless the facility also reads records from elsewhere. That is [M3](/docs/hiecm/v3/api/m3), a separate integration.
- **[UHI](/docs/hiecm/v3/getting-started/glossary#uhi).** Appointments, ambulances and pharmacy ordering run on a different gateway.
- **[NHCX](/docs/hiecm/v3/getting-started/glossary#nhcx).** Claims exchange runs on a different gateway again, and no endpoint on it has been documented here yet.

## What to read next

- [M1 overview](/docs/hiecm/v3/api/m1) and the [M1 API reference](/reference/hiecm-m1).
- [M2 overview](/docs/hiecm/v3/api/m2) and the [M2 API reference](/reference/hiecm-m2).
- [M2 errors](/docs/hiecm/v3/api/m2/errors), the full ABDM error code list.
- [M2 steps and calls](/reference/hiecm-m2), what sandbox exit asks you to demonstrate.
- [PHR applications](/docs/hiecm/v3/concepts/phr), the other side of every flow here.
