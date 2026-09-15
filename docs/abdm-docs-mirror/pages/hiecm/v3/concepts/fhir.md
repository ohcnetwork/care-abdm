# FHIR and health record formats

Every health record that moves inside [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) travels as a [FHIR](/docs/hiecm/v3/getting-started/glossary#fhir) bundle, not a PDF in an envelope of your own design and not your database rows. This page gives the version, the profiles, the bundle shape and how to validate one; the packaging detail is in the [M2 guide](/docs/hiecm/v3/api/m2).

## R4, with Indian profiles

ABDM uses FHIR release 4. Base FHIR is loose: it says a `MedicationRequest` exists, not which fields an Indian prescription must fill. That second layer is a profile, and for ABDM the profiles are published by the National Resource Centre for EHR Standards, NRCES, at [nrces.in/ndhm/fhir/r4](https://nrces.in/ndhm/fhir/r4/index.html). "ABDM compliant FHIR" means R4 conforming to those profiles. Read the NRCES implementation guide for field level questions. It is not restated here.

## Two ways to build any record

| Shape             | What it is                                                             | When you use it                                          |
| ----------------- | ---------------------------------------------------------------------- | -------------------------------------------------------- |
| Simple bundle     | A FHIR bundle wrapping a PDF or image attachment that holds the detail | Your source document is a scan, a signed PDF or an image |
| Structured bundle | A FHIR bundle with coded health information in FHIR resources          | Your system holds the data as fields, and can code it    |

Both are compliant. A structured bundle is more useful to the receiver, because it can be searched rather than only displayed.

## The record types

There are eight record types. Implementing all of them is mandatory for an [HMIS](/docs/hiecm/v3/getting-started/glossary#hmis).

| Record type              | What it holds                                                                                                                    | [HI type](/docs/hiecm/v3/getting-started/glossary#hi-type) code |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Diagnostic Report Record | Radiology and laboratory reports                                                                                                 | `DiagnosticReport`                                              |
| Discharge Summary Record | The discharge summary for the ABDM health data set                                                                               | `DischargeSummary`                                              |
| Health Document Record   | Unstructured historical records, usually uploaded by patients through a health locker                                            | `HealthDocumentRecord`                                          |
| Immunization Record      | Immunisations, vaccine certificates and next dose recommendations                                                                | `ImmunizationRecord`                                            |
| OP Consult Record        | Outpatient notes: examinations, procedures, medications and clinical advice                                                      | `OPConsultation`                                                |
| Prescription Record      | Medication advice, following Pharmacy Council of India guidelines                                                                | `Prescription`                                                  |
| Wellness Record          | Vitals, physical examination and general health data, often captured in a [PHR](/docs/hiecm/v3/getting-started/glossary#phr) app | `WellnessRecord`                                                |
| Invoice Record           | Pharmacy invoices, consultation invoices and other billing                                                                       | `Invoice`                                                       |

The names come from M2, the codes from the M3 HI type table and the M2 error message for an invalid HI type. The two lists are not published as one table; they are paired here by name, one to one.

Two mismatches. The M3 table displays `HealthDocumentRecord` as "Record artifact" rather than as a health document, and omits `Invoice`, which appears only in the M2 error message. Check the swagger before you send `Invoice` in a consent request.

## Which resources a record carries

The reference service on the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) side supports these resources inside a bundle.

- **Clinical content:** `Observation`, `Condition`, `MedicationRequest`, `DocumentReference`, `DiagnosticReport`, `Procedure`.
- **Context and reference entities:** `Medication`, `Practitioner`, `Patient`, `Organization`, `Encounter`.

That is the union across record types, not a mapping. Which resources belong to which record type is not documented here. The NRCES profile for each type is the authority.

## The bundle shape

Every record is a `Bundle` of `type: document`, and the first entry must be a `Composition`.

```json
{  "resourceType": "Bundle",  "id": "bundle01",  "timestamp": "2020-01-01T15:32:26.605+05:30",  "type": "document",  "entry": [    {      "fullUrl": "Composition/1",      "resource": {        "resourceType": "Composition",        "id": "1",        "status": "final",        "type": {          "coding": [            {              "system": "https://ndhm.gov.in/sct",              "code": "440545006",              "display": "Prescription record"            }          ]        }      }    }  ]}
```

That is the skeleton. The full sample, with the Organization, the Encounter and the section entries, is on [M2 use cases](/reference/hiecm-m2).

### Why the Composition comes first

A bundle on its own is a bag of resources. The Composition turns it into a document: what this is, who it is about, who wrote it, who attests to it, and which resources make up its sections. Without it, a receiving system has a `MedicationRequest` and no idea whether it belongs to a prescription, a discharge summary or a draft.

`Composition.type` carries the SNOMED CT code that answers "what is this". Two are documented: `440545006` for a prescription record and `721981007` for a diagnostic report. The rest have their own codes in the NRCES profiles.

### The rules that fail validation

| Field                         | Rule                                                                                                                                                                                      |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                          | Unique per bundle, and resolvable inside your own system for traceability                                                                                                                 |
| `timestamp`                   | The time the document was issued                                                                                                                                                          |
| `identifier`                  | Traces the document back to your system                                                                                                                                                   |
| `type`                        | Must be `document`                                                                                                                                                                        |
| `meta.versionId`              | Set it on the bundle, so updates can be checked against the latest version                                                                                                                |
| `entry[].fullUrl`             | A logical URL of the form `resource-type/id`, resolvable inside the bundle. Never an absolute URL.                                                                                        |
| `Composition.attester.party`  | References an `Organization` whose `identifier.value` is the facility's [HIP](/docs/hiecm/v3/getting-started/glossary#hip) id as registered in the facility registry. Mode is `official`. |
| `Composition.section.entry[]` | Top level resources only. Referenced resources such as Patient, Encounter and Practitioner belong in the bundle, not in the section entries.                                              |

The attester rule has an environment trap. The organization identifier system is the ABDM facility registry at [nhpr.abdm.gov.in](https://nhpr.abdm.gov.in/nhpr/v4/home) for production and [hspsbx.abdm.gov.in](https://hspsbx.abdm.gov.in/nhpr/v4/home) for sandbox. A bundle that passes in sandbox with the sandbox value is not right in production.

One more thing to watch. `Composition.type.coding.system` is `https://ndhm.gov.in/sct` in the sample above, while `section.code.coding.system` in the same sample is `https://affinitydomain.in/sct`. The two differ in the sample itself. Take the system values from the NRCES profile, not from the sample.

## Validate before you ship

Run this procedure locally. You need JDK 8 or higher.

1. Create a folder and download the FHIR validator CLI, version 6.2.1, from [the HAPI FHIR core release](https://github.com/hapifhir/org.hl7.fhir.core/releases/download/6.2.1/validator_cli.jar). Save `validator_cli.jar` into it.
2. Get a bundle to test: one your own system produced, or an NRCES example from [nrces.in/ndhm/fhir/r4](https://nrces.in/ndhm/fhir/r4/index.html), switching to the JSON tab to download it.
3. Run the validator from that folder:

```shell
java -jar validator_cli.jar <YOUR_BUNDLE_FILENAME>.json -ig https://nrces.in/ndhm/fhir/r4
```

It checks structural correctness, conformance to the NRCES profiles, and required fields and constraints. Editing an NRCES example that already validates towards your own data is faster than starting from an empty file.

## Where this is implemented

- [M2 use cases](/reference/hiecm-m2), the full bundle sample and validation in context.
- [How a record travels](/docs/hiecm/v3/concepts/data-flow), what happens to the bundle after you build it.
- [Care contexts and linking](/docs/hiecm/v3/concepts/linking), how records are grouped and made findable.
- [Consent](/docs/hiecm/v3/concepts/consent), where the HI type codes above are chosen and read.
