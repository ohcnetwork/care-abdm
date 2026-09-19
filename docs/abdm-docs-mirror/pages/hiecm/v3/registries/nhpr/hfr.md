# HFR, the facility registry

[HFR](/docs/hiecm/v3/getting-started/glossary#hfr) is the Health Facility Registry, the places half of [NHPR](/docs/hiecm/v3/registries/nhpr) alongside the [HPR](/docs/hiecm/v3/registries/nhpr/hpr). It is a national directory of hospitals, clinics, diagnostic laboratories, imaging centres and pharmacies, and a facility has to enrol here before it can do anything else on [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm).

## Why it blocks everything else

A facility needs a valid facility ID and registration in the [HIP](/docs/hiecm/v3/getting-started/glossary#hip) role before it can create health records and share them. A product that has finished [M2](/docs/hiecm/v3/api/m2) or [M3](/docs/hiecm/v3/api/m3) against the sandbox cannot go live without this registry.

What the facility gets: a trusted identity, a listing in national search results, less paperwork on licence renewals and insurance empanelment, and access to ABDM's digital services.

## What a facility record holds

Three layers, one call each.

| Layer                  | What goes in it                                                                                                                                                                                                                                                                                |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic information      | Name, ownership and its subtypes, system of medicine, facility type and subtype, speciality type, operational status, type of service, the full address as codes, latitude and longitude, contact details, opening days and hours, and two mandatory photographs of the board and the building |
| Additional information | Yes or no flags for a dialysis centre, pharmacy, blood bank, cath lab, diagnostic lab and imaging centre, plus scheme identifiers the facility already holds: NHRR, NIN, AB-PMJAY, Rohini, ECHS, CGHS, CEA registration and a state insurance scheme ID                                        |
| Detailed information   | Specialities per system of medicine, and the sections that apply to this facility type: medical infrastructure and bed counts, pharmacy details, blood bank details, diagnostic services, imaging services                                                                                     |

Which parts of the detailed layer are mandatory depends on the facility type, the type of service and the system of medicine, and the rules are on [the HPR and HFR call list](/docs/hiecm/v3/api/m4). Two of them shape your form. An inpatient or day care facility must submit at least one bed count greater than zero. An imaging centre, diagnostic laboratory, blood bank or pharmacy need not submit medical infrastructure at all.

### Codes, not names

Ownership, facility type, facility subtype, speciality, system of medicine, operational status and days of operation come from HFR's own master data calls. Demographic fields come from the Local Government Directory at [lgdirectory.gov.in](https://lgdirectory.gov.in/), through the LGD state, district and sub district calls. HFR APIs accept only the code for any field where master data is defined, never the display value, so build the master data fetch first or every write call fails validation.

## The onboarding journey

Five calls, in a fixed order.

1. **Deduplicate search.** Check the facility is not already listed.
2. **Basic facility information.** Creates the record and returns a tracking ID. That ID is your facility's unique identification number until you submit. Pass it as the facility ID on every later call in the sequence.
3. **Additional information.** Takes the tracking ID.
4. **Detailed information.** Takes the tracking ID.
5. **Submit facility details.** Sends the facility for verification.

Without call five the facility does not exist

If you do not make the submit call, the facility stays in draft. A draft facility goes nowhere, and nothing else in ABDM can use it. Running the first four calls and getting a tracking ID back does not mean you are registered.

To update a facility later, send the same calls with the facility ID or tracking ID in the payload rather than creating a new record.

## The link to the HPR token

Your client credentials are not enough. Basic facility information takes an **HPR token in the header**, generated from an HPR ID and password. Submit facility takes an **`x-hpird-auth` token in the header**. Obtain both from the HPR token flow, and set each header by the name the call asks for.

Both come from a person, not from your application. That is why [HPR](/docs/hiecm/v3/registries/nhpr/hpr) comes first in a rollout, and why somebody in your organisation needs an [HPID](/docs/hiecm/v3/getting-started/glossary#hpid) with facility manager rights, role 2 or role 3, before you write a line of HFR code.

## The facility ID

A submitted and verified facility carries a facility ID, and that ID identifies it in every record you share. Two formats are documented for it:

| Where                                                               | Format                                                            |
| ------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Bridge linkage, facility search, nearby search, send OTP to contact | Starts with `IN` and is 12 characters in total                    |
| Deduplicate search                                                  | A 6 digit numeric value, labelled there as the facility unique ID |

One parameter name carries two different formats. Take the format from the reference page for the call you are making.

## Bridge linkage

A bridge is your software's connection to ABDM. Registering a facility gives it an identity; linking a bridge makes your system resolvable as that facility, in the HIP or [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) direction, so records flow to it. The call takes a facility ID, the facility name, a bridge ID, a HIP name, a type of `HIP` or `HIU`, and an active flag.

The HIP name is the one field a patient sees. It is the name shown in the [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) or [PHR](/docs/hiecm/v3/getting-started/glossary#phr) app when the patient searches for the hospital. It must be 15 characters or fewer, carry no special characters, and be unique for every bridge within a facility. The suggested pattern is the hospital name plus the bridge name: hospital XYZ on bridge BRIDGE TEST becomes `XYZ BRIDGE`. Fifteen characters is short, so pick what a patient will recognise.

## Finding a facility

| Call                             | What it is for                                                                                                                                                                                 |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Deduplicate search               | Name, district and sub district, before creating a record                                                                                                                                      |
| Search facility                  | By facility ID, or by ownership code, state LGD code and facility name. Fuzzy on the name, exact on everything else, paginated                                                                 |
| Nearby search                    | Latitude, longitude and a radius in kilometres, with optional filters for ownership, speciality and ABDM enabled. Results are ordered nearest first                                            |
| Send and validate OTP to contact | Sends an [OTP](/docs/hiecm/v3/getting-started/glossary#otp) to the mobile number registered against a facility, then validates it. This proves control of a facility record you did not create |

Base URLs for every call on this page are on [NHPR](/docs/hiecm/v3/registries/nhpr).

## Request and response formats

This page gives what a facility record holds and the order the calls go in. Take the request and response shapes from the health facility registry sandbox documentation alongside it.

Two paths are fixed here:

| Call                | Path                              |
| ------------------- | --------------------------------- |
| Fetch facility type | `v1.5/facility/fetchfacilitytype` |
| Get specialities    | `/v1.5/facility/get-specialities` |

## Next

- [HPR](/docs/hiecm/v3/registries/nhpr/hpr), which issues the token these calls need.
- [NHPR](/docs/hiecm/v3/registries/nhpr), the parent page.
- [the HPR and HFR call list](/docs/hiecm/v3/api/m4), parameter tables and `HIS-` error codes.
- [M2 Attach, Health Information Provider Services](/docs/hiecm/v3/api/m2), which needs this facility ID.
